import re


class LinkFinder:
    def find(self, code):
        urls = re.findall(r"https?://[^\s\"'>)]+", code)
        apis = re.findall(r"/api/[a-zA-Z0-9/_\-]+", code)
        ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", code)
        refs = re.findall(r"[a-zA-Z0-9_.-]+@[a-zA-Z0-9_.-]+", code)
        return {"urls": urls, "api_paths": apis, "ips": ips, "emails": refs}
