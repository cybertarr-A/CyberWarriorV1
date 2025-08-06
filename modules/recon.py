# modules/recon.py

import requests
import os
from config import paths

class ReconResult:
    def __init__(self, headers=None, subdomains=None):
        self.headers = headers or {}
        self.subdomains = subdomains or []

class ReconTool:
    def __init__(self, target=None):
        self.target = target
        self.headers = {}
        self.subdomains = []
        print("ReconTool initialized")
        if target:
            self.run()

    def run(self):
        print(f"Running recon on {self.target}")
        domain = self.target.replace("http://", "").replace("https://", "").split("/")[0]
        self.subdomains = find_subdomains(domain)
        self.headers = grab_headers(self.target)

        output = f"[Subdomains]\n" + "\n".join(self.subdomains) + "\n\n[Headers]\n"
        for k, v in self.headers.items():
            output += f"{k}: {v}\n"

        save_result("recon_output.txt", output)
        return output

    def gather_info(self, target):
        # Optionally allow separate gather_info call
        self.target = target
        domain = target.replace("http://", "").replace("https://", "").split("/")[0]
        headers = grab_headers(target)
        subdomains = find_subdomains(domain)
        return ReconResult(headers=headers, subdomains=subdomains)

    def fetch_html(self, target):
        print(f"Fetching HTML snippet for {target}")
        try:
            resp = requests.get(target, timeout=5)
            return resp.text[:500]  # Return first 500 chars of HTML
        except Exception as e:
            print(f"[!] Failed to fetch HTML: {e}")
            return "<html><body>Failed to fetch snippet</body></html>"


def scan_target(target):
    print(f"Scanning target: {target}")
    # Placeholder for scanning logic
    return f"Scanned result for {target}"


def find_subdomains(domain):
    print(f"  [+] Finding subdomains for {domain}")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    subdomains = set()

    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        for item in data:
            name = item.get('name_value', '')
            for sub in name.split("\n"):
                subdomains.add(sub.strip())
    except Exception as e:
        print(f"  [!] Error during subdomain fetch: {e}")

    return list(subdomains)


def grab_headers(url):
    print(f"  [+] Grabbing headers for {url}")
    try:
        resp = requests.get(url, timeout=5)
        return dict(resp.headers)
    except Exception as e:
        print(f"  [!] Failed to grab headers: {e}")
        return {}


def save_result(filename, content):
    directory = paths.get("result_dir", "results")
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists

    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  [✔] Saved: {path}")
