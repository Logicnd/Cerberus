import os
import io
import sys
from flask import Flask, render_template, request, send_file, redirect, url_for, session
base_dir = os.path.dirname(os.path.abspath(__file__))
pkg_dir = os.path.abspath(os.path.join(base_dir, ".."))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)
from recon.recon_engine import ReconModule
from scanning.scan_engine import ScanModule
from reporting.report_engine import ReportModule
from codeintel.translator import Translator
from codeintel.analysis import Analyzer
from codeintel.links import LinkFinder
from codeintel.report import markdown_summary
from codeintel.docgen import generate as doc_generate


def _load_env(path):
    if not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except Exception:
        pass

root_dir = os.path.abspath(os.path.join(base_dir, "..", ".."))
_load_env(os.path.join(root_dir, ".env"))
_load_env(os.path.join(os.path.dirname(base_dir), ".env"))

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("CERBERUS_SECRET", os.urandom(24))

last_results = {}
audit_log = "audit.log"
comments = []
APP_USERNAME = os.environ.get("CERBERUS_USERNAME", "cerberus")
APP_PASSWORD = os.environ.get("CERBERUS_PASSWORD", "change-me")
DEMO_MODE = os.environ.get("CERBERUS_DEMO", "").lower() in ("1", "true", "yes", "on")


def require_role(*roles):
    def wrapper(fn):
        def inner(*args, **kwargs):
            if DEMO_MODE:
                if not session.get("user"):
                    session["user"] = "demo"
                return fn(*args, **kwargs)
            if session.get("user"):
                return fn(*args, **kwargs)
            return redirect(url_for("login"))
        inner.__name__ = fn.__name__
        return inner
    return wrapper

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
@require_role("admin", "analyst")
def scan():
    target = request.form.get("target", "").strip()
    if not target:
        return redirect(url_for("index"))
    recon = ReconModule(target)
    recon_data = recon.run()
    scanner = ScanModule(target, recon_data)
    findings = scanner.run()
    reporter = ReportModule(findings, recon_data)
    reporter.generate_report("report.json")
    reporter.generate_markdown("report.md")
    last_results["target"] = target
    last_results["recon"] = recon_data
    last_results["findings"] = findings
    _audit("scan", {"target": target})
    return render_template("results.html", target=target, recon=recon_data, findings=findings)

@app.route("/translate", methods=["GET", "POST"])
def translate():
    if request.method == "GET":
        return render_template("translate.html")
    code = request.form.get("code", "")
    src = request.form.get("src", "python")
    dst = request.form.get("dst", "html")
    tr = Translator()
    out = tr.translate(code, src, dst)
    an = Analyzer()
    res = an.static_analysis(code, src)
    lf = LinkFinder()
    links = lf.find(code)
    md = markdown_summary("Translation", out, res, links)
    with open("translation.md", "w", encoding="utf-8") as f:
        f.write(md)
    doc = doc_generate("Translation Doc", out, res, links)
    with open("translation_doc.md", "w", encoding="utf-8") as f:
        f.write(doc)
    _audit("translate", {"src": src, "dst": dst})
    return render_template("translate.html", code=code, output=out, src=src, dst=dst, analysis=res, links=links)

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "GET":
        return render_template("analyze.html")
    code = request.form.get("code", "")
    lang = request.form.get("lang", "python")
    an = Analyzer()
    res = an.static_analysis(code, lang)
    lf = LinkFinder()
    links = lf.find(code)
    md = markdown_summary("Analysis", None, res, links)
    with open("analysis.md", "w", encoding="utf-8") as f:
        f.write(md)
    doc = doc_generate("Analysis Doc", None, res, links)
    with open("analysis_doc.md", "w", encoding="utf-8") as f:
        f.write(doc)
    _audit("analyze", {"lang": lang})
    return render_template("analyze.html", code=code, lang=lang, analysis=res, links=links)

@app.route("/decode", methods=["GET", "POST"])
def decode():
    if request.method == "GET":
        return render_template("decode.html")
    scheme = request.form.get("scheme", "base64")
    data = request.form.get("data", "")
    key = request.form.get("key", "")
    from codeintel.decoder import Decoder
    d = Decoder()
    output = ""
    if scheme == "base64":
        output = d.base64_decode(data)
    elif scheme == "hex":
        output = d.hex_decode(data)
    elif scheme == "rot13":
        output = d.rot13(data)
    elif scheme == "xor":
        output = d.xor_decode(data, key)
    else:
        r = d.auto(data)
        output = r.get("decoded")
    return render_template("decode.html", scheme=scheme, data=data, key=key, output=output)

@app.route("/batch", methods=["GET", "POST"])
@require_role("admin", "analyst")
def batch():
    if request.method == "GET":
        return render_template("batch.html")
    source_lang = request.form.get("source_lang", "python")
    target_lang = request.form.get("target_lang", "html")
    texts = request.form.get("texts", "")
    items = [t for t in texts.split("\n\n") if t.strip()]
    tr = Translator()
    translated = tr.batch_translate([(c, source_lang, target_lang) for c in items])
    an = Analyzer()
    analyzed = an.batch_analyze([(c, source_lang) for c in items])
    return render_template("batch.html", source_lang=source_lang, target_lang=target_lang, texts=texts, translated=translated, analyzed=analyzed)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=None)
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if username == APP_USERNAME and password == APP_PASSWORD:
        session["user"] = username
        _audit("login", {"user": username})
        return redirect(url_for("index"))
    return render_template("login.html", error="invalid")

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")
    if username == APP_USERNAME and password == APP_PASSWORD:
        session["user"] = username
        _audit("login", {"user": username})
        return {"ok": True}
    return {"ok": False, "error": "invalid"}, 401

@app.route("/logout", methods=["POST"])
def logout():
    u = session.pop("user", None)
    _audit("logout", {"user": u})
    return redirect(url_for("index"))

def _audit(action, detail):
    try:
        with open(audit_log, "a", encoding="utf-8") as f:
            f.write(f"{action} {detail}\n")
    except Exception:
        pass

@app.route("/collab", methods=["GET"])
def collab():
    room = request.args.get("room", "default")
    room_comments = [c for c in comments if c.get("room") == room]
    return render_template("collab.html", comments=room_comments, room=room)

@app.route("/comment", methods=["POST"])
def comment():
    user = session.get("user", "guest")
    text = request.form.get("text", "")
    room = request.form.get("room", "default")
    if text:
        comments.append({"user": user, "text": text, "room": room})
        _audit("comment", {"user": user})
    return redirect(url_for("collab", room=room))

@app.route("/repo", methods=["GET"])
@require_role("admin")
def repo():
    out = ""
    try:
        import subprocess
        r = subprocess.run(["git", "status"], capture_output=True, text=True)
        out = r.stdout or r.stderr
    except Exception:
        out = "no git available"
    return render_template("repo.html", output=out)

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404, message="Not Found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", code=500, message="Server Error"), 500

@app.after_request
def add_headers(resp):
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "no-referrer"
    resp.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; frame-ancestors 'none'; connect-src 'self'"
    return resp

@app.route("/status", methods=["GET"])
@require_role("admin")
def status():
    import platform
    import socket
    info = {}
    info["os"] = platform.system()
    info["release"] = platform.release()
    info["version"] = platform.version()
    info["machine"] = platform.machine()
    info["python"] = platform.python_version()
    host = socket.gethostname()
    info["hostname"] = host
    ips = []
    try:
        ips = socket.gethostbyname_ex(host)[2]
    except Exception:
        ips = []
    info["ips"] = ips
    info["env_count"] = len(os.environ)
    return render_template("status.html", info=info)
@app.route("/download/json", methods=["GET"])
@require_role("admin", "analyst")
def download_json():
    if not os.path.exists("report.json"):
        return redirect(url_for("index"))
    return send_file("report.json", as_attachment=True, download_name="report.json")

@app.route("/download/md", methods=["GET"])
@require_role("admin", "analyst")
def download_md():
    if not os.path.exists("report.md"):
        return redirect(url_for("index"))
    return send_file("report.md", as_attachment=True, download_name="report.md")


if __name__ == "__main__":
    print("UI running at http://localhost:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
