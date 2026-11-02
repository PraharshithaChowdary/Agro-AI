/**
 * Generates sample k6 output data matching 100 VUs × 60s for local testing of report generator
 */
const fs = require('fs');
const path = require('path');

const reportsDir = path.join(__dirname, 'reports');
if (!fs.existsSync(reportsDir)) fs.mkdirSync(reportsDir, { recursive: true });

const outputFile = path.join(reportsDir, 'baseline-result.json');
const stream = fs.createWriteStream(outputFile, { encoding: 'utf8' });

const endpoints = [
  { name: '/health', avg: 45, variance: 20, errorProb: 0.001 },
  { name: '/api/auth/login', avg: 180, variance: 60, errorProb: 0.005 },
  { name: '/api/auth/register', avg: 240, variance: 80, errorProb: 0.008 },
  { name: '/api/assistant/chat', avg: 420, variance: 150, errorProb: 0.015 },
  { name: '/api/plants/search', avg: 110, variance: 40, errorProb: 0.003 },
  { name: '/api/plants/categories', avg: 75, variance: 25, errorProb: 0.002 },
  { name: '/api/nutrition/calculate', avg: 195, variance: 70, errorProb: 0.006 },
  { name: '/api/production/supported-plants', avg: 85, variance: 30, errorProb: 0.002 },
  { name: '/api/production/soil-types', avg: 65, variance: 20, errorProb: 0.001 },
];

const startTime = Date.now() - 60000;
const totalReqs = 7200; // ~120 RPS for 60s

for (let i = 0; i < totalReqs; i++) {
  const ep = endpoints[Math.floor(Math.random() * endpoints.length)];
  const offset = Math.floor(Math.random() * 60000);
  const timeStr = new Date(startTime + offset).toISOString();
  const dur = Math.max(15, ep.avg + (Math.random() * 2 - 1) * ep.variance);
  const isErr = Math.random() < ep.errorProb;
  const status = isErr ? (Math.random() < 0.5 ? 500 : 503) : 200;

  const point = {
    type: 'Point',
    metric: 'http_req_duration',
    data: {
      time: timeStr,
      value: Math.round(dur * 100) / 100,
      tags: {
        endpoint: ep.name,
        status: String(status),
        method: ep.name.includes('calculate') || ep.name.includes('login') || ep.name.includes('register') || ep.name.includes('chat') ? 'POST' : 'GET'
      }
    }
  };
  stream.write(JSON.stringify(point) + '\n');

  const checkPoint = {
    type: 'Point',
    metric: 'checks',
    data: {
      time: timeStr,
      value: isErr ? 0 : 1
    }
  };
  stream.write(JSON.stringify(checkPoint) + '\n');
}

// Add threshold data
const thresholds = [
  'http_req_duration',
  'http_req_failed',
  'agro_error_rate',
  'agro_health_duration',
  'agro_login_duration',
  'agro_register_duration',
  'agro_chat_duration',
  'agro_plant_search_duration',
  'agro_nutrition_duration',
  'agro_production_duration'
];

for (const th of thresholds) {
  const metricObj = {
    type: 'Metric',
    metric: th,
    data: {
      thresholds: {
        'rate<0.05': { ok: true },
        'p(95)<2000': { ok: true }
      }
    }
  };
  stream.write(JSON.stringify(metricObj) + '\n');
}

stream.end(() => {
  console.log(`Successfully generated ${totalReqs} sample records at ${outputFile}`);
});

