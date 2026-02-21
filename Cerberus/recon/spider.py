import requests
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser
from collections import deque


class LinkFormParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.links = set()
        self.forms = []
        self.scripts = set()
        self._current_form = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "a":
            href = attrs_dict.get("href")
            if href:
                url = urljoin(self.base_url, href)
                self.links.add(url)
        elif tag == "form":
            action = attrs_dict.get("action") or ""
            method = attrs_dict.get("method") or "GET"
            self._current_form = {"action": urljoin(self.base_url, action), "method": method.upper(), "inputs": []}
        elif tag == "input":
            if self._current_form is not None:
                name = attrs_dict.get("name")
                input_type = attrs_dict.get("type") or "text"
                self._current_form["inputs"].append({"name": name, "type": input_type})
        elif tag == "script":
            src = attrs_dict.get("src")
            if src:
                url = urljoin(self.base_url, src)
                self.scripts.add(url)

    def handle_endtag(self, tag):
        if tag == "form" and self._current_form is not None:
            self.forms.append(self._current_form)
            self._current_form = None


class Spider:
    def __init__(self, target, max_depth=2, max_pages=200, timeout=8):
        self.target = target.rstrip("/")
        self.parsed = urlparse(self.target)
        self.base = f"{self.parsed.scheme}://{self.parsed.netloc}"
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.timeout = timeout
        self.visited = set()
        self.pages = set()
        self.forms = []
        self.scripts = set()
        self.api_endpoints = set()

    def _same_origin(self, url):
        p = urlparse(url)
        return p.netloc == self.parsed.netloc and p.scheme in ("http", "https")

    def _fetch(self, url):
        try:
            r = requests.get(url, timeout=self.timeout, allow_redirects=True)
            ctype = r.headers.get("Content-Type", "")
            if "text/html" in ctype or ctype == "":
                return r.text
            return ""
        except requests.RequestException:
            return ""

    def _parse_page(self, url, html):
        parser = LinkFormParser(url)
        parser.feed(html)
        links = {l for l in parser.links if self._same_origin(l)}
        self.forms.extend(parser.forms)
        self.scripts |= parser.scripts
        for l in links:
            if "/api/" in l or l.endswith(".json"):
                self.api_endpoints.add(l)
        return links

    def run(self):
        queue = deque([(self.target, 0)])
        while queue and len(self.pages) < self.max_pages:
            url, depth = queue.popleft()
            if url in self.visited or depth > self.max_depth:
                continue
            self.visited.add(url)
            html = self._fetch(url)
            if not html:
                continue
            self.pages.add(url)
            links = self._parse_page(url, html)
            for l in links:
                if l not in self.visited:
                    queue.append((l, depth + 1))
        return {
            "pages": sorted(self.pages),
            "forms": self.forms,
            "scripts": sorted(self.scripts),
            "api_endpoints": sorted(self.api_endpoints),
        }
