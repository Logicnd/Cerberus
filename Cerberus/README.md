# Cerberus: Educational Vulnerability Assessment Framework

## Overview
Cerberus is a modular framework designed for educational purposes and authorized security assessments. It assists security researchers in identifying potential weaknesses in web applications and infrastructure to improve security posture.

## Ethical Guidelines
This tool is intended for:
-   Authorized security assessments (Penetration Testing) with explicit permission.
-   Educational research to understand security concepts.
-   Defensive analysis to identify and patch vulnerabilities.

**Warning:** The usage of this tool for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state, and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.

## Modules
1.  **Reconnaissance**: Information gathering techniques (Passive and Active).
2.  **Scanning**: Identification of potential security misconfigurations and vulnerabilities.
3.  **Reporting**: Comprehensive reporting of findings with remediation advice.

## Usage
```python
python cerberus.py --target <url>
```

## JavaScript
```bash
node js/spider.js --target <url> --depth 2 --limit 200
```

## Go
```bash
go run go/dnswhois/main.go -target <url>
```

## UI
```bash
python ui/app.py
# open http://127.0.0.1:5000
```
### Pages
- /scan: run recon + passive scan on a target
- /translate: translate code between languages with analysis and links
- /analyze: analyze code for dependencies, complexity, patterns
- /decode: decode base64/hex/rot13/xor and auto-detect
- /batch: batch translate/analyze multiple items
- /collab: team comments with rooms
- /repo: repository status (admin)
- /status: system status (admin)

### Auth
- Create a .env file in the project root:
```bash
CERBERUS_USERNAME=cerberus
CERBERUS_PASSWORD=change-me
CERBERUS_SECRET=some-long-random-string
```
- Credentials are loaded from .env (or the process env) and used for the single login

## Web (Next.js)
```bash
cd web
npm install
npm run dev
```
- Set NEXT_PUBLIC_API_BASE to the Flask UI base URL, for example:
```bash
set NEXT_PUBLIC_API_BASE=http://127.0.0.1:5000
npm run dev
```
- Deploy to Vercel by importing the web folder as the project root
