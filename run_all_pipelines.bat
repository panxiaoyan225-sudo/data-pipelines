@echo off
:: 1. Navigate to the main pipeline folder
cd /d "C:\Users\ADMIN\My Drive\Python\pipeline"

:: 2. Activate the virtual environment
call .\venv\Scripts\activate

:: 3. Run scripts from the NEW /dags subfolder
python .\pipeline_py\titanic_pipeline.py
python .\pipeline_py\ranking_pipeline.py
python .\pipeline_py\auditor.py
python .\pipeline_py\dup_pipelines.py

pause