@echo off
title Avaliacao de Desempenho e Acuracia - Sentinela CCTV
cd /d "%~dp0"
echo ===================================================
echo   AVALIANDO VIDEOS DO GABARITO COM O SENTINELA
echo ===================================================

set "PYTHON_EXE=python"
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"

"%PYTHON_EXE%" scripts\benchmark.py
pause
