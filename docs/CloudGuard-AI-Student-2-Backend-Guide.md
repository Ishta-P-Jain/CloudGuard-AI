# CloudGuard AI - Student 2 Backend Guide

Role: FastAPI, PostgreSQL, Localstack, APIs, database design, and integration layer.

You are building the middle part of CloudGuard AI. The frontend asks for data. The security engine creates findings. Your backend connects everything.

## 1. Your Role In Simple Words

You are building the server.

The server receives requests from the React dashboard, talks to Localstack, runs the security engine, saves data in PostgreSQL, and sends results back to the frontend.

Analogy: In a restaurant, the backend is the kitchen manager. It receives orders, asks cooks to prepare food, stores bills, and sends food back to customers.

If the backend does not exist, the frontend has nothing real to display.

## 2. Concepts You Must Understand First

### Backend

What it is: The hidden part of an application that processes data.

Why we need it: The frontend cannot safely talk directly to databases, Groq, or cloud services.

Problem it solves: It centralizes business logic.

How it fits: FastAPI is the backend of CloudGuard AI.

Analogy: The backend is the engine of a car.

If we do not use it: The project becomes insecure and unorganized.

### HTTP

What it is: The communication system used by browsers and servers.

Why we need it: React and FastAPI talk using HTTP.

Problem it solves: It gives a standard way to request and send data.

How it fits: The frontend sends HTTP requests such as `POST /api/scans`.

Analogy: HTTP is like a postal service for web applications.

If we do not use it: Frontend and backend cannot communicate normally.

### REST API

What it is: A style for designing web APIs using URLs and HTTP methods.

Why we need it: It keeps backend endpoints simple and predictable.

Problem it solves: It avoids random, confusing communication patterns.

How it fits: CloudGuard AI uses endpoints like `/api/scans` and `/api/findings/{id}/explain`.

Analogy: A restaurant menu has fixed item names. A REST API has fixed endpoint names.

If we do not use it: Student 1 will not know how to request data.

### FastAPI

What it is: A Python framework for building APIs.

Why we need it: It lets us create backend endpoints quickly.

Problem it solves: It handles request routing, validation, and documentation.

How it fits: FastAPI exposes CloudGuard AI APIs.

Analogy: FastAPI is like a ready-made reception desk for your backend.

If we do not use it: You would need to build server behavior manually.

### Database

What it is: A system for storing structured data.

Why we need it: Scan results and AI explanations must be saved.

Problem it solves: Data remains available after the request finishes.

How it fits: PostgreSQL stores scans, findings, AI explanations, and usage limits.

Analogy: A database is like a library with organized shelves.

If we do not use it: Every scan result disappears when the backend restarts.

### PostgreSQL

What it is: A powerful open-source relational database.

Why we need it: It is reliable and commonly used in industry.

Problem it solves: It stores related data such as scans and findings.

How it fits: CloudGuard AI uses PostgreSQL on Railway.

Analogy: PostgreSQL is like an Excel workbook designed for serious applications.

If we do not use it: The project loses professional database value.

### Docker

What it is: A tool that runs software in containers.

Why we need it: Localstack is easiest to run with Docker.

Problem it solves: It avoids installing many services manually.

How it fits: Localstack runs inside a Docker container.

Analogy: Docker is like a lunchbox that contains everything a program needs.

If we do not use it: Localstack setup becomes harder.

### Localstack

What it is: A local simulator for AWS services.

Why we need it: Beginners should not use real AWS accounts for security testing.

Problem it solves: It lets us create fake AWS resources safely.

How it fits: Backend scans Localstack using boto3.

Analogy: Localstack is like a flight simulator for AWS.

If we do not use it: You either use unsafe real AWS or fake JSON data.

## 3. Installations

### Install Python

Website: `https://www.python.org/downloads/`

What to click:

1. Click "Download Python".
2. Run installer.
3. Select "Add python.exe to PATH".
4. Click Install Now.

Version: Python 3.11 or 3.12.

Verify:

```powershell
python --version
```

Command explanation:

- What it does: Shows Python version.
- Why we run it: FastAPI backend uses Python.
- Expected output: `Python 3.11.x` or `Python 3.12.x`.
- Common error: `python is not recognized`.
- Fix: Reinstall Python and select "Add to PATH".

### Install Docker Desktop

Website: `https://www.docker.com/products/docker-desktop/`

What to click:

1. Download Docker Desktop for Windows.
2. Run installer.
3. Keep "Use WSL 2" enabled if asked.
4. Restart computer if asked.
5. Open Docker Desktop.

Verify:

```powershell
docker --version
```

Command explanation:

- What it does: Shows Docker version.
- Why we run it: Localstack runs through Docker.
- Expected output: `Docker version ...`.
- Common error: Docker daemon not running.
- Fix: Open Docker Desktop and wait until it says running.

### Install PostgreSQL Locally

Website: `https://www.postgresql.org/download/windows/`

What to click:

1. Click "Download the installer".
2. Choose latest stable PostgreSQL version.
3. Run installer.
4. Keep PostgreSQL Server and pgAdmin selected.
5. Set a password you will remember.
6. Keep default port `5432`.

Verify:

```powershell
psql --version
```

Command explanation:

- What it does: Shows PostgreSQL command-line tool version.
- Why we run it: Confirms PostgreSQL tools installed.
- Expected output: `psql (PostgreSQL) ...`.
- Common error: `psql is not recognized`.
- Fix: Add PostgreSQL `bin` folder to PATH or use pgAdmin.

## 4. Backend Folder Structure

```text
backend/
  app/
    main.py
    config.py
    database.py
    api/
      routes_health.py
      routes_scans.py
      routes_findings.py
      routes_reports.py
    models/
      scan.py
      finding.py
      ai_explanation.py
      usage_limit.py
    schemas/
      scan_schema.py
      finding_schema.py
      ai_schema.py
    cloud/
      localstack_client.py
      s3_client.py
      iam_client.py
      ec2_client.py
    services/
      scanner_service.py
      risk_service.py
      report_service.py
    seed/
      create_vulnerable_localstack_resources.py
  requirements.txt
```

## 5. APIs Student 1 Requires

Student 1 needs stable JSON responses.

Do not keep changing field names after Week 3.

Required endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Check backend |
| POST | `/api/scans` | Run scan |
| GET | `/api/scans/latest` | Latest scan |
| GET | `/api/scans/{scan_id}/findings` | Findings list |
| POST | `/api/findings/{finding_id}/explain` | AI explanation |
| GET | `/api/reports/{scan_id}/pdf` | PDF download |

## 6. How Student 3 Plugs Into FastAPI

Student 3 gives you:

- Rule engine function
- Risk scoring function
- AI explanation service
- PDF report service

Your backend calls these services from API routes.

Example flow:

```text
POST /api/scans
  -> scanner_service collects Localstack resources
  -> Student 3 rule_engine checks resources
  -> Student 3 risk_service calculates score
  -> backend saves scan and findings
  -> backend returns JSON to Student 1
```

## 7. Useful Commands

### Create Virtual Environment

```powershell
python -m venv .venv
```

Command explanation:

- What it does: Creates an isolated Python environment.
- Why we run it: Keeps project packages separate from global Python.
- Expected output: A `.venv` folder appears.
- Common error: Python not found.
- Fix: Reinstall Python with PATH enabled.

### Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

Command explanation:

- What it does: Activates the project Python environment.
- Why we run it: Installed packages should go into this project only.
- Expected output: Terminal shows `(.venv)` at the start.
- Common error: Script execution disabled.
- Fix: Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then retry.

### Install Backend Packages

```powershell
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv boto3 pydantic
```

Command explanation:

- What it does: Installs backend libraries.
- Why we run it: FastAPI, database, environment variables, and AWS clients need these.
- Expected output: `Successfully installed ...`.
- Common error: pip cannot build package.
- Fix: Use `psycopg2-binary`, not `psycopg2`.

### Start FastAPI

```powershell
uvicorn app.main:app --reload
```

Command explanation:

- What it does: Starts the backend server.
- Why we run it: Frontend needs a running API.
- Expected output: URL such as `http://127.0.0.1:8000`.
- Common error: `ModuleNotFoundError`.
- Fix: Run the command from the `backend` folder and check file names.

### Start Localstack

```powershell
docker compose up
```

Command explanation:

- What it does: Starts services defined in `docker-compose.yml`.
- Why we run it: Localstack must be running before scanning fake AWS resources.
- Expected output: Logs showing Localstack is ready.
- Common error: Docker not running.
- Fix: Open Docker Desktop first.

## 8. Localstack Setup

Create `docker-compose.yml` in the project root:

```yaml
version: "3.8"

services:
  localstack:
    image: localstack/localstack:latest
    ports:
      - "4566:4566"
    environment:
      - SERVICES=s3,iam,ec2
      - AWS_DEFAULT_REGION=us-east-1
```

What this file does:

- Starts Localstack
- Enables S3, IAM, and EC2
- Exposes Localstack on port `4566`

Why port matters:

A port is like a door number on your computer. FastAPI talks to Localstack through door `4566`.

## 9. Database Tables

Use these tables:

- `scans`: one row per scan
- `findings`: one row per detected issue
- `ai_explanations`: cached AI responses
- `ai_usage_limits`: daily AI request count

Analogy:

- `scans` is the exam paper.
- `findings` are the mistakes found in the paper.
- `ai_explanations` are teacher explanations for mistakes.
- `ai_usage_limits` is a counter so you do not overuse paid AI.

## 10. Day-By-Day Roadmap

### Week 1

Main objective: set up the backend workspace, learn the moving parts of FastAPI and PostgreSQL, and get the first API and database pieces running in a simple way.

By the end of the week: the backend project should run locally, the virtual environment should be active, FastAPI should answer a health request, PostgreSQL should be connected, and the basic scan and finding models should be ready for the next weeks.

Day 1: Install the tools, open the backend folder, and verify the machine is ready

Today's goal: prepare the computer for backend work and make sure Python, Git, and VS Code are available.

Simple language:

- `Python` is the language the backend uses.
- `VS Code` is where you write the code.
- `Git` helps your team share work safely.
- `PowerShell` is the terminal where you type commands.

Step-by-step:

1. Open the Start menu and launch `PowerShell`.
2. Check whether Python is installed.

Before you run this command, know that it only shows the installed version and does not change anything.

```powershell
python --version
```

Expected result: a Python version number such as `Python 3.12.x`.

3. Check whether Git is installed.

Before you run this command, know that it confirms Git is available for source control.

```powershell
git --version
```

Expected result: a Git version such as `git version 2.x.x`.

4. Open the project folder in VS Code.
5. In the left sidebar, confirm the `backend` folder exists, along with the `app`, `api`, `models`, `schemas`, `services`, `cloud`, and `seed` folders from the architecture section above.
6. If any folder is missing, create it now so the backend files stay organized from the beginning.
7. Create a `.gitignore` file in the backend root if it does not already exist and add the virtual environment folder name `.venv` to it.
8. Create an empty `.env` file in the backend root so sensitive values stay out of code.

Expected result: your workspace is open, the project folders are visible, and the terminal tools are confirmed to work.

Verification:

- Python version command returns a version number.
- Git version command returns a version number.
- The backend folder structure matches the guide.

Common mistakes and fixes:

- If Python is not recognized, reinstall Python and check "Add Python to PATH".
- If Git is not recognized, reinstall Git and restart PowerShell.
- If VS Code opens the wrong folder, close it and reopen the project root.

Checklist:

- [ ] Python is installed and recognized
- [ ] Git is installed and recognized
- [ ] VS Code opens the project folder
- [ ] Backend folder structure exists
- [ ] `.gitignore` and `.env` files exist

Day 2: Create the virtual environment and install backend packages

Today's goal: isolate the project packages so this backend does not depend on random global installations.

Simple language:

- A `virtual environment` is a private Python workspace for this project.
- `requirements` are the packages the project needs.

Step-by-step:

1. Open the terminal in VS Code.
2. Create the virtual environment.

Before you run the command below, know that it makes a `.venv` folder with its own Python setup.

```powershell
python -m venv .venv
```

Expected result: a new `.venv` folder appears in the backend directory.

3. Activate the virtual environment.

Before you run the command below, know that it tells the terminal to use the project Python instead of the system Python.

```powershell
.\.venv\Scripts\Activate.ps1
```

Expected result: `(.venv)` appears at the start of the terminal line.

4. Install the backend packages listed in the architecture guide.

Before you run the command below, know that it downloads FastAPI, the server runner, database tools, environment tools, and AWS client tools.

```powershell
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv boto3 pydantic
```

Expected result: pip finishes with a success message.

5. Save the package list to `requirements.txt` so the team can install the same tools later.
6. Keep the terminal open because the next steps use the same environment.

Verification:

- The terminal shows `(.venv)`.
- The package install finishes without errors.
- `requirements.txt` contains the installed packages.

Common mistakes and fixes:

- If activation is blocked, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again.
- If `psycopg2-binary` fails, make sure you are using the binary package, not `psycopg2`.
- If the terminal does not show `(.venv)`, the virtual environment is not active yet.

Checklist:

- [ ] `.venv` folder exists
- [ ] Virtual environment is active
- [ ] Backend packages are installed
- [ ] `requirements.txt` is recorded

Day 3: Build the first FastAPI app and confirm Swagger works

Today's goal: create the server entry point and prove that the backend can answer a request.

Simple language:

- A `route` is a URL the backend listens to.
- `Swagger UI` is the browser page that shows and tests your API.

Step-by-step:

1. Open `app/main.py`.
2. Create a small FastAPI app object in that file.
3. Add a `/api/health` route that returns a simple JSON response such as `{"status": "ok"}`.
4. Create a placeholder `/api/scans` route so the frontend team can see the API shape early.
5. Save the file.
6. Start the backend server.

Before you run this command, know that it launches the FastAPI development server and keeps it running in the terminal.

```powershell
uvicorn app.main:app --reload
```

Expected result: the terminal shows the server is running on `http://127.0.0.1:8000`.

7. Open the browser and visit `http://127.0.0.1:8000/docs`.

Expected result: Swagger UI opens and shows your routes.

8. Add CORS middleware to `main.py` now so Student 1 can connect from Day 5 of their guide onward.

Add this after creating the FastAPI app object:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Student 1 local dev URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

When Student 1 deploys to Vercel, add the Vercel URL to `allow_origins` as well.

Verification:

- `GET /api/health` returns an `ok` response.
- Swagger UI loads without an error.
- The terminal stays active while the server runs.

Common mistakes and fixes:

- If you see `ModuleNotFoundError`, confirm you are running the command from the backend folder.
- If the route does not appear in Swagger, check the function name and the decorator syntax.
- If the server closes immediately, look for a syntax error in `main.py`.

Checklist:

- [ ] `app/main.py` exists
- [ ] `/api/health` works
- [ ] Placeholder `/api/scans` exists
- [ ] Swagger UI opens in the browser

Day 4: Connect PostgreSQL and make the backend aware of the database

Today's goal: give the backend a place to store scan results and findings.

Simple language:

- A `database connection` is the link between the backend and PostgreSQL.
- `Environment variables` keep secret values out of code.

Step-by-step:

1. Open PostgreSQL if it is already installed on your machine, or open the Railway dashboard if your team is using Railway PostgreSQL for development.
2. Create a database named `cloudguard_ai` if you are using local PostgreSQL.
3. Open `app/config.py` and add the database connection string variable.
4. Open `app/database.py` and create the SQLAlchemy engine and session setup.
5. Make sure the backend reads the connection string from `.env`.
6. Save the files.
7. Restart the FastAPI server so the new configuration is loaded.

Before you run anything else, know that this step teaches the backend where the database lives.

Expected result: the backend starts without database errors and can connect to PostgreSQL.

Verification:

- Open the database tool and confirm the `cloudguard_ai` database exists.
- Restart the backend and watch for connection errors.
- If you have a test connection route or startup log, confirm it shows a successful database link.

Common mistakes and fixes:

- If the backend cannot find the database URL, check the `.env` file name and spelling.
- If PostgreSQL is not running, start the service or open the Railway database connection settings.
- If the password is wrong, update the connection string and restart the server.

Checklist:

- [ ] Database exists
- [ ] Connection string is in `.env`
- [ ] `config.py` and `database.py` are created
- [ ] Backend connects to PostgreSQL

Day 5: Create scan and finding models and prepare the first real tables

Today's goal: define the data structure for scan results so later weeks can save and read them.

Simple language:

- A `model` is a Python description of a database table.
- A `table` is where one kind of data is stored.

Step-by-step:

1. Open `app/models/scan.py` and define the fields for a scan record.
2. Open `app/models/finding.py` and define the fields for a finding record.
3. In the `finding.py` model, include a boolean field named `has_ai_explanation` with a default value of `False`. This field is your responsibility to manage. It starts as `False` when a finding is first saved. Your backend sets it to `True` after a successful AI explanation is saved to the `ai_explanations` table. Student 1 reads this field to decide whether to show the "Explain & Fix" button as already-answered or still pending.
4. Open `app/schemas/scan_schema.py` and `app/schemas/finding_schema.py` so request and response data stay organized.
5. Make sure each field matches the architecture guide so the frontend and backend use the same names.
6. If your project uses SQLAlchemy table creation in development, run the startup code once so the tables are created.
7. Open PostgreSQL or pgAdmin and refresh the schema to look for the new tables.

Before you move on, know that this step gives the project a place to store actual scan results instead of temporary data.

Expected result: the `scans` and `findings` tables are ready for later work.

Verification:

- The model files exist in the correct folders.
- The database schema shows the new tables.
- The `findings` table has a `has_ai_explanation` column that defaults to `False`.
- The backend still starts cleanly after the new models are added.

Common mistakes and fixes:

- If table creation fails, check that the model names and imports are correct.
- If the database shows no tables, restart the server or rerun the schema creation step.
- If the schema names do not match the guide, update them now before later weeks depend on them.
- If `has_ai_explanation` is missing, Student 1's UI will not know which findings already have cached explanations.

Checklist:

- [ ] `scan.py` model exists
- [ ] `finding.py` model exists
- [ ] `has_ai_explanation` boolean field exists with default `False`
- [ ] Schema files exist
- [ ] `scans` and `findings` tables are ready

### Week 2

Day 6:

- Learn: Docker.
- Install: Docker Desktop.
- Build: Localstack docker compose.
- Run the seed script after Localstack starts: `python seed/create_vulnerable_localstack_resources.py`. This creates fake S3 buckets, IAM users, and EC2 security groups that Student 3's rules are designed to detect. Without seeding, a scan returns zero findings and the dashboard looks empty.
- Outcome: Localstack starts and contains vulnerable fake resources ready for scanning.

Day 7:

- Learn: AWS services at beginner level.
- Build: boto3 Localstack client.
- Outcome: Backend connects to Localstack.

Day 8:

- Learn: S3 buckets.
- Build: List S3 buckets from Localstack.
- Outcome: Backend sees fake buckets.

Day 9:

- Learn: IAM users and policies.
- Build: List IAM users and policies.
- Outcome: Backend sees fake IAM data.

Day 10:

- Learn: EC2 and security groups.
- Build: List EC2 security groups.
- Outcome: Backend sees fake networking rules.

### Week 3

**Important coordination note:** Before starting Day 11, confirm with Student 3 that `run_scan()` is importable from `rules/rule_engine.py` and `calculate_score()` is importable from `services/risk_service.py`. If Student 3 is still building rules, ask them for a temporary version that returns a hardcoded list of sample findings. You can integrate against that and swap in the real version later without changing your code.

Day 11:

- Integrate Student 3's rule engine.
- Outcome: Raw resources become findings.

Day 12:

- Save scan records.
- Outcome: Scan is stored in PostgreSQL.

Day 13:

- Save finding records.
- Outcome: Findings API returns database data.

Day 14:

- Add latest scan API.
- Outcome: Frontend can load latest results.

Day 15:

- Integration checkpoint with Student 1.
- Outcome: Run Scan button works.

### Week 4

Day 16:

- Add AI explanation endpoint.
- Outcome: Endpoint accepts finding ID.

Day 17:

- Connect Student 3's AI service.
- Outcome: Groq response returns through FastAPI.

Day 18:

- Save AI explanation in database.
- After saving the explanation to the `ai_explanations` table, update the matching finding's `has_ai_explanation` field to `True`. This is what tells Student 1's UI that the explanation is already cached.
- Outcome: Repeated requests use cache and Student 1's button reflects the correct state.

Day 19:

- Add daily usage limit.
- Outcome: AI cost is controlled.

Day 20:

- Integration checkpoint with Student 3.
- Outcome: Explain & Fix works.

### Week 5

Day 21:

- Add PDF report endpoint.
- Outcome: Backend returns PDF file.

Day 22:

- Test report download with frontend.
- Outcome: Browser downloads PDF.

Day 23:

- Add CORS settings.
- Allowed origins: `http://localhost:5173` for local development and the Vercel frontend URL for production. Add both to the FastAPI `CORSMiddleware` so Student 1 is never blocked.
- Outcome: Vercel frontend can call backend.

Day 24:

- Add `.env.example`.
- Outcome: Team knows required variables.

Day 25:

- Backend cleanup and error handling.
- Outcome: Demo flow is stable.

### Week 6

Day 26:

- Prepare Railway deployment.
- Outcome: Backend code is on GitHub.

Day 27:

- Deploy backend to Railway.
- Outcome: Public backend URL works.

Day 28:

- Connect Railway PostgreSQL.
- Outcome: Database works in production.

Day 29:

- Test all API endpoints.
- Outcome: Backend is demo-ready.

Day 30:

- Practice explaining backend.
- Outcome: You can answer viva questions.

## 11. Testing Instructions

Test backend health:

```powershell
curl http://127.0.0.1:8000/api/health
```

Command explanation:

- What it does: Sends a request to the backend health endpoint.
- Why we run it: To check the backend is running.
- Expected output: `{"status":"ok"}`.
- Common error: Connection refused.
- Fix: Start FastAPI using `uvicorn app.main:app --reload`.

Test Localstack:

```powershell
curl http://localhost:4566/_localstack/health
```

Command explanation:

- What it does: Checks Localstack health.
- Why we run it: Scanner needs Localstack.
- Expected output: JSON showing services.
- Common error: Cannot connect.
- Fix: Start Docker Desktop and run `docker compose up`.

## 12. Viva Answers For Student 2

Question: What did you build?

Answer: I built the FastAPI backend that connects the frontend, database, Localstack scanner, AI service, and PDF report generation.

Question: Why FastAPI?

Answer: FastAPI is beginner-friendly, fast to develop with, and automatically provides API documentation.

Question: Why PostgreSQL?

Answer: PostgreSQL stores scan results, findings, cached AI explanations, and usage limits in a structured way.

Question: Why Localstack?

Answer: Localstack lets us safely simulate AWS services without using real AWS accounts or spending money.
