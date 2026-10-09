from core.session import http
from core.banner import Banner
from colorama import Fore

class HeadersScanner:
    def __init__(self, t, e):
        self.t = t; self.e = e

    def run(self):
        r = http.get(self.t.url)
        if not r:
            Banner.scan_line("Headers", Fore.RED + "✗ No response", "❌")
            return

        Banner.section("Response Headers")
        for k, v in r.headers.items():
            Banner.result(k, v[:60])
        Banner.section_end()

        required = {
            "Content-Security-Policy": "Prevents XSS",
            "X-Frame-Options": "Prevents Clickjacking",
            "X-Content-Type-Options": "Prevents MIME sniffing",
            "Strict-Transport-Security": "Enforces HTTPS",
            "Referrer-Policy": "Controls referrer",
            "Permissions-Policy": "Controls features",
        }
        Banner.section("Security Headers Check")
        for h, desc in required.items():
            if h in r.headers:
                Banner.result("✅ " + h, r.headers[h][:45], Fore.GREEN)
            else:
                Banner.result("❌ " + h, "MISSING (" + desc + ")", Fore.RED)
                self.e.add(title="Missing Header: " + h, severity="MEDIUM",
                    desc=desc, url=self.t.url,
                    fix="Add " + h + " header.",
                    owasp="A05 - Security Misconfiguration", module="Headers Check")
        Banner.section_end()

        for h in ["X-Powered-By", "Server", "X-AspNet-Version"]:
            if h in r.headers:
                self.e.add(title="Info Disclosure: " + h, severity="LOW",
                    desc=h + ": " + r.headers[h], url=self.t.url,
                    fix="Remove " + h + " header.",
                    owasp="A05 - Security Misconfiguration", module="Headers Check")
