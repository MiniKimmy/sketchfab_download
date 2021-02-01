@echo off
chcp 65001

.\bin\py\python.exe ./code/main.py
if ERRORLEVEL 1 (
	goto:end
)

color A

echo [32m!!!!!!!!!DOWNLOAD SUCCESSS!!!!!!!!![0m
echo [32m!!!!!!!!!DOWNLOAD SUCCESSS!!!!!!!!![0m
echo [32m!!!!!!!!!DOWNLOAD SUCCESSS!!!!!!!!![0m

:end
pause
