@echo off
:: 1. Navigate to your project folder
cd /d "C:\Users\ADMIN\My Drive\Python\pipeline\dags\run_auditor.bat"

:: 2. Activate the virtual environment and run the script
call .\venv\Scripts\activate
python dags\Auditor.py

:: 3. Optional: pause (only use this for testing to see the terminal window)
:: pause