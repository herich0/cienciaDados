from bs4 import BeautifulSoup
from typing import Dict, Set
import requests
import re

def paragraph_mention(text: str, keyword: str) -> bool:
    soup = BeautifulSoup(text, "html5lib")
    paragraphs = soup("p")
    return any(keyword.lower() in paragraphs.lower() for p in paragraphs)

url = "https://www.house.gov/representatives"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")
all_urls = [a["href"] for a in soup("a") if "href" in a.attrs]

regex = r"^https?://.+\.house\.gov/?$"
assert re.match(regex, "http://joel.house.gov")
assert re.match(regex, "https://joel.house.gov/")
assert not re.match(regex, "https://joel.house.com")
assert not re.match(regex, "https://joel.house.gov/biography")

good_urls = [url for url in all_urls if re.match(regex, url)]
good_urls = list(set(good_urls))  # Remove duplicates

press_releases: Dict[str, set] = {}
for house_url in good_urls:
    html = requests.get(house_url).text
    soup = BeautifulSoup(html, "html5lib")
    pr_links = [a["href"] for a in soup("a") if "press_releases" in a.text.lower()]
    # print(f"{house_url}: {pr_links}")
    press_releases[house_url] = set(pr_links)


print ("\nBuscando palavra 'data' nos comunicados de imprensa\n")

for house_url, pr_links in press_releases.items():
    for pr_link in pr_links:
        try:
            html = requests.get(pr_link, timeout=5).text
            if paragraph_mention(html, "data"):
                print(f"{house_url} Encontrado em: {pr_link}")
                break
        except requests.RequestException:
            continue