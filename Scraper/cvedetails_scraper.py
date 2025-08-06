import requests
from bs4 import BeautifulSoup
import time
import csv
import os

BASE_URL = "https://www.cvedetails.com/vulnerability-list.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CyberWarriorBot/1.0)"
}

def get_page(url, retries=3):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.text
    except requests.RequestException as e:
        if retries > 0:
            time.sleep(2)
            return get_page(url, retries - 1)
        print(f"[ERROR] Failed to fetch {url}: {e}")
    return None

def parse_table(soup):
    table = soup.find("table", {"id": "vulnslisttable"})
    if not table:
        return []

    rows = table.find_all("tr")[1:]  # Skip header row
    cves = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 8:
            cves.append({
                "CVE_ID": cols[1].text.strip(),
                "CWE_ID": cols[2].text.strip(),
                "Vuln_Type": cols[4].text.strip(),
                "Publish_Date": cols[5].text.strip(),
                "Update_Date": cols[6].text.strip(),
                "Score": cols[7].text.strip(),
                "Gained_Access_Level": cols[8].text.strip(),
                "Summary": cols[9].text.strip()
            })
    return cves

def scrape_cvedetails(pages=2, output_file="cvedetails_data.csv"):
    all_data = []
    print(f"[INFO] Scraping CVE Details (first {pages} pages)...")
    for page in range(1, pages + 1):
        url = f"{BASE_URL}?page={page}"
        html = get_page(url)
        if not html:
            continue
        soup = BeautifulSoup(html, "html.parser")
        data = parse_table(soup)
        all_data.extend(data)
        time.sleep(1)

    if not all_data:
        print("[ERROR] No data scraped. Check selectors or if the site blocked the bot.")
        return

    if not os.path.exists("data"):
        os.makedirs("data")

    filepath = os.path.join("data", output_file)
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_data[0].keys())
        writer.writeheader()
        writer.writerows(all_data)

    print(f"[SUCCESS] Scraped {len(all_data)} CVEs to '{filepath}'")
