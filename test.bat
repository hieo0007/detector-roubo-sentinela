@echo off
title Teste do Pipeline de Camera e Video
cd /d "%~dp0"
echo ===================================================
echo   TESTANDO CAMERAS E GERANDO VIDEO DE TESTE
echo ===================================================
"C:\Users\hiro0007\AppData\Local\Programs\Python\Python312\python.exe" -m src.test_pipeline
pause
