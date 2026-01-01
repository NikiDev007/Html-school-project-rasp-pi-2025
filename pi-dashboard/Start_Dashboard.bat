@echo off
title PiStatus Dashboard - Starter
color 0B

echo =======================================================
echo          PISTATUS DASHBOARD - STARTER
echo =======================================================
echo.

:: Schritt 1: Pruefen ob Python installiert ist
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python wurde nicht gefunden! 
    echo Bitte installieren Sie Python von python.org
    pause
    exit
)

:: Schritt 2: Bibliotheken installieren/pruefen
echo [1/3] Pruefe und installiere Bibliotheken (Flask, psutil)...
pip install flask psutil --quiet
if %errorlevel% neq 0 (
    echo [WARNUNG] Fehler beim Installieren der Bibliotheken. 
    echo Versuche fortzufahren...
)

:: Schritt 3: Kurze Pause und Browser oeffnen
echo [2/3] Oeffne Browser...
timeout /t 3 /nobreak > nul
start http://127.0.0.1:5000

:: Schritt 4: Flask Server starten
echo [3/3] Starte Backend-Server (app.py)...
echo.
echo -------------------------------------------------------
echo Server laeuft! Schliessen Sie dieses Fenster zum Beenden.
echo -------------------------------------------------------
echo.
python app.py

pause