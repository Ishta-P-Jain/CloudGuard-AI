import sys
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL
from app.models.scan import Scan
from app.models.finding import Finding

API_BASE_URL = "http://127.0.0.1:8000"

def check_db_direct():
    """
    Directly query the database using SQLAlchemy models to verify persistence.
    """
    print("\n--- Database Verification ---")
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        scan_count = db.query(Scan).count()
        finding_count = db.query(Finding).count()
        
        print("db_connection: OK")
        print("Database Records Count:")
        print(f"   - Scans Table: {scan_count} records")
        print(f"   - Findings Table: {finding_count} records")
        
        db.close()
    except Exception as e:
        print(f"db_connection failed: {e}")

def check_api_endpoints():
    """
    Simulates API requests to test the Week 3 scans and findings routes.
    """
    print("\n--- API Routes Verification ---")
    
    # 1. Test POST /api/scans
    print("1. Running new scan (POST /api/scans)...")
    try:
        post_response = requests.post(f"{API_BASE_URL}/api/scans", timeout=15)
        if post_response.status_code == 201:
            scan_data = post_response.json()
            scan_id = scan_data.get("scan_id")
            score = scan_data.get("score")
            summary = scan_data.get("summary", {})
            print("   Trigger Scan: OK")
            print(f"   Generated Scan ID: {scan_id}")
            print(f"   Calculated Score: {score}/100")
            print(f"   Findings Summary: {summary}")
        else:
            print(f"   Trigger Scan failed: HTTP {post_response.status_code} - {post_response.text}")
            return
    except requests.exceptions.ConnectionError:
        print(f"   Connection failed: Is uvicorn running on {API_BASE_URL}?")
        return
        
    # 2. Test GET /api/scans/latest
    print("\n2. Fetching latest scan summary (GET /api/scans/latest)...")
    try:
        latest_resp = requests.get(f"{API_BASE_URL}/api/scans/latest")
        if latest_resp.status_code == 200:
            latest_data = latest_resp.json()
            print(f"   Fetch Latest: OK (Scan ID: {latest_data.get('scan_id')})")
        else:
            print(f"   Fetch Latest failed: HTTP {latest_resp.status_code}")
    except Exception as e:
        print(f"   Fetch Latest query error: {e}")

    # 3. Test GET /api/scans/{scan_id}/findings
    print(f"\n3. Fetching findings for Scan ID: {scan_id} (GET /api/scans/{{scan_id}}/findings)...")
    try:
        findings_resp = requests.get(f"{API_BASE_URL}/api/scans/{scan_id}/findings")
        if findings_resp.status_code == 200:
            findings = findings_resp.json()
            print(f"   Fetch Findings: OK ({len(findings)} findings returned)")
            for i, f in enumerate(findings[:3]):
                print(f"      - Finding #{i+1}: [{f.get('service')}] {f.get('title')} ({f.get('severity')})")
            if len(findings) > 3:
                print(f"      - ... and {len(findings) - 3} more.")
        else:
            print(f"   Fetch Findings failed: HTTP {findings_resp.status_code}")
    except Exception as e:
        print(f"   Fetch Findings query error: {e}")

def main():
    print("=== CLOUDGUARD AI - WEEK 3 INTEGRATION DIAGNOSTICS ===")
    
    # Check if LocalStack is running
    print("\n--- Checking LocalStack Status ---")
    try:
        ls_resp = requests.get("http://localhost:4566/_localstack/health", timeout=5)
        if ls_resp.status_code == 200:
            print("LocalStack: OK")
        else:
            print("LocalStack: Not responding healthily")
    except Exception:
        print("LocalStack: Connection refused (Ensure Docker Desktop is running & docker compose is up)")

    check_api_endpoints()
    check_db_direct()

if __name__ == "__main__":
    main()
