@echo off
title SENTINELA - Sistema de Monitoramento Patrimonial
cd /d "%~dp0"
cls
echo =====================================================================
echo           SENTINELA - MONITORAMENTO DE SEGURANCA CCTV
echo =====================================================================
echo.
echo [1/3] Liberando conexoes e preparando ambiente...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /f /pid %%a >nul 2>&1
)
echo [2/3] Carregando modulos de visao computacional...
echo [3/3] Abrindo painel de monitoramento no navegador...
echo.
echo Para encerrar o sistema, feche esta janela.
echo =====================================================================
echo.
"C:\Users\hiro0007\AppData\Local\Programs\Python\Python312\python.exe" -m src.app
pause
