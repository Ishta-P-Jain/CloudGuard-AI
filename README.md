# CloudGuard AI - Cloud Security Auditing Platform

CloudGuard AI is a lightweight, AI-powered cloud security posture management (CSPM) tool. It automatically scans cloud infrastructures, calculates security risk scores, lists detailed vulnerability findings, and leverages Groq's LLM API to provide on-demand remediation guidelines—caching the AI explanations locally to control API costs.

Live on : https://cloudguard-ai-three.vercel.app/

---

## 🚀 Key Features

* **Simulated Cloud Auditing**: Audits AWS environments simulated via **LocalStack** (S3, IAM, and EC2 resources) without incurring real cloud costs.
* **10-Point Rule Engine**: Scans for common cloud misconfigurations:
  * Public S3 bucket access & public write permissions
  * Missing bucket default encryption
  * IAM users lacking Multi-Factor Authentication (MFA)
  * Overly permissive wildcard policies & root administrator privileges
  * Security groups exposing SSH (Port 22) or RDP (Port 3389) publicly
* **Dynamic Security Scoring**: Calculates a risk rating from `0-100` based on the count and severity of active findings.
* **On-Demand AI Explanations & Caching**: Connects to the **Groq API** (`llama3-8b-8192` model) to deliver custom remediation steps. It implements database caching to avoid duplicate API calls and a **50-request daily cap** to control API usage costs.
* **PDF Report Compilation**: Generates professional PDF security scan reports with integrated risk distribution pie charts, color-coded summaries, and remediation checklists.
* **Historical Audit Tracking**: Maintains a persistent history of previous scan runs, severity breakdowns, and scores in a **PostgreSQL** database.

---

## 🛠️ Technology Stack

* **Frontend**: React (Vite), Tailwind CSS, Recharts (Risk graphs), React Router.
* **Backend**: FastAPI (Python), SQLAlchemy (ORM), Pydantic (Data validation).
* **Database**: PostgreSQL (Persistence).
* **Infrastructure / Utilities**: LocalStack (Docker container), Boto3 (AWS SDK), ReportLab (PDF compiler).
* **AI Provider**: Groq Cloud API.

---

## 📂 Repository Structure

```text
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes (scans, findings, reports)
│   │   ├── cloud/        # Boto3 LocalStack resource collectors
│   │   ├── models/       # SQLAlchemy PostgreSQL ORM models
│   │   ├── schemas/      # Pydantic validation schemas
│   │   ├── services/     # AI service, PDF reports, and Scanner controls
│   │   ├── database.py   # DB configuration & sessions
│   │   ├── main.py       # FastAPI application entry point
│   ├── tests/            # Automated Pytest test suite (32 unit tests)
│   ├── requirements.txt  # Python packages
│   └── .env.example      # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/   # UI elements (Score, charts, findings table)
│   │   ├── pages/        # Dashboard, History, Reports views
│   │   ├── lib/          # Normalization utilities
│   ├── package.json
└── docker-compose.yml    # LocalStack orchestrator
