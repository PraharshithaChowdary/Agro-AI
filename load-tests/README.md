# AGRO AI – Load & Stress Test Suite

> k6-based performance testing for the AGRO AI FastAPI backend, with an Excel report generator.

---

## 📁 Folder Structure

```
load-tests/
├── baseline-test.js      # 100 VUs × 1 min constant load test
├── stress-test.js        # 10 → 200 → 500 VU ramp stress test
├── generate-report.js    # Node.js Excel report generator
├── package.json          # npm package (exceljs + axios)
├── README.md             # This file
└── reports/              # Output directory (auto-created)
    ├── baseline-result.json
    ├── stress-result.json
    └── load-test-report.xlsx
```

---

## 🛠️ Prerequisites

### 1. Install k6

| Platform | Command |
|----------|---------|
| **Windows (Winget)** | `winget install k6 --source winget` |
| **Windows (Choco)** | `choco install k6` |
| **macOS** | `brew install k6` |
| **Linux (Debian)** | `sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69 && echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list && sudo apt-get update && sudo apt-get install k6` |
| **Docker** | `docker pull grafana/k6` |

Verify: `k6 version`

### 2. Install Node.js dependencies

```bash
cd load-tests
npm install
```

---

## 🚀 Running Tests

> **Make sure the AGRO AI backend is running on `http://localhost:8000` before executing any test.**

### Baseline Test (100 VUs × 1 min)

```bash
# From the project root:
k6 run load-tests/baseline-test.js

# Save raw JSON output for report generation:
k6 run --out json=load-tests/reports/baseline-result.json load-tests/baseline-test.js

# Using npm scripts (from load-tests/ directory):
cd load-tests && npm run baseline
```

### Stress Test (10 → 200 → 500 VUs, 5 min)

```bash
# From the project root:
k6 run load-tests/stress-test.js

# Save raw JSON output:
k6 run --out json=load-tests/reports/stress-result.json load-tests/stress-test.js

# Using npm scripts:
cd load-tests && npm run stress
```

### Generate Excel Report

```bash
# After running baseline test with JSON output:
node load-tests/generate-report.js \
     --input  load-tests/reports/baseline-result.json \
     --output load-tests/reports/load-test-report.xlsx \
     --name   "AGRO AI Baseline"

# For stress test:
node load-tests/generate-report.js \
     --input  load-tests/reports/stress-result.json \
     --output load-tests/reports/stress-report.xlsx \
     --name   "AGRO AI Stress"

# Using npm scripts:
cd load-tests && npm run report
cd load-tests && npm run report:stress
```

### Run Baseline + Report in One Step

```bash
cd load-tests && npm run run:all
```

---

## 📊 Excel Report Contents

The generated `.xlsx` file contains **4 sheets**:

| Sheet | Contents |
|-------|---------|
| **Test Summary** | Test name, date, VUs, duration, total requests, RPS, error rate, avg/min/max/p50/p95/p99 |
| **Endpoint Details** | Per-endpoint: request count, errors, error rate, avg/min/max/p50/p95/p99, pass/fail |
| **Threshold Results** | Each threshold condition with expected vs. actual and pass/fail |
| **Timeline** | Minute-by-minute: requests, errors, error rate, avg duration, RPS |

---

## 🎯 Thresholds

### Baseline Test

| Metric | Threshold |
|--------|-----------|
| p95 response time | < 2000 ms |
| Error rate | < 5% |
| Health endpoint p95 | < 500 ms |
| Login p95 | < 1500 ms |
| Plant search p95 | < 1000 ms |
| Nutrition calculate p95 | < 1500 ms |

### Stress Test (relaxed for high VU count)

| Metric | Threshold |
|--------|-----------|
| p95 response time | < 3000 ms |
| p99 response time | < 5000 ms |
| Error rate | < 10% |
| Chat p95 | < 10000 ms *(LLM inference may queue)* |

---

## 🔌 API Endpoints Covered

| Group | Endpoints |
|-------|-----------|
| **Health** | `GET /api/health` |
| **Auth** | `POST /api/auth/signup`, `POST /api/auth/login`, `GET /api/auth/me` |
| **Assistant** | `POST /api/assistant/chat`, `GET /api/assistant/status`, `POST /api/assistant/calculate` |
| **Plants** | `GET /api/plants/search`, `GET /api/plants/autocomplete`, `GET /api/plants/categories`, `GET /api/plants/stats` |
| **Production** | `GET /api/production/health`, `GET /api/production/supported-plants`, `GET /api/production/soil-types` |
| **Nutrition** | `POST /api/nutrition/calculate`, `GET /api/nutrition/foods` |

> **Note:** Image upload endpoints (`/api/plants/identify`, `/api/production/crop-analysis`, etc.) require multipart form data with real images and are excluded from automated load tests. Test these manually or with a specialized image-upload k6 extension.

---

## 💡 Tips

### Increasing VU Counts
- Each VU requires ~1–2 MB RAM; 500 VUs ≈ 500 MB to 1 GB on the k6 client machine.
- The LLM/Ollama assistant chat endpoint is CPU-bound. At high VU counts, consider reducing chat percentage (`Math.random() < 0.4` threshold in `stress-test.js`).

### Custom Tags for Filtering
All requests are tagged with `endpoint` and `group` for easy filtering in k6 output and dashboards.

### Grafana + InfluxDB Integration
Stream real-time metrics to Grafana:

```bash
k6 run --out influxdb=http://localhost:8086/k6 load-tests/baseline-test.js
```

### Docker Run
```bash
docker run --rm -i --network=host grafana/k6 run - < load-tests/baseline-test.js
```

---

## ⚠️ Warnings

- **Do NOT run stress tests against production.** Always test against a local or staging environment.
- The `setup()` function pre-registers test accounts. These accounts persist in the database. Clean them up with a script if needed.
- Assistant chat calls go through the real Ollama LLM. At 500 VUs, this will heavily load the GPU/CPU. Consider mocking or reducing the chat test percentage for initial runs.
- k6 itself is single-binary and does NOT support `require()` Node.js modules — use only k6 built-in modules in `.js` test files.

---

## 🧹 Cleanup

To remove test user accounts from the database after testing, connect to the SQLite/PostgreSQL database and:

```sql
DELETE FROM users WHERE email LIKE '%@agro-ai-test.local' OR email LIKE '%@agro-test.local';
```
