# 📊 AGRO AI — Automated Test Results & Passed Excel Reports

This directory contains the complete Excel test execution reports for the AGRO AI platform:

| # | Excel Report File | Test Suite | Scope & Pass Rate | Details |
|---|---|---|---|---|
| 1 | **[`1-Load-Test-Report-100VUs-Passed.xlsx`](./1-Load-Test-Report-100VUs-Passed.xlsx)** | k6 Load & Performance | **100 VUs × 60s (120 RPS, 99.53% Pass)** | 4 Sheets: Test Summary, Endpoint Details, Threshold Results, Timeline |
| 2 | **[`2-Security-Vulnerability-Report.xlsx`](./2-Security-Vulnerability-Report.xlsx)** | SAST + DAST + Dependencies | **Full Scan Complete (7 Scanners)** | 4 Sheets: Security Findings, Endpoint Inventory, Dependency Vulnerabilities, Risk Summary |
| 3 | **[`3-Selenium-Web-E2E-300-Tests-Passed.xlsx`](./3-Selenium-Web-E2E-300-Tests-Passed.xlsx)** | Selenium WebDriver E2E | **300+ Test Cases Passed (100% Pass Rate)** | 4 Sheets: Test Summary, Test Details (300+ rows), Category Breakdown, Failed Tests |
| 4 | **[`4-Appium-Mobile-330-Tests-Passed.xlsx`](./4-Appium-Mobile-330-Tests-Passed.xlsx)** | Appium 2 / WebdriverIO Mobile | **330 Test Cases Passed (100% Pass Rate)** | 4 Sheets: Mobile Test Summary, Test Details (330 rows), Device Coverage, Failed Tests |

---

### Test Categories Covered in Selenium & Appium Suites:
- **Authentication & Security**: Login, Session Tokens, Password Reset, Lockout prevention (60 TCs)
- **User Registration & Validation**: Multi-step registration, field validations, role assignment (60 TCs)
- **Farmer Dashboard & Telemetry**: Weather widget, crop health cards, real-time analytics (60 TCs)
- **Plant Disease Diagnosis & Camera Upload**: Leaf scanning, image recognition, treatment advisory (40–60 TCs)
- **AI Agricultural Assistant**: Real-time LLM farming advice, streaming responses (30–40 TCs)
- **Crop Nutrition & Fertilizer Calculator**: NPK calculation, soil recommendations (30–40 TCs)
