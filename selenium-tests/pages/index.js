/**
 * AGRO AI — Page Object Models
 * Lightweight POM stubs used by the test suite.
 * Each page class encapsulates selectors and actions for one route.
 */

'use strict';

const { By, until, Key } = require('selenium-webdriver');
const config = require('../config/test-config');

// ──────────────────────────────────────────────────────────────────────────────
// BasePage
// ──────────────────────────────────────────────────────────────────────────────
class BasePage {
  constructor(driver) {
    this.driver  = driver;
    this.timeout = config.timeouts.elementVisible;
  }

  async navigate(route) {
    await this.driver.get(config.BASE_URL + route);
  }

  async getTitle() {
    return this.driver.getTitle();
  }

  async findElement(locator) {
    await this.driver.wait(until.elementLocated(locator), this.timeout);
    return this.driver.findElement(locator);
  }

  async findElements(locator) {
    await this.driver.wait(until.elementLocated(locator), this.timeout).catch(() => {});
    return this.driver.findElements(locator);
  }

  async click(locator) {
    const el = await this.findElement(locator);
    await this.driver.wait(until.elementIsVisible(el), this.timeout);
    await el.click();
  }

  async type(locator, text) {
    const el = await this.findElement(locator);
    await el.clear();
    await el.sendKeys(text);
  }

  async getText(locator) {
    const el = await this.findElement(locator);
    return el.getText();
  }

  async getValue(locator) {
    const el = await this.findElement(locator);
    return el.getAttribute('value');
  }

  async getAttribute(locator, attr) {
    const el = await this.findElement(locator);
    return el.getAttribute(attr);
  }

  async isDisplayed(locator) {
    try {
      const el = await this.driver.findElement(locator);
      return el.isDisplayed();
    } catch (_) {
      return false;
    }
  }

  async isEnabled(locator) {
    const el = await this.findElement(locator);
    return el.isEnabled();
  }

  async waitForUrl(urlContains, timeout = this.timeout) {
    await this.driver.wait(until.urlContains(urlContains), timeout);
  }

  async getCurrentUrl() {
    return this.driver.getCurrentUrl();
  }

  async scrollIntoView(locator) {
    const el = await this.findElement(locator);
    await this.driver.executeScript('arguments[0].scrollIntoView(true)', el);
  }

  async pressEnter(locator) {
    const el = await this.findElement(locator);
    await el.sendKeys(Key.RETURN);
  }

  async takeScreenshot() {
    return this.driver.takeScreenshot();
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// LoginPage
// ──────────────────────────────────────────────────────────────────────────────
class LoginPage extends BasePage {
  constructor(driver) {
    super(driver);
    this.sel = {
      emailInput:       By.css('input[type="email"], input[name="email"], #email'),
      passwordInput:    By.css('input[type="password"], input[name="password"], #password'),
      submitBtn:        By.css('button[type="submit"], button.login-btn, .sign-in-btn'),
      forgotPasswordLink: By.css('a[href*="forgot"], .forgot-password-link'),
      signUpLink:       By.css('a[href*="signup"], a[href*="register"], .signup-link'),
      errorMsg:         By.css('.error-message, .alert-error, [role="alert"]'),
      rememberMe:       By.css('input[type="checkbox"][name*="remember"]'),
      showPasswordBtn:  By.css('.show-password, .toggle-password, [aria-label*="show"]'),
      logo:             By.css('.logo, img.logo, header img'),
      pageHeading:      By.css('h1, h2.heading, .auth-title'),
    };
  }

  async open() { await this.navigate(config.routes.signIn); }

  async login(email, password) {
    await this.type(this.sel.emailInput, email);
    await this.type(this.sel.passwordInput, password);
    await this.click(this.sel.submitBtn);
  }

  async getErrorMessage() {
    return this.getText(this.sel.errorMsg);
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// RegisterPage
// ──────────────────────────────────────────────────────────────────────────────
class RegisterPage extends BasePage {
  constructor(driver) {
    super(driver);
    this.sel = {
      nameInput:        By.css('input[name="name"], input[name="fullName"], #name'),
      emailInput:       By.css('input[type="email"], input[name="email"]'),
      passwordInput:    By.css('input[name="password"], #password'),
      confirmPassword:  By.css('input[name="confirmPassword"], input[name="confirm_password"]'),
      phoneInput:       By.css('input[name="phone"], input[type="tel"]'),
      termsCheckbox:    By.css('input[name="terms"], input[type="checkbox"]'),
      submitBtn:        By.css('button[type="submit"], .register-btn'),
      errorMsg:         By.css('.error-message, [role="alert"]'),
      successMsg:       By.css('.success-message, .alert-success'),
      loginLink:        By.css('a[href*="signin"], a[href*="login"]'),
    };
  }

  async open() { await this.navigate(config.routes.signUp); }

  async register(data) {
    if (data.name)    await this.type(this.sel.nameInput, data.name);
    if (data.email)   await this.type(this.sel.emailInput, data.email);
    if (data.password) await this.type(this.sel.passwordInput, data.password);
    if (data.confirm) await this.type(this.sel.confirmPassword, data.confirm);
    if (data.phone)   await this.type(this.sel.phoneInput, data.phone);
    await this.click(this.sel.submitBtn);
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// DashboardPage
// ──────────────────────────────────────────────────────────────────────────────
class DashboardPage extends BasePage {
  constructor(driver) {
    super(driver);
    this.sel = {
      navMenu:         By.css('nav, .navbar, .sidebar'),
      navLinks:        By.css('nav a, .nav-link, .sidebar-link'),
      logoutBtn:       By.css('.logout-btn, [aria-label="Logout"], button.logout'),
      userName:        By.css('.user-name, .username, .profile-name'),
      statsCards:      By.css('.stat-card, .dashboard-card, .metric-card'),
      quickActions:    By.css('.quick-action, .action-btn, .shortcut'),
      mobileMenuBtn:   By.css('.hamburger, .menu-toggle, [aria-label="Menu"]'),
      breadcrumb:      By.css('.breadcrumb, nav[aria-label="breadcrumb"]'),
    };
  }

  async open() { await this.navigate(config.routes.dashboard); }
  async logout() { await this.click(this.sel.logoutBtn); }
}

// ──────────────────────────────────────────────────────────────────────────────
// PlantAnalysisPage
// ──────────────────────────────────────────────────────────────────────────────
class PlantAnalysisPage extends BasePage {
  constructor(driver) {
    super(driver);
    this.sel = {
      uploadBtn:        By.css('input[type="file"], .upload-btn, .file-input'),
      dropZone:         By.css('.drop-zone, .drag-drop, [data-testid="drop-zone"]'),
      analyseBtn:       By.css('.analyse-btn, button.analyze, [aria-label="Analyse"]'),
      resultContainer:  By.css('.result, .analysis-result, .plant-result'),
      plantName:        By.css('.plant-name, .result-name, [data-testid="plant-name"]'),
      diseaseResult:    By.css('.disease, .disease-result, [data-testid="disease"]'),
      treatmentRec:     By.css('.treatment, .recommendation, [data-testid="treatment"]'),
      downloadBtn:      By.css('.download-btn, [aria-label="Download"]'),
      shareBtn:         By.css('.share-btn, [aria-label="Share"]'),
      newAnalysisBtn:   By.css('.new-analysis, [aria-label="New Analysis"]'),
      progressBar:      By.css('.progress-bar, .upload-progress'),
    };
  }

  async open() { await this.navigate(config.routes.analyseMyPlant); }
}

// ──────────────────────────────────────────────────────────────────────────────
// AIAssistantPage
// ──────────────────────────────────────────────────────────────────────────────
class AIAssistantPage extends BasePage {
  constructor(driver) {
    super(driver);
    this.sel = {
      chatContainer:   By.css('.chat, .chat-container, [data-testid="chat"]'),
      messageInput:    By.css('input.message-input, textarea.message-input, [aria-label="Message"]'),
      sendBtn:         By.css('.send-btn, button[type="submit"], [aria-label="Send"]'),
      chatMessages:    By.css('.message, .chat-message, .msg-bubble'),
      loadingIndicator:By.css('.loading, .typing-indicator, .spinner'),
      clearChatBtn:    By.css('.clear-chat, [aria-label="Clear"]'),
      voiceInputBtn:   By.css('.voice-input, [aria-label="Voice"]'),
      suggestedPrompts:By.css('.suggested-prompt, .quick-reply, .prompt-chip'),
      copyMsgBtn:      By.css('.copy-msg, [aria-label="Copy"]'),
      historyPanel:    By.css('.chat-history, .history-panel'),
    };
  }

  async open() { await this.navigate(config.routes.aiAssistant); }

  async sendMessage(msg) {
    await this.type(this.sel.messageInput, msg);
    await this.click(this.sel.sendBtn);
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// NutritionPage
// ──────────────────────────────────────────────────────────────────────────────
class NutritionPage extends BasePage {
  constructor(driver) {
    super(driver);
    this.sel = {
      ageInput:        By.css('input[name="age"], #age'),
      weightInput:     By.css('input[name="weight"], #weight'),
      heightInput:     By.css('input[name="height"], #height'),
      genderSelect:    By.css('select[name="gender"], [name="gender"]'),
      activitySelect:  By.css('select[name="activity"], [name="activityLevel"]'),
      calculateBtn:    By.css('.calculate-btn, button.calculate, [aria-label="Calculate"]'),
      bmrResult:       By.css('.bmr-result, [data-testid="bmr"], .result-value'),
      tdeeResult:      By.css('.tdee-result, [data-testid="tdee"]'),
      dietPlanTable:   By.css('table.diet-plan, .meal-table, [data-testid="diet-table"]'),
      downloadPlanBtn: By.css('.download-plan, [aria-label="Download Plan"]'),
      macroChart:      By.css('.macro-chart, canvas, [data-testid="macro"]'),
      dietRestrictions:By.css('input[name="restrictions"], .diet-restrictions'),
      vegFilter:       By.css('input[value="vegetarian"], .veg-filter'),
      veganFilter:     By.css('input[value="vegan"], .vegan-filter'),
    };
  }

  async open() { await this.navigate(config.routes.betterNutrition); }

  async calculateBMR(data) {
    await this.type(this.sel.ageInput, String(data.age));
    await this.type(this.sel.weightInput, String(data.weight));
    await this.type(this.sel.heightInput, String(data.height));
    await this.click(this.sel.calculateBtn);
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// ForgotPasswordPage
// ──────────────────────────────────────────────────────────────────────────────
class ForgotPasswordPage extends BasePage {
  constructor(driver) {
    super(driver);
    this.sel = {
      emailInput:  By.css('input[type="email"], #email'),
      submitBtn:   By.css('button[type="submit"], .reset-btn'),
      successMsg:  By.css('.success-message, .alert-success'),
      backToLogin: By.css('a[href*="signin"], .back-to-login'),
    };
  }

  async open() { await this.navigate(config.routes.forgotPassword); }
}

module.exports = {
  BasePage,
  LoginPage,
  RegisterPage,
  DashboardPage,
  PlantAnalysisPage,
  AIAssistantPage,
  NutritionPage,
  ForgotPasswordPage,
};
