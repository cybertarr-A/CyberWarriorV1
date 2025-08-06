# modules/scanner.py

import requests
import time
import os
import socket
from config import paths  # Ensure config.py has 'result_dir'

class ScannerResult:
    def __init__(self, open_ports=None, findings=None):
        self.open_ports = open_ports if open_ports else []
        self.findings = findings if findings else []

def scan_headers(target):
    try:
        response = requests.get(target)
        print("\n[+] HTTP Headers:")
        for header, value in response.headers.items():
            print(f"    {header}: {value}")
    except Exception as e:
        print(f"[-] Failed to fetch headers: {e}")

def scan_ports(host):
    print("\n[+] Port Scanning (top 10 ports):")
    common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445]
    open_ports = []

    for port in common_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
                print(f"    [+] Port {port} is OPEN")
            else:
                print(f"    [-] Port {port} is CLOSED")
    return open_ports

def detect_tech_stack(target):
    try:
        response = requests.get(target)
        headers = response.headers
        print("\n[+] Technology Fingerprinting:")
        server = headers.get("Server", "Unknown")
        powered_by = headers.get("X-Powered-By", "Unknown")
        print(f"    Server: {server}")
        print(f"    Powered By: {powered_by}")

        body = response.text.lower()
        if "wordpress" in body:
            print("    CMS: WordPress detected")
        elif "drupal" in body:
            print("    CMS: Drupal detected")
        elif "joomla" in body:
            print("    CMS: Joomla detected")
    except Exception as e:
        print(f"[-] Failed tech detection: {e}")

def find_endpoints(target):
    print("\n[+] Endpoint Discovery:")
    common_paths = ['admin', 'login', 'dashboard', 'api', 'config', '.git', 'robots.txt']
    for path in common_paths:
        url = f"{target.rstrip('/')}/{path}"
        try:
            r = requests.get(url)
            if r.status_code == 200:
                print(f"    [+] Found endpoint: {url}")
        except Exception:
            pass

# === SQLi Tests ===

sqli_payloads = [
    "' OR '1'='1",
    "'; WAITFOR DELAY '0:0:5'--",
    "\" OR \"\"=\"",
    "' OR 1=1--",
    "1 OR sleep(5)#"
]

error_signatures = [
    "you have an error in your sql syntax",
    "unclosed quotation mark",
    "sql syntax",
    "mysql_fetch",
    "syntax error"
]

def test_error_based_sqli(target):
    print("  [+] Testing Error-Based SQLi...")
    results = []
    for payload in sqli_payloads:
        test_url = f"{target}?id={payload}"
        try:
            resp = requests.get(test_url, timeout=7)
            for error in error_signatures:
                if error.lower() in resp.text.lower():
                    results.append(f"[VULN] Error-based SQLi at {test_url}")
                    break
        except Exception as e:
            print(f"    [!] Error testing payload: {payload} | {e}")
    return results

def test_blind_time_based_sqli(target):
    print("  [+] Testing Time-Based Blind SQLi...")
    payload = "' OR SLEEP(5)--"
    test_url = f"{target}?id={payload}"
    vulnerable = False
    try:
        start = time.time()
        requests.get(test_url, timeout=10)
        elapsed = time.time() - start
        if elapsed > 4.5:
            vulnerable = True
    except Exception as e:
        print(f"    [!] Blind SQLi test failed: {e}")

    return [f"[VULN] Blind SQLi (Time-based) at {test_url}"] if vulnerable else []

# === FINAL ENTRY POINT ===

def scan_target(target, paths=None):
    if paths is None:
        # fallback default
        paths = {"result_dir": "results"}

    print(f"[*] Running Scanner on {target}")
    host = target.replace("http://", "").replace("https://", "").split("/")[0]

    scan_headers(target)
    detect_tech_stack(target)
    find_endpoints(target)
    open_ports = scan_ports(host)

    results = []
    results += test_error_based_sqli(target)
    results += test_blind_time_based_sqli(target)

    result_path = os.path.join(paths["result_dir"], "scanner_output.txt")
    os.makedirs(paths["result_dir"], exist_ok=True)

    with open(result_path, "w") as f:
        if results:
            f.write("\n".join(results))
        else:
            f.write("No SQLi vulnerabilities detected.")

    print(f"  [✔] Scanner results saved to {result_path}")

    return ScannerResult(open_ports=open_ports, findings=results)
