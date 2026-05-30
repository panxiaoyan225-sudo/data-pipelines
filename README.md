Your updated Markdown file is ready for your project repository. 

I have integrated the API key management, the decoupled Python-to-SQL architecture, and the cross-database native linking scenario (along with its architectural connection to Azure Data Factory Linked Services). I also added a clean, professional **Repository Structure tree map** that precisely highlights your new files and folders, which is a major bonus for interviewers reviewing your GitHub profile.

### Raw Markdown File
[file-tag: code-generated-file-0-1780152980968482768]

```markdown
# Multi-Source Data Engineering Framework & AI Auditor
[🚀 View Data Pipeline Infographic](https://panxiaoyan225-sudo.github.io/data-pipelines/data_infographic.html)

Technical implementations of automated data workflows, secure API ingestions, and processing pipelines designed for high-reliability data environments. This framework bridges the gap between **Data Engineering efficiency** and **Data Science rigor** through three distinct execution paradigms: **Legacy Local Automation** for zero-overhead tasks, **Cross-Database Native Linking (Pure SQL)**, and **Multi-Platform CI/CD** (Azure & GitHub) for production-grade orchestration.

## 🎯 Project Philosophy: From Local to CI/CD
This project demonstrates a **high-performance, low-footprint architecture** optimized for native environments. By migrating from heavy Docker/WSL setups to a native Windows environment—and orchestrating via **Azure DevOps** and **GitHub Actions** — I achieved a **95% reduction in RAM overhead** (from 4GB+ to <200MB) while maintaining real-time monitoring.

The framework proves that reliability doesn't require high resource costs; it requires precise orchestration, whether via **Windows Task Scheduler** for local agility or **Cloud-Managed Workflows** for automated, secret-managed deployment.

---

## 🏗️ System Architecture
The framework orchestrates data through four specialized layers:
1. **Ingestion Layer:** Multi-protocol support for REST APIs (JSON) using secure bearer token authentication and legacy flat files (CSV).
2. **Validation Layer (The Gatekeeper):** A custom Data Quality suite (`data_validator.py`) that enforces schema integrity and logical consistency.
3. **Persistence & Linkage Layer:** Structured relational storage using SQLite / MySQL alongside decoupled database-to-database connectivity models.
4. **Audit & Alerting:** A Slack-integrated monitoring system that detects statistical anomalies and pushes real-time notifications.

---

## 🚀 Orchestration & Deployment Methods

### 1. Legacy Method: Windows Task Scheduler
The original implementation utilizes native Windows tools to minimize background resource consumption.
* **Trigger:** A master `run_all_pipelines.bat` script handles the execution sequence.
* **Execution:** Scheduled local execution under the user's security context.

### 2. Enterprise Method: Azure DevOps CI/CD
The first production migration used `azure-pipelines.yml` with a self-hosted agent.
* **Security:** Secrets managed in **Variable Groups** (`Pipeline-Secrets`).
* **Environment:** Optimized to bypass Windows user-profile permission restrictions.

### 3. Modern Method: GitHub Actions (Self-Hosted Service)
The current implementation utilizes GitHub Actions for decentralized automation.
* **Runner Architecture:** Implemented a **self-hosted runner** configured as a **Windows Service** (`MyLocalLaptop`) for 99.9% availability without manual terminal sessions.
* **Secret Management:** Individual encryption of sensitive credentials (DB_PASS, SLACK_TOKEN, API_KEY) via **GitHub Repository Secrets**.
* **Reliability Engineering:** * Implemented `PYTHONUTF8: 1` environment variables to ensure data integrity during audit log generation.
    * Uses a dedicated directory (`C:\actions-runner`) to separate CI/CD orchestration from core Windows system files, ensuring stable execution.

---

## 🔄 Featured Pipelines & Scenarios

### Scenario 1 & 2: Decoupled API Ingestion & Relational Staging (Python to SQL)
Demonstrates secure production-grade API harvesting and transactional staging. The logic is strictly **decoupled** into modular scripts inside the folder structure to prevent cross-contamination if upstream schemas change.
* **Extraction (`api_pipeline.py`):** Dynamically injects secure tokens via `.env` management, builds professional standard request headers with a 10-second request timeout, and executes strict exception handling (`HTTPError`, `ConnectionError`).
* **Ingestion (`Python to SQL.py`):** Imports the extraction logic as a module, generates parameterized SQL injection guardrails, maps incoming nested JSON objects dynamically to an atomic tabular schema, handles execution rollback on transaction failure, and enforces explicit cursor lifecycle drops.

### Scenario 3: Database-to-Database Native Link (Pure SQL)
Demonstrates cross-database connectivity inside the database engine layer without the overhead of application code. Maps directly to the conceptual architecture of creating **Linked Services** and **Datasets** inside cloud orchestrators like **Azure Data Factory (ADF)**.
* **Script (`database_link.sql`):** Establishes an atomic mapping (`ATTACH DATABASE`) to simulate external siloed architectures (e.g., Inventory, ERP systems), executes transactional joins across distinct logical databases via 4-part name aliases (`main` vs `RemoteInventoryDB`), and triggers clean post-execution connection detachment (`DETACH`).
* **Execution Engine (`run_sql_link.py`):** A custom compilation module that filters out structural SQL metadata/comments (`--`) before execution to eliminate cursor driver crashes, parsing instructions sequentially while trapping real-time output.

---

## 📁 Repository Structure
```text
pipeline/
│
├── .env                         # Local Secret Configuration (Excluded from Git)
├── .gitignore                   # Safe configuration guardrails
├── practice_warehouse.db        # Simulated target Analytics Data Warehouse
│
└── APIKey_DataConection/        # 🛠️ Secure Connection & API Practice Modules
    ├── api_pipeline.py          # Scenario 1: Secure REST API Harvester
    ├── Python to SQL.py         # Scenario 2: Decoupled SQL Injection Guarded Ingestor
    ├── check_db_data.py         # Validation Module: Cursor Fetch Auditor
    ├── database_link.sql        # Scenario 3: Pure Cross-DB Link Query Matrix
    └── run_sql_link.py          # SQL Comment-Filtered Execution Engine