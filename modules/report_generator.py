import os
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        print("ReportGenerator initialized")

    def save_report(self, target, headers, open_ports, findings, html_snippet, output_dir="reports"):
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Create a safe filename by replacing ':' and '/' and other problematic chars
        safe_target = target.replace("://", "_").replace("/", "_").replace(":", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_target}_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# 🛡️ CyberWarrior Report\n")
            f.write(f"**Target:** {target}\n")
            f.write(f"**Scan Time:** {timestamp}\n\n")

            f.write("## 🔍 Headers\n")
            if headers:
                for k, v in headers.items():
                    f.write(f"- {k}: {v}\n")
            else:
                f.write("No headers found.\n")
            f.write("\n")

            f.write("## 🌐 Open Ports\n")
            if open_ports:
                for port in open_ports:
                    f.write(f"- Port {port} open\n")
            else:
                f.write("No open ports found.\n")
            f.write("\n")

            f.write("## 🤖 AI Findings\n")
            if findings:
                for finding in findings:
                    f.write(f"- {finding}\n")
            else:
                f.write("No AI findings.\n")
            f.write("\n")

            f.write("## 🧬 HTML Snippet\n```html\n")
            # Write only first 500 chars of snippet for brevity
            snippet = html_snippet[:500]
            if len(html_snippet) > 500:
                snippet += "..."
            f.write(snippet + "\n```\n")

        print(f"✅ Report saved to {filepath}")
        return filepath


def generate_report(target, recon_data, scan_data, exploit_data, ai_summary, output_dir="reports"):
    rg = ReportGenerator()

    headers = getattr(recon_data, "headers", {}) if recon_data else {}
    open_ports = getattr(scan_data, "open_ports", []) if scan_data else []
    findings = getattr(exploit_data, "findings", []) if exploit_data else []
    html_snippet = getattr(recon_data, "html", "<no html>") if recon_data else "<no html>"

    return rg.save_report(target, headers, open_ports, findings, ai_summary, output_dir)
