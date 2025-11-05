@echo off
REM Launch ProjectRoadmapper Dashboard (Silent - no console window)
REM This batch file will be hidden when launched via shortcut

REM Change to script directory
cd /d "%~dp0"

REM Run Python script
python launch_dashboard.py

if errorlevel 1 (
    REM If error, show window briefly to display error
    echo Error: Could not start dashboard.
    echo Make sure Python and roadmapper are installed.
    timeout /t 5
)
