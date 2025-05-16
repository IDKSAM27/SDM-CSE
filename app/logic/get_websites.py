import requests
import time
from urllib.parse import urlparse
import os

from dotenv import load_dotenv
load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")
HEADERS = {"User-Agent": "Mozilla/5.0"}

def is_shopify(html):
    return "cdn.shopify.com" in html or "myshopify.com" in html

def fetch_google_search_urls(query, count=10):
    params = {
        "api_key": SERP_API_KEY,
        "engine": "google",
        "q": query,
        "num": count,
    }
    res = requests.get("https://serpapi.com/search.json", params=params)
    data = res.json()
    links = []
    for result in data.get("organic_results", []):
        link = result.get("link")
        if link and "google" not in link:
            links.append(link)
    return links

def normalize_url(url):
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
    elif parsed.scheme not in ["http", "https"]:
        url = "https://" + parsed.netloc + parsed.path
    return url

def get_websites(country, state, industry, count=10, only_shopify=False):
    query = f"{industry} in {state}, {country}"
    websites = fetch_google_search_urls(query, count)
    results = []

    for site in websites:
        try:
            site = normalize_url(site)
            start = time.time()
            res = requests.get(site, headers=HEADERS, timeout=5)
            load_time = round(time.time() - start, 2)
            html = res.text
            domain = urlparse(site).netloc

            if only_shopify and not is_shopify(html):
                continue

            results.append({
                "url": site,
                "domain": domain,
                "status": res.status_code,
                "load_time": load_time,
                "shopify": is_shopify(html)
            })

        except Exception:
            results.append({
                "url": site,
                "domain": urlparse(site).netloc,
                "status": "down",
                "load_time": None,
                "shopify": False
            })

    return results
