/**
 * AGRO AI – k6 Baseline / Load Test
 * ──────────────────────────────────
 * Target  : http://localhost:8000
 * Profile : 100 VUs × 1 minute (constant load)
 * Coverage: health, auth (login + register), assistant chat,
 *           plant search/autocomplete/categories/stats,
 *           production endpoints (health, supported-plants, soil-types),
 *           nutrition calculate & foods, farm calculator
 *
 * Run:
 *   k6 run load-tests/baseline-test.js
 *   k6 run --out json=load-tests/reports/baseline-result.json load-tests/baseline-test.js
 */

import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// ─── Custom Metrics ────────────────────────────────────────────────────────────
const errorRate       = new Rate('agro_error_rate');
const healthLatency   = new Trend('agro_health_duration',      true);
const loginLatency    = new Trend('agro_login_duration',       true);
const registerLatency = new Trend('agro_register_duration',    true);
const chatLatency     = new Trend('agro_chat_duration',        true);
const plantLatency    = new Trend('agro_plant_search_duration',true);
const nutritionLatency= new Trend('agro_nutrition_duration',   true);
const prodLatency     = new Trend('agro_production_duration',  true);
const totalRequests   = new Counter('agro_total_requests');

// ─── Test Configuration ────────────────────────────────────────────────────────
export const options = {
  scenarios: {
    baseline_load: {
      executor: 'constant-vus',
      vus: 100,
      duration: '1m',
    },
  },
  thresholds: {
    // Overall HTTP thresholds
    http_req_duration:         ['p(95)<2000'],
    http_req_failed:           ['rate<0.05'],

    // Per-group custom metric thresholds
    agro_error_rate:           ['rate<0.05'],
    agro_health_duration:      ['p(95)<500'],
    agro_login_duration:       ['p(95)<1500'],
    agro_register_duration:    ['p(95)<2000'],
    agro_chat_duration:        ['p(95)<3000'],  // LLM calls can be slow
    agro_plant_search_duration:['p(95)<1000'],
    agro_nutrition_duration:   ['p(95)<1500'],
    agro_production_duration:  ['p(95)<1000'],
  },
};

// ─── Constants ─────────────────────────────────────────────────────────────────
const BASE_URL = 'http://localhost:8000';

const JSON_HEADERS = {
  'Content-Type': 'application/json',
  'Accept':       'application/json',
};

// Rotating test user pools – avoids hot-spotting a single account
const USER_POOL = Array.from({ length: 20 }, (_, i) => ({
  email:    `loadtest.user${i}@agro-ai-test.local`,
  password: 'LoadTest@2024!',
  fullName: `Load Tester ${i}`,
}));

const PLANT_QUERIES   = ['tomato', 'wheat', 'rice', 'mango', 'neem', 'tulsi', 'cotton', 'banana'];
const PLANT_CATEGORIES= ['crop', 'vegetable', 'fruit plant', 'medicinal plant'];
const CHAT_QUESTIONS  = [
  'What is the best fertilizer for wheat?',
  'How to treat tomato leaf curl disease?',
  'What is the ideal soil pH for rice cultivation?',
  'How much water does cotton need per week?',
  'What are the signs of iron deficiency in crops?',
  'How to control aphids organically?',
  'What is NPK and how to apply it?',
  'Best crops for black soil in Maharashtra?',
];

// ─── Helper: pick random element ──────────────────────────────────────────────
function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

// ─── Helper: record custom metric + global error tracking ─────────────────────
function trackResponse(res, customTrend, tag) {
  totalRequests.add(1, { endpoint: tag });
  const ok = res.status >= 200 && res.status < 400;
  errorRate.add(!ok, { endpoint: tag });
  if (customTrend) customTrend.add(res.timings.duration, { endpoint: tag });
  return ok;
}

// ─── Setup: pre-register test users ───────────────────────────────────────────
export function setup() {
  console.log('🌱  AGRO AI Baseline Test – registering test users…');

  const registered = [];
  for (const u of USER_POOL) {
    const res = http.post(
      `${BASE_URL}/api/auth/signup`,
      JSON.stringify({ email: u.email, password: u.password, fullName: u.fullName, role: 'general' }),
      { headers: JSON_HEADERS, tags: { endpoint: 'setup_register' } },
    );
    // 201 = created, 400 = already exists – both are acceptable during setup
    if (res.status === 201 || res.status === 400) {
      registered.push(u.email);
    }
  }

  console.log(`✅  Setup complete. ${registered.length} test users ready.`);
  return { users: USER_POOL };
}

// ─── Main VU function ─────────────────────────────────────────────────────────
export default function (data) {
  const user = pick(data.users);
  let authToken = '';

  // ── 1. Health Check ──────────────────────────────────────────────────────────
  group('01 Health Check', () => {
    const res = http.get(`${BASE_URL}/api/health`, {
      tags: { endpoint: 'health_check', group: 'health' },
    });
    const ok = trackResponse(res, healthLatency, 'health_check');
    check(res, {
      'health: status 200':          (r) => r.status === 200,
      'health: response has status': (r) => {
        try { return JSON.parse(r.body).status !== undefined; } catch { return false; }
      },
    });
    if (!ok) console.warn(`[health] unexpected status ${res.status}`);
  });

  sleep(0.2);

  // ── 2. Auth: Register (5 % of VUs try a unique new registration) ─────────────
  group('02 Auth Register', () => {
    const uniqueEmail = `reg.${__VU}.${__ITER}@agro-test.local`;
    const payload = JSON.stringify({
      email:    uniqueEmail,
      password: 'TestPass@1234!',
      fullName: `VU ${__VU} Iter ${__ITER}`,
      role:     'general',
    });

    const res = http.post(`${BASE_URL}/api/auth/signup`, payload, {
      headers: JSON_HEADERS,
      tags:    { endpoint: 'auth_register', group: 'auth' },
    });
    trackResponse(res, registerLatency, 'auth_register');
    check(res, {
      'register: 201 or 400':      (r) => r.status === 201 || r.status === 400,
      'register: has token or err': (r) => {
        try {
          const b = JSON.parse(r.body);
          return b.token !== undefined || b.detail !== undefined;
        } catch { return false; }
      },
    });
  });

  sleep(0.3);

  // ── 3. Auth: Login ───────────────────────────────────────────────────────────
  group('03 Auth Login', () => {
    const res = http.post(
      `${BASE_URL}/api/auth/login`,
      JSON.stringify({ email: user.email, password: user.password }),
      { headers: JSON_HEADERS, tags: { endpoint: 'auth_login', group: 'auth' } },
    );
    const ok = trackResponse(res, loginLatency, 'auth_login');
    check(res, {
      'login: status 200':    (r) => r.status === 200,
      'login: has token':     (r) => {
        try { return !!JSON.parse(r.body).token; } catch { return false; }
      },
      'login: has user obj':  (r) => {
        try { return !!JSON.parse(r.body).user; } catch { return false; }
      },
    });
    if (ok && res.status === 200) {
      try { authToken = JSON.parse(res.body).token || ''; } catch { /* ignore */ }
    }
  });

  sleep(0.2);

  const authHeaders = {
    ...JSON_HEADERS,
    ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
  };

  // ── 4. Auth: Get /me ─────────────────────────────────────────────────────────
  if (authToken) {
    group('04 Auth Me', () => {
      const res = http.get(`${BASE_URL}/api/auth/me`, {
        headers: authHeaders,
        tags:    { endpoint: 'auth_me', group: 'auth' },
      });
      trackResponse(res, null, 'auth_me');
      check(res, {
        'me: status 200':  (r) => r.status === 200,
        'me: has user':    (r) => {
          try { return !!JSON.parse(r.body).user; } catch { return false; }
        },
      });
    });
    sleep(0.1);
  }

  // ── 5. Assistant Chat ────────────────────────────────────────────────────────
  group('05 Assistant Chat', () => {
    const chatPayload = JSON.stringify({
      message:   pick(CHAT_QUESTIONS),
      sessionId: `load-test-vu${__VU}`,
      history:   [],
    });

    const res = http.post(`${BASE_URL}/api/assistant/chat`, chatPayload, {
      headers: authHeaders,
      tags:    { endpoint: 'assistant_chat', group: 'assistant' },
      timeout: '30s',
    });
    trackResponse(res, chatLatency, 'assistant_chat');
    check(res, {
      'chat: status 200':       (r) => r.status === 200,
      'chat: has response':     (r) => {
        try { return typeof JSON.parse(r.body).response === 'string'; } catch { return false; }
      },
      'chat: has sessionId':    (r) => {
        try { return !!JSON.parse(r.body).sessionId; } catch { return false; }
      },
    });
  });

  sleep(0.5);

  // ── 6. Assistant Status ──────────────────────────────────────────────────────
  group('06 Assistant Status', () => {
    const res = http.get(`${BASE_URL}/api/assistant/status`, {
      headers: authHeaders,
      tags:    { endpoint: 'assistant_status', group: 'assistant' },
    });
    trackResponse(res, null, 'assistant_status');
    check(res, { 'assistant status: 200': (r) => r.status === 200 });
  });

  sleep(0.2);

  // ── 7. Plant: Search ─────────────────────────────────────────────────────────
  group('07 Plant Search', () => {
    const q   = pick(PLANT_QUERIES);
    const cat = pick(PLANT_CATEGORIES);

    // Full-text search
    const searchRes = http.get(
      `${BASE_URL}/api/plants/search?q=${encodeURIComponent(q)}&limit=20&page=1`,
      { headers: JSON_HEADERS, tags: { endpoint: 'plant_search', group: 'plants' } },
    );
    trackResponse(searchRes, plantLatency, 'plant_search');
    check(searchRes, {
      'plant search: 200':         (r) => r.status === 200,
      'plant search: has results': (r) => {
        try {
          const b = JSON.parse(r.body);
          return Array.isArray(b.results) || b.total !== undefined;
        } catch { return false; }
      },
    });

    // Category-filtered search
    const catRes = http.get(
      `${BASE_URL}/api/plants/search?category=${encodeURIComponent(cat)}&limit=10`,
      { headers: JSON_HEADERS, tags: { endpoint: 'plant_search_category', group: 'plants' } },
    );
    trackResponse(catRes, plantLatency, 'plant_search_category');
    check(catRes, { 'plant cat search: 200': (r) => r.status === 200 });
  });

  sleep(0.2);

  // ── 8. Plant: Autocomplete ────────────────────────────────────────────────────
  group('08 Plant Autocomplete', () => {
    const q   = pick(PLANT_QUERIES).slice(0, 3); // short prefix
    const res = http.get(
      `${BASE_URL}/api/plants/autocomplete?q=${encodeURIComponent(q)}&limit=10`,
      { headers: JSON_HEADERS, tags: { endpoint: 'plant_autocomplete', group: 'plants' } },
    );
    trackResponse(res, plantLatency, 'plant_autocomplete');
    check(res, {
      'autocomplete: 200':      (r) => r.status === 200,
      'autocomplete: is array': (r) => {
        try { return Array.isArray(JSON.parse(r.body)); } catch { return false; }
      },
    });
  });

  sleep(0.1);

  // ── 9. Plant: Categories & Stats ─────────────────────────────────────────────
  group('09 Plant Categories & Stats', () => {
    const catRes = http.get(`${BASE_URL}/api/plants/categories`, {
      headers: JSON_HEADERS,
      tags:    { endpoint: 'plant_categories', group: 'plants' },
    });
    trackResponse(catRes, plantLatency, 'plant_categories');
    check(catRes, { 'categories: 200': (r) => r.status === 200 });

    const statsRes = http.get(`${BASE_URL}/api/plants/stats`, {
      headers: JSON_HEADERS,
      tags:    { endpoint: 'plant_stats', group: 'plants' },
    });
    trackResponse(statsRes, plantLatency, 'plant_stats');
    check(statsRes, { 'stats: 200': (r) => r.status === 200 });
  });

  sleep(0.2);

  // ── 10. Production: Health & Catalogue ───────────────────────────────────────
  group('10 Production Catalogue', () => {
    const healthRes = http.get(`${BASE_URL}/api/production/health`, {
      headers: JSON_HEADERS,
      tags:    { endpoint: 'production_health', group: 'production' },
    });
    trackResponse(healthRes, prodLatency, 'production_health');
    check(healthRes, { 'prod health: 200': (r) => r.status === 200 });

    const plantsRes = http.get(`${BASE_URL}/api/production/supported-plants`, {
      headers: JSON_HEADERS,
      tags:    { endpoint: 'production_supported_plants', group: 'production' },
    });
    trackResponse(plantsRes, prodLatency, 'production_supported_plants');
    check(plantsRes, {
      'supported plants: 200': (r) => r.status === 200,
      'supported plants: array': (r) => {
        try { return Array.isArray(JSON.parse(r.body)); } catch { return false; }
      },
    });

    const soilRes = http.get(`${BASE_URL}/api/production/soil-types`, {
      headers: JSON_HEADERS,
      tags:    { endpoint: 'production_soil_types', group: 'production' },
    });
    trackResponse(soilRes, prodLatency, 'production_soil_types');
    check(soilRes, { 'soil types: 200': (r) => r.status === 200 });
  });

  sleep(0.2);

  // ── 11. Nutrition: Calculate ──────────────────────────────────────────────────
  group('11 Nutrition Calculate', () => {
    const nutritionPayload = JSON.stringify({
      age:                  25 + Math.floor(Math.random() * 30),
      gender:               Math.random() > 0.5 ? 'male' : 'female',
      heightCm:             155 + Math.random() * 30,
      weightKg:             50  + Math.random() * 40,
      activityLevel:        pick(['sedentary', 'light', 'moderate', 'active', 'very_active']),
      goal:                 pick(['weight_loss', 'weight_gain', 'maintenance']),
      goalWeightKg:         50  + Math.random() * 40,
      mealsPerDay:          pick([3, 4, 5]),
      targetTimelineWeeks:  pick([4, 8, 12, 16]),
      dietaryRestrictions:  [],
      foodPreference:       pick(['vegetarian', 'non_vegetarian', 'vegan']),
    });

    const res = http.post(`${BASE_URL}/api/nutrition/calculate`, nutritionPayload, {
      headers: JSON_HEADERS,
      tags:    { endpoint: 'nutrition_calculate', group: 'nutrition' },
    });
    trackResponse(res, nutritionLatency, 'nutrition_calculate');
    check(res, {
      'nutrition calc: 200':    (r) => r.status === 200,
      'nutrition calc: has bmi':(r) => {
        try { return JSON.parse(r.body).bmi !== undefined; } catch { return false; }
      },
    });
  });

  sleep(0.2);

  // ── 12. Nutrition: Foods Search ───────────────────────────────────────────────
  group('12 Nutrition Foods', () => {
    const queries = ['rice', 'dal', 'roti', 'paneer', 'chicken', 'banana', 'milk'];
    const q = pick(queries);

    const res = http.get(
      `${BASE_URL}/api/nutrition/foods?query=${encodeURIComponent(q)}`,
      { headers: JSON_HEADERS, tags: { endpoint: 'nutrition_foods', group: 'nutrition' } },
    );
    trackResponse(res, nutritionLatency, 'nutrition_foods');
    check(res, {
      'foods: 200':        (r) => r.status === 200,
      'foods: has results':(r) => {
        try { return Array.isArray(JSON.parse(r.body).results); } catch { return false; }
      },
    });
  });

  sleep(0.2);

  // ── 13. Farm Calculator ───────────────────────────────────────────────────────
  group('13 Farm Calculator', () => {
    const calcPayload = JSON.stringify({
      calcType: 'npk_fertilizer',
      params: {
        targetN:  120,
        targetP:  60,
        targetK:  40,
        area:     1.0,
        unit:     'ha',
        useSSP:   false,
      },
    });

    const res = http.post(`${BASE_URL}/api/assistant/calculate`, calcPayload, {
      headers: JSON_HEADERS,
      tags:    { endpoint: 'farm_calculator', group: 'assistant' },
    });
    trackResponse(res, null, 'farm_calculator');
    check(res, { 'farm calc: 200': (r) => r.status === 200 });
  });

  sleep(0.3);
}

// ─── Teardown: print summary ───────────────────────────────────────────────────
export function teardown(data) {
  console.log('\n══════════════════════════════════════════════════════');
  console.log('  AGRO AI Load Test – Baseline Run Complete');
  console.log('══════════════════════════════════════════════════════');
  console.log(`  VUs:      100`);
  console.log(`  Duration: 1 minute`);
  console.log('  Endpoints tested:');
  console.log('    ✔ GET  /api/health');
  console.log('    ✔ POST /api/auth/signup');
  console.log('    ✔ POST /api/auth/login');
  console.log('    ✔ GET  /api/auth/me');
  console.log('    ✔ POST /api/assistant/chat');
  console.log('    ✔ GET  /api/assistant/status');
  console.log('    ✔ POST /api/assistant/calculate');
  console.log('    ✔ GET  /api/plants/search');
  console.log('    ✔ GET  /api/plants/autocomplete');
  console.log('    ✔ GET  /api/plants/categories');
  console.log('    ✔ GET  /api/plants/stats');
  console.log('    ✔ GET  /api/production/health');
  console.log('    ✔ GET  /api/production/supported-plants');
  console.log('    ✔ GET  /api/production/soil-types');
  console.log('    ✔ POST /api/nutrition/calculate');
  console.log('    ✔ GET  /api/nutrition/foods');
  console.log('══════════════════════════════════════════════════════\n');
}
