

#!/usr/bin/env python3
"""
TikTok Live Viewer Bot using Opera in headless mode with built-in VPN.
"""

import argparse
import json
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class TikTokBot:
    def __init__(self, config):
        self.config = config
        self.browser = None

    def start_browser(self):
        """Start Opera browser in headless mode with VPN."""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Enable Opera's built-in VPN if configured
        if self.config.get('use_vpn', False):
            options.add_extension('/path/to/opera/vpn/extension.crx')

        self.browser = webdriver.Opera(options=options)
        return self.browser

    def stop_browser(self):
        """Stop the browser and clean up."""
        if self.browser:
            self.browser.quit()
            self.browser = None

    def view_live(self, url, duration):
        """
        View a TikTok live stream for specified duration.

        Args:
            url (str): URL of the TikTok live stream
            duration (int): Duration in seconds to view the stream
        """
        try:
            self.browser.get(url)
            print(f"[INFO] Started viewing: {url}")

            # Simulate viewer engagement
            start_time = time.time()
            while time.time() - start_time < duration:
                # Randomly interact with the page
                if random.random() < 0.1:  # 10% chance to click like
                    try:
                        like_button = self.browser.find_element(By.XPATH, "//button[contains(@aria-label, 'Like')]")
                        like_button.click()
                        print("[INFO] Liked the video")
                    except Exception as e:
                        print(f"[WARNING] Could not like video: {e}")

                time.sleep(random.uniform(1, 5))

            print(f"[INFO] Finished viewing after {duration} seconds")

        except Exception as e:
            print(f"[ERROR] Failed to view live stream: {e}")
            self.stop_browser()

    def run(self):
        """Main bot execution loop."""
        try:
            self.start_browser()
            url = self.config.get('tiktok_url', 'https://www.tiktok.com/live')

            for _ in range(self.config.get('max_viewers', 1)):
                duration = random.randint(
                    self.config.get('view_duration_min', 5),
                    self.config.get('view_duration_max', 30)
                )
                self.view_live(url, duration)

                # Random delay between viewers
                time.sleep(random.uniform(2, 10))

        finally:
            self.stop_browser()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TikTok Live Viewer Bot")
    parser.add_argument('--config', type=str, default='config.json',
                       help='Path to configuration file')
    args = parser.parse_args()

    # Load configuration
    with open(args.config, 'r') as f:
        config = json.load(f)

    bot = TikTokBot(config)
    bot.run()
