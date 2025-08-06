# modules/core.py

import os
from modules.recon import ReconTool
from modules.scanner import scan_target
from modules.exploit import ExploitEngine
from modules.ai_analysis import AICore as BaseAICore
from modules.report_generator import ReportGenerator
from modules.nmap_scanner import AdvancedNmapScanner

# Paths config
paths = {
    "result_dir": "results"
}
os.makedirs(paths["result_dir"], exist_ok=True)

class CyberCore:
    def __init__(self, target):
        self.target = target
        print(f"[*] Initializing CyberCore for target: {self.target}")

        self.recon = ReconTool()
        self.exploit = ExploitEngine()
        self.ai = BaseAICore()
        self.reporter = ReportGenerator()
        self.scanner = scan_target(self.target, paths)

    def run(self):
        print(f"[+] Running base scan on: {self.target}")
        print(self.scanner)

    def run_full_scan(self):
        print(f"🌐 Starting full scan on: {self.target}")

        try:
            recon_data = self.recon.gather_info(self.target)
        except Exception as e:
            print(f"[!] Recon failed: {e}")
            recon_data = None

        try:
            scan_data = self.scanner.scan_ports(self.target)
        except Exception as e:
            print(f"[!] Scan failed: {e}")
            scan_data = None

        try:
            exploit_data = self.exploit.exploit_target(self.target)
        except Exception as e:
            print(f"[!] Exploit phase failed: {e}")
            exploit_data = None

        try:
            html_snippet = self.recon.fetch_html(self.target)
        except Exception as e:
            print(f"[!] Fetch HTML failed: {e}")
            html_snippet = "<no html>"

        findings = self.ai.analyze(recon_data, scan_data, exploit_data)

        headers = getattr(recon_data, "headers", {}) if recon_data else {}
        open_ports = getattr(scan_data, "open_ports", []) if scan_data else []
        findings_list = getattr(exploit_data, "findings", []) if exploit_data else []

        self.reporter.save_report(
            self.target, headers, open_ports, findings_list, html_snippet
        )

        print("🎯 Full scan completed.\n")
        print("AI Summary:\n", findings)


class AICore(BaseAICore):
    def __init__(self):
        super().__init__()
        self.nmap_scanner = AdvancedNmapScanner()
        # Add other AI-specific modules here

    def run_advanced_nmap(self, target):
        return self.nmap_scanner.run_advanced_scan(target)

    def run_recon(self, target):
        print("[*] Running Recon in AI Core")
        return self.recon.gather_info(target)

    def run_scan(self, target):
        print("[*] Running Scanner in AI Core")
        return scan_target(target, paths)

    def run_exploit(self, target):
        print("[*] Running Exploit in AI Core")
        engine = ExploitEngine()
        return engine.exploit_target(target)

    def analyze_ai(self, target):
        print("[*] Running AI analysis")
        # Could be enhanced with ML model inference here
        return f"AI analysis summary for {target} (simulated)"

    def generate_report(self, target, recon_data, scan_data, exploit_data, ai_summary):
        print("[*] Generating report in AI Core")
        reporter = ReportGenerator()
        headers = getattr(recon_data, "headers", {}) if recon_data else {}
        open_ports = getattr(scan_data, "open_ports", []) if scan_data else []
        findings = getattr(exploit_data, "findings", []) if exploit_data else []
        html_snippet = getattr(recon_data, "html", "<no html>") if recon_data else "<no html>"

        return reporter.save_report(
            target, headers, open_ports, findings, ai_summary
        )

    def run_all(self, target):
        print("[*] Running full AICore pipeline")

        recon_data = self.run_recon(target)
        nmap_data = self.run_advanced_nmap(target)
        scan_data = self.run_scan(target)
        exploit_data = self.run_exploit(target)
        ai_summary = self.analyze_ai(target)

        report_path = self.generate_report(
            target, recon_data, scan_data, exploit_data, ai_summary
        )

        print(f"Report saved at: {report_path}")

        # Print Nmap summary
        if nmap_data:
            print("\n[+] Nmap Scan Summary:")
            print(f" Hostname: {nmap_data.get('hostname', 'Unknown')}")
            print(f" State: {nmap_data.get('state', 'Unknown')}")
            os_matches = nmap_data.get('os', [])
            if os_matches:
                print(f" OS Matches: {[os['name'] for os in os_matches]}")

            for proto, ports in nmap_data.get('protocols', {}).items():
                print(f"\n Protocol: {proto}")
                for p in ports:
                    print(f"  Port {p['port']}: {p['state']} - {p['name']} {p['product']} {p['version']}")
                    if p.get('scripts'):
                        for sid, output in p['scripts'].items():
                            print(f"    Script [{sid}]: {output}")

            if nmap_data.get('scripts'):
                print("\n Host Scripts Output:")
                for sid, output in nmap_data['scripts'].items():
                    print(f" Script [{sid}]: {output}")

        return report_path


if __name__ == "__main__":
    target = input("Enter target URL or IP: ").strip()
    if target:
        core = CyberCore(target)
        core.run_full_scan()
    else:
        print("No target provided. Exiting.")
