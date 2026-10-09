from core.session import http
from core.banner import Banner
from colorama import Fore

class DirBruteScanner:
    def __init__(self, t, e):
        self.t = t; self.e = e

    def run(self):
        dirs = ["admin","login","dashboard","api","backup","config","uploads",
                "upload","images","static","assets","css","js","media","files",
                "docs","test","dev","staging","private","secret","data","db",
                "phpmyadmin","wp-admin","wp-content","cgi-bin","vendor",
                "log","logs","debug","panel","console",".git",".env",
                "robots.txt","sitemap.xml",".htaccess","server-status"]
        found = []
        for i, d in enumerate(dirs):
            Banner.progress(i+1, len(dirs), "/" + d)
            r = http.get(self.t.url + "/" + d, allow_redirects=False)
            if r and r.status_code in [200, 301, 302, 403]:
                if r.status_code == 200 and "404" in r.text.lower()[:100]:
                    continue
                found.append(("/" + d, r.status_code))
                color = Fore.RED if r.status_code == 200 else Fore.YELLOW
                Banner.result("  /" + d, "HTTP " + str(r.status_code), color)

        Banner.section("Directories: " + str(len(found)))
        for path, code in found:
            sev = "HIGH" if path in ["/.env","/.git","/backup","/config"] and code == 200 else "INFO"
            if sev == "HIGH":
                self.e.add(title="Sensitive Path: " + path, severity=sev,
                    desc="Accessible sensitive directory", url=self.t.url + path,
                    fix="Restrict access.", owasp="A01 - Broken Access Control",
                    module="Dir Bruteforce")
        Banner.section_end()
