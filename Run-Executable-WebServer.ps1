# Define the URL to the .exe file on the web server
$exeUrl = "https://raw.githubusercontent.com/CharaDreemurrUTnDT/LinuxDBAssistant/refs/heads/main/versions/0.0.5/db-assistant-0.0.5.exe"

# Define the local path where the .exe will be downloaded
$localExePath = "C:\linuxinstaller\linuxinstaller.exe"

# Extract the folder path from the localExePath
$localFolderPath = Split-Path -Path $localExePath

# Optional: Add arguments to pass to the .exe
# Leave $arguments empty if no arguments are needed
$arguments = ""

# Check if the folder exists, and create it if it doesn't
if (-Not (Test-Path -Path $localFolderPath)) {
    Write-Host "Folder $localFolderPath does not exist. Creating it now..." -ForegroundColor Yellow
    try {
        New-Item -ItemType Directory -Path $localFolderPath -Force | Out-Null
        Write-Host "Folder created successfully." -ForegroundColor Green
    } catch {
        Write-Host "An error occurred while trying to create the folder: $_" -ForegroundColor Red
        exit
    }
}

# Download the .exe file from the web server
try {
    Write-Host "Downloading the executable from $exeUrl to $localExePath..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $exeUrl -OutFile $localExePath
    Write-Host "Download completed successfully." -ForegroundColor Green
} catch {
    Write-Host "An error occurred while downloading the executable: $_" -ForegroundColor Red
    exit
}

# Check if the .exe file exists locally after download
if (Test-Path $localExePath) {
    Write-Host "Found downloaded executable at $localExePath. Attempting to run it..." -ForegroundColor Green

    try {
        # Start the .exe with optional arguments
        Start-Process -FilePath $localExePath -ArgumentList $arguments -NoNewWindow -Wait
        Write-Host "Executable ran successfully." -ForegroundColor Green
    } catch {
        Write-Host "An error occurred while trying to run the executable: $_" -ForegroundColor Red
    }
} else {
    Write-Host "The downloaded executable file was not found at $localExePath. Please check the path and try again." -ForegroundColor Red
}
