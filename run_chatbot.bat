@echo off
echo ========================================
echo    Tutor Chatbot - Local Runner
echo ========================================
echo.
echo Choose your interface:
echo 1. FastAPI (Full Web Interface) - Recommended
echo 2. Gradio (Simple Interface)
echo.
set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Starting FastAPI interface...
    python run_local.py --interface fastapi
) else if "%choice%"=="2" (
    echo.
    echo Starting Gradio interface...
    python run_local.py --interface gradio
) else (
    echo Invalid choice. Starting FastAPI by default...
    python run_local.py --interface fastapi
)

pause