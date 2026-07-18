from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models.scan import Scan
from app.models.finding import Finding
from app.models.ai_explanation import AIExplanation
from app.models.usage_limit import UsageLimit

from app.api import routes_scans, routes_findings, routes_reports

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CloudGuard AI Backend",
    description="AI-powered cloud security auditing platform backend API.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://cloudguard-ai-three.vercel.app",
        "https://cloudguard-ai.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_scans.router)
app.include_router(routes_findings.router)
app.include_router(routes_reports.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to CloudGuard AI Backend 🚀"
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}
