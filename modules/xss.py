import time
from core.engine import inject_params, get_forms
from core.session import http
from core.banner import Banner
from colorama import Fore

class XSSScanner:
    def __init__(self, t, e):
        self.t = t; self.e = e

    def run(self):
        payloads = ['<script>alert("HS")</script>','<img src=x onerror=alert("HS")>',
                    '<svg onload=alert("HS")>','"><script>alert(1)</script>',
                    "'-alert(1)-'",'<details open ontoggle=alert(1)>']
        url = self.t.url
        urls = [url] if "?" in url else [url+"?q=test",url+"?search=test",url+"?s=test"]

        for u in urls:
            for pl in payloads:
                for inj in inject_params(u, pl):
                    r = http.get(inj["url"])
                    if r and pl in r.text:
                        self.e.add(title="Reflected XSS", severity="HIGH",
                            desc="XSS payload reflected in '" + inj["param"] + "'",
                            url=inj["url"], param=inj["param"], payload=pl,
                            evidence="Payload reflected unescaped",
                            fix="Encode output. Use CSP header.",
                            owasp="A03 - Injection", module="XSS Scanner")
                        return
                    time.sleep(0.2)

        # DOM XSS check
        r = http.get(url)
        if r:
            import re
            sinks = [r"document\.write\s*\(",r"\.innerHTML\s*=",r"eval\s*\("]
            sources = [r"location\.hash",r"location\.search",r"document\.URL"]
            fs = [s for s in sinks if re.search(s, r.text)]
            fo = [s for s in sources if re.search(s, r.text)]
            if fs and fo:
                self.e.add(title="DOM-based XSS (Potential)", severity="MEDIUM",
                    desc="DOM sinks + sources found", url=url,
                    evidence="Sinks: " + str(fs[:2]) + " Sources: " + str(fo[:2]),
                    fix="Sanitize DOM inputs.", owasp="A03 - Injection", module="XSS Scanner")
