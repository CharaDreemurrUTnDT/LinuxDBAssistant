# LinuxDBAssistant
This is for assisting Windows Users to Dual Boot Windows and Linux without an USB Drive, giving them options to assist them!
# Options
Open Disk management
Extract the iso to a specific partition using 7zip (7zip needs to be on the PATH)
Verify ISO Integrity (This option is still a WIP, so i havent tested it yet)
Install reFInd boot manager!
# Requirements
- Python (If you are using the .py file)
- 7zip added to PATH
- UEFI Bios. This will not work for Legacy Bios or UEFI-CSM.
# Guide 
- First, shrink your C: Drive for free space for Linux and the partition the ISO is gonna be stored in.
- Create a partition, the size depends on the size of the distributions´s iso. (I personally recommend FAT32 for the format, if there is a file bigger than 4GB on your distribution´s iso, use NTFS.)
- Extract the ISO to the partition youve created using the extract iso option.
- Install reFInd using the Install reFInd option.
- Boot to reFInd.
- Choose the efi file on the partition you created. (If it doesn´t work, try another file!)
- Follow the install process for your distribution!
# Questions you will probably ask.
Q: Why did you create this?
A: I installed linux a bunch of times on my friend´s laptop, without any USB, just booting from EFI files natively. When i got my PC that came with Windows 10, i was excited to install Linux on it, but was dissapointed because of my motherboard not having a option to boot from EFI files. I then remembered this frustation a few days ago, and decided to bring the fix to life!
Q:Why reFInd boot manager?:
A: bcdedit was giving too many error, and reFInd detects every efi file.
Q: Why python?
A: Python was the easiest option.
# License
The license that this project is using, is MIT, you can see the details of the license on the section for the License.
