![12 Sem Título_20250618230020](https://github.com/user-attachments/assets/d10c7e4b-277f-4d3c-aa88-7e337493b545)


This is for assisting Windows Users to install Linux on their machines without a USB.

[![License](https://img.shields.io/github/license/CharaUTnDT/LinuxDBAssistant)](https://github.com/CharaUTnDT/LinuxDBAssistant/blob/main/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/CharaUTnDT/LinuxDBAssistant?label=release)](https://github.com/CharaUTnDT/LinuxDBAssistant/releases)
[![Issues](https://img.shields.io/github/issues/CharaUTnDT/LinuxDBAssistant)](https://github.com/CharaUTnDT/LinuxDBAssistant/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/CharaUTnDT/LinuxDBAssistant)](https://github.com/CharaUTnDT/LinuxDBAssistant/pulls)
[![Contributors](https://img.shields.io/github/contributors/CharaUTnDT/LinuxDBAssistant)](https://github.com/CharaUTnDT/LinuxDBAssistant/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/CharaUTnDT/LinuxDBAssistant?style=flat-square)](https://github.com/CharaUTnDT/LinuxDBAssistant/network/members)
[![Stars](https://img.shields.io/github/stars/CharaUTnDT/LinuxDBAssistant?style=flat-square)](https://github.com/CharaUTnDT/LinuxDBAssistant/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/CharaUTnDT/LinuxDBAssistant)](https://github.com/CharaUTnDT/LinuxDBAssistant/commits)
[![Last Release Date](https://img.shields.io/github/release-date/CharaUTnDT/LinuxDBAssistant)](https://github.com/CharaUTnDT/LinuxDBAssistant/releases)
# Options
- Extract the ISO to a specific partition using 7zip or NanaZip (7zip needs to be on the path.)
- Verify ISO Integrity (It needs to be a sha256 or md5 hash, OpenPGP support is planned)
- Change Local Time to UTC Time (Proceed with caution!) (I think if you dual booted before you noticed the time was off every restart you did to Windows. Well, with this option, both Linux and Windows will be using UTC time, which means, no more errors in time with this!)
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
- A: I got frustrated because i couldn´t install linux without a USB on my PC, so i decided to do some research and bring the fix to life.
- Q: Why python?
- A: I heard a bunch of times that Python is good for beginners. 
# License
[![License](https://img.shields.io/github/license/CharaUTnDT/LinuxDBAssistant)](https://github.com/CharaUTnDT/LinuxDBAssistant/blob/main/LICENSE)
# [Unsupported Distros](https://github.com/CharaUTnDT/LinuxDBAssistant/blob/main/UnsupportedDistros.md)
