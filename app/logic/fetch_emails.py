import re
import requests

def extract_emails_from_html(html):
    # Simple regex for emails
    return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html)

def get_emails(websites):
    results = []
    for url in websites:
        try:
            res = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            emails = extract_emails_from_html(res.text)
            results.append({
                "website": url,
                "emails": emails
            })
        except Exception as e:
            results.append({
                "website": url,
                "emails": []
            })
    return results
