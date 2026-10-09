from core.session import http
from core.banner import Banner
from colorama import Fore

class CORSScanner:
    def __init__(self, t, e):
        self.t = t; self.e = e

    def run(self):
        tests = [
            ("https://evil.com", "Arbitrary Origin"),
            ("null", "Null Origin"),
            ("https://evil." + self.t.host, "Subdomain Trust"),
        ]
        for origin, desc in tests:
            r = http.get(self.t.url, headers={"Origin": origin})
            if r:
                acao = r.headers.get("Access-Control-Allow-Origin", "")
                acac = r.headers.get("Access-Control-Allow-Credentials", "")
                if origin in acao or acao == "*":
                    sev = "HIGH" if "true" in acac.lower() else "MEDIUM"
                    Banner.result("⚠️ " + desc, "ACAO: " + acao + " ACAC: " + acac, Fore.RED)
                    self.e.add(title="CORS: " + desc, severity=sev,
                        desc="Server allows " + desc,
                        url=self.t.url, payload="Origin: " + origin,
                        evidence="ACAO: " + acao,
                        fix="Whitelist specific origins.",
                        owasp="A05 - Security Misconfiguration", module="CORS Scanner")
                else:
                    Banner.result("✅ " + desc, "Blocked", Fore.GREEN)
