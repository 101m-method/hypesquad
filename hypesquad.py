import os
import sys
import subprocess
import requests

if os.name == "nt":
    os.system("")

BANNER = r"""
   ╔══════════════════════════════════════════════════╗
   ║                                                  ║
   ║        ██╗  ██╗██╗   ██╗██████╗ ███████╗         ║
   ║        ██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝         ║
   ║        ███████║ ╚████╔╝ ██████╔╝█████╗           ║
   ║        ██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══╝           ║
   ║        ██║  ██║   ██║   ██║     ███████╗         ║
   ║        ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝         ║
   ║                                                  ║
   ║              H Y P E S Q U A D                   ║
   ║                                                  ║
   ║                  By & Flamezz                    ║
   ║          discord.gg/101m                         ║
   ╚══════════════════════════════════════════════════╝
"""

Houses = {
    "1": ("Bravery", 1, "Mor"),
    "2": ("Brilliance", 2, "Turuncu"),
    "3": ("Balance", 3, "Yesil"),
    "4": ("Rozeti Kaldir", None, ""),
}

IS_TERMUX = "com.termux" in os.environ.get("PREFIX", "") or os.path.exists("/data/data/com.termux")
IS_WINDOWS = os.name == "nt"

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"


def clear():
    os.system("cls" if IS_WINDOWS else "clear")


def print_banner():
    print(f"{CYAN}{BANNER}{RESET}")


def _headers(token: str) -> dict:
    return {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }


def _handle_response(resp) -> str:
    """'ok' | 'auth' | 'rate' | 'other' döner."""
    if resp.status_code in (200, 204):
        return "ok"
    if resp.status_code == 401:
        return "auth"
    if resp.status_code == 429:
        return "rate"
    return "other"


def apply_hypesquad(token: str, house_id: int):
    url = "https://discord.com/api/v9/hypesquad/online"
    try:
        resp = requests.post(url, json={"house_id": house_id}, headers=_headers(token), timeout=15)
        return _handle_response(resp), resp.status_code
    except requests.exceptions.RequestException as e:
        return ("error", str(e))


def remove_hypesquad(token: str):
    url = "https://discord.com/api/v9/hypesquad/online"
    try:
        resp = requests.delete(url, headers=_headers(token), timeout=15)
        return _handle_response(resp), resp.status_code
    except requests.exceptions.RequestException as e:
        return ("error", str(e))


def token_al():
    """Token'ı görünür şekilde al."""
    while True:
        print(f"{CYAN}token > {RESET}", end="", flush=True)
        try:
            t = input().strip()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)
        if t:
            return t
        print(f"{RED}[!] Token bos olamaz, tekrar gir.{RESET}\n")


def hanedan_menu():
    print(f"\n{BOLD}{WHITE}  Hanedan Sec:{RESET}\n")
    print(f"  {MAGENTA}[1]{RESET} {BOLD}Bravery{RESET}    {DIM}(Mor){RESET}")
    print(f"  {YELLOW}[2]{RESET} {BOLD}Brilliance{RESET} {DIM}(Turuncu){RESET}")
    print(f"  {GREEN}[3]{RESET} {BOLD}Balance{RESET}    {DIM}(Yesil){RESET}")
    print(f"  {RED}[4]{RESET} {BOLD}Rozeti Kaldir{RESET}")
    print(f"  {DIM}[q]{RESET} {BOLD}Cikis{RESET}")
    print()


def islem_yap(token, secim):
    house_name, house_id, _ = Houses[secim]

    if secim == "4":
        print(f"\n{YELLOW}[*] {house_name} islemi uygulaniyor...{RESET}")
        durum, kod = remove_hypesquad(token)
        if durum == "ok":
            print(f"{GREEN}[+] HypeSquad rozeti kaldirildi.{RESET}")
            print(f"{DIM}[i] Rozet profilinde hala gozukuyorsa Discord'u kapatip yeniden ac.{RESET}")
            return True
        if durum == "auth":
            print(f"{RED}[!] Token gecersiz veya suresi dolmus.{RESET}")
            print(f"{RED}[!] Kaldirma basarisiz oldu.{RESET}")
            return False
        if durum == "rate":
            print(f"{YELLOW}[!] Rate limit. Biraz bekleyip tekrar dene.{RESET}")
            return True
        if durum == "error":
            print(f"{RED}[!] Baglanti hatasi: {kod}{RESET}")
            return True
        print(f"{RED}[!] Beklenmeyen durum kodu: {kod}{RESET}")
        return True

    print(f"\n{YELLOW}[*] {house_name} hanedani uygulaniyor...{RESET}")
    durum, kod = apply_hypesquad(token, house_id)
    if durum == "ok":
        print(f"{GREEN}[+] {house_name} hanedani uygulandi.{RESET}")
        print(f"{DIM}[i] Rozet profilinde gozukmuyorsa Discord'u kapatip yeniden ac.{RESET}")
        return True
    if durum == "auth":
        print(f"{RED}[!] Token gecersiz veya suresi dolmus.{RESET}")
        print(f"{RED}[!] Uygulama basarisiz oldu.{RESET}")
        return False
    if durum == "rate":
        print(f"{YELLOW}[!] Rate limit. Biraz bekleyip tekrar dene.{RESET}")
        return True
    if durum == "error":
        print(f"{RED}[!] Baglanti hatasi: {kod}{RESET}")
        return True
    print(f"{RED}[!] Beklenmeyen durum kodu: {kod}{RESET}")
    return True


def main():
    clear()
    print_banner()
    print(f"{DIM}   discord.gg/101m  |  By & Flamezz{RESET}\n")

    token = token_al()

    while True:
        clear()
        print_banner()
        print(f"{DIM}   discord.gg/101m  |  By & Flamezz{RESET}\n")
        print(f"{DIM}   token: {token[:6]}...{token[-4:]}{RESET}")

        hanedan_menu()
        print(f"{CYAN}secim > {RESET}", end="", flush=True)
        try:
            secim = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if secim == "q":
            break
        if secim not in Houses:
            print(f"{RED}[!] Gecersiz secim.{RESET}")
            continue

        gecerli = islem_yap(token, secim)

        if not gecerli:
            # token geçersiz → baştan token al
            print()
            token = token_al()

        print(f"\n{DIM}devam etmek icin Enter... (q + Enter = cikis){RESET}", end="", flush=True)
        try:
            devam = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if devam == "q":
            break

    clear()
    print(f"{DIM}By & Flamezz  |  discord.gg/101m{RESET}")


if __name__ == "__main__":
    main()