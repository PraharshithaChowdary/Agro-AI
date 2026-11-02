'use strict';

/**
 * AGRO AI Selenium Test Configuration
 */
module.exports = {
  BASE_URL: process.env.BASE_URL || 'http://localhost:5173',
  BACKEND_URL: process.env.BACKEND_URL || 'http://localhost:8000',
  TEST_TIMEOUT: parseInt(process.env.TEST_TIMEOUT || '30000'),
  PAGE_LOAD_WAIT: parseInt(process.env.PAGE_LOAD_WAIT || '1500'),
  SCREENSHOT_PATH: process.env.SCREENSHOT_PATH || './screenshots',
  HEADLESS: process.env.HEADLESS !== 'false',
  BROWSER: process.env.BROWSER || 'chrome',
  IMPLICIT_WAIT: 5000,
  EXPLICIT_WAIT: 10000,
  PAGE_LOAD_TIMEOUT: 30000,
  TEST_USER: {
    email: process.env.TEST_EMAIL || 'selenium_e2e@agro-test.com',
    password: process.env.TEST_PASSWORD || 'Selenium@Test123',
    name: 'Selenium Test User',
  },
};
