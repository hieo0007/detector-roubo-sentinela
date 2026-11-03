@echo off
title Avaliacao de Deteccao de Roubo - 5 Videos Reais
cd /d "%~dp0"
echo ===================================================
echo   AVALIANDO OS 5 VIDEOS DE FURTO COM A IA
echo ===================================================
"C:\Users\hiro0007\AppData\Local\Programs\Python\Python312\python.exe" -m src.benchmark_5_videos
pause
