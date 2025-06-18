![LinuxDBAssistant](https://github.com/user-attachments/assets/67e10e60-949f-417c-bee5-6a8897df35b0)
This is for assisting Windows Users to Dual Boot Windows and Linux without an USB Drive, giving them options to assist them!
# Options
- Open Disk management
- Extract the iso to a specific partition using 7zip or NanaZip (7zip needs to be on the path.)
- Verify ISO Integrity (It needs to be a sha256 or md5 hash, OpenPGP support is planned)
- Change localtime to UTC Time (Proceed with caution!) (I think if you dual booted before you noticed the time was off every restart you did to Windows. Well, with this option, both Linux and Windows will be using UTC time, which means, no more errors in time with this!)
- Redirect user to MiniTool´s Partition Wizard (This should only be used in case Disk Management doesn´t allow the user to shrink the necessary space, otherwise you should use Disk Management.)
- Choose your distro!
- Show the list of currently known unsupported distros.
- Reboot to Windows Recovery!
# Requirements
- Python (If you are using the .py file)
- 7zip added to PATH or NanaZIP
- UEFI Bios. This will not work for Legacy Bios or UEFI-CSM.
- Pillow, Requests and PyWebView for the .py version (can be installed with ````pip install requests pillow pywebview````)
# How to download:
[![Download from SourceForge](https://a.fsdn.com/con/app/sf-download-button)](https://sourceforge.net/projects/linuxdbassistant/files/v2.1/)
[![GitHub release](https://img.shields.io/github/v/release/CharaUTnDT/LinuxDBAssistant?label=Download%20from%20GitHub%20Releases)](https://github.com/CharaUTnDT/LinuxDBAssistant/releases/latest)
- The only use for the .py version is for debugging.
# Guide 
- First, shrink your C: Drive for free space for Linux and the partition the ISO is gonna be stored in.
- Create a partition, the size depends on the size of the distributions´s iso. (I personally recommend FAT32 for the format, if there is a file bigger than 4GB on your distribution´s iso, use NTFS.)
- Extract the ISO to the partition youve created using the extract iso option.
- Boot to Windows Recovery using one of this 2 methods: Holding shift when clicking the restart button or going to settings -> system -> recovery -> advanced reboot 
- Choose the EFI OS option.
- Follow the install process for your distribution!
# Questions you will probably ask.
- Q: Why did you create this?
- A: I installed linux a bunch of times on my friend´s laptop, without any USB, just booting from EFI files natively. When i got my PC that came with Windows 10, i was excited to install Linux on it, but was dissapointed because of my motherboard not having a option to boot from EFI files. I then remembered this frustation a few days ago, and decided to bring the fix to life!
- Q: Why python?
- A: Python was the easiest option.
# License
The license that this project is using, is MIT, you can see the details of the license on the section for the License.
# Why is there no more files on the source code?
Removed all the added files because the source code was getting messy, and the powershell script is now deprecated so there is now no use for the versions folder.
If you want to compile the .exe file yourself, there's a tutorial here: https://github.com/CharaDreemurrUTnDT/LinuxDBAssistant/blob/main/Compiling.md
# Distros that do not support this method
- Debian
- EndeavourOS
