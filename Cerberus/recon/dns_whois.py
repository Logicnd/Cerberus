import socket
from urllib.parse import urlparse


class DNSWhois:
    def __init__(self, target, timeout=10):
        self.target = target
        self.timeout = timeout

    def _domain(self):
        p = urlparse(self.target)
        host = p.netloc
        if ":" in host:
            host = host.split(":")[0]
        return host

    def resolve(self):
        host = self._domain()
        ip = None
        ptr = None
        try:
            ip = socket.gethostbyname(host)
        except Exception:
            ip = None
        if ip:
            try:
                ptr = socket.gethostbyaddr(ip)[0]
            except Exception:
                ptr = None
        return {"host": host, "ip": ip, "ptr": ptr}

    def _whois_query(self, server, query):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((server, 43))
            s.sendall((query + "\r\n").encode("utf-8"))
            data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
            s.close()
            return data.decode(errors="ignore")
        except Exception:
            return ""

    def whois(self):
        domain = self._domain()
        tld = domain.split(".")[-1].lower() if "." in domain else ""
        server = "whois.iana.org"
        if tld in {"com", "net"}:
            server = "whois.verisign-grs.com"
        resp = self._whois_query(server, domain)
        return {"server": server, "raw": resp}

    def run(self):
        return {"dns": self.resolve(), "whois": self.whois()}
