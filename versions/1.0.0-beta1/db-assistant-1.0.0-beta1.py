import os
import platform
import subprocess
import hashlib
import shutil
import urllib.request
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


# Check system compatibility
def check_compatibility():
    system = platform.system()
    arch = platform.architecture()[0]

    if system == "Windows":
        if arch == "32bit":
            messagebox.showerror("Incompatible System", "This application does not support 32-bit systems.")
            exit()
        elif platform.release() in ["8.1", "8", "7", "Vista", "XP", "ME", "2000", "98", "95"]:
            messagebox.showerror("Incompatible System", f"Unsupported Windows version: {platform.release()}.")
            exit()
        elif platform.release() == "10":
            messagebox.showwarning("Warning", "Legacy BIOS is unsupported on Windows 10 systems.")
    elif system == "Darwin":  # macOS
        messagebox.showerror("Incompatible System", "This application is not supported on macOS.")
        exit()
    elif system == "Linux":
        messagebox.showerror("Incompatible System", "This application is not supported on Linux.")
        exit()
    else:
        messagebox.showerror("Incompatible System", f"Unsupported Operating System: {system}.")
        exit()


# Check and install 7-Zip if not installed
def ensure_7zip_installed():
    try:
        subprocess.run(["7z"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        messagebox.showinfo("Installing Dependency", "7-Zip is not installed. Installing now...")
        subprocess.run(["winget", "install", "-e", "--id", "7zip.7zip"], check=True)


# Open Disk Management
def open_disk_management():
    try:
        subprocess.run(["diskmgmt.msc"], shell=True)
    except FileNotFoundError:
        messagebox.showerror("Error", "Disk Management tool not found.")


# Open file dialog to select an ISO file
def select_iso_file():
    return filedialog.askopenfilename(title="Select ISO File", filetypes=[("ISO files", "*.iso")])


# Open directory dialog to select an output folder
def select_output_folder():
    return filedialog.askdirectory(title="Select Output Directory")


# Extract ISO using 7-Zip
def extract_iso(iso_path, output_dir):
    try:
        subprocess.run(["7z", "x", iso_path, f"-o{output_dir}"], check=True)
        messagebox.showinfo("Success", f"Extraction complete! Files extracted to: {output_dir}")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "7-Zip failed to extract the ISO.")
    except FileNotFoundError:
        messagebox.showerror("Error", "7-Zip executable not found. Please ensure it is installed and added to the system PATH.")


# Verify ISO integrity
def verify_iso_integrity(iso_path, hash_algo, user_hash):
    try:
        hash_func = getattr(hashlib, hash_algo)()
        with open(iso_path, "rb") as iso:
            for chunk in iter(lambda: iso.read(4096), b""):
                hash_func.update(chunk)
        iso_checksum = hash_func.hexdigest()
        if iso_checksum == user_hash:
            messagebox.showinfo("Success", "ISO integrity verified successfully!")
        else:
            messagebox.showerror("Failure", "ISO integrity verification failed. Checksum mismatch.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Install rEFInd Boot Manager
def install_refind():
    try:
        refind_url = "https://sourceforge.net/projects/refind/files/latest/download"
        refind_zip, _ = urllib.request.urlretrieve(refind_url, "refind.zip")
        refind_extract_path = r"C:\linuxinstaller\reFInd"  # Fixed: Escaped backslashes

        with zipfile.ZipFile(refind_zip, "r") as zip_ref:
            zip_ref.extractall(refind_extract_path)

        subprocess.run(["mountvol", "B:", "/S"], check=True, shell=True)
        shutil.copytree(
            os.path.join(refind_extract_path, "refind-bin", "refind"),
            r"B:\EFI\refind",  # Fixed: Escaped backslashes
            dirs_exist_ok=True,
        )
        subprocess.run(
            ["bcdedit", "/set", "{bootmgr}", "path", r"\EFI\refind\refind_x64.efi"],  # Fixed: Escaped backslashes
            check=True,
        )

        shutil.rmtree(refind_extract_path, ignore_errors=True)
        os.remove(refind_zip)

        messagebox.showinfo("Success", "rEFInd installed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# GUI Application
class LinuxDBAssistantGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LinuxDBAssistant")
        self.geometry("250x300")  # Compact window size
        self.resizable(False, False)  # Disable resizing
        self.update_theme()  # Update the theme when the app initializes
        self.setup_gui()

    def update_theme(self):
        """Update the GUI to match the system's dark or light mode."""
        if self.is_dark_mode():
            self.configure(bg="black")
            self.fg_color = "white"
        else:
            self.configure(bg="white")
            self.fg_color = "black"

    def is_dark_mode(self):
        """Detect if the system is in dark mode."""
        if platform.system() == "Windows":
            import ctypes
            try:
                key = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
                with ctypes.windll.advapi32.RegOpenKeyExW(
                    ctypes.HKEY_CURRENT_USER, key, 0, ctypes.KEY_READ
                ) as hkey:
                    value = ctypes.wintypes.DWORD()
                    ctypes.windll.advapi32.RegQueryValueExW(hkey, "AppsUseLightTheme", None, None, value)
                    return value.value == 0
            except Exception:
                return False
        elif platform.system() == "Darwin":  # macOS
            import subprocess
            try:
                output = subprocess.check_output(
                    ["defaults", "read", "-g", "AppleInterfaceStyle"], stderr=subprocess.DEVNULL
                )
                return "Dark" in output.decode()
            except subprocess.CalledProcessError:
                return False
        else:
            return False

    def setup_gui(self):
        tk.Label(self, text="LinuxDBAssistant", font=("Arial", 14), bg=self["bg"], fg=self.fg_color).pack(pady=5)

        options_frame = tk.Frame(self, bg=self["bg"])
        options_frame.pack(pady=10)

        ttk.Button(options_frame, text="Disk Management", command=open_disk_management).pack(fill="x", pady=2)
        ttk.Button(options_frame, text="Extract ISO", command=self.extract_iso_gui).pack(fill="x", pady=2)
        ttk.Button(options_frame, text="Verify ISO Integrity", command=self.verify_iso_gui).pack(fill="x", pady=2)
        ttk.Button(options_frame, text="Install rEFInd", command=install_refind).pack(fill="x", pady=2)
        ttk.Button(options_frame, text="Exit", command=self.quit).pack(fill="x", pady=2)

    def extract_iso_gui(self):
        iso_path = select_iso_file()
        if not iso_path:
            return
        output_dir = select_output_folder()
        if not output_dir:
            return
        extract_iso(iso_path, output_dir)

    def verify_iso_gui(self):
        iso_path = select_iso_file()
        if not iso_path:
            return

        hash_algo = tk.StringVar(value="md5")
        user_hash = tk.StringVar()

        verify_window = tk.Toplevel(self)
        verify_window.title("Verify ISO Integrity")
        verify_window.geometry("200x150")  # Compact size for the dialog

        tk.Label(verify_window, text="Hash Algorithm:", font=("Arial", 10)).pack(pady=3)
        tk.Radiobutton(verify_window, text="MD5", variable=hash_algo, value="md5").pack(anchor="w", padx=10)
        tk.Radiobutton(verify_window, text="SHA256", variable=hash_algo, value="sha256").pack(anchor="w", padx=10)

        tk.Label(verify_window, text="Checksum:", font=("Arial", 10)).pack(pady=3)
        tk.Entry(verify_window, textvariable=user_hash).pack(pady=3)

        ttk.Button(verify_window, text="Verify", command=lambda: verify_iso_integrity(iso_path, hash_algo.get(), user_hash.get())).pack(pady=5)


if __name__ == "__main__":
    check_compatibility()
    ensure_7zip_installed()
    app = LinuxDBAssistantGUI()
    app.mainloop()