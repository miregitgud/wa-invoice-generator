@echo off
echo Building WA Invoice Generator...
python -m PyInstaller --noconsole --onefile --name "WA Invoice Generator.py" main.py
echo.
echo Build complete! Your app is in the "dist" folder.
pause