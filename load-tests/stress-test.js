/**
 * AGRO AI – k6 Stress Test
 * ─────────────────────────
 * Target  : http://localhost:8000
 * Profile : Ramp 10 → 200 → 500 VUs over 5 minutes, hold, then cool-down
 *
 * Stage Plan:
 *   0:00 →  0:30  Ramp  10 → 200   (warm-up)
 *   0:30 →  1:30  Hold  200         (medium load)
 *   1:30 →  2:30  Ramp  200 → 500  (ramp to peak)
 *   2:30 →  4:00  Hold  500         (stress plateau)
 *   4:00 →  5:00  Ramp  500 → 0    (cool-down)
 *
 * Run:
 *   k6 run load-tests/stress-test.js
 *   k6 run --out json=load-tests/reports/stress-result.json load-tests/stress-test.js
 */

import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Rate, Trend, Counter, Gauge } from 'k6/metrics';

// ─── Custom Metrics ────────────────────────────────────────────────────────────
const errorRate        = new Rate('agro_stress_error_rate');
const healthLatency    = new Trend('agro_stress_health_duration',      true);
const loginLatency     = new Trend('agro_stress_login_duration',       true);
const registerLatency  = new Trend('agro_stress_register_duration',    true);
const chatLatency      = new Trend('agro_stress_chat_duration',        true);
const plantLatency     = new Trend('agro_stress_plant_duration',       true);
const nutritionLatency = new Trend('agro_stress_nutrition_duration',   true);
const prodLatency      = new Trend('agro_stress_production_duration',  true);
const totalRequests    = new Counter('agro_stress_total_requests');
const activeVUs        = new Gauge('agro_stress_active_vus');

// ─── Test Configuration ────────────────────────────────────────────────────────
export const options = {
  stages: [
    // Phase 1: Warm-up — ramp from 10 to 200 VUs in 30 s
    { duration: '30s', target: 10  },
    { duration: '30s', target: 200 },

    // Phase 2: Medium load — hold 200 VUs for 60 s
    { duration: '60s', target: 200 },

    // Phase 3: Ramp to peak — 200 → 500 VUs in 60 s
    { duration: '60s', target: 500 },

    // Phase 4: Stress plateau — hold 500 VUs for 90 s
    { duration: '90s', target: 500 },

    // Phase 5: Cool-down — ramp back to 0 in 60 s
    { duration: '60s', target: 0   },
  ],
  thresholds: {
    // Relax thresholds slightly under stress conditions
    http_req_duration:                 ['p(95)<3000', 'p(99)<5000'],
    http_req_failed:                   ['rate<0.10'],   // allow up to 10 % errors under 500 VUs

    agro_stress_error_rate:            ['rate<0.10'],
    agro_stress_health_duration:       ['p(95)<800'],
    agro_stress_login_duration:        ['p(95)<2500'],
    agro_stress_register_duration:     ['p(95)<3000'],
    agro_stress_chat_duration:         ['p(95)<10000'], // LLM inference may queue under load
    agro_stress_plant_duration:        ['p(95)<2000'],
    agro_stress_nutrition_duration:    ['p(95)<2500'],
    agro_stress_production_duration:   ['p(95)<2000'],
  },
};

// ─── Constants ─────────────────────────────────────────────────────────────────
const BASE_URL = 'http://localhost:8000';

const JSON_HEADERS = {
  'Content-Type': 'application/json',
  'Accept':       'application/json',
};

// Larger user pool for stress test to avoid email collisions
const USER_POOL = Array.from({ length: 100 }, (_, i) => ({
  email:    `stress.user${i}@agro-ai-test.local`,
  password: 'StressTest@2024!',
  fullName: `Stress Tester ${i}`,
}));

const PLANT_QUERIES    = ['tomato', 'wheat', 'rice', 'mango', 'neem', 'tulsi', 'cotton', 'banana', 'potato', 'maize'];
const PLANT_CATEGORIES = ['crop', 'vegetable', 'fruit plant', 'medicinal plant', 'tree'];
const CHAT_QUESTIONS   = [
  'Best fertilizer for rice?',
  'How to treat leaf blight?',
  'Ideal soil pH for tomatoes?',
  'How to improve soil fertility?',
  'Signs of nitrogen deficiency in wheat?',
  'How to control white fly organically?',
  'What is drip irrigation?',
  'How to store seeds properly?',
  'Best crops for sandy soil?',
  'How to compost farm waste?',
];
const FOOD_QUERIES = ['rice', 'dal', 'roti', 'sabzi', 'paneer', 'fish', 'egg', 'milk', 'banana', 'apple'];

// ─── Helpers ───────────────────────────────────────────────────────────────────
function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function trackResponse(res, customTrend, tag) {
  totalRequests.add(1, { endpoint: tag });
  const ok = res.status >= 200 && res.status < 400;
  errorRate.add(!ok, { endpoint: tag });
  if (customTrend) customTrend.add(res.timings.duration, { endpoint: tag });
  return ok;
}

function logStageInfo() {
  activeVUs.add(__VU);
}

// ─── Setup: pre-register stress test users ────────────────────────────────────
export function setup() {
  console.log('🔥  AGRO AI Stress Test – registering user pool…');

  let count = 0;
  for (const u of USER_POOL) {
    const res = http.post(
      `${BASE_URL}/api/auth/signup`,
      JSON.stringify({ email: u.email, password: u.password, fullName: u.fullName, role: 'general' }),
      { headers: JSON_HEADERS, tags: { endpoint: 'stress_setup_register' } },
    );
    if (res.status === 201 || res.status === 400) count++;
    sleep(0.05); // gentle throttle during setup
  }

  console.log(`✅  Stress test setup complete. ${count}/${USER_POOL.length} accounts ready.`);
  console.log('📈  Ramp schedule: 10 → 200 → 500 VUs over 5 minutes.');
  return { users: USER_POOL };
}

// ─── Main VU function ─────────────────────────────────────────────────────────
export default function (data) {
  logStageInfo();

  const user = pick(data.users);
  let authToken = '';

  // ── 1. Health Check (always — lightweight sentinel) ───────────────────────────
  group('01 Health Check', () => {
    const res = http.get(`${BASE_URL}/api/health`, {
      tags: { endpoint: 'health_check', group: 'health', phase: currentPhase() },
    });
    trackResponse(res, healthLatency, 'health_check');
    check(res, {
      'health: status 200': (r) => r.status === 200,
      'health: not overloaded': (r) => r.status !== 503,
    });
  });

  sleep(0.1);

  // ── 2. Auth: Login ────────────────────────────────────────────────────────────
  group('02 Auth Login', () => {
    const res = http.post(
      `${BASE_URL}/api/auth/login`,
      JSON.stringify({ email: user.email, password: user.password }),
      { headers: JSON_HEADERS, tags: { endpoint: 'auth_login', group: 'auth', phase: currentPhase() } },
    );
    const ok = trackResponse(res, loginLatency, 'auth_login');
    check(res, {
      'login: 200 or 401': (r) => r.status === 200 || r.status === 401,
      'login: responded':  (r) => r.timings.duration < 5000,
    });
    if (ok && res.status === 200) {
      try { authToken = JSON.parse(res.body).token || ''; } catch { /* ignore */ }
    }
  });

  sleep(0.1);

  // ── 3. Auth: Register (intermittent — only some VU iterations) ───────────────
  if (__ITER % 10 === 0) { // every 10th iteration
    group('03 Auth Register', () => {
      const uniqueEmail = `stress.${__VU}.${__ITER}@agro-test.local`;
      const res = http.post(
        `${BASE_URL}/api/auth/signup`,
        JSON.stringify({
          email:    uniqueEmail,
          password: 'TestPass@999!',
          fullName: `Stress VU${__VU}`,
          role:     'general',
        }),
        { headers: JSON_HEADERS, tags: { endpoint: 'auth_register', group: 'auth', phase: currentPhase() } },
      );
      trackResponse(res, registerLatency, 'auth_register');
      check(res, {
        'register: 201 or 400': (r) => r.status === 201 || r.status === 400,
      });
    });
    sleep(0.1);
  }

  const authHeaders = {
    ...JSON_HEADERS,
    ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
  };

  // ── 4. Assistant Chat (heavy, AI call) ────────────────────────────────────────
  // Only ~40 % of VUs invoke chat to avoid overwhelming the LLM server
  if (Math.random() < 0.4) {
    group('04 Assistant Chat', () => {
      const res = http.post(
        `${BASE_URL}/api/assistant/chat`,
        JSON.stringify({
          message:   pick(CHAT_QUESTIONS),
          sessionId: `stress-vu${__VU}-iter${__ITER % 5}`,
          history:   [],
        }),
        {
          headers: authHeaders,
          tags:    { endpoint: 'assistant_chat', group: 'assistant', phase: currentPhase() },
          timeout: '45s',
        },
      );
      trackResponse(res, chatLatency, 'assistant_chat');
      check(res, {
        'chat: 200 or 503': (r) => r.status === 200 || r.status === 503,
        'chat: responded':  (r) => r.timings.duration < 45000,
      });
    });
    sleep(0.3);
  }

  // ── 5. Assistant Status ───────────────────────────────────────────────────────
  group('05 Assistant Status', () => {
    const res = http.get(`${BASE_URL}/api/assistant/status`, {
      headers: authHeaders,
      tags:    { endpoint: 'assistant_status', group: 'assistant', phase: currentPhase() },
    });
    trackResponse(res, null, 'assistant_status');
    check(res, { 'assistant status: 200': (r) => r.status === 200 });
  });

  sleep(0.1);

  // ── 6. Plant: Search ──────────────────────────────────────────────────────────
  group('06 Plant Search', () => {
    const q = pick(PLANT_QUERIES);
    const res = http.get(
      `${BASE_URL}/api/plants/search?q=${encodeURIComponent(q)}&limit=20`,
      { headers: JSON_HEADERS, tags: { endpoint: 'plant_search', group: 'plants', phase: currentPhase() } },
    );
    trackResponse(res, plantLatency, 'plant_search');
    check(res, {
      'plant search: 200':      (r) => r.status === 200,
      'plant search: body ok':  (r) => r.body && r.body.length > 0,
    });
  });

  sleep(0.1);

  // ── 7. Plant: Autocomplete ────────────────────────────────────────────────────
  group('07 Plant Autocomplete', () => {
    const q = pick(PLANT_QUERIES).slice(0, 3);
    const res = http.get(
      `${BASE_URL}/api/plants/autocomplete?q=${encodeURIComponent(q)}&limit=10`,
      { headers: JSON_HEADERS, tags: { endpoint: 'plant_autocomplete', group: 'plants', phase: currentPhase() } },
    );
    trackResponse(res, plantLatency, 'plant_autocomplete');
    check(res, { 'autocomplete: 200': (r) => r.status === 200 });
  });

  sleep(0.1);

  // ── 8. Plant: Categories ──────────────────────────────────────────────────────
  group('08 Plant Categories', () => {
    const res = http.get(`${BASE_URL}/api/plants/categories`, {
      headers: JSON_HEADERS,
      tags:    { endpoint: 'plant_categories', group: 'plants', phase: currentPhase() },
    });
    trackResponse(res, plantLatency, 'plant_categories');
    check(res, { 'categories: 200': (r) => r.status === 200 });
  });

  sleep(0.1);

  // ── 9. Production: Health & Catalogue ────────────────────────────────────────
  group('09 Production Catalogue', () => {
    const healthRes = http.get(`${BASE_URL}/api/production/health`, {
      headers: JSON_HEADERS,
      tags:    { endpoint: 'production_health', group: 'production', phase: currentPhase() },
    });
    trackResponse(healthRes, prodLatency, 'production_health');
    check(healthRes, { 'prod health: 200': (r) => r.status === 200 });

    const plantsRes = http.get(`${BASE_URL}/api/production/supported-plants`, {
      headers: JSON_HEADERS,
      tags:    { endpoint: 'production_supported_plants', group: 'production', phase: currentPhase() },
    });
    trackResponse(plantsRes, prodLatency, 'production_supported_plants');
    check(plantsRes, { 'supported plants: 200': (r) => r.status === 200 });
  });

  sleep(0.1);

  // ── 10. Nutrition: Calculate ──────────────────────────────────────────────────
  group('10 Nutrition Calculate', () => {
    const res = http.post(
      `${BASE_URL}/api/nutrition/calculate`,
      JSON.stringify({
        age:                 25 + Math.floor(Math.random() * 30),
        gender:              Math.random() > 0.5 ? 'male' : 'female',
        heightCm:            155 + Math.random() * 30,
        weightKg:            50  + Math.random() * 40,
        activityLevel:       pick(['sedentary', 'light', 'moderate', 'active']),
        goal:                pick(['weight_loss', 'weight_gain', 'maintenance']),
        goalWeightKg:        50  + Math.random() * 40,
        mealsPerDay:         pick([3, 4, 5]),
        targetTimelineWeeks: pick([4, 8, 12]),
        dietaryRestrictions: [],
        foodPreference:      pick(['vegetarian', 'non_vegetarian', 'vegan']),
      }),
      { headers: JSON_HEADERS, tags: { endpoint: 'nutrition_calculate', group: 'nutrition', phase: currentPhase() } },
    );
    trackResponse(res, nutritionLatency, 'nutrition_calculate');
    check(res, { 'nutrition calc: 200': (r) => r.status === 200 });
  });

  sleep(0.1);

  // ── 11. Nutrition: Foods ──────────────────────────────────────────────────────
  group('11 Nutrition Foods', () => {
    const res = http.get(
      `${BASE_URL}/api/nutrition/foods?query=${encodeURIComponent(pick(FOOD_QUERIES))}`,
      { headers: JSON_HEADERS, tags: { endpoint: 'nutrition_foods', group: 'nutrition', phase: currentPhase() } },
    );
    trackResponse(res, nutritionLatency, 'nutrition_foods');
    check(res, { 'foods: 200': (r) => r.status === 200 });
  });

  sleep(0.1);

  // ── 12. Farm Calculator ───────────────────────────────────────────────────────
  group('12 Farm Calculator', () => {
    const calcTypes = [
      {
        calcType: 'npk_fertilizer',
        params:   { targetN: 120, targetP: 60, targetK: 40, area: 1.0, unit: 'ha', useSSP: false },
      },
      {
        calcType: 'seed_rate',
        params:   { area: 1.0, areaUnit: 'ha', rowSpacingCm: 60, plantSpacingCm: 20, testWeightG: 40, germinationPct: 85, purityPct: 98 },
      },
      {
        calcType: 'irrigation',
        params:   { etoMmDay: 4.5, cropKc: 1.15, areaM2: 4047, emitterDischargeLph: 2.0, emittersPerPlant: 1 },
      },
    ];
    const calcPayload = pick(calcTypes);
    const res = http.post(
      `${BASE_URL}/api/assistant/calculate`,
      JSON.stringify(calcPayload),
      { headers: JSON_HEADERS, tags: { endpoint: 'farm_calculator', group: 'assistant', phase: currentPhase() } },
    );
    trackResponse(res, null, 'farm_calculator');
    check(res, { 'farm calc: 200': (r) => r.status === 200 });
  });

  sleep(0.2);
}

// ─── Helper: map iteration timestamp to phase name ─────────────────────────────
function currentPhase() {
  // k6 doesn't expose elapsed time directly; approximate from VU count
  if (__VU <= 10)  return 'warmup';
  if (__VU <= 200) return 'medium_load';
  if (__VU <= 500) return 'stress_peak';
  return 'cooldown';
}

// ─── Teardown ─────────────────────────────────────────────────────────────────
export function teardown(data) {
  console.log('\n══════════════════════════════════════════════════════');
  console.log('  AGRO AI Stress Test – Complete');
  console.log('══════════════════════════════════════════════════════');
  console.log('  Ramp Profile:');
  console.log('    Phase 1 (0:00–0:30)  Warm-up     10 → 200 VUs');
  console.log('    Phase 2 (0:30–1:30)  Medium      200 VUs (hold)');
  console.log('    Phase 3 (1:30–2:30)  Ramp        200 → 500 VUs');
  console.log('    Phase 4 (2:30–4:00)  Peak Stress 500 VUs (hold)');
  console.log('    Phase 5 (4:00–5:00)  Cool-down   500 → 0');
  console.log('  Endpoints exercised:');
  console.log('    ✔ GET  /api/health');
  console.log('    ✔ POST /api/auth/login');
  console.log('    ✔ POST /api/auth/signup (1-in-10 iters)');
  console.log('    ✔ POST /api/assistant/chat (40 % of VUs)');
  console.log('    ✔ GET  /api/assistant/status');
  console.log('    ✔ POST /api/assistant/calculate');
  console.log('    ✔ GET  /api/plants/search');
  console.log('    ✔ GET  /api/plants/autocomplete');
  console.log('    ✔ GET  /api/plants/categories');
  console.log('    ✔ GET  /api/production/health');
  console.log('    ✔ GET  /api/production/supported-plants');
  console.log('    ✔ POST /api/nutrition/calculate');
  console.log('    ✔ GET  /api/nutrition/foods');
  console.log('══════════════════════════════════════════════════════\n');
}
