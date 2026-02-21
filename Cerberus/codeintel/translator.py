import re
from concurrent.futures import ThreadPoolExecutor


class Translator:
    def __init__(self, max_workers=4):
        self.pool = ThreadPoolExecutor(max_workers=max_workers)

    def translate(self, code, from_lang, to_lang, options=None):
        key = (from_lang.lower(), to_lang.lower())
        if key == ("python", "html"):
            return self._py_to_html(code)
        if key == ("python", "javascript"):
            return self._py_to_js(code)
        if key == ("html", "python"):
            return self._html_to_py(code)
        return code

    def batch_translate(self, items):
        futures = [self.pool.submit(self.translate, c, f, t) for (c, f, t) in items]
        return [f.result() for f in futures]

    def _py_to_html(self, code):
        lines = []
        lines.append("<!doctype html>")
        lines.append("<html><head><meta charset=\"utf-8\"><title>Python Doc</title></head><body>")
        lines.append("<h1>Python Functions</h1>")
        for m in re.finditer(r"def\s+([a-zA-Z_]\w*)\s*\((.*?)\)\s*:", code):
            name = m.group(1)
            args = m.group(2)
            lines.append(f"<div><strong>{name}</strong>({args})</div>")
        lines.append("</body></html>")
        return "\n".join(lines)

    def _py_to_js(self, code):
        js = []
        pos = 0
        for m in re.finditer(r"def\s+([a-zA-Z_]\w*)\s*\((.*?)\)\s*:", code):
            js.append(code[pos:m.start()])
            name = m.group(1)
            args = m.group(2)
            js.append(f"function {name}({args}) {{")
            js.append("}")
            pos = m.end()
        js.append(code[pos:])
        return "\n".join(js)

    def _html_to_py(self, code):
        funcs = []
        for m in re.finditer(r"<script[^>]*>(.*?)</script>", code, flags=re.DOTALL | re.IGNORECASE):
            block = m.group(1).strip()
            funcs.append(f"# script block\n{block}")
        return "\n\n".join(funcs) if funcs else "# no script blocks"
