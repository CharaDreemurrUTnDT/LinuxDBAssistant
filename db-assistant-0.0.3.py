import os
import subprocess
import urllib.request
import zipfile
import shutil


def print_ascii_logo():
    """Prints the ASCII logo at startup."""
    ascii_logo = r"""
     _      _                  _____  ____                  _     _              _   
    | |    (_)                |  __ \|  _ \   /\           (_)   | |            | |  
    | |     _ _ __  _   ___  _| |  | | |_) | /  \   ___ ___ _ ___| |_ __ _ _ __ | |_ 
    | |    | | '_ \| | | \ \/ / |  | |  _ < / /\ \ / __/ __| / __| __/ _` | '_ \| __|
    | |____| | | | | |_| |>  <| |__| | |_) / ____ \\__ \__ \ \__ \ || (_| | | | | |_ 
    |______|_|_| |_|\__,_/_/\_\_____/|____/_/    \_\___/___/_|___/\__\__,_|_| |_|\__|
                                                                                  
                                                                                  
    """
    print(ascii_logo)


def open_disk_management():
    """Opens the Disk Management tool in Windows."""
    print("Opening Disk Management...")
    subprocess.run(["diskmgmt.msc"], shell=True)


def extract_iso_with_7zip(iso_path, output_dir):
    """Extracts an ISO file to a specific partition using 7-Zip."""
    if not os.path.isfile(iso_path):
        print(f"Error: ISO file '{iso_path}' does not exist.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    command = ['7z', 'x', iso_path, f'-o{output_dir}']
    try:
        subprocess.run(command, check=True)
        print(f"Extraction complete! Files extracted to: {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error: 7-Zip failed to extract the ISO. Details: {e}")
    except FileNotFoundError:
        print("Error: 7-Zip executable not found. Please ensure it is installed and added to the system PATH.")


def verify_iso_integrity(iso_path, checksum_url):
    """Verifies the ISO file's integrity by comparing its checksum."""
    if not os.path.isfile(iso_path):
        print(f"Error: ISO file '{iso_path}' does not exist.")
        return

    print("Downloading checksum file...")
    try:
        checksum_file, _ = urllib.request.urlretrieve(checksum_url)
    except Exception as e:
        print(f"Error downloading checksum file: {e}")
        return

    print("Calculating ISO checksum...")
    import hashlib
    hash_md5 = hashlib.md5()
    with open(iso_path, "rb") as iso:
        for chunk in iter(lambda: iso.read(4096), b""):
            hash_md5.update(chunk)

    iso_checksum = hash_md5.hexdigest()
    print(f"Calculated checksum: {iso_checksum}")

    with open(checksum_file, "r") as f:
        if iso_checksum in f.read():
            print("ISO integrity verified successfully!")
        else:
            print("ISO integrity verification failed. Checksum mismatch.")

    os.remove(checksum_file)


def mount_esp():
    """Mounts the EFI System Partition (ESP) to the B: drive."""
    print("Mounting EFI System Partition (ESP) to B: drive...")
    try:
        subprocess.run(["mountvol", "B:", "/S"], check=True, shell=True)
        print("ESP mounted successfully to B:.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to mount ESP. Details: {e}")


def install_refind():
    """Automatically installs the rEFInd boot manager manually on Windows."""
    print("Downloading rEFInd...")
    refind_url = "https://sourceforge.net/projects/refind/files/latest/download"
    try:
        refind_zip, _ = urllib.request.urlretrieve(refind_url, "refind.zip")
    except Exception as e:
        print(f"Error downloading rEFInd: {e}")
        return

    print("Extracting rEFInd to C:\\linuxinstaller\\reFInd...")
    refind_extract_path = "C:\\linuxinstaller\\reFInd"
    try:
        with zipfile.ZipFile(refind_zip, "r") as zip_ref:
            zip_ref.extractall(refind_extract_path)
    except Exception as e:
        print(f"Error extracting rEFInd: {e}")
        return

    print("Installing rEFInd...")
    refind_dir = os.path.join(refind_extract_path, "refind-bin")
    if not os.path.exists(refind_dir):
        print("Error: rEFInd directory structure not found. Please check the extracted files.")
        return

    # Mount ESP to B:
    mount_esp()

    # Copy rEFInd files to ESP
    esp_refind_dir = os.path.join("B:\\EFI\\refind")
    if not os.path.exists(esp_refind_dir):
        os.makedirs(esp_refind_dir)

    try:
        shutil.copytree(os.path.join(refind_dir, "refind"), esp_refind_dir, dirs_exist_ok=True)
        print(f"Copied rEFInd files to {esp_refind_dir}")
    except Exception as e:
        print(f"Error copying rEFInd files: {e}")
        return

    # Add boot entry for rEFInd
    print("Adding boot entry for rEFInd...")
    try:
        subprocess.run(
            ["bcdedit", "/set", "{bootmgr}", "path", "\\EFI\\refind\\refind_x64.efi"],
            check=True,
        )
        print("rEFInd boot entry added successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error adding rEFInd boot entry: {e}")

    # Clean up
    os.remove(refind_zip)
    shutil.rmtree(refind_extract_path, ignore_errors=True)


def main():
    print_ascii_logo()

    while True:
        print("\nDual Boot Assistant")
        print("[1.] Open Disk Management")
        print("[2.] Extract ISO to a specific partition using 7-Zip")
        print("[3.] Verify ISO integrity")
        print("[4.] Install rEFInd Boot Manager")
        print("[5.] Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            open_disk_management()
        elif choice == "2":
            iso_path = input("Enter the path to the ISO file: ")
            output_dir = input("Enter the output directory (partition): ")
            extract_iso_with_7zip(iso_path, output_dir)
        elif choice == "3":
            iso_path = input("Enter the path to the ISO file: ")
            checksum_url = input("Enter the URL of the checksum file: ")
            verify_iso_integrity(iso_path, checksum_url)
        elif choice == "4":
            install_refind()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
