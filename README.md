# Multi-Source Data Engineering Framework & AI Auditor

Technical implementations of automated data workflows and processing pipelines designed for high-reliability data environments. This framework bridges the gap between **Data Engineering efficiency** and **Data Science rigor** through automated data quality (DQ) and real-time anomaly detection.

## 🎯 Project Philosophy
Most modern pipelines are over-engineered with heavy dependencies. This project demonstrates a **high-performance, low-footprint architecture** optimized for native environments. By migrating from heavy Docker/WSL/Airflow setups to a native environment, I achieved a **95% reduction in RAM overhead** (from 4GB+ to <200MB) while maintaining production-grade reliability.



## 🏗️ System Architecture
The framework orchestrates data through four specialized layers:
1. **Ingestion Layer:** Multi-protocol support for REST APIs (JSON) and legacy flat files (CSV).
2. **Validation Layer (The Gatekeeper):** A custom Data Quality suite (`data_validator.py`) that enforces schema integrity and logical consistency before database commits.
3. **Persistence Layer:** Structured relational storage using MySQL and SQLite.
4. **Audit & Alerting:** A Slack-integrated monitoring system that detects statistical anomalies and pushes real-time notifications.

## 🔄 The Pipelines
* **University Intelligence Pipeline:** Consumes nested JSON from REST APIs, transforming complex nested lists into relational strings and optimized SQL tables.
* **Titanic Historical Flow:** Ingests raw passenger data from public CSV sources into MySQL, featuring automated handling of missing values for historical analysis.
* **Data Quality Validator:** A specialized script (`data_validator.py`) that acts as a pre-load gatekeeper, checking for data types, range constraints, and schema drifts.
* **Automated Data Auditor:** Monitors transaction tables (e.g., `sakila.payment`) for anomalies like high-value payments, sending instant alerts via the Slack API.
* **Duplicate Detection System:** A data integrity script (`dup_pipeline.py`) that scans ingested datasets for redundant records, ensuring a "Single Source of Truth."

## 🛠️ Tech Stack
* **Languages:** Python 3.10+, SQL
* **Databases:** MySQL, SQLite
* **Orchestration:** Windows Task Scheduler & Batch Scripting
* **Alerting:** Slack API (Real-time notifications)

## 📁 Project Structure
* `/pipeline_py`: Primary Python logic for ETL processes and `dup_pipeline.py`.
* `/statistics`: Scripts focused on database operations and efficient data handling.
* `run_all_pipelines.bat`: The master automation trigger.
* `data_validator.py`: The validation engine for automated DQ checks.