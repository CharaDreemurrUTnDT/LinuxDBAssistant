# LinuxDBAssistant Launcher - PowerShell Script (EXE only, downloads from internet links)
# Edit the URLs below to point to your .exe files online.

function Show-Menu {
    Clear-Host
    Write-Host ""
    Write-Host "`e[38;5;146m _      _                  _____  ____                  _     _              _   " 
    Write-Host " | |    (_)                |  __ \|  _ \   /\           (_)   | |            | |  " 
    Write-Host " | |     _ _ __  _   ___  _| |  | | |_) | /  \   ___ ___ _ ___| |_ __ _ _ __ | |_ " 
    Write-Host " | |    | | '_ \| | | \ \/ / |  | |  _ < / /\ \ / __/ __| / __| __/ _` | '_ \| __|" 
    Write-Host " | |____| | | | | |_| |>  <| |__| | |_) / ____ \\__ \__ \ \__ \ || (_| | | | | |_ " 
    Write-Host " |______|_|_| |_|\__,_/_/\_\_____/|____/_/    \_\___/___/_|___/\__\__,_|_| |_|\__|`e[0m"
    Write-Host ""
    Write-Host "`e[38;5;146mMade by CharaUTnDT on Github`e[0m"
    Write-Host ""
    Write-Host "`e[38;5;146mChoose a version to run:`e[0m"
    Write-Host "`e[38;5;146m[1] GUI Version (Windows)`e[0m"
    Write-Host "`e[38;5;146m[2] Terminal Version (Windows, Colored)`e[0m"
    Write-Host "`e[38;5;146m[3] Terminal Version (Windows, Non Colored)`e[0m"
    Write-Host "`e[38;5;146m[4] Exit`e[0m"
    Write-Host ""
}

function Get-And-Run {
    param(
        [string]$url,
        [string]$filename
    )
    $tempPath = "$env:TEMP\$filename"
    if (!(Test-Path $tempPath)) {
        Write-Host "`e[38;5;146mDownloading $filename...`e[0m"
        try {
            Invoke-WebRequest -Uri $url -OutFile $tempPath
        } catch {
            Write-Host "`e[31mFailed to download $filename. Check your internet connection or the link.`e[0m"
            return
        }
    } else {
        Write-Host "`e[38;5;146m$filename already downloaded.`e[0m"
    }
    Start-Process wt.exe -ArgumentList $tempPath
}

function Start-GUI {
    # Replace the URL below with your GUI .exe download link
    $guiUrl = "https://tinyurl.com/db-assistant-gui"
    Get-And-Run -url $guiUrl -filename "db-assistant-2.1.exe"
}

function Start-Terminal-Colored {
    # Replace the URL below with your colored terminal .exe download link
    $termUrl = "https://tinyurl.com/db-assistant-terminal"
    Get-And-Run -url $termUrl -filename "db-assistant-terminal-2.1.exe"
}

function Start-Terminal-NonColored {
    # Replace the URL below with your non-colored terminal .exe download link
    $termUrl = "https://tinyurl.com/db-assistant-nc"
    Get-And-Run -url $termUrl -filename "db-assistant-2.1-terminal-nc.exe"
}

do {
    Show-Menu
    $choice = Read-Host "Enter your choice"
    switch ($choice) {
        "1" { Start-GUI }
        "2" { Start-Terminal-Colored }
        "3" { Start-Terminal-NonColored }
        "4" { Write-Host "`e[38;5;146mGoodbye!`e[0m"; break }
        default { Write-Host "`e[31mInvalid choice. Please try again.`e[0m" }
    }
    if ($choice -ne "4") {
        Write-Host ""
        Write-Host "`e[38;5;146mPress Enter to return to the menu...`e[0m"
        [void][System.Console]::ReadLine()
    }
} while ($choice -ne "4")