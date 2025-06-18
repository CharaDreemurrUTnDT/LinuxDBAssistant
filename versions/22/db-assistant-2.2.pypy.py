import os
import sys
import platform
import ctypes
import subprocess
import requests
import io
import webbrowser
from tkinter import Tk, Frame, Label, Button, messagebox, filedialog, simpledialog, Toplevel, Text, Scrollbar, StringVar, Radiobutton
from PIL import Image, ImageTk
import logging
import traceback

UNSUPPORTED_DISTROS_URL = "https://raw.githubusercontent.com/CharaDreemurrUTnDT/LinuxDBAssistant/refs/heads/main/UnsupportedDistros.md"
DISTRO_CHOOSER_URL = "https://distrochooser.de/"
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
        messagebox.showerror("Unsupported", "32-bit systems are not supported.")
        sys.exit()
    if system != "Windows":
        messagebox.showerror("Unsupported", "Only Windows 10 and 11 are supported.")
        sys.exit()
    if win_ver is None or win_ver.major != 10:
        messagebox.showerror("Unsupported", "Only Windows 10 and 11 are supported.")
        sys.exit()
    # No legacy BIOS detection

def ensure_7zip_installed():
    # Check for 7zip or nanazip, install if missing
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
    # Not installed, try to install
    win_ver = sys.getwindowsversion()
    try:
        if win_ver.build >= 22000:
            url = "https://github.com/M2Team/NanaZip/releases/latest/download/NanaZip-Installer-x64.msixbundle"
            logging.info("Installing NanaZip for Windows 11.")
            os.startfile(url)
            messagebox.showinfo("Continue", "After installing NanaZip, please restart this application.")
            sys.exit()
        else:
            url = "https://www.7-zip.org/a/7z2301-x64.exe"
            logging.info("Installing 7-Zip for Windows 10.")
            os.startfile(url)
            messagebox.showinfo("Continue", "After installing 7-Zip, please restart this application.")
            sys.exit()
    except Exception as e:
        log_exception(e, "Failed to install archiver")
        messagebox.showerror("Error", f"Failed to start installer:\n{e}")

def extract_iso_gui():
    logging.info("User selected Extract ISO option.")
    try:
        archiver = ensure_7zip_installed()
        logging.debug(f"Archiver selected: {archiver}")
        file_path = filedialog.askopenfilename(title="Select ISO file", filetypes=[("ISO files", "*.iso")])
        if not file_path:
            logging.warning("No ISO file selected.")
            return
        logging.info(f"ISO file selected: {file_path}")
        out_dir = filedialog.askdirectory(title="Select output folder")
        if not out_dir:
            logging.warning("No output directory selected.")
            return
        logging.info(f"Output directory selected: {out_dir}")
        logging.debug(f"Running extraction: {archiver} x {file_path} -o{out_dir} -y")
        subprocess.check_call([archiver, "x", file_path, f"-o{out_dir}", "-y"])
        messagebox.showinfo("Success", "ISO extracted successfully!")
        logging.info("ISO extracted successfully.")
    except Exception as e:
        log_exception(e, "Failed to extract ISO")
        messagebox.showerror("Error", f"Failed to extract ISO:\n{e}")

def calculate_hashes(file_path):
    import hashlib
    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
            sha256_hash.update(chunk)
    return md5_hash.hexdigest(), sha256_hash.hexdigest()

def hash_checker_gui():
    import hashlib
    import tkinter as tk
    root = tk.Toplevel()
    root.title("MD5/SHA256 Checker")
    root.geometry("500x350")
    hash_choice = StringVar(value="md5")

    def choose_file():
        path = filedialog.askopenfilename(title="Select file to check")
        if path:
            file_entry.config(state="normal")
            file_entry.delete(0, "end")
            file_entry.insert(0, path)
            file_entry.config(state="readonly")
            logging.info(f"File selected for hash checking: {path}")

    def check_hash():
        try:
            file_path = file_entry.get()
            if not file_path:
                logging.warning("No file selected for hash checking.")
                messagebox.showerror("No file", "No file selected.")
                return
            actual_md5, actual_sha256 = calculate_hashes(file_path)
            result = f"File: {file_path}\n\n"
            if hash_choice.get() in ("md5", "both"):
                expected_md5 = md5_entry.get()
                if not expected_md5:
                    logging.warning("MD5 hash not provided by user.")
                    messagebox.showerror("Missing input", "MD5 hash not provided.")
                    return
                result += (
                    f"Expected MD5:   {expected_md5}\n"
                    f"Actual MD5:     {actual_md5}\n"
                    f"MD5 Match:      {'YES' if expected_md5.lower() == actual_md5.lower() else 'NO'}\n\n"
                )
                logging.info(f"MD5 checked: expected={expected_md5}, actual={actual_md5}")
            if hash_choice.get() in ("sha256", "both"):
                expected_sha256 = sha256_entry.get()
                if not expected_sha256:
                    logging.warning("SHA256 hash not provided by user.")
                    messagebox.showerror("Missing input", "SHA256 hash not provided.")
                    return
                result += (
                    f"Expected SHA256: {expected_sha256}\n"
                    f"Actual SHA256:   {actual_sha256}\n"
                    f"SHA256 Match:    {'YES' if expected_sha256.lower() == actual_sha256.lower() else 'NO'}"
                )
                logging.info(f"SHA256 checked: expected={expected_sha256}, actual={actual_sha256}")
            messagebox.showinfo("Hash Comparison Result", result)
        except Exception as e:
            log_exception(e, "Hash checking failed")
            messagebox.showerror("Error", f"Hash checking failed:\n{e}")

    # GUI layout
    file_frame = Frame(root)
    file_frame.pack(pady=10)
    Button(file_frame, text="Choose File", command=choose_file).pack(side="left")
    file_entry = tk.Entry(file_frame, width=50, state="readonly")
    file_entry.pack(side="left", padx=5)

    hash_frame = Frame(root)
    hash_frame.pack(pady=10)
    Radiobutton(hash_frame, text="MD5", variable=hash_choice, value="md5").pack(side="left")
    Radiobutton(hash_frame, text="SHA256", variable=hash_choice, value="sha256").pack(side="left")
    Radiobutton(hash_frame, text="Both", variable=hash_choice, value="both").pack(side="left")

    md5_label = Label(root, text="Expected MD5:")
    md5_label.pack()
    md5_entry = tk.Entry(root, width=60)
    md5_entry.pack()

    sha256_label = Label(root, text="Expected SHA256:")
    sha256_label.pack()
    sha256_entry = tk.Entry(root, width=60)
    sha256_entry.pack()

    Button(root, text="Check Hash", command=check_hash).pack(pady=10)

def open_disk_management():
    try:
        logging.info("Opening Disk Management.")
        subprocess.Popen("diskmgmt.msc", shell=True)
    except Exception as e:
        log_exception(e, "Failed to open Disk Management")
        messagebox.showerror("Error", f"Failed to open Disk Management:\n{e}")

def open_partition_wizard_info():
    proceed = messagebox.askyesno(
        "Warning",
        "Mini Tool Partition Wizard can cause serious damage to your partitions. Only use this as a last resort, if Disk Management doesn´t allow you to shrink the necessary space from your disk. Otherwise, you should use Disk Management.\n\nDo you want to proceed to Mini Tool Partition Wizard's website?"
    )
    if proceed:
        webbrowser.open("https://www.partitionwizard.com/")

def reboot_to_windows_recovery():
    try:
        subprocess.run("shutdown /r /o /f /t 0", shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to reboot to Windows Recovery:\n{e}")

def show_unsupported_distros():
    try:
        response = requests.get(UNSUPPORTED_DISTROS_URL)
        response.raise_for_status()
        content = response.text
    except Exception as e:
        content = f"Failed to fetch unsupported distros:\n{e}"
    win = Toplevel()
    win.title("Unsupported Distros")
    win.geometry("500x400")
    text = Text(win, wrap="word")
    text.insert("1.0", content)
    text.config(state="disabled")
    text.pack(expand=True, fill="both")
    scrollbar = Scrollbar(win, command=text.yview)
    text.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

def open_distro_chooser():
    try:
        import webview
        try:
            webview.create_window("Distro Chooser", DISTRO_CHOOSER_URL, width=1024, height=700)
            webview.start(gui='tkinter', debug=False)
        except Exception as e:
            messagebox.showerror("Webview Error", f"pywebview failed to start:\n{e}\nOpening in your browser instead.")
            webbrowser.open(DISTRO_CHOOSER_URL)
    except ImportError:
        messagebox.showerror("Missing Dependency", "Please install 'pywebview' with:\npip install pywebview")
        webbrowser.open(DISTRO_CHOOSER_URL)

def set_windows_utc_time():
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
        messagebox.showinfo("Success", "Registry value 'RealTimeIsUniversal' set to 1.\nWindows will now use UTC for the hardware clock.")
        logging.info("Successfully set RealTimeIsUniversal=1.")
    except PermissionError:
        logging.error("Permission denied while setting RealTimeIsUniversal.")
        messagebox.showerror("Permission Denied", "You must run this program as administrator to change this setting.")
    except Exception as e:
        log_exception(e, "Failed to set UTC time")
        messagebox.showerror("Error", f"Failed to set UTC time:\n{e}")

# Advanced logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

def log_exception(e, msg="Exception occurred"):
    logging.error(f"{msg}: {e}")
    logging.debug(traceback.format_exc())

class LinuxDBAssistantGUI(Tk):
    def __init__(self):
        super().__init__()
        self.title("LinuxDBAssistant")
        self.geometry("400x540")  # Increased window size
        self.resizable(False, False)
        self.fg_color = "#222"
        self.bg_color = "#fff"
        self.set_theme()
        self.logo_img = None
        self.setup_gui()

    def set_theme(self):
        if self.is_dark_mode():
            self.bg_color = "#222"
            self.fg_color = "#fff"
        else:
            self.bg_color = "#fff"
            self.fg_color = "#222"
        self.configure(bg=self.bg_color)

    def is_dark_mode(self):
        try:
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return value == 0
        except Exception:
            return False

    def setup_gui(self):
        # Header text
        Label(self, text="LinuxDBAssistant", font=("Arial", 18, "bold"), bg=self["bg"], fg=self.fg_color).pack(pady=12)

        options_frame = Frame(self, bg=self["bg"])
        options_frame.pack(pady=10, fill="x")

        btn_font = ("Segoe UI", 11)
        btn_height = 1
        btn_width = 32  # Set a fixed width for all buttons

        Button(options_frame, text="Extract ISO", font=btn_font, height=btn_height, width=btn_width, command=extract_iso_gui).pack(fill="x", pady=3, padx=12)
        Button(options_frame, text="MD5/SHA256 Checker", font=btn_font, height=btn_height, width=btn_width, command=hash_checker_gui).pack(fill="x", pady=3, padx=12)
        Button(options_frame, text="Open Disk Management", font=btn_font, height=btn_height, width=btn_width, command=open_disk_management).pack(fill="x", pady=3, padx=12)
        Button(options_frame, text="MiniTool Partition Wizard", font=btn_font, height=btn_height, width=btn_width, command=open_partition_wizard_info).pack(fill="x", pady=3, padx=12)
        Button(options_frame, text="Show Unsupported Distros", font=btn_font, height=btn_height, width=btn_width, command=show_unsupported_distros).pack(fill="x", pady=3, padx=12)
        Button(options_frame, text="Distro Chooser", font=btn_font, height=btn_height, width=btn_width, command=open_distro_chooser).pack(fill="x", pady=3, padx=12)
        Button(options_frame, text="Reboot to Windows Recovery", font=btn_font, height=btn_height, width=btn_width, command=reboot_to_windows_recovery).pack(fill="x", pady=3, padx=12)
        Button(options_frame, text="Change localtime to UTC Time", font=btn_font, height=btn_height, width=btn_width, command=set_windows_utc_time).pack(fill="x", pady=3, padx=12)
        Button(options_frame, text="Exit LinuxDBAssistant", font=btn_font, height=btn_height, width=btn_width, command=self.quit).pack(fill="x", pady=3, padx=12)

        # Add a separator line
        Frame(self, height=2, bd=1, relief="sunken", bg="#888").pack(fill="x", padx=8, pady=(10, 0))

        # Add the credit label at the bottom
        Label(self, text="Made by CharaUTnDT on Github", font=("Segoe UI", 9, "italic"), bg=self["bg"], fg="#666").pack(pady=(6, 10))

if __name__ == "__main__":
    if os.name == 'nt' and not is_admin():
        params = ' '.join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1
        )
        sys.exit()
    check_compatibility()
    app = LinuxDBAssistantGUI()
    app.mainloop()
