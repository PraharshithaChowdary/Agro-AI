/**
 * AGRO AI - LoginPage Page Object
 * Mobile-first selectors for Appium + WebdriverIO
 */

class LoginPage {
  // ─── Selectors ─────────────────────────────────────────────────────────────

  get welcomeContainer() {
    return $('//android.webkit.WebView//android.view.View[@content-desc]') ||
           $('~welcome') ||
           $('[data-testid="welcome-screen"]');
  }

  get loginButton() {
    return $('[data-testid="login-btn"]') ||
           $('//button[contains(normalize-space(),"Login")]') ||
           $('//a[contains(normalize-space(),"Login")]') ||
           $('[aria-label="Login"]');
  }

  get registerButton() {
    return $('[data-testid="register-btn"]') ||
           $('//button[contains(normalize-space(),"Register")]') ||
           $('//a[contains(normalize-space(),"Register")]');
  }

  get emailInput() {
    return $('[data-testid="email-input"]') ||
           $('input[type="email"]') ||
           $('input[name="email"]') ||
           $('[placeholder*="email" i]');
  }

  get passwordInput() {
    return $('[data-testid="password-input"]') ||
           $('input[type="password"]') ||
           $('input[name="password"]') ||
           $('[placeholder*="password" i]');
  }

  get submitButton() {
    return $('[data-testid="submit-btn"]') ||
           $('button[type="submit"]') ||
           $('//button[contains(normalize-space(),"Sign In")]') ||
           $('//button[contains(normalize-space(),"Login")]');
  }

  get forgotPasswordLink() {
    return $('[data-testid="forgot-password"]') ||
           $('//a[contains(normalize-space(),"Forgot")]') ||
           $('//button[contains(normalize-space(),"Forgot")]');
  }

  get errorMessage() {
    return $('[data-testid="error-message"]') ||
           $('[role="alert"]') ||
           $('.toast') ||
           $('[class*="error"]') ||
           $('[class*="alert"]');
  }

  get successToast() {
    return $('[data-testid="success-toast"]') ||
           $('[class*="success"]') ||
           $('[class*="toast"][class*="success"]');
  }

  get loadingSpinner() {
    return $('[data-testid="loading-spinner"]') ||
           $('[class*="spinner"]') ||
           $('[class*="loading"]') ||
           $('[role="progressbar"]');
  }

  get rememberMeToggle() {
    return $('[data-testid="remember-me"]') ||
           $('input[type="checkbox"][name*="remember"]') ||
           $('[name="rememberMe"]');
  }

  get logoImage() {
    return $('[data-testid="logo"]') ||
           $('img[alt*="AGRO"]') ||
           $('img[alt*="logo" i]');
  }

  get loginFormContainer() {
    return $('[data-testid="login-form"]') ||
           $('form') ||
           $('[class*="login-form"]') ||
           $('[class*="auth-form"]');
  }

  get backButton() {
    return $('[data-testid="back-btn"]') ||
           $('[aria-label="Go back"]') ||
           $('button.back') ||
           $('[class*="back-button"]');
  }

  get passwordToggleBtn() {
    return $('[data-testid="password-toggle"]') ||
           $('[aria-label*="password" i][type="button"]') ||
           $('button[class*="password-toggle"]');
  }

  get googleLoginBtn() {
    return $('[data-testid="google-login"]') ||
           $('button[class*="google"]') ||
           $('//button[contains(normalize-space(),"Google")]');
  }

  get pageTitle() {
    return $('h1') || $('h2') || $('[class*="title"]');
  }

  // ─── Actions ───────────────────────────────────────────────────────────────

  async open() {
    const url = global.APP_URL || process.env.APP_URL || 'http://10.0.2.2:5173';
    await browser.url(url);
    await browser.pause(2000);
  }

  async tapLoginButton() {
    const btn = await this.loginButton;
    await btn.waitForDisplayed({ timeout: 10000 });
    await btn.click();
    await browser.pause(1000);
  }

  async tapRegisterButton() {
    const btn = await this.registerButton;
    await btn.waitForDisplayed({ timeout: 10000 });
    await btn.click();
    await browser.pause(1000);
  }

  async enterEmail(email) {
    const input = await this.emailInput;
    await input.waitForDisplayed({ timeout: 10000 });
    await input.click();
    await browser.pause(500);
    await input.clearValue();
    await input.setValue(email);
  }

  async enterPassword(password) {
    const input = await this.passwordInput;
    await input.waitForDisplayed({ timeout: 10000 });
    await input.click();
    await browser.pause(500);
    await input.clearValue();
    await input.setValue(password);
  }

  async tapSubmit() {
    const btn = await this.submitButton;
    await btn.waitForDisplayed({ timeout: 10000 });
    await btn.click();
    await browser.pause(2000);
  }

  async login(email, password) {
    await this.enterEmail(email);
    await this.enterPassword(password);
    await this.tapSubmit();
  }

  async waitForErrorMessage(timeout = 10000) {
    const msg = await this.errorMessage;
    await msg.waitForDisplayed({ timeout });
    return await msg.getText();
  }

  async waitForSuccessToast(timeout = 10000) {
    const toast = await this.successToast;
    await toast.waitForDisplayed({ timeout });
    return await toast.getText();
  }

  async isLoginFormVisible() {
    try {
      const form = await this.loginFormContainer;
      return await form.isDisplayed();
    } catch {
      return false;
    }
  }

  async isEmailFieldFocused() {
    const input = await this.emailInput;
    const isFocused = await input.isFocused();
    return isFocused;
  }

  async tapForgotPassword() {
    const link = await this.forgotPasswordLink;
    await link.waitForDisplayed({ timeout: 10000 });
    await link.click();
    await browser.pause(1000);
  }

  async toggleRememberMe() {
    const toggle = await this.rememberMeToggle;
    await toggle.click();
    await browser.pause(300);
  }

  async togglePasswordVisibility() {
    const btn = await this.passwordToggleBtn;
    await btn.click();
    await browser.pause(300);
  }

  async getPasswordFieldType() {
    const input = await this.passwordInput;
    return await input.getAttribute('type');
  }

  async scrollToSubmitButton() {
    const btn = await this.submitButton;
    await btn.scrollIntoView();
    await browser.pause(500);
  }

  async dismissKeyboard() {
    try {
      await browser.hideKeyboard();
    } catch {
      // On web-based PWA, pressing Enter or tapping outside
      await browser.keys(['Escape']);
    }
  }

  async getEmailInputType() {
    const input = await this.emailInput;
    return await input.getAttribute('type');
  }

  async isSubmitButtonEnabled() {
    const btn = await this.submitButton;
    return await btn.isEnabled();
  }

  async getLogoSrc() {
    const logo = await this.logoImage;
    return await logo.getAttribute('src');
  }

  async tapBack() {
    try {
      const btn = await this.backButton;
      await btn.click();
    } catch {
      await browser.back();
    }
    await browser.pause(1000);
  }

  async rotateToLandscape() {
    await browser.setOrientation('LANDSCAPE');
    await browser.pause(1000);
  }

  async rotateToPortrait() {
    await browser.setOrientation('PORTRAIT');
    await browser.pause(1000);
  }

  async getOrientation() {
    return await browser.getOrientation();
  }
}

module.exports = new LoginPage();
