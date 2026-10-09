import time, socket, re
from datetime import datetime
from urllib.parse import urlparse, urljoin
from colorama import Fore, Style
from core.session import http
from core.banner import Banner
from bs4 import BeautifulSoup

class Finding:
    def __init__(self, title, severity, desc, url, param="", payload="", evidence="", fix="", owasp="", module=""):
        self.title = title; self.severity = severity; self.desc = desc
        self.url = url; self.param = param; self.payload = payload
        self.evidence = evidence; self.fix = fix; self.owasp = owasp
        self.module = module; self.time = datetime.now().strftime("%H:%M:%S")
    def to_dict(self):
        return {k: getattr(self, k) for k in ["title","severity","desc","url",
            "param","payload","evidence","fix","owasp","module","time"]}

class Target:
    def __init__(self, url):
        self.url = url.strip().rstrip("/")
        if not self.url.startswith(("http://","https://")):
            self.url = "https://" + self.url
        self.p = urlparse(self.url)
        self.host = self.p.hostname
        self.domain = self.host.replace("www.","") if self.host else ""
        self.ip = None; self.alive = False; self.server = None

    def validate(self):
        try:
            self.ip = socket.gethostbyname(self.host)
            Banner.scan_line("DNS", Fore.GREEN + "✓ " + self.ip, "🌐")
            r = http.get(self.url, timeout=15)
            if not r:
                Banner.scan_line("HTTP", Fore.RED + "✗ No response", "❌")
                return False
            self.alive = True
            self.server = r.headers.get("Server", "Unknown")
            Banner.scan_line("HTTP", Fore.GREEN + "✓ " + str(r.status_code) + " | " + self.server, "📡")
            return True
        except Exception as e:
            Banner.scan_line("Target", Fore.RED + "✗ " + str(e)[:40], "❌")
            return False

class Engine:
    def __init__(self, url):
        self.target = Target(url)
        self.findings = []
        self.start = None; self.end = None; self.modules = []

    def validate(self):
        return self.target.validate()

    def add(self, **kw):
        f = Finding(**kw)
        self.findings.append(f)
        Banner.vuln(f.severity, f.title + " | " + f.url[:40])

    def run_module(self, mod_class, name):
        Banner.header(name)
        t = time.time()
        try:
            m = mod_class(self.target, self)
            m.run()
            e = round(time.time() - t, 2)
            c = len([f for f in self.findings if f.module == name])
            print("  " + Fore.GREEN + "[✓] " + name + " (" + str(e) + "s) - " +
                  str(c) + " findings" + Style.RESET_ALL)
            self.modules.append({"name": name, "findings": c, "time": e})
        except Exception as ex:
            print("  " + Fore.RED + "[✗] " + name + ": " + str(ex) + Style.RESET_ALL)

    def timer_start(self): self.start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def timer_stop(self): self.end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def summary(self):
        return {
            "target": {"url": self.target.url, "ip": self.target.ip, "server": self.target.server},
            "time": {"start": self.start, "end": self.end},
            "total": len(self.findings),
            "severity": {s: len([f for f in self.findings if f.severity == s])
                         for s in ["CRITICAL","HIGH","MEDIUM","LOW","INFO"]},
            "modules": self.modules,
            "findings": [f.to_dict() for f in self.findings],
        }

def inject_params(url, payload):
    from urllib.parse import parse_qs, urlencode, urlunparse
    p = urlparse(url)
    params = parse_qs(p.query, keep_blank_values=True)
    res = []
    for k in params:
        m = params.copy(); m[k] = [payload]
        nq = urlencode(m, doseq=True)
        res.append({"url": urlunparse((p.scheme,p.netloc,p.path,p.params,nq,p.fragment)),
                     "param": k, "payload": payload})
    return res

def get_links(html, base):
    soup = BeautifulSoup(html, "html.parser")
    h = urlparse(base).hostname
    return list(set(urljoin(base, a["href"]) for a in soup.find_all("a", href=True)
                    if urlparse(urljoin(base, a["href"])).hostname == h))

def get_forms(html, base):
    soup = BeautifulSoup(html, "html.parser")
    fs = []
    for f in soup.find_all("form"):
        fd = {"action": urljoin(base, f.get("action","")),
              "method": f.get("method","GET").upper(), "inputs": []}
        for i in f.find_all(["input","textarea","select"]):
            n = i.get("name","")
            if n: fd["inputs"].append({"name":n,"type":i.get("type","text"),"value":i.get("value","")})
        if fd["inputs"]: fs.append(fd)
    return fs
