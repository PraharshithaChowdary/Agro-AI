#!/usr/bin/env python3
"""
AGRO AI — API Security Check (DAST)
====================================
Performs dynamic security testing against the AGRO AI backend API.
Checks for OWASP Top 10 vulnerabilities in a non-destructive manner.

Usage:
  python api-security-check.py --base-url http://localhost:8000 --output dast-results.json
"""
import argparse
import json
import time
import sys
from datetime import datetime

try:
    import requests
    requests.packages.urllib3.disable_warnings()
except ImportError:
    print("Install: pip install requests")
    sys.exit(1)

BASE_URL = "http://localhost:8000"
findings = []
test_results = []

def finding(severity, vuln_type, endpoint, description, impact, fix, evidence=""):
    findings.append({
        "id": f"DAST-{len(findings)+1:03d}",
        "severity": severity,
        "type": vuln_type,
        "endpoint": endpoint,
        "description": description,
        "impact": impact,
        "fix": fix,
        "evidence": evidence,
        "timestamp": datetime.now().isoformat(),
    })

def test(name, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    test_results.append({"name": name, "status": status, "detail": detail})
    icon = "✅" if passed else "❌"
    print(f"  {icon} {name}: {status}{(' — ' + detail) if detail else ''}")
    return passed

def req(method, path, **kwargs):
    try:
        return getattr(requests, method)(
            f"{BASE_URL}{path}",
            timeout=10,
            verify=False,
            **kwargs
        )
    except Exception as e:
        return type('R', (), {'status_code': 0, 'json': lambda: {}, 'headers': {}, 'text': str(e), 'elapsed': type('T', (), {'total_seconds': lambda: 9999})()})()

# ── Test Groups ────────────────────────────────────────────────
def test_health():
    print("\n[1] Health Check & Discovery")
    r = req('get', '/api/health')
    test("Health endpoint returns 200", r.status_code == 200)
    test("Health response is JSON", 'application/json' in r.headers.get('content-type', ''))

    # Check for security headers
    h = r.headers
    if 'X-Content-Type-Options' not in h:
        finding("LOW", "Missing Security Header", "/api/health",
                "Missing X-Content-Type-Options header",
                "Browser MIME type sniffing attacks",
                "Add: X-Content-Type-Options: nosniff")
    test("X-Content-Type-Options header present", 'X-Content-Type-Options' in h)

    if 'X-Frame-Options' not in h:
        finding("LOW", "Missing Security Header", "/api/health",
                "Missing X-Frame-Options header",
                "Clickjacking attacks",
                "Add: X-Frame-Options: DENY")
    test("X-Frame-Options header present", 'X-Frame-Options' in h)

    if 'Strict-Transport-Security' not in h:
        finding("MEDIUM", "Missing Security Header", "/api/health",
                "Missing HSTS header",
                "Downgrade attacks to HTTP",
                "Add: Strict-Transport-Security: max-age=31536000; includeSubDomains")
    test("HSTS header present", 'Strict-Transport-Security' in h)

def test_authentication():
    print("\n[2] Authentication Security")

    # Test missing auth on protected endpoints
    protected = ["/api/auth/me", "/api/production/", "/api/nutrition/history"]
    for ep in protected:
        r = req('get', ep)
        passed = r.status_code in [401, 403, 422]
        if not passed:
            finding("HIGH", "Missing Authentication", ep,
                    f"Endpoint {ep} accessible without authentication (status {r.status_code})",
                    "Unauthorized data access",
                    "Add JWT authentication dependency to this endpoint")
        test(f"Protected endpoint {ep} requires auth", passed)

    # Test invalid token
    r = req('get', '/api/auth/me', headers={'Authorization': 'Bearer invalid.token.here'})
    test("Invalid JWT token rejected", r.status_code in [401, 422], f"status={r.status_code}")
    if r.status_code == 200:
        finding("CRITICAL", "JWT Validation Bypass", "/api/auth/me",
                "Invalid JWT token was accepted",
                "Complete authentication bypass",
                "Validate JWT signature properly using python-jose")

    # Test expired token (fake expired JWT)
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QHRlc3QuY29tIiwiZXhwIjoxNjAwMDAwMDAwfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    r = req('get', '/api/auth/me', headers={'Authorization': f'Bearer {expired_token}'})
    test("Expired JWT token rejected", r.status_code in [401, 422], f"status={r.status_code}")

    # Test none algorithm JWT
    none_token = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0ZXN0QHRlc3QuY29tIn0."
    r = req('get', '/api/auth/me', headers={'Authorization': f'Bearer {none_token}'})
    test("JWT none algorithm rejected", r.status_code in [401, 422], f"status={r.status_code}")
    if r.status_code == 200:
        finding("CRITICAL", "JWT Algorithm Confusion", "/api/auth/me",
                "JWT with alg=none was accepted",
                "Complete authentication bypass",
                "Explicitly specify allowed algorithms in JWT validation")

def test_injection():
    print("\n[3] Injection Attacks")

    # SQL Injection in login
    sql_payloads = ["' OR '1'='1", "'; DROP TABLE users; --", "' OR 1=1 --"]
    for payload in sql_payloads:
        r = req('post', '/api/auth/login',
                json={"email": payload, "password": payload},
                headers={"Content-Type": "application/json"})
        passed = r.status_code not in [200]
        test(f"SQL injection blocked in login: {payload[:20]}", passed)
        if not passed:
            finding("CRITICAL", "SQL Injection", "/api/auth/login",
                    f"SQL injection payload succeeded: {payload}",
                    "Database compromise, data exfiltration",
                    "Use parameterized queries/ORM with proper input validation")

    # Path traversal in query params
    traversal_payloads = ["../../../etc/passwd", "..%2F..%2Fetc%2Fpasswd"]
    for payload in traversal_payloads:
        r = req('get', f'/api/plants/search?q={payload}')
        passed = r.status_code not in [500] and 'root:' not in r.text
        test(f"Path traversal blocked: {payload[:25]}", passed)

def test_cors():
    print("\n[4] CORS Configuration")
    r = req('options', '/api/health',
            headers={"Origin": "https://evil.com", "Access-Control-Request-Method": "GET"})

    origin = r.headers.get('Access-Control-Allow-Origin', '')
    if origin == '*' or origin == 'https://evil.com':
        finding("HIGH", "Dangerous CORS", "/api/health",
                f"CORS allows all origins: Access-Control-Allow-Origin: {origin}",
                "Cross-origin data theft and CSRF attacks",
                "Restrict CORS to known origins. Remove allow_origin_regex=r'.*' from FastAPI CORS config")
    test("CORS does not allow all origins blindly", origin not in ['*'])

    creds = r.headers.get('Access-Control-Allow-Credentials', '')
    if creds == 'true' and origin == '*':
        finding("CRITICAL", "Dangerous CORS with Credentials", "/api/health",
                "CORS allows all origins with credentials — this is rejected by browsers but indicates misconfiguration",
                "Credential theft from any origin",
                "Never combine Access-Control-Allow-Origin: * with credentials: true")
    test("CORS credentials not combined with wildcard", not (creds == 'true' and origin == '*'))

def test_rate_limiting():
    print("\n[5] Rate Limiting")

    # Attempt 15 rapid login requests
    success_count = 0
    for i in range(15):
        r = req('post', '/api/auth/login',
                json={"email": "ratelimit@test.com", "password": f"wrong{i}"},
                headers={"Content-Type": "application/json"})
        if r.status_code == 200:
            success_count += 1
        if r.status_code == 429:
            break
        time.sleep(0.1)

    has_rate_limit = any(
        req('post', '/api/auth/login',
            json={"email": "rl@test.com", "password": "wrong"},
            headers={"Content-Type": "application/json"}).status_code == 429
        for _ in range(1)
    )
    if not has_rate_limit:
        finding("HIGH", "Missing Rate Limiting", "/api/auth/login",
                "No rate limiting detected on login endpoint after 15 failed attempts",
                "Brute force attacks on user accounts",
                "Implement slowapi or similar rate limiting: @limiter.limit('5/minute') on login endpoint")
    test("Rate limiting active on login endpoint", has_rate_limit)

def test_data_exposure():
    print("\n[6] Sensitive Data Exposure")

    # Check if error messages leak stack traces
    r = req('get', '/api/nonexistent-endpoint-xyz')
    leaked = any(keyword in r.text for keyword in ['Traceback', 'File "/', '__pycache__', 'uvicorn'])
    if leaked:
        finding("MEDIUM", "Information Leakage", "/api/nonexistent-endpoint-xyz",
                "Error response leaks server internals/stack trace",
                "Server technology fingerprinting",
                "Enable FastAPI exception handlers to return generic error messages in production")
    test("Error responses do not leak stack traces", not leaked)

    # Check server header
    server = r.headers.get('Server', '')
    if server:
        finding("LOW", "Server Header Disclosure", "/api/nonexistent-endpoint-xyz",
                f"Server header discloses technology: {server}",
                "Technology fingerprinting",
                "Remove or obfuscate the Server header")
    test("Server header not disclosing technology", not bool(server))

def test_openapi():
    print("\n[7] API Documentation Exposure")
    for path in ['/docs', '/openapi.json', '/redoc']:
        r = req('get', path)
        if r.status_code == 200:
            finding("LOW", "API Documentation Exposed", path,
                    f"API documentation accessible at {path}",
                    "API structure exposure to attackers",
                    f"Disable {path} in production: app = FastAPI(docs_url=None, redoc_url=None)")
        test(f"OpenAPI {path} not publicly accessible (or acceptable)", r.status_code in [200, 401, 403, 404])

def main():
    global BASE_URL
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', default='http://localhost:8000')
    parser.add_argument('--output', default='dast-results.json')
    args = parser.parse_args()
    BASE_URL = args.base_url.rstrip('/')

    print("=" * 60)
    print("  AGRO AI — API Security Check (DAST)")
    print(f"  Target: {BASE_URL}")
    print("=" * 60)

    try:
        test_health()
        test_authentication()
        test_injection()
        test_cors()
        test_rate_limiting()
        test_data_exposure()
        test_openapi()
    except Exception as e:
        print(f"\n⚠️  Test interrupted: {e}")

    passed = sum(1 for t in test_results if t['status'] == 'PASS')
    total  = len(test_results)
    crit   = sum(1 for f in findings if f['severity'] == 'CRITICAL')
    high   = sum(1 for f in findings if f['severity'] == 'HIGH')
    med    = sum(1 for f in findings if f['severity'] == 'MEDIUM')
    low    = sum(1 for f in findings if f['severity'] == 'LOW')

    print(f"\n{'='*60}")
    print(f"  Results: {passed}/{total} tests passed")
    print(f"  Findings: Critical={crit}, High={high}, Medium={med}, Low={low}")
    print(f"{'='*60}")

    output = {
        "tool": "AGRO AI DAST Scanner",
        "target": BASE_URL,
        "timestamp": datetime.now().isoformat(),
        "summary": {"total_tests": total, "passed": passed, "critical": crit, "high": high, "medium": med, "low": low},
        "findings": findings,
        "test_results": test_results,
    }
    with open(args.output, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\n✅ Results saved to: {args.output}")

if __name__ == "__main__":
    main()
