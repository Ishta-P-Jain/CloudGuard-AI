from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
# Import models to register them in SQLAlchemy's Base metadata before calling create_all
from app.models.scan import Scan
from app.models.finding import Finding
from app.models.ai_explanation import AIExplanation
from app.models.usage_limit import UsageLimit

from app.api import routes_scans, routes_findings

# 1. Initialize and auto-create database tables
# Base.metadata.create_all triggers Table creation if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CloudGuard AI Backend",
    description="AI-powered cloud security auditing platform backend API.",
    version="1.0.0"
)

# 2. Add CORS Middleware to support local React dashboard communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow local React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Register route routers
app.include_router(routes_scans.router)
app.include_router(routes_findings.router)

@app.get("/")
def home():
    return {
        "message": "Welcome to CloudGuard AI Backend 🚀"
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}