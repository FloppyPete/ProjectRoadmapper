@echo off
REM Launch ProjectRoadmapper Dashboard
REM Double-click this file to start the dashboard

echo Starting ProjectRoadmapper Dashboard...
echo.

python launch_dashboard.py

if errorlevel 1 (
    echo.
    echo Error: Could not start dashboard.
    echo Make sure Python and roadmapper are installed.
    echo.
    pause
)

