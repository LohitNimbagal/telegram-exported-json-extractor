@echo off
setlocal

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

:: Check if result.json exists, if not use example if available
if not exist "result.json" (
    if exist "example_result.json" (
        echo Warning: result.json not found. Using example_result.json...
        copy "example_result.json" "result.json" >nul
    ) else (
        echo Error: result.json not found and no example file exists.
        echo Please follow the instructions in README.md to export your chat.
        pause
        exit /b 1
    )
)

:: Run the extractor
python extractor.py %*

pause
