$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (-not (Test-Path "venv/Scripts/python.exe")) {
    py -m venv venv
    if ($LASTEXITCODE -ne 0) { throw "Virtual environment creation failed" }
}
$boardPython = Join-Path $PSScriptRoot "venv/Scripts/python.exe"
& $boardPython -m pip install -r general/requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Package installation failed" }
Set-Location (Join-Path $PSScriptRoot "general")
& $boardPython prepare_db.py
if ($LASTEXITCODE -ne 0) { throw "Database setup failed: check PostgreSQL and general/.env" }
& $boardPython verify_board.py
if ($LASTEXITCODE -ne 0) { throw "Board verification failed" }
Start-Process -FilePath $boardPython -ArgumentList "app.py" -WorkingDirectory (Join-Path $PSScriptRoot "monitor/backend")
Start-Process "http://127.0.0.1:5100/"
& $boardPython app.py
