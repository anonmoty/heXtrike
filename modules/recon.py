import socket, re
from core.session import http
from core.banner import Banner
from colorama import Fore

class ReconScanner:
    def __init__(self, t, e):
        self.t = t; self.e = e

    def run(self):
        Banner.section("Target Reconnaissance")
        Banner.result("URL", self.t.url)
        Banner.result("IP", self.t.ip or "N/A")
        Banner.result("Server", self.t.server or "N/A")

        r = http.get(self.t.url)
        if r:
            Banner.result("Status", str(r.status_code))
            Banner.result("Size", str(len(r.text)) + " bytes")
            Banner.result("Time", str(round(r.elapsed.total_seconds(), 3)) + "s")

            # Tech detect
            body = r.text.lower()
            techs = []
            for kw, name in {"wp-content":"WordPress","joomla":"Joomla","drupal":"Drupal",
                "laravel":"Laravel","django":"Django","react":"React","angular":"Angular",
                "vue":"Vue.js","next":"Next.js","bootstrap":"Bootstrap","jquery":"jQuery",
                "graphql":"GraphQL","express":"Express","flask":"Flask"}.items():
                if kw in body: techs.append(name)
            for h in ["X-Powered-By","Server"]:
                if h in r.headers: techs.append(r.headers[h])
            techs = list(set(techs))
            if techs:
                Banner.result("Tech", ", ".join(techs[:5]), Fore.CYAN)
                self.e.add(title="Technologies", severity="INFO",
                    desc=", ".join(techs), url=self.t.url,
                    owasp="A06 - Vulnerable Components", module="Recon")

            # Emails
            emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r.text))
            emails = {e for e in emails if "example.com" not in e and "sentry" not in e}
            if emails:
                Banner.result("Emails", ", ".join(list(emails)[:3]), Fore.LIGHTGREEN_EX)

        # Ports
        ports = {22:"SSH",80:"HTTP",443:"HTTPS",3306:"MySQL",5432:"PostgreSQL",
                 6379:"Redis",8080:"HTTP-Alt",27017:"MongoDB"}
        open_p = []
        for port, svc in ports.items():
            try:
                s = socket.socket(); s.settimeout(1.5)
                if s.connect_ex((self.t.ip, port)) == 0:
                    open_p.append(str(port) + "/" + svc)
                s.close()
            except: pass
        if open_p:
            Banner.result("Open Ports", ", ".join(open_p), Fore.YELLOW)

        Banner.section_end()
