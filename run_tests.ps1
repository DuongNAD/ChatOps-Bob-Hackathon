# PowerShell script to run tests easily
# Usage: .\run_tests.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Running Tests for IBM Hackathon" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (Test-Path ".\venv\Scripts\python.exe") {
    Write-Host "Using virtual environment..." -ForegroundColor Green
    $pythonPath = ".\venv\Scripts\python.exe"
} elseif (Test-Path "C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe") {
    Write-Host "Using system Python..." -ForegroundColor Yellow
    $pythonPath = "C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe"
} else {
    Write-Host "Python not found!" -ForegroundColor Red
    Write-Host "Please install Python or check the path." -ForegroundColor Yellow
    exit 1
}

Write-Host "Python: $pythonPath" -ForegroundColor Cyan
Write-Host ""

# Run pytest
Write-Host "Running tests..." -ForegroundColor Yellow
Write-Host ""

& $pythonPath -m pytest -v

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Tests Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Made with Bob
