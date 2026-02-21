import re
from concurrent.futures import ThreadPoolExecutor


class Analyzer:
    def __init__(self, max_workers=4):
        self.pool = ThreadPoolExecutor(max_workers=max_workers)

    def static_analysis(self, code, lang="python"):
        deps = self._dependencies(code, lang)
        comp = self._complexity(code, lang)
        vulns = self._vulnerabilities(code, lang)
        return {"dependencies": deps, "complexity": comp, "vulnerabilities": vulns}

    def _dependencies(self, code, lang):
        if lang == "python":
            return re.findall(r"^\s*(?:import|from)\s+([a-zA-Z_][\w\.]*)", code, flags=re.MULTILINE)
        if lang == "html":
            urls = re.findall(r"src=[\"']([^\"']+)[\"']", code)
            return urls
        return []

    def _complexity(self, code, lang):
        keys = ["if", "for", "while", "and", "or", "try", "except", "with"]
        count = 0
        for k in keys:
            count += len(re.findall(r"\b" + k + r"\b", code))
        return {"cyclomatic_like": count}

    def _vulnerabilities(self, code, lang):
        issues = []
        patterns = [
            (r"\beval\s*\(", "Use of eval"),
            (r"\bexec\s*\(", "Use of exec"),
            (r"os\.system\s*\(", "OS command execution"),
            (r"subprocess\.(Popen|call|run)\s*\(", "Subprocess execution"),
            (r"requests\.\w+\s*\([^)]*verify\s*=\s*False", "Insecure TLS"),
        ]
        for pat, desc in patterns:
            if re.search(pat, code):
                issues.append({"type": "pattern", "detail": desc})
        urls = re.findall(r"https?://[^\s\"'>)]+", code)
        if urls:
            issues.append({"type": "external_refs", "count": len(urls)})
        return issues

    def batch_analyze(self, items):
        futures = [self.pool.submit(self.static_analysis, c, l) for (c, l) in items]
        return [f.result() for f in futures]
