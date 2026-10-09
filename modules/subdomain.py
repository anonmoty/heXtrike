import socket
from core.session import http
from core.banner import Banner
from colorama import Fore

class SubdomainScanner:
    def __init__(self, t, e):
        self.t = t; self.e = e

    def run(self):
        subs = ["www","mail","ftp","admin","dev","staging","api","app","blog","cdn",
                "cloud","cpanel","db","demo","docs","git","help","jenkins","login","m",
                "monitor","mysql","ns1","ns2","panel","portal","smtp","ssh","stage",
                "static","store","support","test","vpn","webmail","wiki","beta"]
        found = []
        for i, sub in enumerate(subs):
            Banner.progress(i+1, len(subs), sub + "." + self.t.domain)
            try:
                ip = socket.gethostbyname(sub + "." + self.t.domain)
                found.append(sub + "." + self.t.domain + " → " + ip)
            except: pass

        try:
            r = http.get("https://crt.sh/?q=%25." + self.t.domain + "&output=json", timeout=12)
            if r and r.status_code == 200:
                for entry in r.json():
                    for n in entry.get("name_value","").split("\n"):
                        n = n.strip().lower()
                        if n and "*" not in n:
                            found.append(n)
        except: pass

        found = list(set(found))
        Banner.section("Subdomains: " + str(len(found)))
        for s in sorted(found)[:20]:
            Banner.result("🔎", s, Fore.GREEN)
        Banner.section_end()
        if found:
            self.e.add(title="Subdomains Found: " + str(len(found)), severity="INFO",
                desc=str(len(found)) + " subdomains discovered", url=self.t.url,
                evidence=", ".join(sorted(found)[:10]),
                owasp="A05 - Security Misconfiguration", module="Subdomain Enum")
