# Script to associate .html files with Google Chrome on Windows
# Run as Administrator for this to work

$ChromePaths = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)

$ChromePath = $null
foreach ($path in $ChromePaths) {
    if (Test-Path $path) {
        $ChromePath = $path
        Write-Host "Found Chrome at: $ChromePath"
        break
    }
}

if (-not $ChromePath) {
    Write-Host "ERROR: Google Chrome not found. Please install Chrome first."
    exit 1
}

# Check if running as admin
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "WARNING: This script should be run as Administrator."
    Write-Host "Otherwise, registry changes may fail."
    Write-Host ""
}

# Use cmd.exe to set file associations
Write-Host "Setting file associations..."

# Set the association for .html files to htmlfile
cmd /c "assoc .html=ChromeHTML" 2>$null

# Set the ftype for ChromeHTML to open with Chrome
cmd /c "ftype ChromeHTML=`"$ChromePath`" %%1" 2>$null

# Also set for .htm files
cmd /c "assoc .htm=ChromeHTML" 2>$null

Write-Host "File associations updated successfully!"
Write-Host "HTML files (.html and .htm) will now open with Google Chrome."
