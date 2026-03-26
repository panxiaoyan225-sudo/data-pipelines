# Multi-Source Data Engineering Framework & AI Auditor

Technical implementations of automated data workflows and processing pipelines designed for high-reliability data environments. This framework bridges the gap between **Data Engineering efficiency** and **Data Science rigor** through three distinct execution paradigms: **Legacy Local Automation** for zero-overhead tasks, and **Multi-Platform CI/CD** (Azure & GitHub) for production-grade orchestration.

## 🎯 Project Philosophy: From Local to CI/CD
Most modern pipelines are over-engineered with heavy dependencies. This project demonstrates a **high-performance, low-footprint architecture** optimized for native environments. By migrating from heavy Docker/WSL setups to a native Windows environment—and orchestrating via **Azure DevOps** and **GitHub Actions**—I achieved a **95% reduction in RAM overhead** (from 4GB+ to <200MB) while maintaining real-time monitoring.

The framework proves that reliability doesn't require high resource costs; it requires precise orchestration, whether via **Windows Task Scheduler** for local agility or **Cloud-Managed Workflows** for automated, secret-managed deployment.

---

## 🏗️ System Architecture
The framework orchestrates data through four specialized layers:
1. **Ingestion Layer:** Multi-protocol support for REST APIs (JSON) and legacy flat files (CSV).
2. **Validation Layer (The Gatekeeper):** A custom Data Quality suite (`data_validator.py`) that enforces schema integrity and logical consistency.
3. **Persistence Layer:** Structured relational storage using MySQL (`sakila` and custom schemas).
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
* **Secret Management:** Individual encryption of sensitive credentials (DB_PASS, SLACK_TOKEN) via **GitHub Repository Secrets**.
* **Reliability Engineering:** * Implemented `PYTHONUTF8: 1` environment variables to ensure data integrity during audit log generation.
    * Uses a dedicated directory (`C:\actions-runner`) to separate CI/CD orchestration from core Windows system files, ensuring stable execution.

---

## 🔄 Featured Pipelines
* **University Intelligence Pipeline:** Consumes nested JSON from REST APIs, transforming complex data into optimized SQL tables.
* **Data Quality Validator:** A specialized script (`data_validator.py`) acting as a pre-load gatekeeper for schema integrity.
* **Automated Data Auditor:** Monitors transaction tables for anomalies, sending instant alerts via the Slack API.
* **Duplicate Detection System:** A data integrity script (`dup_pipeline.py`) ensuring a "Single Source of Truth".

---

## 🛠️ Technical Stack
* **Languages:** Python (ETL, Audit, Alerting)
* **Databases:** MySQL (Relational Storage)
* **DevOps:** GitHub Actions, Azure DevOps, YAML, PowerShell
* **Monitoring:** Slack API Integration
* **Environment:** Windows Native (Self-Hosted Runners)