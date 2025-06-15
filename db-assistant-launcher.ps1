# LinuxDBAssistant Launcher - PowerShell Script (EXE only, uses your shortened URLs)

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

function Download-And-Run {
    param(
        [string]$url,
        [string]$filename
    )
    $tempPath = "$env:TEMP\$filename"
    if (!(Test-Path $tempPath)) {
        Write-Host "`e[38;5;146mDownloading $filename...`e[0m"
        try {
            Invoke-WebRequest -Uri $url -OutFile $tempPath -UseBasicParsing
        } catch {
            Write-Host "`e[31mFailed to download $filename. Check your internet connection or the link.`e[0m"
            return
        }
    } else {
        Write-Host "`e[38;5;146m$filename already downloaded.`e[0m"
    }
    Start-Process wt.exe -ArgumentList $tempPath
}

function Run-GUI {
    $guiUrl = "https://tinyurl.com/db-assistant-gui"
    Download-And-Run -url $guiUrl -filename "LinuxDBAssistant-GUI.exe"
}

function Run-Terminal-Colored {
    $termUrl = "https://tinyurl.com/db-assistant-terminal"
    Download-And-Run -url $termUrl -filename "LinuxDBAssistant-Terminal-Colored.exe"
}

function Run-Terminal-NonColored {
    $termUrl = "https://tinyurl.com/db-assistant-nc"
    Download-And-Run -url $termUrl -filename "LinuxDBAssistant-Terminal-NonColored.exe"
}

do {
    Show-Menu
    $choice = Read-Host "Enter your choice"
    switch ($choice) {
        "1" { Run-GUI }
        "2" { Run-Terminal-Colored }
        "3" { Run-Terminal-NonColored }
        "4" { Write-Host "`e[38;5;146mGoodbye!`e[0m"; break }
        default { Write-Host "`e[31mInvalid choice. Please try again.`e[0m" }
    }
    if ($choice -ne "4") {
        Write-Host ""
        Write-Host "`e[38;5;146mPress Enter to return to the menu...`e[0m"
        [void][System.Console]::ReadLine()
    }
} while ($choice -ne "4")
