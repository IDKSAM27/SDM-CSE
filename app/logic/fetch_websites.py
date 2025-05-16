import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def is_shopify(html):
    return "cdn.shopify.com" in html or "myshopify.com" in html

def get_websites(country, state, industry, count, only_shopify=False):
    dummy_domains = [
        f"https://www.{industry.replace(' ', '')}{i}.com" for i in range(1, count + 2)
    ]

    results = []
    for url in dummy_domains:
        try:
            start = time.time()
            res = requests.get(url, headers=HEADERS, timeout=5)
            load_time = round(time.time() - start, 2)
            html = res.text
            parsed_url = urlparse(url)

            if only_shopify and not is_shopify(html):
                continue

            results.append({
                "url": url,
                "status": res.status_code,
                "load_time": load_time,
                "shopify": is_shopify(html),
                "domain": parsed_url.netloc
            })

        except Exception:
            results.append({
                "url": url,
                "status": "down",
                "load_time": None,
                "shopify": False,
                "domain": urlparse(url).netloc
            })

    return results