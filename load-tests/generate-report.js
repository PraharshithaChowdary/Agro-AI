#!/usr/bin/env node
/**
 * AGRO AI Load Test – Excel Report Generator
 * ────────────────────────────────────────────
 * Reads k6 JSON output and produces a multi-sheet Excel workbook:
 *
 *   Sheet 1 – Test Summary        : overall stats
 *   Sheet 2 – Endpoint Details    : per-endpoint breakdown
 *   Sheet 3 – Threshold Results   : pass / fail status per threshold
 *   Sheet 4 – Timeline            : time-series request/error counts
 *
 * Usage:
 *   # Run k6 with JSON output first:
 *   k6 run --out json=load-tests/reports/baseline-result.json load-tests/baseline-test.js
 *
 *   # Then generate the Excel report:
 *   node load-tests/generate-report.js \
 *        --input  load-tests/reports/baseline-result.json \
 *        --output load-tests/reports/load-test-report.xlsx \
 *        --name   "AGRO AI Baseline"
 *
 *   # Or use npm scripts:
 *   cd load-tests && npm run report
 */

'use strict';

const fs      = require('fs');
const path    = require('path');
const readline = require('readline');
const ExcelJS = require('exceljs');

// ─── CLI argument parsing ──────────────────────────────────────────────────────
const args = process.argv.slice(2);
function getArg(flag, defaultVal) {
  const idx = args.indexOf(flag);
  return idx !== -1 && args[idx + 1] ? args[idx + 1] : defaultVal;
}

const INPUT_FILE  = getArg('--input',  path.join(__dirname, 'reports', 'baseline-result.json'));
const OUTPUT_FILE = getArg('--output', path.join(__dirname, 'reports', 'load-test-report.xlsx'));
const TEST_NAME   = getArg('--name',   'AGRO AI Load Test');

// ─── Colour palette ───────────────────────────────────────────────────────────
const COLORS = {
  headerBg:   '1A5276',  // dark blue
  headerFont: 'FFFFFF',
  passGreen:  'D5F5E3',
  failRed:    'FADBD8',
  altRow:     'EBF5FB',
  titleBg:    '2ECC71',
  warnOrange: 'FAD7A0',
  borderColor:'B2BABB',
};

// ─── Metric accumulators ──────────────────────────────────────────────────────
// k6 JSON stream format: each line is one data point (metric, point, etc.)
const endpointStats = {};  // keyed by tag.endpoint
const timelineMap   = {};  // keyed by minute bucket
const thresholdData = {};  // keyed by threshold name
let   summaryData   = {};
let   testStartMs   = null;
let   testEndMs     = null;
let   totalChecks   = 0;
let   passedChecks  = 0;

// ─── Accumulate metric point into endpoint stats ───────────────────────────────
function accumulate(endpoint, durationMs, isError) {
  if (!endpoint) return;
  if (!endpointStats[endpoint]) {
    endpointStats[endpoint] = {
      count: 0, errors: 0,
      durations: [],
      totalDuration: 0,
      min: Infinity, max: -Infinity,
    };
  }
  const s = endpointStats[endpoint];
  s.count++;
  if (isError) s.errors++;
  s.durations.push(durationMs);
  s.totalDuration += durationMs;
  if (durationMs < s.min) s.min = durationMs;
  if (durationMs > s.max) s.max = durationMs;
}

// ─── Percentile helper ────────────────────────────────────────────────────────
function percentile(sortedArr, p) {
  if (!sortedArr.length) return 0;
  const idx = Math.ceil((p / 100) * sortedArr.length) - 1;
  return sortedArr[Math.max(0, idx)];
}

// ─── Parse k6 JSON line-by-line ───────────────────────────────────────────────
async function parseK6Json(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`Input file not found: ${filePath}\nRun k6 with --out json=<file> first.`);
  }

  console.log(`📂  Reading k6 output: ${filePath}`);

  const rl = readline.createInterface({
    input:     fs.createReadStream(filePath, { encoding: 'utf8' }),
    crlfDelay: Infinity,
  });

  for await (const rawLine of rl) {
    const line = rawLine.trim();
    if (!line) continue;

    let obj;
    try { obj = JSON.parse(line); } catch { continue; }

    const { type, metric, data } = obj;

    // ── Summary object (last line in some k6 versions) ──────────────────────
    if (type === 'Point' && metric === 'http_req_duration') {
      const ts      = new Date(data.time).getTime();
      const dur     = data.value;
      const tags    = data.tags || {};
      const endpoint= tags.endpoint || tags.name || tags.url || 'unknown';
      const status  = parseInt(tags.status || '0', 10);
      const isError = status >= 400 || status === 0;

      if (!testStartMs || ts < testStartMs) testStartMs = ts;
      if (!testEndMs   || ts > testEndMs)   testEndMs   = ts;

      accumulate(endpoint, dur, isError);

      // Timeline: bucket by minute
      const minute = Math.floor((ts - (testStartMs || ts)) / 60000);
      if (!timelineMap[minute]) timelineMap[minute] = { requests: 0, errors: 0, totalDur: 0 };
      timelineMap[minute].requests++;
      if (isError) timelineMap[minute].errors++;
      timelineMap[minute].totalDur += dur;
    }

    // ── Checks ────────────────────────────────────────────────────────────────
    if (type === 'Point' && metric === 'checks') {
      totalChecks++;
      if (data.value === 1) passedChecks++;
    }

    // ── Threshold results ─────────────────────────────────────────────────────
    if (type === 'Metric' && data && data.thresholds) {
      const name = metric;
      thresholdData[name] = thresholdData[name] || {};
      Object.assign(thresholdData[name], data.thresholds);
    }

    // ── Summary (k6 end-of-run summary object) ─────────────────────────────
    if (type === 'Summary' && data && data.metrics) {
      summaryData = data;
    }
  }

  console.log(`✅  Parsed ${Object.keys(endpointStats).length} distinct endpoints.`);
}

// ─── Build aggregated summary stats ───────────────────────────────────────────
function buildSummaryStats() {
  let totalRequests = 0, totalErrors = 0, totalDuration = 0;
  const allDurations = [];

  for (const [, s] of Object.entries(endpointStats)) {
    totalRequests += s.count;
    totalErrors   += s.errors;
    totalDuration += s.totalDuration;
    allDurations.push(...s.durations);
  }

  allDurations.sort((a, b) => a - b);

  const durationSec = testStartMs && testEndMs ? (testEndMs - testStartMs) / 1000 : 60;
  const rps         = durationSec > 0 ? totalRequests / durationSec : 0;
  const errorRate   = totalRequests > 0 ? (totalErrors / totalRequests) * 100 : 0;
  const avgDur      = allDurations.length ? totalDuration / totalRequests : 0;

  return {
    totalRequests,
    totalErrors,
    rps,
    errorRate,
    avgDuration:  avgDur,
    minDuration:  allDurations[0]        || 0,
    maxDuration:  allDurations[allDurations.length - 1] || 0,
    p50:          percentile(allDurations, 50),
    p95:          percentile(allDurations, 95),
    p99:          percentile(allDurations, 99),
    durationSec,
    checkPassRate: totalChecks > 0 ? (passedChecks / totalChecks) * 100 : 100,
  };
}

// ─── Style helpers ────────────────────────────────────────────────────────────
function styleHeader(row, bgHex = COLORS.headerBg, fgHex = COLORS.headerFont) {
  row.eachCell((cell) => {
    cell.fill   = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF' + bgHex } };
    cell.font   = { bold: true, color: { argb: 'FF' + fgHex }, size: 11 };
    cell.border = {
      top:    { style: 'thin', color: { argb: 'FF' + COLORS.borderColor } },
      left:   { style: 'thin', color: { argb: 'FF' + COLORS.borderColor } },
      bottom: { style: 'thin', color: { argb: 'FF' + COLORS.borderColor } },
      right:  { style: 'thin', color: { argb: 'FF' + COLORS.borderColor } },
    };
    cell.alignment = { vertical: 'middle', horizontal: 'center', wrapText: true };
  });
}

function styleDataRow(row, altRow = false) {
  const bg = altRow ? 'FF' + COLORS.altRow : 'FFFFFFFF';
  row.eachCell((cell) => {
    cell.fill   = { type: 'pattern', pattern: 'solid', fgColor: { argb: bg } };
    cell.border = {
      top:    { style: 'hair', color: { argb: 'FFCCCCCC' } },
      left:   { style: 'hair', color: { argb: 'FFCCCCCC' } },
      bottom: { style: 'hair', color: { argb: 'FFCCCCCC' } },
      right:  { style: 'hair', color: { argb: 'FFCCCCCC' } },
    };
    cell.alignment = { vertical: 'middle', wrapText: false };
  });
}

function ms(val) { return Math.round(val); }
function pct(val) { return parseFloat(val.toFixed(2)); }
function rnd2(val) { return parseFloat(val.toFixed(2)); }

// ─── Sheet 1: Test Summary ─────────────────────────────────────────────────────
function buildSummarySheet(wb, stats) {
  const ws = wb.addWorksheet('Test Summary', {
    pageSetup: { fitToPage: true, fitToWidth: 1 },
  });

  ws.columns = [
    { header: 'Metric',  key: 'metric', width: 35 },
    { header: 'Value',   key: 'value',  width: 30 },
  ];

  // Title row
  const titleRow = ws.addRow(['AGRO AI Load Test Report']);
  titleRow.height = 28;
  ws.mergeCells(`A1:B1`);
  const titleCell = ws.getCell('A1');
  titleCell.value = `AGRO AI Load Test Report`;
  titleCell.font  = { bold: true, size: 16, color: { argb: 'FFFFFFFF' } };
  titleCell.fill  = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF' + COLORS.headerBg } };
  titleCell.alignment = { vertical: 'middle', horizontal: 'center' };

  // Column header row
  const hdr = ws.addRow(['Metric', 'Value']);
  hdr.height = 22;
  styleHeader(hdr);

  const rows = [
    ['Test Name',             TEST_NAME],
    ['Test Date',             new Date().toLocaleString()],
    ['Duration (seconds)',    rnd2(stats.durationSec)],
    ['Total Requests',        stats.totalRequests],
    ['Total Errors',          stats.totalErrors],
    ['RPS (requests/sec)',    rnd2(stats.rps)],
    ['Error Rate (%)',        pct(stats.errorRate)],
    ['Avg Response Time (ms)',ms(stats.avgDuration)],
    ['Min Response Time (ms)',ms(stats.minDuration)],
    ['Max Response Time (ms)',ms(stats.maxDuration)],
    ['p50 Response Time (ms)',ms(stats.p50)],
    ['p95 Response Time (ms)',ms(stats.p95)],
    ['p99 Response Time (ms)',ms(stats.p99)],
    ['Check Pass Rate (%)',   pct(stats.checkPassRate)],
    ['Endpoints Tested',      Object.keys(endpointStats).length],
  ];

  rows.forEach((r, i) => {
    const row = ws.addRow(r);
    row.height = 18;
    styleDataRow(row, i % 2 === 0);
    // Highlight bad error rate
    if (r[0] === 'Error Rate (%)' && r[1] > 5) {
      ws.getCell(`B${row.number}`).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF' + COLORS.failRed } };
    }
    if (r[0] === 'p95 Response Time (ms)' && r[1] > 2000) {
      ws.getCell(`B${row.number}`).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF' + COLORS.failRed } };
    }
  });

  ws.getColumn('metric').font = { bold: true };
  return ws;
}

// ─── Sheet 2: Endpoint Details ─────────────────────────────────────────────────
function buildEndpointSheet(wb) {
  const ws = wb.addWorksheet('Endpoint Details');

  ws.columns = [
    { header: 'Endpoint',         key: 'endpoint', width: 35 },
    { header: 'Requests',         key: 'count',    width: 12 },
    { header: 'Errors',           key: 'errors',   width: 10 },
    { header: 'Error Rate (%)',   key: 'errRate',  width: 14 },
    { header: 'Avg (ms)',         key: 'avg',      width: 12 },
    { header: 'Min (ms)',         key: 'min',      width: 12 },
    { header: 'Max (ms)',         key: 'max',      width: 12 },
    { header: 'p50 (ms)',         key: 'p50',      width: 12 },
    { header: 'p95 (ms)',         key: 'p95',      width: 12 },
    { header: 'p99 (ms)',         key: 'p99',      width: 12 },
    { header: 'Pass/Fail',        key: 'pass',     width: 12 },
  ];

  const hdr = ws.getRow(1);
  hdr.values = ws.columns.map(c => c.header);
  hdr.height = 22;
  styleHeader(hdr);

  const P95_THRESHOLD_MS = 2000;
  const ERR_THRESHOLD    = 5;

  let rowIdx = 0;
  for (const [endpoint, s] of Object.entries(endpointStats)) {
    const sorted    = [...s.durations].sort((a, b) => a - b);
    const avg       = s.count ? s.totalDuration / s.count : 0;
    const errRate   = s.count ? (s.errors / s.count) * 100 : 0;
    const p50v      = percentile(sorted, 50);
    const p95v      = percentile(sorted, 95);
    const p99v      = percentile(sorted, 99);
    const passed    = p95v <= P95_THRESHOLD_MS && errRate <= ERR_THRESHOLD;

    const row = ws.addRow({
      endpoint,
      count:   s.count,
      errors:  s.errors,
      errRate: pct(errRate),
      avg:     ms(avg),
      min:     s.min === Infinity ? 0 : ms(s.min),
      max:     s.max === -Infinity ? 0 : ms(s.max),
      p50:     ms(p50v),
      p95:     ms(p95v),
      p99:     ms(p99v),
      pass:    passed ? '✅ PASS' : '❌ FAIL',
    });

    row.height = 17;
    styleDataRow(row, rowIdx % 2 === 0);

    // Colour the pass/fail cell
    const passCell = ws.getCell(`K${row.number}`);
    passCell.fill = {
      type: 'pattern', pattern: 'solid',
      fgColor: { argb: 'FF' + (passed ? COLORS.passGreen : COLORS.failRed) },
    };
    passCell.font = { bold: true };

    // Colour p95 red if threshold exceeded
    if (p95v > P95_THRESHOLD_MS) {
      ws.getCell(`I${row.number}`).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF' + COLORS.failRed } };
    }
    if (errRate > ERR_THRESHOLD) {
      ws.getCell(`D${row.number}`).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF' + COLORS.failRed } };
    }

    rowIdx++;
  }

  // Auto-filter
  ws.autoFilter = { from: 'A1', to: `K1` };

  return ws;
}

// ─── Sheet 3: Threshold Results ────────────────────────────────────────────────
function buildThresholdSheet(wb, stats) {
  const ws = wb.addWorksheet('Threshold Results');

  ws.columns = [
    { header: 'Threshold Name',   key: 'name',     width: 38 },
    { header: 'Condition',        key: 'condition', width: 22 },
    { header: 'Actual Value',     key: 'actual',    width: 18 },
    { header: 'Pass/Fail',        key: 'result',    width: 14 },
  ];

  const hdr = ws.getRow(1);
  hdr.values = ws.columns.map(c => c.header);
  hdr.height = 22;
  styleHeader(hdr);

  // Combine parsed threshold data with computed stats
  const builtinThresholds = [
    { name: 'http_req_duration (p95)',  condition: 'p(95) < 2000ms',  actual: `${ms(stats.p95)} ms`,  passed: stats.p95 < 2000 },
    { name: 'http_req_failed',          condition: 'rate < 5%',        actual: `${pct(stats.errorRate)}%`, passed: stats.errorRate < 5 },
    { name: 'Overall Error Rate',       condition: '< 5%',             actual: `${pct(stats.errorRate)}%`, passed: stats.errorRate < 5 },
    { name: 'Check Pass Rate',          condition: '>= 95%',           actual: `${pct(stats.checkPassRate)}%`, passed: stats.checkPassRate >= 95 },
    { name: 'RPS',                      condition: '>= 10 req/s',      actual: `${rnd2(stats.rps)} rps`, passed: stats.rps >= 10 },
  ];

  // Add threshold data parsed from JSON output
  for (const [metricName, thresholds] of Object.entries(thresholdData)) {
    for (const [condition, detail] of Object.entries(thresholds)) {
      builtinThresholds.push({
        name:    metricName,
        condition,
        actual:  detail.ok !== undefined ? (detail.ok ? 'met' : 'not met') : 'see details',
        passed:  detail.ok !== false,
      });
    }
  }

  builtinThresholds.forEach((t, i) => {
    const row = ws.addRow({ name: t.name, condition: t.condition, actual: t.actual, result: t.passed ? '✅ PASS' : '❌ FAIL' });
    row.height = 18;
    styleDataRow(row, i % 2 === 0);

    const resultCell = ws.getCell(`D${row.number}`);
    resultCell.fill = {
      type: 'pattern', pattern: 'solid',
      fgColor: { argb: 'FF' + (t.passed ? COLORS.passGreen : COLORS.failRed) },
    };
    resultCell.font = { bold: true };
  });

  return ws;
}

// ─── Sheet 4: Timeline ─────────────────────────────────────────────────────────
function buildTimelineSheet(wb) {
  const ws = wb.addWorksheet('Timeline');

  ws.columns = [
    { header: 'Minute',         key: 'minute',   width: 12 },
    { header: 'Requests',       key: 'reqs',     width: 14 },
    { header: 'Errors',         key: 'errors',   width: 12 },
    { header: 'Error Rate (%)', key: 'errRate',  width: 16 },
    { header: 'Avg Duration (ms)', key: 'avgDur',width: 20 },
    { header: 'RPS',            key: 'rps',      width: 10 },
  ];

  const hdr = ws.getRow(1);
  hdr.values = ws.columns.map(c => c.header);
  hdr.height = 22;
  styleHeader(hdr);

  const minutes = Object.keys(timelineMap).map(Number).sort((a, b) => a - b);

  if (!minutes.length) {
    ws.addRow({ minute: 'N/A', reqs: 'No timeline data available.', errors: '', errRate: '', avgDur: '', rps: '' });
    return ws;
  }

  minutes.forEach((min, i) => {
    const t        = timelineMap[min];
    const errRate  = t.requests > 0 ? (t.errors / t.requests) * 100 : 0;
    const avgDur   = t.requests > 0 ? t.totalDur / t.requests : 0;
    const rps      = t.requests / 60;

    const row = ws.addRow({
      minute:  `${min}:00 – ${min + 1}:00`,
      reqs:    t.requests,
      errors:  t.errors,
      errRate: pct(errRate),
      avgDur:  ms(avgDur),
      rps:     rnd2(rps),
    });
    row.height = 17;
    styleDataRow(row, i % 2 === 0);

    if (errRate > 5) {
      ws.getCell(`D${row.number}`).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF' + COLORS.failRed } };
    }
  });

  return ws;
}

// ─── Main ─────────────────────────────────────────────────────────────────────
async function main() {
  console.log('\n╔═══════════════════════════════════════════════════╗');
  console.log('║   AGRO AI Load Test – Excel Report Generator     ║');
  console.log('╚═══════════════════════════════════════════════════╝\n');

  try {
    await parseK6Json(INPUT_FILE);
  } catch (err) {
    console.error(`\n❌  Error reading input: ${err.message}`);
    process.exit(1);
  }

  const stats = buildSummaryStats();

  console.log(`\n📊  Summary:  ${stats.totalRequests} requests | ${rnd2(stats.rps)} RPS | ` +
              `p95=${ms(stats.p95)}ms | errors=${pct(stats.errorRate)}%`);

  // Ensure output directory exists
  const outDir = path.dirname(OUTPUT_FILE);
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const wb = new ExcelJS.Workbook();
  wb.creator  = 'AGRO AI Load Test Suite';
  wb.created  = new Date();
  wb.modified = new Date();
  wb.properties.date1904 = false;

  console.log('📝  Building Excel workbook…');
  buildSummarySheet(wb, stats);
  buildEndpointSheet(wb);
  buildThresholdSheet(wb, stats);
  buildTimelineSheet(wb);

  await wb.xlsx.writeFile(OUTPUT_FILE);

  console.log(`\n✅  Report saved: ${OUTPUT_FILE}`);
  console.log('   Sheets: Test Summary | Endpoint Details | Threshold Results | Timeline\n');

  // Print quick summary table
  console.log('┌─────────────────────────────────────┬──────────────┐');
  console.log('│ Metric                              │ Value        │');
  console.log('├─────────────────────────────────────┼──────────────┤');
  console.log(`│ Total Requests                      │ ${String(stats.totalRequests).padEnd(12)} │`);
  console.log(`│ RPS                                 │ ${String(rnd2(stats.rps)).padEnd(12)} │`);
  console.log(`│ Error Rate                          │ ${String(pct(stats.errorRate) + '%').padEnd(12)} │`);
  console.log(`│ p50 Response Time                   │ ${String(ms(stats.p50) + ' ms').padEnd(12)} │`);
  console.log(`│ p95 Response Time                   │ ${String(ms(stats.p95) + ' ms').padEnd(12)} │`);
  console.log(`│ p99 Response Time                   │ ${String(ms(stats.p99) + ' ms').padEnd(12)} │`);
  console.log(`│ Check Pass Rate                     │ ${String(pct(stats.checkPassRate) + '%').padEnd(12)} │`);
  console.log('└─────────────────────────────────────┴──────────────┘');
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
