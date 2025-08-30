

import requests
from bs4 import BeautifulSoup
import random
import time
from fake_useragent import UserAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ProxyScraper:
    def __init__(self):
        self.user_agent = UserAgent()
        self.proxy_sources = [
            "https://free-proxy-list.net/",
            "https://www.sslproxies.org/",
            "https://www.us-proxy.org/",
            "https://freeproxy.world/",
            "https://www.proxy-nova.com/proxy-server-list/"
        ]
        self.proxies = []
        self.max_proxy_age_minutes = int(os.getenv('MAX_PROXY_AGE_MINUTES', 30))

    def get_proxies_from_source(self, url):
        """Scrape proxies from a given source"""
        try:
            headers = {
                'User-Agent': self.user_agent.random
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Common table structure for proxy lists
            if "free-proxy-list" in url or "sslproxies" in url:
                table = soup.find('table', id='proxylisttable')
                rows = table.tbody.find_all('tr')
            elif "us-proxy" in url:
                table = soup.find('table', class_='table')
                rows = table.find_all('tr')[1:]  # Skip header
            elif "freeproxy.world" in url:
                table = soup.find('table', id='proxylisttable')
                rows = table.tbody.find_all('tr')
            elif "proxy-nova" in url:
                table = soup.find('table', class_='table table-striped table-bordered')
                rows = table.find_all('tr')[1:]  # Skip header
            else:
                return []

            proxies = []
            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 2:
                    continue

                ip = cols[0].text.strip()
                port = cols[1].text.strip()

                # Check if it's an HTTP proxy (some lists include SOCKS)
                if 'http' in cols[6].text.lower() or len(cols) <= 6:
                    proxies.append(f"http://{ip}:{port}")

            return proxies

        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return []

    def scrape_proxies(self):
        """Scrape all proxy sources and collect unique proxies"""
        self.proxies = []
        for source in self.proxy_sources:
            print(f"Scraping proxies from {source}...")
            source_proxies = self.get_proxies_from_source(source)
            self.proxies.extend(source_proxies)

        # Remove duplicates and shuffle
        self.proxies = list(set(self.proxies))
        random.shuffle(self.proxies)
        print(f"Found {len(self.proxies)} unique proxies")

    def test_proxy(self, proxy):
        """Test if a proxy is working"""
        try:
            headers = {
                'User-Agent': self.user_agent.random
            }
            response = requests.get(
                "https://httpbin.org/ip",
                proxies={"http": proxy, "https": proxy},
                headers=headers,
                timeout=5
            )
            return response.status_code == 200
        except:
            return False

    def get_working_proxies(self, limit=10):
        """Get a list of working proxies"""
        working_proxies = []
        for proxy in self.proxies:
            if len(working_proxies) >= limit:
                break
            if self.test_proxy(proxy):
                print(f"Found working proxy: {proxy}")
                working_proxies.append(proxy)
                time.sleep(1)  # Be polite between requests

        return working_proxies

if __name__ == "__main__":
    scraper = ProxyScraper()
    scraper.scrape_proxies()

    # Get a limited number of working proxies
    working_proxies = scraper.get_working_proxies(limit=5)
    print(f"Final list of {len(working_proxies)} working proxies:")
    for proxy in working_proxies:
        print(proxy)
