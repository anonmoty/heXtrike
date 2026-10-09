from core.session import http
from core.banner import Banner
from colorama import Fore
import time

class MisconfigScanner:
    def __init__(self, t, e):
        self.t = t; self.e = e

    def run(self):
        # Debug endpoints
        debug = ["/__debug__/","/debug/","/actuator","/actuator/env",
                 "/swagger-ui.html","/api-docs","/graphql","/server-status",
                 "/elmah.axd","/trace.axd","/telescope","/phpinfo.php"]
        for ep in debug:
            r = http.get(self.t.url + ep)
            if r and r.status_code == 200 and len(r.text) > 50:
                if "404" not in r.text.lower()[:100] and "not found" not in r.text.lower()[:100]:
                    self.e.add(title="Debug Endpoint: " + ep, severity="HIGH",
                        desc="Debug page accessible", url=self.t.url + ep,
                        fix="Disable debug in production.",
                        owasp="A05 - Security Misconfiguration", module="Misconfig")
            time.sleep(0.2)

        # Sensitive files
        files = [".env",".git/HEAD",".git/config","backup.sql","wp-config.php.bak",
                 "config.php.bak",".DS_Store","crossdomain.xml"]
        for f in files:
            r = http.get(self.t.url + "/" + f)
            if r and r.status_code == 200 and "404" not in r.text.lower()[:100]:
                sev = "CRITICAL" if f in [".env",".git/HEAD","backup.sql"] else "HIGH"
                self.e.add(title="Sensitive File: " + f, severity=sev,
                    desc="File accessible", url=self.t.url + "/" + f,
                    evidence=r.text[:100],
                    fix="Block access to " + f,
                    owasp="A01 - Broken Access Control", module="Misconfig")
            time.sleep(0.2)

        # HTTP methods
        r = http.get(self.t.url, method="OPTIONS") if hasattr(http, 'get') else None
        r = http.s.request("OPTIONS", self.t.url, timeout=10, verify=False)
        if r:
            allow = r.headers.get("Allow", "")
            dangerous = [m for m in ["PUT","DELETE","TRACE"] if m in allow.upper()]
            if dangerous:
                self.e.add(title="Dangerous HTTP Methods", severity="MEDIUM",
                    desc="Methods: " + ", ".join(dangerous), url=self.t.url,
                    evidence="Allow: " + allow,
                    fix="Disable unnecessary methods.",
                    owasp="A05 - Security Misconfiguration", module="Misconfig")
