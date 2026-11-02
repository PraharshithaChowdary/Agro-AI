/**
 * AGRO AI - WebdriverIO + Appium Configuration
 * Supports Android (Chrome) and iOS (Safari) for PWA testing
 */

require('dotenv').config();

const APP_URL = process.env.APP_URL || 'http://10.0.2.2:5173'; // 10.0.2.2 = localhost for Android emulator
const PLATFORM = process.env.PLATFORM || 'android';
const APPIUM_HOST = process.env.APPIUM_HOST || 'localhost';
const APPIUM_PORT = parseInt(process.env.APPIUM_PORT || '4723');
const DEVICE_NAME = process.env.DEVICE_NAME || 'Pixel 4 API 30';
const ANDROID_VERSION = process.env.ANDROID_VERSION || '11.0';
const IOS_DEVICE = process.env.IOS_DEVICE || 'iPhone 13';
const IOS_VERSION = process.env.IOS_VERSION || '16.0';
const IMPLICIT_WAIT = parseInt(process.env.IMPLICIT_WAIT || '10000');
const PAGE_LOAD_TIMEOUT = parseInt(process.env.PAGE_LOAD_TIMEOUT || '30000');

// Android Chrome capabilities for PWA testing
const androidCapabilities = {
  platformName: 'Android',
  'appium:automationName': 'UiAutomator2',
  'appium:deviceName': DEVICE_NAME,
  'appium:platformVersion': ANDROID_VERSION,
  'appium:browserName': 'Chrome',
  'appium:chromedriverAutodownload': true,
  'appium:newCommandTimeout': 300,
  'appium:noReset': false,
  'appium:fullReset': false,
  'appium:chromeOptions': {
    args: [
      '--disable-popup-blocking',
      '--no-first-run',
      '--disable-infobars',
      '--disable-notifications',
      '--allow-insecure-localhost',
      '--enable-experimental-web-platform-features'
    ]
  },
  'appium:appWaitActivity': '*',
  'goog:chromeOptions': {
    mobileEmulation: {
      deviceName: 'Pixel 4'
    }
  }
};

// iOS Safari capabilities for PWA testing
const iosCapabilities = {
  platformName: 'iOS',
  'appium:automationName': 'XCUITest',
  'appium:deviceName': IOS_DEVICE,
  'appium:platformVersion': IOS_VERSION,
  'appium:browserName': 'Safari',
  'appium:newCommandTimeout': 300,
  'appium:noReset': false,
  'appium:safariInitialUrl': APP_URL,
  'appium:safariAllowPopups': true,
  'appium:safariIgnoreFraudWarning': true,
  'appium:safariOpenLinksInBackground': false
};

const selectedCapabilities = PLATFORM === 'ios' ? iosCapabilities : androidCapabilities;

exports.config = {
  //
  // ====================
  // Runner Configuration
  // ====================
  runner: 'local',
  hostname: APPIUM_HOST,
  port: APPIUM_PORT,
  path: '/wd/hub',

  //
  // ==================
  // Specify Test Files
  // ==================
  specs: [
    './tests/**/*.js'
  ],

  exclude: [],

  //
  // ============
  // Capabilities
  // ============
  maxInstances: 1,

  capabilities: [selectedCapabilities],

  //
  // ===================
  // Test Configurations
  // ===================
  logLevel: 'info',
  bail: 0,
  waitforTimeout: IMPLICIT_WAIT,
  connectionRetryTimeout: 120000,
  connectionRetryCount: 3,

  //
  // ========
  // Services
  // ========
  services: [
    ['appium', {
      args: {
        address: APPIUM_HOST,
        port: APPIUM_PORT,
        relaxedSecurity: true,
        allowInsecure: ['chromedriver_autodownload'],
        log: './appium-tests/logs/appium.log'
      },
      logFileName: 'appium.log',
      outputDir: './appium-tests/logs/'
    }]
  ],

  //
  // ==========
  // Frameworks
  // ==========
  framework: 'mocha',
  mochaOpts: {
    ui: 'bdd',
    timeout: 120000,
    retries: 1
  },

  //
  // ====================
  // Test Suites
  // ====================
  suites: {
    login: ['./tests/agro-ai-mobile-tests.js'],
    dashboard: ['./tests/agro-ai-mobile-tests.js'],
    plant: ['./tests/agro-ai-mobile-tests.js'],
    ai: ['./tests/agro-ai-mobile-tests.js'],
    nutrition: ['./tests/agro-ai-mobile-tests.js'],
    all: ['./tests/agro-ai-mobile-tests.js']
  },

  //
  // ==========
  // Reporters
  // ==========
  reporters: [
    'spec',
    ['allure', {
      outputDir: './appium-tests/reports/allure-results',
      disableWebdriverStepsReporting: true,
      disableWebdriverScreenshotsReporting: false
    }]
  ],

  //
  // ==============
  // Hooks
  // ==============

  /**
   * Gets executed once before all workers get launched.
   */
  onPrepare: function (config, capabilities) {
    const fs = require('fs');
    const dirs = [
      './appium-tests/reports',
      './appium-tests/reports/screenshots',
      './appium-tests/reports/allure-results',
      './appium-tests/logs'
    ];
    dirs.forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    });
    console.log('\n🌱 AGRO AI Mobile Test Suite Starting...');
    console.log(`📱 Platform: ${PLATFORM.toUpperCase()}`);
    console.log(`🌐 App URL: ${APP_URL}`);
    console.log(`📋 Device: ${PLATFORM === 'ios' ? IOS_DEVICE : DEVICE_NAME}\n`);
  },

  /**
   * Gets executed before test execution begins.
   */
  before: async function (capabilities, specs) {
    // Set browser URL
    global.APP_URL = APP_URL;

    // Add custom commands
    browser.addCommand('tapByCoordinates', async function (x, y) {
      await browser.touchAction([
        { action: 'tap', x, y }
      ]);
    });

    browser.addCommand('swipeDown', async function () {
      const { width, height } = await browser.getWindowSize();
      await browser.touchAction([
        { action: 'press', x: width / 2, y: height * 0.3 },
        { action: 'moveTo', x: width / 2, y: height * 0.7 },
        'release'
      ]);
    });

    browser.addCommand('swipeUp', async function () {
      const { width, height } = await browser.getWindowSize();
      await browser.touchAction([
        { action: 'press', x: width / 2, y: height * 0.7 },
        { action: 'moveTo', x: width / 2, y: height * 0.3 },
        'release'
      ]);
    });

    // Navigate to the app
    await browser.url(APP_URL);
    await browser.setWindowSize(390, 844); // iPhone 14-like viewport for PWA
  },

  /**
   * Gets executed after each test
   */
  afterTest: async function (test, context, { error, result, duration, passed }) {
    if (!passed) {
      const path = require('path');
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const testName = test.title.replace(/[^a-zA-Z0-9]/g, '_').substring(0, 50);
      const screenshotPath = path.resolve(
        `./appium-tests/reports/screenshots/${testName}_${timestamp}.png`
      );
      try {
        await browser.saveScreenshot(screenshotPath);
        console.log(`📸 Screenshot saved: ${screenshotPath}`);
      } catch (e) {
        console.warn('Could not save screenshot:', e.message);
      }
    }
  },

  /**
   * Gets executed after all tests are done
   */
  onComplete: async function (exitCode, config, capabilities, results) {
    console.log('\n🌱 AGRO AI Mobile Test Suite Complete!');
    console.log(`✅ Passed: ${results && results.passed || 0}`);
    console.log(`❌ Failed: ${results && results.failed || 0}`);
    console.log(`📊 Reports: ./appium-tests/reports/\n`);

    // Trigger Excel report generation
    try {
      const { generateExcelReport } = require('./utils/excel-reporter');
      await generateExcelReport();
      console.log('📑 Excel report generated!');
    } catch (e) {
      console.warn('Could not generate Excel report:', e.message);
    }
  }
};
