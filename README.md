# Multi-Source Data Engineering Framework & AI Auditor

Technical implementations of automated data workflows and processing pipelines designed for high-reliability data environments. This framework bridges the gap between **Data Engineering efficiency** and **Data Science rigor** through two distinct execution paradigms: **Legacy Local Automation** for zero-overhead desktop tasks and **Modern CI/CD** for production-grade, self-hosted orchestration.

## 🎯 Project Philosophy: From Local to CI/CD
Most modern pipelines are over-engineered with heavy dependencies. This project demonstrates a **high-performance, low-footprint architecture** optimized for native environments. By migrating from heavy Docker/WSL/Airflow setups to a native Windows environment—and eventually to a structured **Azure DevOps CI/CD pipeline**—I achieved a **95% reduction in RAM overhead** (from 4GB+ to <200MB) while maintaining production-grade reliability and real-time monitoring.

The framework proves that reliability doesn't require high resource costs; it requires precise orchestration, whether via **Windows Task Scheduler** for local agility or **Azure Pipelines** for automated, secret-managed deployment.

---

## 🏗️ System Architecture
The framework orchestrates data through four specialized layers:
1. **Ingestion Layer:** Multi-protocol support for REST APIs (JSON) and legacy flat files (CSV).
2. **Validation Layer (The Gatekeeper):** A custom Data Quality suite (`data_validator.py`) that enforces schema integrity and logical consistency before database commits.
3. **Persistence Layer:** Structured relational storage using MySQL.
4. **Audit & Alerting:** A Slack-integrated monitoring system that detects statistical anomalies and pushes real-time notifications.

---

## 🔄 The Pipelines
* **University Intelligence Pipeline:** Consumes nested JSON from REST APIs, transforming complex nested lists into relational strings and optimized SQL tables.
* **Titanic Historical Flow:** Ingests raw passenger data from public CSV sources into MySQL, featuring automated handling of missing values for historical analysis.
* **Data Quality Validator:** A specialized script (`data_validator.py`) that acts as a pre-load gatekeeper, checking for data types, range constraints, and schema drifts.
* **Automated Data Auditor:** Monitors transaction tables (e.g., `sakila.payment`) for anomalies like high-value payments, sending instant alerts via the Slack API.
* **Duplicate Detection System:** A data integrity script (`dup_pipeline.py`) that scans ingested datasets for redundant records, ensuring a "Single Source of Truth".

---

## 🚀 Orchestration & Deployment Methods

This framework supports two distinct deployment patterns:

### 1. Legacy Method: Windows Task Scheduler & Batch
The original implementation utilizes native Windows tools to minimize background resource consumption.
* **Trigger:** A master `run_all_pipelines.bat` script handles the execution sequence.
* **Scheduler:** Windows Task Scheduler triggers the batch file at defined intervals.
* **Execution:** Runs locally under the user's security context.
* **Best For:** Low-complexity, single-user desktop environments where overhead must be near zero.

### 2. Modern Method: Azure DevOps CI/CD (Self-Hosted)
The current production implementation uses an `azure-pipelines.yml` configuration with a self-hosted agent named `MyLocalLaptop`.
* **Triggers:**
    * **CI:** Automatic runs triggered by every `push` or `PR` to the `main` branch.
    * **Scheduled:** Daily automated execution at 02:00 UTC via Cron.
* **Security:** Secrets (DB credentials, Slack tokens) are managed in Azure DevOps **Variable Groups** (`Pipeline-Secrets`) and injected at runtime into a secure `.env` file.
* **Environment:** Configured to use a dedicated public Python path (`C:\Python312`) to bypass Windows user-profile permission restrictions and solve "Access is denied" errors.
* **Encoding:** Implements `PYTHONUTF8: 1` to ensure special characters (emojis/audit symbols) render correctly across