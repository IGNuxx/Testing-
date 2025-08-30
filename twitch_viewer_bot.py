import os
import time
import random
from dotenv import load_dotenv
from twitchAPI.twitch import Twitch
from proxy_scraper import ProxyScraper

# Load environment variables
load_dotenv()

class TwitchViewerBot:
    def __init__(self):
        self.client_id = os.getenv('TWITCH_CLIENT_ID')
        self.client_secret = os.getenv('TWITCH_CLIENT_SECRET')
        self.stream_url = os.getenv('STREAM_URL', 'https://www.twitch.tv/')
        self.stream_username = os.getenv('STREAM_USERNAME')

        if not all([self.client_id, self.client_secret, self.stream_username]):
            raise ValueError("Missing required environment variables")

        # Initialize Twitch API client
        self.twitch = Twitch(client_id=self.client_id, client_secret=self.client_secret)

    def get_auth_token(self):
        """Get OAuth token for Twitch API"""
        try:
            auth = self.twitch.get_auth_token()
            return auth['access_token']
        except Exception as e:
            print(f"Error getting auth token: {str(e)}")
            return None

    def view_stream_with_proxy(self, proxy):
        """View stream using a specific proxy"""
        try:
            # Set up session with proxy
            session = requests.Session()
            proxies = {
                "http": proxy,
                "https": proxy
            }
            session.proxies.update(proxies)

            # Make request to Twitch stream page
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            stream_url = f"{self.stream_url}{self.stream_username}"
            response = session.get(stream_url, headers=headers, timeout=10)

            if response.status_code == 200:
                print(f"Successfully viewed {stream_url} using proxy: {proxy}")
                return True
            else:
                print(f"Failed to view stream with proxy {proxy}: Status code {response.status_code}")
                return False

        except Exception as e:
            print(f"Error viewing stream with proxy {proxy}: {str(e)}")
            return False

    def boost_viewers(self, num_views=10, max_proxies=20):
        """Boost Twitch viewer count using proxies"""
        if not self.stream_username:
            print("Stream username not specified")
            return

        # Initialize proxy scraper
        proxy_scraper = ProxyScraper()
        proxy_scraper.scrape_proxies()

        # Get working proxies
        working_proxies = proxy_scraper.get_working_proxies(limit=max_proxies)
        if not working_proxies:
            print("No working proxies found")
            return

        print(f"Starting viewer boost for {self.stream_username}")
        print(f"Target: {num_views} views using up to {len(working_proxies)} proxies")

        # Rotate through proxies to view the stream
        proxy_index = 0
        while num_views > 0:
            if proxy_index >= len(working_proxies):
                print("Ran out of working proxies, refreshing list...")
                working_proxies = proxy_scraper.get_working_proxies(limit=max_proxies)
                proxy_index = 0

            proxy = working_proxies[proxy_index]
            success = self.view_stream_with_proxy(proxy)

            if success:
                num_views -= 1
                print(f"Views remaining: {num_views}")

            # Random delay between requests (5-15 seconds)
            time.sleep(random.uniform(5, 15))

            proxy_index += 1

        print("Viewer boost completed!")

if __name__ == "__main__":
    try:
        bot = TwitchViewerBot()
        bot.boost_viewers(num_views=20, max_proxies=10)
    except Exception as e:
        print(f"Error running viewer bot: {str(e)}")
