@echo off
:: 1. Navigate to the main pipeline folder
cd /d "C:\Users\ADMIN\My Drive\Python\pipeline"

:: 2. Activate the virtual environment
call .\venv\Scripts\activate

:: 3. Run scripts from the NEW /dags subfolder
python .\dags\titanic_pipeline.py
python .\dags\ranking_pipeline.py
python .\dags\auditor.py
python .\dags\dup_pipelines.py

pause