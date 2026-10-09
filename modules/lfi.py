import time
from core.engine import inject_params
from core.session import http
from core.banner import Banner

class LFIScanner:
    def __init__(self, t, e):
        self.t = t; self.e = e

    def run(self):
        payloads = ["../../../etc/passwd","....//....//....//etc/passwd",
                    "/etc/passwd","..%2f..%2f..%2fetc%2fpasswd"]
        indicators = ["root:","/bin/bash","/bin/sh"]
        url = self.t.url
        urls = [url] if "?" in url else [url+"?file=test",url+"?page=test",url+"?path=test"]

        for u in urls:
            for pl in payloads:
                for inj in inject_params(u, pl):
                    r = http.get(inj["url"])
                    if r:
                        for ind in indicators:
                            if ind in r.text:
                                self.e.add(title="Local File Inclusion", severity="CRITICAL",
                                    desc="LFI in '" + inj["param"] + "'",
                                    url=inj["url"], param=inj["param"], payload=pl,
                                    evidence=ind,
                                    fix="Whitelist file paths. No user input in includes.",
                                    owasp="A01 - Broken Access Control", module="LFI Scanner")
                                return
                    time.sleep(0.2)
