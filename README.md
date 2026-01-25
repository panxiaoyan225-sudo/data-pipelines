# Multi-Source Data Pipeline & Automated Auditor

This project demonstrates a professional-grade ETL (Extract, Transform, Load) workflow developed in Python and SQL. It features automated data ingestion from multiple sources and a Slack-integrated audit system for data quality monitoring.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Database:** MySQL (Sakila Schema)
* **Automation:** Windows Task Scheduler & Batch Scripting
* **Alerting:** Slack API (Real-time notifications)
* **Environment:** Native Windows (optimized for performance over WSL/Docker)

## 🔄 The Pipelines
1. **Titanic Data Flow:** Ingests raw passenger data from public CSV sources into MySQL for historical analysis.
2. **University Ranking Pipeline:** Consumes JSON data from a REST API, transforms complex nested lists into relational strings, and loads them into a structured database.
3. **Data Auditor:** A specialized script that monitors the `sakila.payment` table for anomalies (e.g., high-value payments) and sends instant alerts to a dedicated Slack channel.
4. **Duplicate Detection System:** A data integrity script (`dup_pipeline.py`) that scans ingested datasets for redundant records, ensuring the "Single Source of Truth" within the MySQL environment.

## 🚀 Key Improvements
* **Performance:** Migrated from a heavy Docker/WSL/Airflow setup to a native Windows environment, reducing RAM usage by **~95%** (from 4GB+ to <200MB).
* **Automation:** Implemented a master `.bat` file for daily execution via Task Scheduler, ensuring consistent data updates without manual intervention.
* **Slack:** Slack-integrated audit system for data quality monitoring

## 📁 Project Structure
* `/pipeline_py`: Primary Python logic for all ETL processes, including `dup_pipeline.py`.
* `/AI_example`: Isolated laboratory environment for experimental AI and data science learning.
* `/statistics`: Python scripts focused on database operations and efficient data handling.
* `run_all_pipelines.bat`: The master automation trigger.