/**
 * AGRO AI - Mobile Gesture Utilities
 * Helper functions for Appium touch interactions
 */

const gestures = {

  /**
   * Swipe from one point to another on screen
   * @param {string} direction - 'up' | 'down' | 'left' | 'right'
   * @param {number} percentage - how much of screen to cover (0-1)
   */
  async swipe(direction = 'up', percentage = 0.5) {
    const { width, height } = await browser.getWindowSize();
    const startX = Math.round(width / 2);
    const startY = Math.round(height / 2);

    let endX = startX;
    let endY = startY;

    switch (direction.toLowerCase()) {
      case 'up':
        endY = Math.round(height * (0.5 - percentage));
        break;
      case 'down':
        endY = Math.round(height * (0.5 + percentage));
        break;
      case 'left':
        endX = Math.round(width * (0.5 - percentage));
        break;
      case 'right':
        endX = Math.round(width * (0.5 + percentage));
        break;
    }

    await browser.touchAction([
      { action: 'press', x: startX, y: startY },
      { action: 'wait', ms: 100 },
      { action: 'moveTo', x: endX, y: endY },
      'release'
    ]);
    await browser.pause(600);
  },

  /**
   * Swipe from specific coordinates to specific coordinates
   * @param {number} startX
   * @param {number} startY
   * @param {number} endX
   * @param {number} endY
   * @param {number} durationMs
   */
  async swipeCoordinates(startX, startY, endX, endY, durationMs = 300) {
    await browser.touchAction([
      { action: 'press', x: startX, y: startY },
      { action: 'wait', ms: durationMs },
      { action: 'moveTo', x: endX, y: endY },
      'release'
    ]);
    await browser.pause(500);
  },

  /**
   * Scroll an element into view
   * @param {WebdriverIO.Element} element
   */
  async scrollIntoView(element) {
    await element.scrollIntoView({ block: 'center', inline: 'center' });
    await browser.pause(500);
  },

  /**
   * Scroll page by percentage
   * @param {number} percentage - 0-1, amount of screen to scroll
   */
  async scrollDown(percentage = 0.4) {
    await this.swipe('up', percentage);
  },

  async scrollUp(percentage = 0.4) {
    await this.swipe('down', percentage);
  },

  /**
   * Scroll until an element is visible
   * @param {Function} elementGetter - function that returns element
   * @param {number} maxScrolls - maximum number of scroll attempts
   * @param {string} direction - scroll direction
   */
  async scrollUntilVisible(elementGetter, maxScrolls = 10, direction = 'up') {
    for (let i = 0; i < maxScrolls; i++) {
      try {
        const element = await elementGetter();
        if (await element.isDisplayed()) {
          return element;
        }
      } catch { /* not visible yet */ }
      await this.swipe(direction, 0.3);
    }
    throw new Error(`Element not found after ${maxScrolls} scrolls`);
  },

  /**
   * Pinch zoom gesture
   * @param {WebdriverIO.Element} element - element to pinch zoom on
   * @param {string} action - 'in' | 'out'
   * @param {number} scale - zoom scale (0.5 = zoom out 50%, 2 = zoom in 200%)
   */
  async pinchZoom(element, action = 'in', scale = 2) {
    const rect = await element.getRect();
    const centerX = Math.round(rect.x + rect.width / 2);
    const centerY = Math.round(rect.y + rect.height / 2);
    const offset = action === 'in' ? 50 : 100;

    if (action === 'in') {
      // Two fingers moving apart (zoom in)
      await browser.multiTouchAction([
        browser.touchAction([
          { action: 'press', x: centerX - offset, y: centerY },
          { action: 'moveTo', x: centerX - Math.round(offset * scale), y: centerY },
          'release'
        ]),
        browser.touchAction([
          { action: 'press', x: centerX + offset, y: centerY },
          { action: 'moveTo', x: centerX + Math.round(offset * scale), y: centerY },
          'release'
        ])
      ]);
    } else {
      // Two fingers moving together (zoom out)
      await browser.multiTouchAction([
        browser.touchAction([
          { action: 'press', x: centerX - Math.round(offset * scale), y: centerY },
          { action: 'moveTo', x: centerX - offset, y: centerY },
          'release'
        ]),
        browser.touchAction([
          { action: 'press', x: centerX + Math.round(offset * scale), y: centerY },
          { action: 'moveTo', x: centerX + offset, y: centerY },
          'release'
        ])
      ]);
    }
    await browser.pause(1000);
  },

  /**
   * Double tap on element
   * @param {WebdriverIO.Element} element
   */
  async doubleTap(element) {
    const rect = await element.getRect();
    const x = Math.round(rect.x + rect.width / 2);
    const y = Math.round(rect.y + rect.height / 2);

    await browser.touchAction([
      { action: 'tap', x, y },
      { action: 'wait', ms: 100 },
      { action: 'tap', x, y }
    ]);
    await browser.pause(500);
  },

  /**
   * Long press on element
   * @param {WebdriverIO.Element} element
   * @param {number} durationMs - how long to press in milliseconds
   */
  async longPress(element, durationMs = 1500) {
    const rect = await element.getRect();
    const x = Math.round(rect.x + rect.width / 2);
    const y = Math.round(rect.y + rect.height / 2);

    await browser.touchAction([
      { action: 'press', x, y },
      { action: 'wait', ms: durationMs },
      'release'
    ]);
    await browser.pause(500);
  },

  /**
   * Long press on element by coordinates
   * @param {number} x
   * @param {number} y
   * @param {number} durationMs
   */
  async longPressCoordinates(x, y, durationMs = 1500) {
    await browser.touchAction([
      { action: 'press', x, y },
      { action: 'wait', ms: durationMs },
      'release'
    ]);
    await browser.pause(500);
  },

  /**
   * Drag and drop from source element to target element
   * @param {WebdriverIO.Element} sourceElement
   * @param {WebdriverIO.Element} targetElement
   */
  async dragAndDrop(sourceElement, targetElement) {
    const sourceRect = await sourceElement.getRect();
    const targetRect = await targetElement.getRect();

    const startX = Math.round(sourceRect.x + sourceRect.width / 2);
    const startY = Math.round(sourceRect.y + sourceRect.height / 2);
    const endX = Math.round(targetRect.x + targetRect.width / 2);
    const endY = Math.round(targetRect.y + targetRect.height / 2);

    await browser.touchAction([
      { action: 'press', x: startX, y: startY },
      { action: 'wait', ms: 1000 },
      { action: 'moveTo', x: Math.round((startX + endX) / 2), y: Math.round((startY + endY) / 2) },
      { action: 'moveTo', x: endX, y: endY },
      'release'
    ]);
    await browser.pause(1000);
  },

  /**
   * Drag and drop by coordinates
   */
  async dragAndDropCoordinates(startX, startY, endX, endY) {
    await browser.touchAction([
      { action: 'press', x: startX, y: startY },
      { action: 'wait', ms: 800 },
      { action: 'moveTo', x: endX, y: endY },
      'release'
    ]);
    await browser.pause(800);
  },

  /**
   * Pull to refresh gesture
   */
  async pullToRefresh() {
    const { width, height } = await browser.getWindowSize();
    await browser.touchAction([
      { action: 'press', x: Math.round(width / 2), y: Math.round(height * 0.15) },
      { action: 'wait', ms: 200 },
      { action: 'moveTo', x: Math.round(width / 2), y: Math.round(height * 0.65) },
      'release'
    ]);
    await browser.pause(2500);
  },

  /**
   * Tap on coordinates
   */
  async tap(x, y) {
    await browser.touchAction([
      { action: 'tap', x, y }
    ]);
    await browser.pause(300);
  },

  /**
   * Tap the center of an element
   */
  async tapElement(element) {
    const rect = await element.getRect();
    const x = Math.round(rect.x + rect.width / 2);
    const y = Math.round(rect.y + rect.height / 2);
    await this.tap(x, y);
  },

  /**
   * Swipe left on a carousel/horizontal scroll
   */
  async swipeCarouselLeft() {
    const { width, height } = await browser.getWindowSize();
    await browser.touchAction([
      { action: 'press', x: Math.round(width * 0.8), y: Math.round(height * 0.5) },
      { action: 'wait', ms: 200 },
      { action: 'moveTo', x: Math.round(width * 0.2), y: Math.round(height * 0.5) },
      'release'
    ]);
    await browser.pause(600);
  },

  /**
   * Swipe right on a carousel/horizontal scroll
   */
  async swipeCarouselRight() {
    const { width, height } = await browser.getWindowSize();
    await browser.touchAction([
      { action: 'press', x: Math.round(width * 0.2), y: Math.round(height * 0.5) },
      { action: 'wait', ms: 200 },
      { action: 'moveTo', x: Math.round(width * 0.8), y: Math.round(height * 0.5) },
      'release'
    ]);
    await browser.pause(600);
  },

  /**
   * Simulate 3G network conditions (via Chrome DevTools Protocol if available)
   */
  async simulate3GNetwork() {
    try {
      await browser.setNetworkConditions({
        offline: false,
        latency: 100,
        download_throughput: 750 * 1024 / 8, // 750 kbps
        upload_throughput: 250 * 1024 / 8
      });
    } catch (e) {
      console.log('Network simulation not supported:', e.message);
    }
  },

  /**
   * Restore normal network conditions
   */
  async restoreNetwork() {
    try {
      await browser.setNetworkConditions({
        offline: false,
        latency: 0,
        download_throughput: -1,
        upload_throughput: -1
      });
    } catch (e) {
      console.log('Could not restore network:', e.message);
    }
  },

  /**
   * Check if element is in viewport
   */
  async isInViewport(element) {
    const rect = await element.getRect();
    const windowSize = await browser.getWindowSize();
    return (
      rect.x >= 0 &&
      rect.y >= 0 &&
      rect.x + rect.width <= windowSize.width &&
      rect.y + rect.height <= windowSize.height
    );
  },

  /**
   * Wait for animation to complete
   */
  async waitForAnimation(ms = 500) {
    await browser.pause(ms);
  },

  /**
   * Get element center coordinates
   */
  async getElementCenter(element) {
    const rect = await element.getRect();
    return {
      x: Math.round(rect.x + rect.width / 2),
      y: Math.round(rect.y + rect.height / 2)
    };
  }
};

module.exports = gestures;
