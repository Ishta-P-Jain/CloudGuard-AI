from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Welcome to CloudGuard AI Backend 🚀"
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/scans")
def scan():
    return {"message": "Coming Soon"}