import random, threading, time, requests
from core.config import Config
from colorama import Fore, Style

class ProxyManager:
    def __init__(self):
        self.pool = []
        self.alive = []
        self.current = None
        self.count = 0
        self.dead = set()
        self.lock = threading.Lock()
        self.on = False
        self.rotate_count = 0
        self.total_rotations = 0
        self.auto_refresh = False
        self._refresh_thread = None

    def fetch(self):
        """Fetch fresh proxies from ProxyScrape"""
        print("  " + Fore.MAGENTA + "[⬡] Fetching proxies from ProxyScrape..." + Style.RESET_ALL)
        all_p = []

        for i, url in enumerate(Config.PROXY_URLS):
            try:
                print("  " + Fore.LIGHTBLACK_EX + "  Source " + str(i+1) + "...", end="")
                r = requests.get(url, timeout=15)
                if r.status_code == 200:
                    px = [p.strip() for p in r.text.strip().split("\n")
                          if ":" in p.strip() and len(p.strip()) > 5]
                    all_p.extend(px)
                    print(Fore.GREEN + " +" + str(len(px)) + Style.RESET_ALL)
                else:
                    print(Fore.RED + " failed" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + " error" + Style.RESET_ALL)

        self.pool = list(set(all_p))
        random.shuffle(self.pool)
        print("  " + Fore.MAGENTA + "[⬡] Total pool: " +
              Fore.WHITE + str(len(self.pool)) + " proxies" + Style.RESET_ALL)

        if self.pool:
            self._check()
        else:
            self.on = False
            print("  " + Fore.YELLOW + "[!] No proxies fetched - direct mode" + Style.RESET_ALL)

    def _check(self, n=20):
        """Health check proxies"""
        print("  " + Fore.MAGENTA + "[⬡] Health checking top " + str(n) + "..." + Style.RESET_ALL)
        self.alive = []
        from core.banner import Banner

        for i, p in enumerate(self.pool[:n]):
            Banner.progress(i + 1, min(n, len(self.pool)), "Test " + p[:18])
            try:
                r = requests.get("http://httpbin.org/ip",
                                 proxies=self._f(p), timeout=5)
                if r.status_code == 200:
                    self.alive.append(p)
            except:
                pass

        print("  " + Fore.MAGENTA + "[⬡] Alive: " +
              Fore.GREEN + str(len(self.alive)) + "/" +
              str(min(n, len(self.pool))) + Style.RESET_ALL)

        if self.alive:
            self.current = random.choice(self.alive)
            self.on = True
            print("  " + Fore.GREEN + "[✓] Active proxy: " +
                  Fore.LIGHTMAGENTA_EX + self.current + Style.RESET_ALL)
            # Start auto-refresh thread
            self._start_auto_refresh()
        else:
            self.on = False
            print("  " + Fore.YELLOW + "[!] No working proxies - direct mode" + Style.RESET_ALL)

    def _f(self, p):
        """Format proxy string"""
        p = p.strip()
        if not p.startswith(("http://", "https://", "socks4://", "socks5://")):
            p = "http://" + p
        return {"http": p, "https": p}

    def get(self):
        """Get current proxy with auto-rotation"""
        if not self.on or not self.alive:
            return None
        with self.lock:
            self.count += 1
            self.rotate_count += 1

            # Auto-rotate after N requests
            if self.rotate_count >= Config.PROXY_ROTATE:
                self._rotate()
                self.rotate_count = 0

            if self.current:
                return self._f(self.current)
        return None

    def _rotate(self):
        """Rotate to a new proxy"""
        if len(self.alive) < 2:
            return

        self.total_rotations += 1
        avail = [p for p in self.alive
                 if p != self.current and p not in self.dead]

        if avail:
            old = self.current
            self.current = random.choice(avail)
            print("  " + Fore.MAGENTA + "[⬡] 🔄 Rotated: " +
                  Fore.LIGHTBLACK_EX + (old or "none")[:18] +
                  Fore.MAGENTA + " → " +
                  Fore.LIGHTMAGENTA_EX + self.current[:18] + Style.RESET_ALL)
        else:
            # All proxies used, reset dead list
            self.dead.clear()
            self.current = random.choice(self.alive)
            print("  " + Fore.MAGENTA + "[⬡] 🔄 Pool reset, rotated → " +
                  Fore.LIGHTMAGENTA_EX + self.current[:18] + Style.RESET_ALL)

    def kill(self):
        """Mark current proxy as dead and rotate"""
        if self.current:
            self.dead.add(self.current)
            if self.current in self.alive:
                self.alive.remove(self.current)
            print("  " + Fore.RED + "[✗] Dead proxy removed: " +
                  self.current[:20] + Style.RESET_ALL)
            self._rotate()

            # If too many dead, re-fetch
            if len(self.alive) < 3 and self.pool:
                print("  " + Fore.YELLOW + "[!] Low proxy count, refreshing..." + Style.RESET_ALL)
                self._check(15)

    def _start_auto_refresh(self):
        """Background thread to refresh proxies every 5 minutes"""
        if self._refresh_thread and self._refresh_thread.is_alive():
            return
        self.auto_refresh = True

        def _refresh_loop():
            while self.auto_refresh:
                time.sleep(300)  # 5 minutes
                if not self.on:
                    break
                print("\n  " + Fore.MAGENTA + "[⬡] Auto-refreshing proxy pool..." + Style.RESET_ALL)
                old_count = len(self.alive)
                self.fetch()
                new_count = len(self.alive)
                if new_count > old_count:
                    print("  " + Fore.GREEN + "[✓] Pool refreshed: " +
                          str(old_count) + " → " + str(new_count) + Style.RESET_ALL)

        self._refresh_thread = threading.Thread(target=_refresh_loop, daemon=True)
        self._refresh_thread.start()

    def status(self):
        """Display proxy status"""
        print()
        print("  " + Fore.MAGENTA + "╔" + "═" * 50 + "╗")
        print("  " + Fore.MAGENTA + "║" + Fore.WHITE + Style.BRIGHT +
              "  🔌 PROXY MANAGER STATUS" + " " * 24 + Fore.MAGENTA + "║")
        print("  " + Fore.MAGENTA + "╠" + "═" * 50 + "╣")

        status_items = [
            ("Status", "🟢 ACTIVE" if self.on else "🔴 OFF"),
            ("Pool Size", str(len(self.pool))),
            ("Alive", Fore.GREEN + str(len(self.alive)) + Style.RESET_ALL),
            ("Dead", Fore.RED + str(len(self.dead)) + Style.RESET_ALL),
            ("Current", str(self.current or "None")[:35]),
            ("Requests", str(self.count)),
            ("Rotations", str(self.total_rotations)),
            ("Auto-Refresh", "🟢 Every 5min" if self.auto_refresh else "🔴 Off"),
            ("Rotate After", str(Config.PROXY_ROTATE) + " requests"),
        ]

        for k, v in status_items:
            print("  " + Fore.MAGENTA + "║" + Fore.WHITE + "  " +
                  k.ljust(14) + ": " + str(v)[:31].ljust(31) + Fore.MAGENTA + "  ║")

        print("  " + Fore.MAGENTA + "╚" + "═" * 50 + "╝" + Style.RESET_ALL)
        print()

    def stop(self):
        """Stop auto-refresh"""
        self.auto_refresh = False


proxy = ProxyManager()
