/**
 * AGRO AI - DashboardPage Page Object
 * Mobile-first selectors for Appium + WebdriverIO
 */

class DashboardPage {
  // ─── Navigation ────────────────────────────────────────────────────────────

  get bottomNavBar() {
    return $('[data-testid="bottom-nav"]') ||
           $('nav[class*="bottom"]') ||
           $('[role="navigation"]') ||
           $('[class*="bottom-nav"]');
  }

  get homeNavTab() {
    return $('[data-testid="nav-home"]') ||
           $('[aria-label="Home"]') ||
           $('[href="/dashboard"]');
  }

  get plantNavTab() {
    return $('[data-testid="nav-plant"]') ||
           $('[aria-label="Plant Analysis"]') ||
           $('[href*="plant"]');
  }

  get aiNavTab() {
    return $('[data-testid="nav-ai"]') ||
           $('[aria-label="AI Assistant"]') ||
           $('[href*="assistant"]');
  }

  get nutritionNavTab() {
    return $('[data-testid="nav-nutrition"]') ||
           $('[aria-label="Nutrition"]') ||
           $('[href*="nutrition"]');
  }

  get profileNavTab() {
    return $('[data-testid="nav-profile"]') ||
           $('[aria-label="Profile"]') ||
           $('[href*="profile"]');
  }

  // ─── Header ────────────────────────────────────────────────────────────────

  get headerBar() {
    return $('[data-testid="header"]') ||
           $('header') ||
           $('[class*="header"]');
  }

  get profileAvatar() {
    return $('[data-testid="profile-avatar"]') ||
           $('[class*="avatar"]') ||
           $('img[alt*="profile" i]');
  }

  get notificationIcon() {
    return $('[data-testid="notification-icon"]') ||
           $('[aria-label="Notifications"]') ||
           $('[class*="notification"]');
  }

  get searchIcon() {
    return $('[data-testid="search-icon"]') ||
           $('[aria-label="Search"]') ||
           $('button[class*="search"]');
  }

  get searchBar() {
    return $('[data-testid="search-bar"]') ||
           $('input[type="search"]') ||
           $('[placeholder*="search" i]');
  }

  get hamburgerMenu() {
    return $('[data-testid="hamburger"]') ||
           $('[aria-label="Menu"]') ||
           $('[class*="hamburger"]');
  }

  // ─── Dashboard Cards ───────────────────────────────────────────────────────

  get dashboardCards() {
    return $$('[data-testid="dashboard-card"]') ||
           $$('[class*="card"]') ||
           $$('[class*="dashboard-item"]');
  }

  get firstCard() {
    return $('[data-testid="dashboard-card"]:first-child') ||
           $('[class*="card"]:first-child');
  }

  get statsSection() {
    return $('[data-testid="stats-section"]') ||
           $('[class*="stats"]') ||
           $('[class*="analytics"]');
  }

  get quickActionFab() {
    return $('[data-testid="fab"]') ||
           $('[aria-label="Quick Action"]') ||
           $('[class*="fab"]') ||
           $('button[class*="floating"]');
  }

  get welcomeGreeting() {
    return $('[data-testid="greeting"]') ||
           $('[class*="greeting"]') ||
           $('h1') ||
           $('[class*="welcome-text"]');
  }

  // ─── Plant Analysis Section ────────────────────────────────────────────────

  get plantAnalysisCard() {
    return $('[data-testid="plant-analysis-card"]') ||
           $('[href*="plant"]') ||
           $('[class*="plant-card"]');
  }

  get cameraButton() {
    return $('[data-testid="camera-btn"]') ||
           $('[aria-label="Camera"]') ||
           $('[class*="camera"]');
  }

  get galleryButton() {
    return $('[data-testid="gallery-btn"]') ||
           $('[aria-label="Gallery"]') ||
           $('[class*="gallery"]');
  }

  get uploadProgressBar() {
    return $('[data-testid="upload-progress"]') ||
           $('[role="progressbar"]') ||
           $('[class*="progress"]');
  }

  // ─── AI Assistant Section ──────────────────────────────────────────────────

  get chatContainer() {
    return $('[data-testid="chat-container"]') ||
           $('[class*="chat"]') ||
           $('[class*="messages"]');
  }

  get chatInput() {
    return $('[data-testid="chat-input"]') ||
           $('textarea[placeholder*="message" i]') ||
           $('input[placeholder*="ask" i]');
  }

  get sendButton() {
    return $('[data-testid="send-btn"]') ||
           $('[aria-label="Send"]') ||
           $('button[type="submit"]');
  }

  get voiceInputButton() {
    return $('[data-testid="voice-btn"]') ||
           $('[aria-label="Voice input"]') ||
           $('[class*="microphone"]');
  }

  // ─── Nutrition Section ─────────────────────────────────────────────────────

  get nutritionForm() {
    return $('[data-testid="nutrition-form"]') ||
           $('form[class*="nutrition"]');
  }

  get ageInput() {
    return $('[data-testid="age-input"]') ||
           $('input[name="age"]') ||
           $('[placeholder*="age" i]');
  }

  get weightInput() {
    return $('[data-testid="weight-input"]') ||
           $('input[name="weight"]') ||
           $('[placeholder*="weight" i]');
  }

  get activitySlider() {
    return $('[data-testid="activity-slider"]') ||
           $('input[type="range"]') ||
           $('[role="slider"]');
  }

  get calculateButton() {
    return $('[data-testid="calculate-btn"]') ||
           $('//button[contains(normalize-space(),"Calculate")]');
  }

  get nutritionResultCard() {
    return $('[data-testid="nutrition-result"]') ||
           $('[class*="result-card"]') ||
           $('[class*="nutrition-result"]');
  }

  // ─── Pull to Refresh ──────────────────────────────────────────────────────

  get pullToRefreshIndicator() {
    return $('[data-testid="refresh-indicator"]') ||
           $('[class*="refresh"]') ||
           $('[class*="pull-to-refresh"]');
  }

  // ─── Crop/Soil Analysis ───────────────────────────────────────────────────

  get cropAnalysisSection() {
    return $('[data-testid="crop-analysis"]') ||
           $('[href*="crop"]') ||
           $('[class*="crop-analysis"]');
  }

  get soilAnalysisSection() {
    return $('[data-testid="soil-analysis"]') ||
           $('[href*="soil"]') ||
           $('[class*="soil-analysis"]');
  }

  // ─── Actions ───────────────────────────────────────────────────────────────

  async waitForDashboard(timeout = 15000) {
    try {
      await this.dashboardCards[0].waitForDisplayed({ timeout });
      return true;
    } catch {
      try {
        await this.bottomNavBar.waitForDisplayed({ timeout: 5000 });
        return true;
      } catch {
        return false;
      }
    }
  }

  async tapHomeTab() {
    const tab = await this.homeNavTab;
    await tab.waitForDisplayed({ timeout: 10000 });
    await tab.click();
    await browser.pause(1000);
  }

  async tapPlantTab() {
    const tab = await this.plantNavTab;
    await tab.waitForDisplayed({ timeout: 10000 });
    await tab.click();
    await browser.pause(1000);
  }

  async tapAITab() {
    const tab = await this.aiNavTab;
    await tab.waitForDisplayed({ timeout: 10000 });
    await tab.click();
    await browser.pause(1000);
  }

  async tapNutritionTab() {
    const tab = await this.nutritionNavTab;
    await tab.waitForDisplayed({ timeout: 10000 });
    await tab.click();
    await browser.pause(1000);
  }

  async tapProfileTab() {
    const tab = await this.profileNavTab;
    await tab.waitForDisplayed({ timeout: 10000 });
    await tab.click();
    await browser.pause(1000);
  }

  async pullToRefresh() {
    const { width, height } = await browser.getWindowSize();
    await browser.touchAction([
      { action: 'press', x: Math.round(width / 2), y: Math.round(height * 0.2) },
      { action: 'moveTo', x: Math.round(width / 2), y: Math.round(height * 0.6) },
      'release'
    ]);
    await browser.pause(2000);
  }

  async tapSearchIcon() {
    const icon = await this.searchIcon;
    await icon.click();
    await browser.pause(500);
  }

  async searchFor(query) {
    await this.tapSearchIcon();
    const bar = await this.searchBar;
    await bar.waitForDisplayed({ timeout: 5000 });
    await bar.setValue(query);
    await browser.pause(500);
  }

  async tapNotificationIcon() {
    const icon = await this.notificationIcon;
    await icon.click();
    await browser.pause(1000);
  }

  async tapProfileAvatar() {
    const avatar = await this.profileAvatar;
    await avatar.click();
    await browser.pause(1000);
  }

  async tapFab() {
    const fab = await this.quickActionFab;
    await fab.click();
    await browser.pause(800);
  }

  async getDashboardCardCount() {
    const cards = await this.dashboardCards;
    return cards.length;
  }

  async isBottomNavVisible() {
    try {
      const nav = await this.bottomNavBar;
      return await nav.isDisplayed();
    } catch {
      return false;
    }
  }

  async swipeLeftOnCards() {
    const { width, height } = await browser.getWindowSize();
    await browser.touchAction([
      { action: 'press', x: Math.round(width * 0.8), y: Math.round(height * 0.5) },
      { action: 'moveTo', x: Math.round(width * 0.2), y: Math.round(height * 0.5) },
      'release'
    ]);
    await browser.pause(800);
  }

  async swipeRightOnCards() {
    const { width, height } = await browser.getWindowSize();
    await browser.touchAction([
      { action: 'press', x: Math.round(width * 0.2), y: Math.round(height * 0.5) },
      { action: 'moveTo', x: Math.round(width * 0.8), y: Math.round(height * 0.5) },
      'release'
    ]);
    await browser.pause(800);
  }

  async getGreetingText() {
    const greeting = await this.welcomeGreeting;
    return await greeting.getText();
  }

  async openHamburgerMenu() {
    try {
      const btn = await this.hamburgerMenu;
      await btn.click();
      await browser.pause(800);
    } catch {
      console.log('No hamburger menu found');
    }
  }

  async enterChatMessage(message) {
    const input = await this.chatInput;
    await input.waitForDisplayed({ timeout: 10000 });
    await input.click();
    await input.setValue(message);
  }

  async sendChatMessage() {
    const btn = await this.sendButton;
    await btn.click();
    await browser.pause(1500);
  }

  async rotateToLandscape() {
    await browser.setOrientation('LANDSCAPE');
    await browser.pause(1000);
  }

  async rotateToPortrait() {
    await browser.setOrientation('PORTRAIT');
    await browser.pause(1000);
  }
}

module.exports = new DashboardPage();
