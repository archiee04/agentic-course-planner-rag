import requests
from bs4 import BeautifulSoup
import os
import urllib3

# disable SSL warnings (for Windows issue)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, verify=False)
    return response.text


def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # remove unwanted tags
    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # remove empty lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    return "\n".join(lines)


def save_text(text, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


def process_url(url, filename):
    html = fetch_page(url)
    clean_text = clean_html(html)
    save_text(clean_text, filename)