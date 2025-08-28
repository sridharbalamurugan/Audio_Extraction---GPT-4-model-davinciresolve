@echo off
echo Setting up DaVinci Resolve Python Scripting Environment
echo ========================================================

REM Check if DaVinci Resolve is installed
if not exist "D:\youtubevlogs\davinci\Resolve.exe" (
    echo WARNING: DaVinci Resolve not found at D:\youtubevlogs\davinci\
    echo Please verify your installation path
    pause
)

REM Set environment variables
echo Setting environment variables...
setx RESOLVE_SCRIPT_API "C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
setx RESOLVE_SCRIPT_LIB "D:\youtubevlogs\davinci\fusionscript.dll"
setx PYTHONPATH "%PYTHONPATH%;C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules\"

echo Environment variables set!

REM Create Scripts folder structure
echo Creating Scripts folder structure...
set "SCRIPTS_PATH=%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts"

if not exist "%SCRIPTS_PATH%" mkdir "%SCRIPTS_PATH%"
if not exist "%SCRIPTS_PATH%\Utility" mkdir "%SCRIPTS_PATH%\Utility"
if not exist "%SCRIPTS_PATH%\Comp" mkdir "%SCRIPTS_PATH%\Comp"
if not exist "%SCRIPTS_PATH%\Tool" mkdir "%SCRIPTS_PATH%\Tool"
if not exist "%SCRIPTS_PATH%\Edit" mkdir "%SCRIPTS_PATH%\Edit"
if not exist "%SCRIPTS_PATH%\Color" mkdir "%SCRIPTS_PATH%\Color" 
if not exist "%SCRIPTS_PATH%\Deliver" mkdir "%SCRIPTS_PATH%\Deliver"

echo Scripts folder structure created at: %SCRIPTS_PATH%

REM Install Python packages
echo Installing required Python packages...
pip install openai requests pathlib

REM Check if FFmpeg is installed
echo Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: FFmpeg not found in PATH
    echo Please install FFmpeg and add to PATH
    echo Download from: https://ffmpeg.org/download.html
) else (
    echo FFmpeg is installed and available
)

echo.
echo Setup completed!
echo.
echo Next steps:
echo 1. Copy your Python scripts to: %SCRIPTS_PATH%\Utility\
echo 2. Set your OpenAI API key: set OPENAI_API_KEY=your_key_here
echo 3. Restart DaVinci Resolve
echo 4. Test with the test_setup.py script
echo.
pause
