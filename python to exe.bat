@echo off
REM ======================================================
REM Build Script for Directory Tree Generator
REM Packages Python script to Windows executable (.exe)
REM ======================================================

setlocal

REM Set Python script name
set SCRIPT_NAME=generate_dir_tree.py

REM Set output directory
set OUTPUT_DIR=dist

REM Check if PyInstaller is installed
echo Checking PyInstaller installation...
pip show pyinstaller > nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
) else (
    echo PyInstaller is already installed.
)

REM Create output directory
if not exist "%OUTPUT_DIR%" (
    mkdir "%OUTPUT_DIR%"
)

REM Build command - create single file executable
echo Building single-file executable...
pyinstaller ^
    --onefile ^
    --name "DirTreeGenerator" ^
    --distpath "%OUTPUT_DIR%" ^
    --workpath build ^
    --specpath build ^
    --console ^
    --clean ^
    %SCRIPT_NAME%

REM Check if build succeeded
if exist "%OUTPUT_DIR%\DirTreeGenerator.exe" (
    echo.
    echo ======================================================
    echo Build successful! Executable location:
    echo %cd%\%OUTPUT_DIR%\DirTreeGenerator.exe
    echo ======================================================
) else (
    echo.
    echo Build failed. Please check error messages.
)

endlocal
pause