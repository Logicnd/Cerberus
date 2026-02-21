import argparse
from recon.recon_engine import ReconModule
from scanning.scan_engine import ScanModule
from reporting.report_engine import ReportModule

def main():
    parser = argparse.ArgumentParser(description="Cerberus: Educational Vulnerability Assessment Framework")
    parser.add_argument("--target", required=True, help="Target URL (e.g., http://example.com)")
    args = parser.parse_args()

    target = args.target
    
    # 1. Reconnaissance
    recon = ReconModule(target)
    recon_data = recon.run()

    # 2. Scanning
    scanner = ScanModule(target, recon_data)
    findings = scanner.run()

    # 3. Reporting
    reporter = ReportModule(findings, recon_data)
    reporter.generate_report()
    reporter.generate_markdown()

if __name__ == "__main__":
    main()
