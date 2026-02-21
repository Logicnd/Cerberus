const { URL } = require("url");

function arg(name, def) {
  const idx = process.argv.indexOf(name);
  if (idx !== -1 && idx + 1 < process.argv.length) return process.argv[idx + 1];
  return def;
}

async function fetchText(u, timeout) {
  const c = AbortController ? new AbortController() : null;
  const t = c ? setTimeout(() => c.abort(), timeout) : null;
  try {
    const r = await fetch(u, { redirect: "follow", signal: c ? c.signal : undefined });
    const ct = r.headers.get("content-type") || "";
    if (ct.includes("text/html") || ct === "") return await r.text();
    return "";
  } catch {
    return "";
  } finally {
    if (t) clearTimeout(t);
  }
}

function sameOrigin(base, u) {
  try {
    const a = new URL(base);
    const b = new URL(u, base);
    return a.protocol === b.protocol && a.host === b.host;
  } catch {
    return false;
  }
}

function abs(base, u) {
  try {
    return new URL(u, base).toString();
  } catch {
    return null;
  }
}

function parseHTML(base, html) {
  const links = new Set();
  const scripts = new Set();
  const forms = [];
  const api = new Set();
  const aRe = /<a[^>]+href=["']([^"'#]+)["']/gi;
  const sRe = /<script[^>]+src=["']([^"']+)["']/gi;
  const fRe = /<form[^>]*?(?:action=["']?([^"'>\s]*)[^>]*?)?(?:method=["']?([^"'>\s]*)[^>]*?)?>/gi;
  const iRe = /<input[^>]*name=["']([^"']+)["'][^>]*?(?:type=["']?([^"'>\s]*)[^>]*)?/gi;
  let m;
  while ((m = aRe.exec(html))) {
    const u = abs(base, m[1]);
    if (u && sameOrigin(base, u)) {
      links.add(u);
      if (u.includes("/api/") || u.endsWith(".json")) api.add(u);
    }
  }
  while ((m = sRe.exec(html))) {
    const u = abs(base, m[1]);
    if (u) scripts.add(u);
  }
  while ((m = fRe.exec(html))) {
    const action = abs(base, m[1] || "");
    const method = (m[2] || "GET").toUpperCase();
    const inputs = [];
    let mi;
    while ((mi = iRe.exec(html))) {
      inputs.push({ name: mi[1], type: mi[2] || "text" });
    }
    forms.push({ action: action || base, method, inputs });
  }
  return { links: Array.from(links), scripts: Array.from(scripts), forms, api_endpoints: Array.from(api) };
}

async function run(target, maxDepth, maxPages, timeout) {
  const visited = new Set();
  const pages = new Set();
  const forms = [];
  const scripts = new Set();
  const api = new Set();
  const q = [[target, 0]];
  while (q.length && pages.size < maxPages) {
    const [u, d] = q.shift();
    if (visited.has(u) || d > maxDepth) continue;
    visited.add(u);
    const html = await fetchText(u, timeout);
    if (!html) continue;
    pages.add(u);
    const parsed = parseHTML(u, html);
    parsed.forms.forEach(f => forms.push(f));
    parsed.scripts.forEach(s => scripts.add(s));
    parsed.api_endpoints.forEach(a => api.add(a));
    for (const l of parsed.links) {
      if (!visited.has(l)) q.push([l, d + 1]);
    }
  }
  return {
    pages: Array.from(pages).sort(),
    forms,
    scripts: Array.from(scripts).sort(),
    api_endpoints: Array.from(api).sort()
  };
}

async function main() {
  const target = arg("--target");
  if (!target) {
    console.error("usage: node spider.js --target <url> [--depth 2] [--limit 200] [--timeout 8000]");
    process.exit(1);
  }
  const depth = parseInt(arg("--depth", "2"), 10);
  const limit = parseInt(arg("--limit", "200"), 10);
  const timeout = parseInt(arg("--timeout", "8000"), 10);
  const data = await run(target, depth, limit, timeout);
  const out = JSON.stringify(data, null, 2);
  console.log(out);
}

main().catch(e => {
  console.error(String(e || "error"));
  process.exit(1);
});
