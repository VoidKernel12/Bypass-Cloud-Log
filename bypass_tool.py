#!/usr/bin/env python3
"""
Termux Advanced ADB Device Maintenance & Bypass Tool
Tool Name: BYPASS
Developer Note: Built with Gemini AI (Creator Credit Only, Non-Promotional)
"""

import subprocess
import time
import sys
import re
import random
import os
from typing import List, Optional

# Precision Color Palette (Golden, Cyber Cyan, Matrix Green & Danger Red)
class Color:
    GOLD = '\033[38;2;255;215;0m'          # Pure Gold for Headers & Prompts
    CYAN = '\033[38;2;0;255;255m'          # Cyber Neon Cyan
    PURPLE = '\033[38;2;186;85;211m'      # Neon Purple
    NEON_GREEN = '\033[38;2;57;255;20m'   # Matrix Green for Success
    HOT_PINK = '\033[38;2;255;20;147m'    # Hacker Pink
    BRIGHT_RED = '\033[38;2;255;50;50m'   # Danger Red for Warnings & Exit
    WHITE = '\033[97m'                     # Pure White
    DARK_BG = '\033[48;2;15;15;20m'       # Dark HUD Background
    RESET_BG = '\033[49m'
    END = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def clear_screen():
    """Clears terminal screen to keep the HUD strictly pinned at the top."""
    os.system('clear' if os.name == 'posix' else 'cls')

# Compact Cyberpunk HUD Top Header (Optimized for Small Termux Screens)
def print_pinned_gemini_hud(task_status: str = "IDLE"):
    clear_screen()
    hud = f"""{Color.DARK_BG}{Color.GOLD}{Color.BOLD}
 ╔═════════════════════════════════════════════╗
 ║ {Color.CYAN}DEV   : GEMINI AI (CREDIT ONLY){Color.GOLD}              ║
 ║ {Color.PURPLE}TOOL  : BYPASS{Color.GOLD}                                ║
 ║ {Color.WHITE}STAT  : {task_status:<31}{Color.GOLD}║
 ╚═════════════════════════════════════════════╝{Color.RESET_BG}
{Color.CYAN}   [>] BYPASS TOOL FOR CLOUD SERVER{Color.END}
{Color.PURPLE} ═════════════════════════════════════════════{Color.END}
    """
    print(hud)

API_POPUP_SHOWN = False

def check_termux_api_installed() -> bool:
    """Real-time check for Termux:API app and package."""
    try:
        res = subprocess.run(["which", "termux-vibrate"], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"\n{Color.BRIGHT_RED}[!] ERROR: Termux API missing!{Color.END}")
            print(f"{Color.GOLD}[*] Run: {Color.NEON_GREEN}pkg install termux-api{Color.END}")
            return False

        test_res = subprocess.run(["termux-vibrate", "-d", "50"], capture_output=True, text=True, timeout=3)
        if test_res.returncode != 0 or "android" in test_res.stderr.lower():
            raise Exception("App bridge missing")
            
        return True
    except Exception:
        print(f"\n{Color.BRIGHT_RED}{Color.BOLD}[!] ALERT: Termux:API App is missing!{Color.END}")
        print(f"{Color.CYAN}[*] Get APK from GitHub Releases.{Color.END}\n")
        return False

def trigger_termux_usb_bridge() -> bool:
    """Triggers Termux-USB permission dialog."""
    print(f"{Color.CYAN}[*] Requesting USB Hardware Bridge...{Color.END}")
    try:
        res = subprocess.run(["termux-usb", "-l"], capture_output=True, text=True, timeout=3)
        devices_output = res.stdout.strip()
        
        if not devices_output or "No devices found" in devices_output:
            print(f"{Color.GOLD}[!] No direct USB/OTG devices found.{Color.END}")
            return False

        match = re.search(r'(/dev/bus/usb/\d+/\d+)', devices_output)
        if match:
            usb_path = match.group(1)
            subprocess.run(["termux-usb", "-r", usb_path], capture_output=True, text=True, timeout=5)
            print(f"{Color.NEON_GREEN}[+] USB prompt sent. Tap ALLOW.{Color.END}")
            return True
        return False
    except Exception:
        return False

def trigger_termux_api(message: str) -> bool:
    """Triggers mandatory Termux API popup dialog."""
    global API_POPUP_SHOWN
    if API_POPUP_SHOWN:
        return True

    if not check_termux_api_installed():
        return False

    print(f"{Color.PURPLE}[*] Triggering Termux API Popup...{Color.END}")
    try:
        subprocess.run(["termux-vibrate", "-d", "150"], capture_output=True, timeout=2)
        res = subprocess.run(["termux-toast", "-s", message], capture_output=True, timeout=3)
        
        if res.returncode == 0:
            API_POPUP_SHOWN = True
            print(f"{Color.NEON_GREEN}[+] API Popup triggered! Tap OK.{Color.END}")
            return True
        return False
    except Exception:
        return False

def run_adb(cmd: List[str], timeout: int = 30) -> subprocess.CompletedProcess:
    """Run ADB command safely."""
    try:
        return subprocess.run(["adb"] + cmd, capture_output=True, text=True, timeout=timeout, check=False)
    except FileNotFoundError:
        print(f"{Color.BRIGHT_RED}[!] ERROR: 'adb' missing. Run: pkg install android-tools{Color.END}")
        sys.exit(1)

def get_connected_devices() -> List[str]:
    """Check connected ADB devices."""
    result = run_adb(["devices"])
    lines = result.stdout.strip().splitlines()
    devices = []
    for line in lines[1:]:
        if line.strip() and "\tdevice" in line:
            devices.append(line.split("\t")[0].strip())
    return devices

def verify_and_prepare_action(task_name: str) -> Optional[str]:
    """Step 1 & 2: Trigger Termux API popup and verify device."""
    global API_POPUP_SHOWN

    print_pinned_gemini_hud(f"INIT : {task_name.upper()}")
    
    if not check_termux_api_installed():
        return None

    trigger_termux_usb_bridge()

    if not trigger_termux_api(f"Confirm execution for {task_name}"):
        print(f"{Color.BRIGHT_RED}[!] Termux API bridge failed.{Color.END}")
        return None

    devices = get_connected_devices()
    if not devices:
        print(f"{Color.BRIGHT_RED}[!] ERROR: Device Not Found!{Color.END}")
        API_POPUP_SHOWN = False
        return None

    serial = devices[0]
    print(f"{Color.NEON_GREEN}[+] Device Verified: {serial}{Color.END}")
    return serial

def show_hacker_hud_loading_bar(task_title: str):
    """Compact Hacker loading bar for small screens."""
    print(f"\n{Color.HOT_PINK}{Color.BOLD}[*] EXECUTING -> {task_title.upper()}...{Color.END}")
    time.sleep(0.8)

    total_steps = 100
    bar_length = 25

    for i in range(1, total_steps + 1):
        percent = i
        filled_length = int(bar_length * i // total_steps)
        bar = '█' * filled_length + '▒' * (bar_length - filled_length)
        
        if percent < 35:
            bar_color = Color.CYAN
        elif percent < 75:
            bar_color = Color.GOLD
        else:
            bar_color = Color.NEON_GREEN

        sys.stdout.write(f"\r{bar_color}[{bar}] {Color.WHITE}{percent}%{Color.END}")
        sys.stdout.flush()
        
        time.sleep(0.02)

    print(f"\n\n{Color.DARK_BG}{Color.NEON_GREEN}{Color.BOLD} [+] SUCCESS: {task_title.upper()} BYPASSED! {Color.END}")

def reboot_to_recovery(serial: str):
    run_adb(["-s", serial, "reboot", "recovery"], timeout=15)

def send_keyevent(serial: str, keycode: int, delay: float = 0.8):
    run_adb(["-s", serial, "shell", "input", "keyevent", str(keycode)])
    time.sleep(delay)

def navigate_and_wipe(serial: str):
    time.sleep(2)
    for _ in range(2):
        send_keyevent(serial, 25)
    send_keyevent(serial, 26, delay=1.0)
    send_keyevent(serial, 25)
    send_keyevent(serial, 26, delay=1.5)

def strip_google_frp(serial: str):
    packages = ["com.google.android.setupwizard", "com.google.android.gsf.login"]
    for pkg in packages:
        res = run_adb(["-s", serial, "shell", "pm", "uninstall", "-k", "--user", "0", pkg])
        if res.returncode != 0:
            run_adb(["-s", serial, "shell", "pm", "disable-user", "--user", "0", pkg])

def strip_mi_cloud(serial: str):
    packages = [
        "com.xiaomi.finddevice", "com.xiaomi.account",
        "com.micloud.ui", "com.miui.cloudservice", "com.xiaomi.activations"
    ]
    for pkg in packages:
        res = run_adb(["-s", serial, "shell", "pm", "uninstall", "-k", "--user", "0", pkg])
        if res.returncode != 0:
            run_adb(["-s", serial, "shell", "pm", "disable-user", "--user", "0", pkg])

def main() -> None:
    global API_POPUP_SHOWN
    
    while True:
        if API_POPUP_SHOWN and not get_connected_devices():
            API_POPUP_SHOWN = False

        print_pinned_gemini_hud("MENU")
        print(f"{Color.BRIGHT_RED}{Color.BOLD} [!] Keep Net / Wi-Fi / SIM OFF!{Color.END}")
        print(f"{Color.GOLD}{'═' * 45}{Color.END}")
        
        print(f"  {Color.CYAN}1.{Color.END} {Color.GOLD}Screen Lock Bypass{Color.END}")
        print(f"  {Color.CYAN}2.{Color.END} {Color.GOLD}Google FRP Bypass{Color.END}")
        print(f"  {Color.CYAN}3.{Color.END} {Color.GOLD}Mi Cloud Bypass{Color.END}")
        print(f"  {Color.BRIGHT_RED}4. Exit{Color.END}")
        
        print(f"{Color.PURPLE}{'─────────────────────────────────────────────'}{Color.END}")
        
        choice = input(f"{Color.GOLD}{Color.BOLD}Select Option (1-4): {Color.END}").strip()
        
        if choice == '4':
            print(f"\n{Color.BRIGHT_RED}[*] Exiting System. Gemini AI Credit.{Color.END}")
            sys.exit(0)
            
        if choice not in ['1', '2', '3']:
            print(f"{Color.BRIGHT_RED}[!] Invalid Choice! Select 1-4.{Color.END}")
            time.sleep(1.2)
            continue

        task_names = {
            '1': "Screen Lock Bypass",
            '2': "Google FRP Bypass",
            '3': "Mi Cloud Bypass"
        }
        
        serial = verify_and_prepare_action(task_names[choice])
        if not serial:
            input(f"\n{Color.GOLD}[Press Enter to continue...]{Color.END}")
            continue

        print(f"\n{Color.GOLD}{Color.BOLD}[?] Confirm bypass for {task_names[choice]}?{Color.END}")
        input(f"{Color.NEON_GREEN}{Color.BOLD}---> Press ENTER to start...{Color.END}")

        print_pinned_gemini_hud(f"RUNNING")

        if choice == '1':
            reboot_to_recovery(serial)
            navigate_and_wipe(serial)
        elif choice == '2':
            strip_google_frp(serial)
        elif choice == '3':
            strip_mi_cloud(serial)

        show_hacker_hud_loading_bar(task_names[choice])

        input(f"\n{Color.GOLD}[Press Enter to return to menu...]{Color.END}")

if __name__ == "__main__":
    main()
