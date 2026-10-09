import sys, time, os, random, shutil
from colorama import Fore, Back, Style, init
init(autoreset=True)

class Banner:
    @staticmethod
    def _w():
        try: return shutil.get_terminal_size().columns
        except: return 80

    @classmethod
    def _matrix_rain(cls, dur=1.2):
        w = min(cls._w(), 90)
        hex_chars = "0123456789ABCDEFアイウエオカキクケコ"
        end = time.time() + dur
        while time.time() < end:
            line = ""
            for _ in range(w):
                r = random.random()
                if r < 0.06:
                    line += Fore.LIGHTMAGENTA_EX + Style.BRIGHT + random.choice(hex_chars)
                elif r < 0.10:
                    line += Fore.MAGENTA + random.choice("0123456789ABCDEF")
                elif r < 0.13:
                    line += Fore.LIGHTBLACK_EX + random.choice("01")
                else:
                    line += " "
            print(line + Style.RESET_ALL)
            time.sleep(0.02)

    @classmethod
    def _glitch(cls, text, n=3):
        g = "▓▒░█▄▀■□╳╬╫╪⬡⬢"
        colors = [Fore.RED, Fore.CYAN, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.YELLOW]
        for _ in range(n):
            out = ""
            for ch in text:
                if ch != " " and random.random() < 0.2:
                    out += random.choice(colors) + random.choice(g)
                else:
                    out += Fore.LIGHTMAGENTA_EX + ch
            sys.stdout.write("\r" + out)
            sys.stdout.flush()
            time.sleep(0.04)
        sys.stdout.write("\r" + text + Style.RESET_ALL + "\n")

    @classmethod
    def _hex_flicker(cls, text, dur=0.8):
        hex_chars = "0123456789ABCDEF"
        end = time.time() + dur
        while time.time() < end:
            out = ""
            for ch in text:
                if ch != " " and random.random() < 0.3:
                    out += Fore.MAGENTA + random.choice(hex_chars)
                else:
                    out += Fore.LIGHTMAGENTA_EX + ch
            sys.stdout.write("\r" + out)
            sys.stdout.flush()
            time.sleep(0.03)
        sys.stdout.write("\r" + Fore.LIGHTMAGENTA_EX + text + Style.RESET_ALL + "\n")

    @classmethod
    def _typing(cls, text, speed=0.02, color=Fore.MAGENTA):
        for ch in text:
            sys.stdout.write(color + ch)
            sys.stdout.flush()
            time.sleep(speed + random.uniform(0, 0.015))
        print(Style.RESET_ALL)

    @classmethod
    def _binary_reveal(cls, text):
        result = list(" " * len(text))
        indices = list(range(len(text)))
        random.shuffle(indices)
        steps = max(1, len(text) // 8)
        hex_chars = "0123456789ABCDEF"
        for batch in range(0, len(indices), steps):
            for idx in indices[batch:batch + steps]:
                result[idx] = text[idx]
            d = ""
            for ch in result:
                if ch == " ":
                    d += Fore.MAGENTA + random.choice(hex_chars)
                else:
                    d += Fore.LIGHTMAGENTA_EX + Style.BRIGHT + ch
            sys.stdout.write("\r  " + d + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.05)
        print()

    @classmethod
    def show(cls):
        os.system("clear" if os.name == "posix" else "cls")

        # Phase 1: Matrix rain with hex chars
        cls._matrix_rain(1.0)
        os.system("clear" if os.name == "posix" else "cls")

        # Phase 2: Loading bar
        for i in range(25):
            sp = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"[i % 10]
            pct = i * 4
            bar_w = 20
            filled = int(bar_w * pct / 100)
            bar = "█" * filled + "░" * (bar_w - filled)
            sys.stdout.write(
                "\r  " + Fore.MAGENTA + sp + " " +
                Fore.LIGHTMAGENTA_EX + "[" + bar + "] " +
                Fore.WHITE + str(pct) + "% " +
                Fore.LIGHTBLACK_EX + "Arming modules..."
            )
            sys.stdout.flush()
            time.sleep(0.04)
        print("\r  " + Fore.GREEN + "✓ All modules loaded!                    ")
        time.sleep(0.3)

        # Phase 3: Hex logo with glitch
        logo = [
            "",
            Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
            "    ██╗  ██╗███████╗██╗  ██╗███████╗████████╗██████╗ ██╗ ██████╗███████╗",
            Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
            "    ██║  ██║██╔════╝╚██╗██╔╝██╔════╝╚══██╔══╝██╔══██╗██║██╔════╝██╔════╝",
            Fore.MAGENTA + Style.BRIGHT +
            "    ███████║█████╗   ╚███╔╝ ███████╗   ██║   ██████╔╝██║██║     █████╗  ",
            Fore.MAGENTA + Style.BRIGHT +
            "    ██╔══██║██╔══╝   ██╔██╗ ╚════██║   ██║   ██╔══██╗██║██║     ██╔══╝  ",
            Fore.MAGENTA +
            "    ██║  ██║███████╗██╔╝ ██╗███████║   ██║   ██║  ██║██║╚██████╗███████╗",
            Fore.MAGENTA +
            "    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝ ╚═════╝╚══════╝",
            "",
        ]
        for line in logo:
            cls._glitch(line, n=3)
            time.sleep(0.01)

        # Phase 4: Hex symbol animation
        hex_frames = [
            ["      ⬡       ", "    ⬡   ⬡     ", "  ⬡   H   ⬡   ",
             "    ⬡   ⬡     ", "      ⬡       "],
            ["      ⬢       ", "    ⬢   ⬢     ", "  ⬢   E   ⬢   ",
             "    ⬢   ⬢     ", "      ⬢       "],
            ["      ⬡       ", "    ⬡   ⬡     ", "  ⬡   X   ⬡   ",
             "    ⬡   ⬡     ", "      ⬡       "],
        ]
        for frame in hex_frames:
            for line in frame:
                print("  " + Fore.LIGHTMAGENTA_EX + line + Style.RESET_ALL)
            time.sleep(0.15)
            if frame != hex_frames[-1]:
                sys.stdout.write("\033[5A")
                sys.stdout.flush()

        # Final hex
        final_hex = [
            Fore.LIGHTMAGENTA_EX + "      ⬡       ",
            Fore.LIGHTMAGENTA_EX + "    ⬡   ⬡     ",
            Fore.MAGENTA + Style.BRIGHT + "  ⬡  HEX  ⬡   ",
            Fore.LIGHTMAGENTA_EX + "    ⬡   ⬡     ",
            Fore.LIGHTMAGENTA_EX + "      ⬡       ",
        ]
        for line in final_hex:
            print("  " + line + Style.RESET_ALL)
            time.sleep(0.03)

        print()

        # Phase 5: Info panel
        info = [
            Fore.MAGENTA + "    ╔" + "═" * 66 + "╗",
            Fore.MAGENTA + "    ║" + Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
            " ⚡ HexStrike v1.0 " + Fore.LIGHTBLACK_EX + "│" +
            Fore.LIGHTYELLOW_EX + " Ultimate Bug Hunting Framework      " + Fore.MAGENTA + "   ║",
            Fore.MAGENTA + "    ╠" + "═" * 66 + "╣",
            Fore.MAGENTA + "    ║" + Fore.WHITE +
            " 🎯 Modules : SQLi|XSS|LFI|SSRF|CORS|Headers|Recon  " + Fore.MAGENTA + "     ║",
            Fore.MAGENTA + "    ║" + Fore.WHITE +
            " 🔌 Proxy   : ProxyScrape Auto-Rotation             " + Fore.MAGENTA + "     ║",
            Fore.MAGENTA + "    ║" + Fore.WHITE +
            " 📊 Reports : HTML + JSON Auto-Save                 " + Fore.MAGENTA + "     ║",
            Fore.MAGENTA + "    ║" + Fore.WHITE +
            " 🛡️  WAF     : Bypass + Obfuscation Engine           " + Fore.MAGENTA + "     ║",
            Fore.MAGENTA + "    ║" + Fore.WHITE +
            " 💀 Status  : " + Fore.RED + "ARMED & HUNTING 🔴" + Fore.WHITE +
            "                    " + Fore.MAGENTA + "     ║",
            Fore.MAGENTA + "    ╚" + "═" * 66 + "╝",
        ]
        for line in info:
            print(line)
            time.sleep(0.03)
        print(Style.RESET_ALL)

        # Phase 6: Binary reveal
        cls._binary_reveal("[ HEXSTRIKE v1.0 - BUG HUNTING FRAMEWORK ACTIVE ]")
        print()

    @classmethod
    def menu(cls):
        M = Fore.MAGENTA; W = Fore.WHITE; LM = Fore.LIGHTMAGENTA_EX
        LY = Fore.LIGHTYELLOW_EX; LG = Fore.LIGHTGREEN_EX
        LC = Fore.LIGHTCYAN_EX; LR = Fore.LIGHTRED_EX; S = Style.RESET_ALL

        lines = [
            "",
            M + "  ╔" + "═" * 66 + "╗",
            M + "  ║" + LM + Style.BRIGHT +
            "              ⚡ HEXSTRIKE ARSENAL ⚡                        " + M + "   ║",
            M + "  ╠" + "═" * 66 + "╣",
            M + "  ║ " + LY + "━━ INJECTION ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ " + M + "   ║",
            M + "  ║  " + LM + "[01]" + W + " 💉 SQLi Scanner        " + LM + "[02]" + W +
            " 🎭 XSS Scanner        " + M + "    ║",
            M + "  ║  " + LM + "[03]" + W + " 📁 LFI Scanner         " + LM + "[04]" + W +
            " 🌐 SSRF Scanner       " + M + "    ║",
            M + "  ║ " + LY + "━━ CONFIGURATION ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ " + M + "   ║",
            M + "  ║  " + LM + "[05]" + W + " 🛡️  Headers Check      " + LM + "[06]" + W +
            " 🔄 CORS Misconfig     " + M + "    ║",
            M + "  ║  " + LM + "[07]" + W + " ⚙️  Misconfig Scan     " + LM + "[08]" + W +
            " 🔓 Auth Bypass        " + M + "    ║",
            M + "  ║ " + LY + "━━ RECON ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ " + M + "   ║",
            M + "  ║  " + LM + "[09]" + W + " 🔍 Full Recon          " + LM + "[10]" + W +
            " 📂 Dir Bruteforce     " + M + "    ║",
            M + "  ╠" + "═" * 66 + "╣",
            M + "  ║  " + LY + "[00]" + LG + " ⚡ RUN ALL             " + LY + "[77]" + LC +
            " 🔌 Proxy Settings    " + M + "    ║",
            M + "  ║  " + LY + "[88]" + LC + " 📊 View Report         " + LY + "[99]" + LR +
            " 🚪 Exit              " + M + "    ║",
            M + "  ╚" + "═" * 66 + "╝",
            S,
        ]
        for line in lines:
            print(line)

    @classmethod
    def header(cls, name):
        w = 58
        print("\n  " + Fore.MAGENTA + "▓" * w)
        print("  " + Fore.MAGENTA + "▓" + Fore.LIGHTMAGENTA_EX + Style.BRIGHT +
              "  ⚡ " + name.center(w - 8) + " " + Fore.MAGENTA + "▓")
        print("  " + Fore.MAGENTA + "▓" * w + Style.RESET_ALL)

    @classmethod
    def result(cls, key, val, color=Fore.WHITE):
        print("  " + Fore.MAGENTA + "│ " + Fore.LIGHTYELLOW_EX +
              key.ljust(20) + Fore.WHITE + ": " + color + str(val)[:55] + Style.RESET_ALL)

    @classmethod
    def vuln(cls, sev, msg):
        icons = {"CRITICAL":"🔴","HIGH":"🟠","MEDIUM":"🟡","LOW":"🟢","INFO":"🔵"}
        colors = {"CRITICAL":Fore.RED+Style.BRIGHT,"HIGH":Fore.LIGHTRED_EX,
                  "MEDIUM":Fore.YELLOW,"LOW":Fore.GREEN,"INFO":Fore.CYAN}
        print("  " + Fore.MAGENTA + "│ " + icons.get(sev,"⚪") + " " +
              colors.get(sev,Fore.WHITE) + "[" + sev + "] " +
              Fore.WHITE + msg[:50] + Style.RESET_ALL)

    @classmethod
    def section(cls, title):
        print("\n  " + Fore.LIGHTYELLOW_EX + "┌─[ " + title + " ]" + "─" * 40 + Style.RESET_ALL)

    @classmethod
    def section_end(cls):
        print("  " + Fore.LIGHTYELLOW_EX + "└" + "─" * 55 + Style.RESET_ALL)

    @classmethod
    def progress(cls, cur, total, desc=""):
        if total == 0: return
        p = cur / total
        w = 28
        bar = "█" * int(w*p) + "░" * (w - int(w*p))
        sys.stdout.write("\r  " + Fore.MAGENTA + "[" + Fore.LIGHTMAGENTA_EX +
                         bar + Fore.MAGENTA + "] " + Fore.WHITE + str(int(p*100)) +
                         "% " + Fore.LIGHTBLACK_EX + desc[:30] + Style.RESET_ALL)
        sys.stdout.flush()
        if cur >= total: print()

    @classmethod
    def scan_line(cls, name, status, icon="🔍"):
        hx = ''.join(random.choices("0123456789ABCDEF", k=8))
        print("  " + Fore.LIGHTBLACK_EX + "[" + time.strftime("%H:%M:%S") + "] " +
              icon + " " + Fore.WHITE + name.ljust(20) +
              Fore.LIGHTBLACK_EX + " 0x" + hx + " " + status + Style.RESET_ALL)

    @classmethod
    def stat_box(cls, stats):
        w = 55
        print("\n  " + Fore.LIGHTGREEN_EX + "╔" + "═" * w + "╗")
        print("  " + Fore.LIGHTGREEN_EX + "║" + Fore.WHITE + Style.BRIGHT +
              "  📊 SCAN SUMMARY".ljust(w) + Fore.LIGHTGREEN_EX + "║")
        print("  " + Fore.LIGHTGREEN_EX + "╠" + "═" * w + "╣")
        for k, v in stats.items():
            print("  " + Fore.LIGHTGREEN_EX + "║  " + Fore.WHITE +
                  k.ljust(22) + ": " + Fore.LIGHTYELLOW_EX +
                  str(v).ljust(w - 27) + Fore.LIGHTGREEN_EX + "║")
        print("  " + Fore.LIGHTGREEN_EX + "╚" + "═" * w + "╝" + Style.RESET_ALL)
