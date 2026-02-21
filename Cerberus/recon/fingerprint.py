import requests
from urllib.parse import urlparse, urljoin


class Fingerprinter:
    def __init__(self, target, recon_data=None, timeout=8):
        self.target = target.rstrip("/")
        self.timeout = timeout
        self.headers = (recon_data or {}).get("http_headers", {})
        self.scripts = (recon_data or {}).get("spider", {}).get("scripts", [])

    def _get_root(self):
        try:
            r = requests.get(self.target, timeout=self.timeout)
            return r.text, dict(r.headers)
        except requests.RequestException:
            return "", {}

    def _detect_frameworks(self, scripts):
        libs = {"react": False, "angular": False, "vue": False, "jquery": False, "next": False, "nuxt": False, "svelte": False}
        for s in scripts:
            low = s.lower()
            if "react" in low:
                libs["react"] = True
            if "angular" in low:
                libs["angular"] = True
            if "vue" in low:
                libs["vue"] = True
            if "jquery" in low or "jq" in low:
                libs["jquery"] = True
            if "next" in low:
                libs["next"] = True
            if "nuxt" in low:
                libs["nuxt"] = True
            if "svelte" in low:
                libs["svelte"] = True
        return libs

    def _detect_cms(self, html):
        cms = {"wordpress": False, "drupal": False, "joomla": False}
        low = html.lower()
        if "wp-content" in low or "wordpress" in low:
            cms["wordpress"] = True
        if "drupal.settings" in low or "drupal" in low:
            cms["drupal"] = True
        if "joomla" in low or "com_content" in low:
            cms["joomla"] = True
        return cms

    def _server_info(self, hdrs):
        return {
            "server": hdrs.get("Server"),
            "powered_by": hdrs.get("X-Powered-By"),
            "via": hdrs.get("Via"),
        }

    def _well_known(self):
        urls = [urljoin(self.target, "/robots.txt"), urljoin(self.target, "/.well-known/security.txt")]
        found = {}
        for u in urls:
            try:
                r = requests.get(u, timeout=self.timeout)
                if r.status_code == 200:
                    found[u] = True
                else:
                    found[u] = False
            except requests.RequestException:
                found[u] = False
        return found

    def run(self):
        html, hdrs = self._get_root()
        server = self._server_info(hdrs or self.headers)
        frameworks = self._detect_frameworks(self.scripts)
        cms = self._detect_cms(html)
        well_known = self._well_known()
        return {"server": server, "frameworks": frameworks, "cms": cms, "well_known": well_known}
