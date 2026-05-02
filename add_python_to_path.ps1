# PowerShell Script to automatically add Python to PATH
# Run this script with Administrator privileges

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Add Python 3.13.3 to PATH" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Possible Python paths
$possiblePaths = @(
    "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python313",
    "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python313\Scripts",
    "C:\Python313",
    "C:\Python313\Scripts"
)

Write-Host "Searching for Python..." -ForegroundColor Yellow

$foundPaths = @()

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        Write-Host "Found: $path" -ForegroundColor Green
        $foundPaths += $path
    }
}

if ($foundPaths.Count -eq 0) {
    Write-Host "Python 3.13.3 not found!" -ForegroundColor Red
    Write-Host "Please check your Python installation path." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "You can find Python with this command:" -ForegroundColor Cyan
    Write-Host 'Get-ChildItem -Path "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\" -Recurse -Filter "python.exe" | Select-Object FullName' -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "Paths to be added to PATH:" -ForegroundColor Cyan
foreach ($path in $foundPaths) {
    Write-Host "   - $path" -ForegroundColor White
}

Write-Host ""
$confirm = Read-Host "Do you want to add these paths to PATH? (Y/N)"

if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "Operation cancelled." -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "Adding to PATH..." -ForegroundColor Yellow

try {
    # Get current User PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    
    # Check if paths already exist
    $pathsToAdd = @()
    foreach ($path in $foundPaths) {
        if ($currentPath -notlike "*$path*") {
            $pathsToAdd += $path
        } else {
            Write-Host "Path already exists: $path" -ForegroundColor Yellow
        }
    }
    
    if ($pathsToAdd.Count -eq 0) {
        Write-Host "All Python paths already in PATH!" -ForegroundColor Green
    } else {
        # Add new paths
        $newPath = $currentPath
        foreach ($path in $pathsToAdd) {
            if ($newPath -ne "") {
                $newPath += ";"
            }
            $newPath += $path
            Write-Host "Added: $path" -ForegroundColor Green
        }
        
        # Update PATH
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Host ""
        Write-Host "Successfully added Python to PATH!" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Complete!" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "IMPORTANT:" -ForegroundColor Yellow
    Write-Host "   1. Close current PowerShell/CMD" -ForegroundColor White
    Write-Host "   2. Open NEW PowerShell/CMD" -ForegroundColor White
    Write-Host "   3. Run: python --version" -ForegroundColor White
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "   cd e:\project\IBM_Hackathon" -ForegroundColor White
    Write-Host "   python -m pip install -r requirements.txt" -ForegroundColor White
    Write-Host "   python -m pytest" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run PowerShell as Administrator:" -ForegroundColor Yellow
    Write-Host "   1. Press Windows + X" -ForegroundColor White
    Write-Host "   2. Select 'Windows PowerShell (Admin)'" -ForegroundColor White
    Write-Host "   3. Run this script again" -ForegroundColor White
    exit 1
}

# Made with Bob
