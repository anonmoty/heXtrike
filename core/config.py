import os
from datetime import datetime

class Config:
    APP = "HexStrike"
    VERSION = "1.0.0"
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORTS = os.path.join(ROOT, "output", "reports")
    TIMEOUT = 12
    DELAY = 0.3
    PROXY_ROTATE = 8
    PROXY_URLS = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=5000&country=all",
    ]
    UAS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 Safari/17.4",
    ]

    @classmethod
    def init(cls):
        os.makedirs(cls.REPORTS, exist_ok=True)

    @classmethod
    def report_path(cls, name, ext="html"):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe = name.replace("https://","").replace("http://","").replace("/","_")[:30]
        return os.path.join(cls.REPORTS, "hex_" + safe + "_" + ts + "." + ext)
