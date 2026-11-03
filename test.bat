@echo off
title Teste do Pipeline de Camera e Video
cd /d "%~dp0"
echo ===================================================
echo   TESTANDO CAMERAS E GERANDO VIDEO DE TESTE
echo ===================================================

set "PYTHON_EXE=python"
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"

"%PYTHON_EXE%" -m src.test_pipeline
pause
