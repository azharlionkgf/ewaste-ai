@echo off
title E-Waste Intelligence System - By Azhar Fareed Mulla
echo.
echo  ======================================================
echo   ⚡ E-WASTE INTELLIGENCE SYSTEM
echo   By: Azhar Fareed Mulla (2SA25MC002)
echo   Guide: Dr. Nisha S Amin
echo  ======================================================
echo.
echo  Starting application on port 8501...
echo  Open browser: http://localhost:8501
echo.
cd /d "%~dp0"
streamlit run app/streamlit_app.py --server.port 8501 --server.headless true --browser.gatherUsageStats false
pause
