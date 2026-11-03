@echo off
title Detector de Roubo via Camera
cd /d "%~dp0"
echo ===================================================
echo   INICIANDO DETECTOR DE ROUBO E CONDUTA SUSPEITA
echo ===================================================

set "PYTHON_EXE=python"
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"

"%PYTHON_EXE%" -m src.main
pause
