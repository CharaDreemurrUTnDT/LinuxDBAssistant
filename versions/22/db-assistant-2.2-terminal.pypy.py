import os
import sys
import platform
import ctypes
import subprocess
import requests
import hashlib
import logging
import traceback
import webbrowser

UNSUPPORTED_DISTROS_URL = "https://raw.githubusercontent.com/CharaDreemurrUTnDT/LinuxDBAssistant/refs/heads/main/UnsupportedDistros.md"
DISTRO_CHOOSER_URL = "https://distrochooser.de/"

HEADER = r"""
 _      _                  _____  ____                  _     _              _   
 | |    (_)                |  __ \|  _ \   /\           (_)   | |            | |  
 | |     _ _ __  _   ___  _| |  | | |_) | /  \   ___ ___ _ ___| |_ __ _ _ __ | |_ 
 | |    | | '_ \| | | \ \/ / |  | |  _ < / /\ \ / __/ __| / __| __/ _` | '_ \| __|
 | |____| | | | | |_| |>  <| |__| | |_) / ____ \\__ \__ \ \__ \ || (_| | | | | |_ 
 |______|_|_| |_|\__,_/_/\_\_____/|____/_/    \_\___/___/_|___/\__\__,_|_| |_|\__|
                                                                                  
                                                                                  
"""

# ANSI color code for #a3a3c2 (approximate: 146)
COLOR = "\033[38;5;146m"
RESET = "\033[0m"

def cprint(text):
    print(f"{COLOR}{text}{RESET}")

# Advanced logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

def log_exception(e, msg="Exception occurred"):
    logging.error(f"{msg}: {e}")
    logging.debug(traceback.format_exc())

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_compatibility():
    system = platform.system()
    arch = platform.architecture()[0]
    win_ver = sys.getwindowsversion() if hasattr(sys, "getwindowsversion") else None
    if arch != "64bit":
        cprint("32-bit systems are not supported.")
        sys.exit()
    if system != "Windows":
        cprint("Only Windows 10 and 11 are supported.")
        sys.exit()
    if win_ver is None or win_ver.major != 10:
        cprint("Only Windows 10 and 11 are supported.")
        sys.exit()

def ensure_7zip_installed():
    def is_installed(cmd):
        try:
            subprocess.check_output([cmd, "--help"], stderr=subprocess.STDOUT)
            logging.debug(f"{cmd} is installed.")
            return True
        except Exception as e:
            logging.debug(f"{cmd} not found: {e}")
            return False

    if is_installed("7z"):
        return "7z"
    if is_installed("nanazip"):
        return "nanazip"
    win_ver = sys.getwindowsversion()
    try:
        if win_ver.build >= 22000:
            url = "https://github.com/M2Team/NanaZip/releases/latest/download/NanaZip-Installer-x64.msixbundle"
            cprint("NanaZip is not installed. Opening download page...")
            os.startfile(url)
            input("After installing NanaZip, press Enter to exit.")
            sys.exit()
        else:
            url = "https://www.7-zip.org/a/7z2301-x64.exe"
            cprint("7-Zip is not installed. Opening download page...")
            os.startfile(url)
            input("After installing 7-Zip, press Enter to exit.")
            sys.exit()
    except Exception as e:
        log_exception(e, "Failed to install archiver")
        cprint(f"Failed to start installer:\n{e}")
        sys.exit()

def extract_iso_cli():
    logging.info("User selected Extract ISO option.")
    try:
        archiver = ensure_7zip_installed()
        logging.debug(f"Archiver selected: {archiver}")
        file_path = input("Enter the path to the ISO file: ").strip('"')
        if not file_path or not os.path.isfile(file_path):
            cprint("No valid ISO file selected.")
            return
        logging.info(f"ISO file selected: {file_path}")
        out_dir = input("Enter the output directory: ").strip('"')
        if not out_dir:
            cprint("No output directory selected.")
            return
        logging.info(f"Output directory selected: {out_dir}")
        logging.debug(f"Running extraction: {archiver} x {file_path} -o{out_dir} -y")
        subprocess.check_call([archiver, "x", file_path, f"-o{out_dir}", "-y"])
        cprint("ISO extracted successfully!")
        logging.info("ISO extracted successfully.")
    except Exception as e:
        log_exception(e, "Failed to extract ISO")
        cprint(f"Failed to extract ISO:\n{e}")

def calculate_hashes(file_path):
    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
            sha256_hash.update(chunk)
    return md5_hash.hexdigest(), sha256_hash.hexdigest()

def hash_checker_cli():
    try:
        file_path = input("Enter the path to the file to check: ").strip('"')
        if not file_path or not os.path.isfile(file_path):
            cprint("No valid file selected.")
            return
        cprint("Check which hash? (md5/sha256/both): ")
        hash_choice = input().strip().lower()
        if hash_choice not in ("md5", "sha256", "both"):
            cprint("Invalid choice.")
            return
        actual_md5, actual_sha256 = calculate_hashes(file_path)
        result = f"File: {file_path}\n\n"
        if hash_choice in ("md5", "both"):
            expected_md5 = input("Enter the expected MD5 hash: ").strip()
            if not expected_md5:
                cprint("MD5 hash not provided.")
                return
            result += (
                f"Expected MD5:   {expected_md5}\n"
                f"Actual MD5:     {actual_md5}\n"
                f"MD5 Match:      {'YES' if expected_md5.lower() == actual_md5.lower() else 'NO'}\n\n"
            )
            logging.info(f"MD5 checked: expected={expected_md5}, actual={actual_md5}")
        if hash_choice in ("sha256", "both"):
            expected_sha256 = input("Enter the expected SHA256 hash: ").strip()
            if not expected_sha256:
                cprint("SHA256 hash not provided.")
                return
            result += (
                f"Expected SHA256: {expected_sha256}\n"
                f"Actual SHA256:   {actual_sha256}\n"
                f"SHA256 Match:    {'YES' if expected_sha256.lower() == actual_sha256.lower() else 'NO'}"
            )
            logging.info(f"SHA256 checked: expected={expected_sha256}, actual={actual_sha256}")
        cprint(result)
    except Exception as e:
        log_exception(e, "Hash checking failed")
        cprint(f"Hash checking failed:\n{e}")

def open_disk_management_cli():
    try:
        logging.info("Opening Disk Management.")
        subprocess.Popen("diskmgmt.msc", shell=True)
        cprint("Disk Management opened.")
    except Exception as e:
        log_exception(e, "Failed to open Disk Management")
        cprint(f"Failed to open Disk Management:\n{e}")

def open_partition_wizard_info_cli():
    cprint(
        "WARNING: Mini Tool Partition Wizard can cause serious damage to your partitions.\n"
        "Only use this as a last resort, if Disk Management doesn´t allow you to shrink the necessary space from your disk.\n"
        "Otherwise, you should use Disk Management."
    )
    proceed = input("Do you want to proceed to Mini Tool Partition Wizard's website? (y/n): ").strip().lower()
    if proceed == "y":
        webbrowser.open("https://www.partitionwizard.com/")

def reboot_to_windows_recovery_cli():
    try:
        subprocess.run("shutdown /r /o /f /t 0", shell=True)
        cprint("Rebooting to Windows Recovery...")
    except Exception as e:
        log_exception(e, "Failed to reboot to Windows Recovery")
        cprint(f"Failed to reboot to Windows Recovery:\n{e}")

def show_unsupported_distros_cli():
    try:
        response = requests.get(UNSUPPORTED_DISTROS_URL)
        response.raise_for_status()
        content = response.text
        cprint("\n--- Unsupported Distros ---\n")
        cprint(content)
        cprint("\n--------------------------\n")
    except Exception as e:
        log_exception(e, "Failed to fetch unsupported distros")
        cprint(f"Failed to fetch unsupported distros:\n{e}")

def open_distro_chooser_cli():
    cprint("Opening Distro Chooser in your browser...")
    webbrowser.open(DISTRO_CHOOSER_URL)

def set_windows_utc_time_cli():
    try:
        import winreg
        logging.info("Attempting to set RealTimeIsUniversal=1 in registry.")
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\TimeZoneInformation",
            0,
            winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY
        )
        winreg.SetValueEx(key, "RealTimeIsUniversal", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        cprint("Registry value 'RealTimeIsUniversal' set to 1. Windows will now use UTC for the hardware clock.")
        logging.info("Successfully set RealTimeIsUniversal=1.")
    except PermissionError:
        logging.error("Permission denied while setting RealTimeIsUniversal.")
        cprint("You must run this program as administrator to change this setting.")
    except Exception as e:
        log_exception(e, "Failed to set UTC time")
        cprint(f"Failed to set UTC time:\n{e}")

def main_menu():
    cprint(HEADER)
    cprint("Made by CharaUTnDT on Github\n")
    cprint("Choose an option:")
    cprint("[1] Extract ISO")
    cprint("[2] MD5/SHA256 Checker")
    cprint("[3] Open Disk Management")
    cprint("[4] MiniTool Partition Wizard")
    cprint("[5] Show Unsupported Distros")
    cprint("[6] Distro Chooser")
    cprint("[7] Reboot to Windows Recovery")
    cprint("[8] Change localtime to UTC Time (PROCEED WITH CAUTION!)")
    cprint("[9] Exit")

def main():
    if os.name == 'nt' and not is_admin():
        cprint("Restarting as administrator...")
        params = ' '.join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1
        )
        sys.exit()
    check_compatibility()
    while True:
        main_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            extract_iso_cli()
        elif choice == "2":
            hash_checker_cli()
        elif choice == "3":
            open_disk_management_cli()
        elif choice == "4":
            open_partition_wizard_info_cli()
        elif choice == "5":
            show_unsupported_distros_cli()
        elif choice == "6":
            open_distro_chooser_cli()
        elif choice == "7":
            reboot_to_windows_recovery_cli()
        elif choice == "8":
            set_windows_utc_time_cli()
        elif choice == "9":
            cprint("Goodbye!")
            break
        else:
            cprint("Invalid choice. Please try again.")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
