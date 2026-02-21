import requests
from .spider import Spider
from .fingerprint import Fingerprinter
from .dns_whois import DNSWhois

class ReconModule:
    def __init__(self, target):
        self.target = target
        self.results = {}

    def run(self):
        print(f"[*] Starting Reconnaissance on {self.target}")
        self._get_http_headers()
        self._run_spider()
        self._run_fingerprint()
        self._run_dns_whois()
        return self.results

    def _get_http_headers(self):
        try:
            response = requests.head(self.target, timeout=5)
            self.results['http_headers'] = dict(response.headers)
            print("[+] HTTP Headers retrieved.")
        except requests.RequestException as e:
            print(f"[-] Error retrieving HTTP headers: {e}")
            self.results['http_headers'] = {}

    def _run_spider(self):
        spider = Spider(self.target)
        data = spider.run()
        self.results['spider'] = data
        print(f"[+] Spider found {len(data.get('pages', []))} pages.")

    def _run_fingerprint(self):
        fp = Fingerprinter(self.target, self.results)
        data = fp.run()
        self.results['fingerprint'] = data
        print("[+] Fingerprinting completed.")

    def _run_dns_whois(self):
        dw = DNSWhois(self.target)
        data = dw.run()
        self.results['dns_whois'] = data
        print("[+] DNS and WHOIS lookup completed.")
