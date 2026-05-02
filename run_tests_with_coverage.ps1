# PowerShell script to run tests with coverage report
# Usage: .\run_tests_with_coverage.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Running Tests with Coverage" -ForegroundColor Cyan
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
    exit 1
}

Write-Host "Python: $pythonPath" -ForegroundColor Cyan
Write-Host ""

# Run pytest with coverage
Write-Host "Running tests with coverage..." -ForegroundColor Yellow
Write-Host ""

& $pythonPath -m pytest --cov=app --cov-report=html --cov-report=term-missing -v

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Tests Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Coverage report generated in: htmlcov/index.html" -ForegroundColor Green
Write-Host "Open it in browser to view detailed coverage." -ForegroundColor Yellow

# Made with Bob
