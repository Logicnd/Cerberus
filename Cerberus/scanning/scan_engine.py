class ScanModule:
    def __init__(self, target, recon_data):
        self.target = target
        self.recon_data = recon_data
        self.findings = []

    def run(self):
        print(f"[*] Starting Vulnerability Scan on {self.target}")
        self._check_security_headers()
        self._check_cookies()
        self._check_csp()
        return self.findings

    def _check_security_headers(self):
        headers = self.recon_data.get('http_headers', {})
        missing_headers = []
        
        security_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options',
            'Content-Security-Policy',
            'Strict-Transport-Security'
        ]

        for header in security_headers:
            if header not in headers:
                missing_headers.append(header)

        if missing_headers:
            self.findings.append({
                'type': 'Missing Security Headers',
                'severity': 'Low',
                'details': f"The following security headers are missing: {', '.join(missing_headers)}",
                'remediation': 'Implement the missing security headers to enhance application security.'
            })
            print(f"[!] Found missing security headers: {len(missing_headers)}")
        else:
            print("[+] All core security headers are present.")

    def _check_cookies(self):
        headers = self.recon_data.get('http_headers', {})
        raw = headers.get('Set-Cookie')
        if not raw:
            return
        if isinstance(raw, str):
            cookies = [raw]
        else:
            cookies = list(raw)
        weak = []
        for c in cookies:
            lower = c.lower()
            if 'secure' not in lower or 'httponly' not in lower:
                weak.append(c.split(';', 1)[0])
        if weak:
            self.findings.append({
                'type': 'Cookie Flags',
                'severity': 'Medium',
                'details': f"The following cookies miss Secure or HttpOnly: {', '.join(weak)}",
                'remediation': 'Set Secure, HttpOnly and SameSite on session and sensitive cookies.'
            })

    def _check_csp(self):
        headers = self.recon_data.get('http_headers', {})
        csp = headers.get('Content-Security-Policy')
        if not csp:
            return
        lower = csp.lower().replace(" ", "")
        if "'unsafe-inline'" in lower or "*" in lower:
            self.findings.append({
                'type': 'Content Security Policy',
                'severity': 'Medium',
                'details': 'CSP contains unsafe-inline or wildcard sources.',
                'remediation': 'Use nonces or hashes and avoid wildcard sources in CSP directives.'
            })
