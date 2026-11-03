@echo off
title Avaliacao de Deteccao de Roubo - 5 Videos Reais
cd /d "%~dp0"
echo ===================================================
echo   AVALIANDO OS 5 VIDEOS DE FURTO COM A IA
echo ===================================================

set "PYTHON_EXE=python"
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"

"%PYTHON_EXE%" -m src.benchmark_5_videos
pause
