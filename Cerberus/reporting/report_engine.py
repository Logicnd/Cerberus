import json
import os

class ReportModule:
    def __init__(self, findings, recon=None):
        self.findings = findings
        self.recon = recon or {}

    def generate_report(self, filename="report.json"):
        print(f"[*] Generating report to {filename}")
        try:
            with open(filename, 'w') as f:
                json.dump(self.findings, f, indent=4)
            print(f"[+] Report generated successfully.")
        except Exception as e:
            print(f"[-] Error generating report: {e}")

    def generate_markdown(self, filename="report.md"):
        print(f"[*] Generating markdown report to {filename}")
        try:
            lines = []
            lines.append("# Cerberus Report")
            lines.append("")
            lines.append("## Reconnaissance")
            hdrs = self.recon.get("http_headers", {})
            lines.append("### HTTP Headers")
            for k, v in hdrs.items():
                lines.append(f"- {k}: {v}")
            dns = self.recon.get("dns_whois", {}).get("dns", {})
            lines.append("### DNS")
            lines.append(f"- Host: {dns.get('host')}")
            lines.append(f"- IP: {dns.get('ip')}")
            lines.append(f"- PTR: {dns.get('ptr')}")
            spider = self.recon.get("spider", {})
            lines.append("### Spider")
            lines.append(f"- Pages: {len(spider.get('pages', []))}")
            lines.append(f"- Forms: {len(spider.get('forms', []))}")
            lines.append(f"- Scripts: {len(spider.get('scripts', []))}")
            fp = self.recon.get("fingerprint", {})
            lines.append("### Fingerprint")
            srv = fp.get("server", {})
            lines.append(f"- Server: {srv.get('server')}")
            lines.append(f"- Powered-By: {srv.get('powered_by')}")
            lines.append("## Findings")
            for item in self.findings:
                lines.append(f"### {item.get('type')}")
                lines.append(f"- Severity: {item.get('severity')}")
                lines.append(f"- Details: {item.get('details')}")
                lines.append(f"- Remediation: {item.get('remediation')}")
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            print("[+] Markdown report generated successfully.")
        except Exception as e:
            print(f"[-] Error generating markdown report: {e}")
