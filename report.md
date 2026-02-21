# Cerberus Report

## Reconnaissance
### HTTP Headers
- content-type: text/html; charset=utf-8
- date: Sat, 21 Feb 2026 22:25:34 GMT
- server: website
- cache-control: no-store, must-revalidate, no-cache
- content-encoding: br
- set-cookie: rbx-ip2=1; domain=roblox.com; expires=Sat, 21-Feb-2026 23:25:34 GMT; path=/, GuestData=UserID=-311850560; domain=.roblox.com; expires=Wed, 09-Jul-2053 22:25:34 GMT; path=/
- vary: Accept-Encoding
- content-security-policy: report-uri https://metrics.roblox.com/v1/csp/report?type=enforce; upgrade-insecure-requests;  script-src 'self' 'unsafe-inline' apis.roblox.com roblox.com *.evidon.com *.gigya.com *.google-analytics.com *.ns1p.net adservice.google.com cdn.arkoselabs.com connect.facebook.net funcaptcha.com js.rbxcdn.com js.stripe.com long.open.weixin.qq.com midas.gtimg.cn radar.cedexis.com res.wx.qq.com roblox-api.arkoselabs.com arkoselabs.roblox.com roblox-load-generator-configuration.s3.us-east-2.amazonaws.com s.ytimg.com sb.scorecardresearch.com static.rbxcdn.com www.google.com www.gstatic.com www.youtube.com h.online-metrix.net request.eprotect.vantivcnp.com request.eprotect.vantivpostlive.com *.googletagmanager.com *.googleadservices.com googleads.g.doubleclick.net cdn.veriff.me *.lightstep.com client-api.arkoselabs.com api.arkoselabs.com *.sierra.chat sierra.chat sc-static.net *.sc-static.net *.snapchat.com *.tapad.com analytics.tiktok.com cdn.safecharge.com;  img-src 'self' data: *.cloudfront.net *.gilcdn.com *.gldcdn.com *.google-analytics.com *.google.com *.kaptcha.com *.rblx.org *.rbxcdn.com *.roblox.com *.robloxlabs.com googleads.g.doubleclick.net i.ytimg.com www.googletagmanager.com robloxcorp.s.llnwi.net roblox-poc.global.ssl.fastly.net d1unuk07s6td74.cloudfront.net *.sierra.chat sierra.chat *.stripe.com *.tarobicdn.com *.tarobidevsandboxcdn.com www.facebook.com *.snapchat.com *.safecharge.com;  connect-src 'self' *.roblox.com *.robloxlabs.com *.rblx.org *.rbx.com *.rbxcdn.com *.roblox.cn *.simulpong.com *.lightstep.com *.ns1p.net *.arkoselabs.com *.kaptcha.com *.google.com *.google-analytics.com *.doubleclick.net *.sentry.io wss://realtime.roblox.com wss://realtime.sitetest1.robloxlabs.com wss://realtime.sitetest2.robloxlabs.com wss://realtime.sitetest3.robloxlabs.com wss://realtime-signalr.roblox.com *.braintree-api.com *.braintreegateway.com d1q2u37vreaobr.cloudfront.net funcaptcha.com robloxcorp.s.llnwi.net roblox-poc.global.ssl.fastly.net d1unuk07s6td74.cloudfront.net *.sierra.chat sierra.chat sc-static.net *.sc-static.net *.snapchat.com *.tapad.com analytics.tiktok.com *.safecharge.com;
- cross-origin-opener-policy: same-origin-allow-popups
- x-frame-options: SAMEORIGIN
- strict-transport-security: max-age=31536000
- roblox-machine-id: f1b527ee-4b49-56c3-0e68-c533fb05d23a
- x-roblox-region: us-central_rbx
- x-roblox-edge: c173
- report-to: {"group":"network-errors","max_age":604800,"endpoints":[{"url":"https://ncs.roblox.com/upload"}]}
- nel: {"report_to":"network-errors","max_age":604800,"success_fraction":0.001,"failure_fraction":1}
### DNS
- Host: www.roblox.com
- IP: 128.116.31.3
- PTR: None
### Spider
- Pages: 1
- Forms: 0
- Scripts: 109
### Fingerprint
- Server: None
- Powered-By: None
## Findings
### Missing Security Headers
- Severity: Low
- Details: The following security headers are missing: X-Content-Type-Options, X-Frame-Options, Content-Security-Policy, Strict-Transport-Security
- Remediation: Implement the missing security headers to enhance application security.