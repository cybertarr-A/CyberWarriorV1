from modules import (
    ReconTool,
    scan_target,
    run_exploit,
    AICore,
    remember_finding,
    list_memory,
)
from modules.report_generator import ReportGenerator
from modules.core import CyberCore

def main():
    target = input("Enter the target URL or IP to run CyberWarriorV1 on: ").strip()
    if not target:
        print("No target provided, exiting.")
        return

    print(f"\n[*] Starting CyberWarriorV1 on target: {target}\n")

    # 1) Recon
    print("=== Recon Stage ===")
    remember_finding(target, "Recon started")
    recon_data = ReconTool(target)
    remember_finding(target, "Recon complete")

    # 2) Scanning
    print("\n=== Scanner Stage ===")
    remember_finding(target, "Scan started")
    scan_output = scan_target(target)
    remember_finding(target, "Scan complete")

    # 3) Exploitation
    print("\n=== Exploit Stage ===")
    remember_finding(target, "Exploit started")
    exploit_results = run_exploit(target)
    remember_finding(target, "Exploit complete")

    # 4) AI Analysis
    print("\n=== AI Analysis Stage ===")
    ai = AICore()

    # DEBUG: print available methods to help you pick the right one
    methods = [m for m in dir(ai) if not m.startswith("__") and callable(getattr(ai, m))]
    print("Available AICore methods:", methods)

    # TODO: replace this with the actual method name once known
    ai_results = "AI analysis method not implemented or unknown"

    remember_finding(target, f"AI analysis: {ai_results}")

    # 5) Report Generation
    print("\n=== Report Generation Stage ===")
    rg = ReportGenerator()
    report_path = rg.save_report(
        target,
        headers=getattr(recon_data, 'headers', {}),
        open_ports=getattr(scan_output, 'open_ports', []),
        findings=getattr(exploit_results, 'findings', []),
        html_snippet=str(ai_results),
    )
    print(f"[✔] Report saved to: {report_path}\n")
    remember_finding(target, f"Report generated at {report_path}")

    # 6) Show Memory Log
    list_memory()

if __name__ == "__main__":
    main()
