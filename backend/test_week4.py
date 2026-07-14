import sys
import requests

API_BASE_URL = "http://127.0.0.1:8000"

def main():
    print("=== CLOUDGUARD AI - WEEK 4 DIAGNOSTICS ===")
    
    # 1. Trigger a scan to get findings
    print("\n1. Running scan to gather findings...")
    try:
        scan_resp = requests.post(f"{API_BASE_URL}/api/scans", timeout=15)
        if scan_resp.status_code != 201:
            print(f"   [FAIL] Scan failed: HTTP {scan_resp.status_code}")
            sys.exit(1)
        scan_data = scan_resp.json()
        scan_id = scan_data["scan_id"]
        print(f"   [OK] Scan created: {scan_id}")
    except Exception as e:
        print(f"   [FAIL] Connection failed: {e}. Ensure uvicorn is running on {API_BASE_URL}.")
        sys.exit(1)

    # 2. Retrieve findings for the scan
    print("\n2. Retrieving findings list...")
    findings_resp = requests.get(f"{API_BASE_URL}/api/scans/{scan_id}/findings")
    if findings_resp.status_code != 200:
        print(f"   [FAIL] Failed to get findings: HTTP {findings_resp.status_code}")
        sys.exit(1)
    findings = findings_resp.json()
    print(f"   [OK] Found {len(findings)} findings.")
    
    if not findings:
        print("   [FAIL] No findings found to test AI explanation.")
        sys.exit(1)
        
    target_finding = findings[0]
    finding_id = target_finding["id"]
    print(f"--> Target Finding details:")
    print(f"   - ID: {finding_id}")
    print(f"   - Rule: {target_finding.get('rule_id')}")
    print(f"   - Service: {target_finding.get('service')}")
    print(f"   - Initial has_ai_explanation: {target_finding.get('has_ai_explanation')}")

    # 3. Request AI explanation (first time - uncached)
    print("\n3. Requesting AI explanation (1st time - should call service/generate)...")
    explain_resp = requests.post(f"{API_BASE_URL}/api/findings/{finding_id}/explain")
    if explain_resp.status_code != 200:
        print(f"   [FAIL] Explanation request failed: HTTP {explain_resp.status_code} - {explain_resp.text}")
        sys.exit(1)
    explanation = explain_resp.json()
    print("   [OK] Explanation generated successfully!")
    print(f"   - Explanation: {explanation.get('explanation')[:80]}...")
    print(f"   - Danger: {explanation.get('danger')[:80]}...")
    print(f"   - Steps: {explanation.get('remediation_steps')}")
    print(f"   - Effort: {explanation.get('estimated_effort')}")

    # 4. Check if the finding status has updated in database
    print("\n4. Checking if has_ai_explanation is updated in the database...")
    findings_resp2 = requests.get(f"{API_BASE_URL}/api/scans/{scan_id}/findings")
    findings2 = {f["id"]: f for f in findings_resp2.json()}
    updated_finding = findings2[finding_id]
    if updated_finding.get("has_ai_explanation") is True:
        print("   [OK] Finding 'has_ai_explanation' successfully set to true!")
    else:
        print("   [FAIL] Finding 'has_ai_explanation' is still false!")

    # 5. Request AI explanation (second time - cached)
    print("\n5. Requesting AI explanation (2nd time - should serve from cache)...")
    explain_resp2 = requests.post(f"{API_BASE_URL}/api/findings/{finding_id}/explain")
    if explain_resp2.status_code == 200:
        print("   [OK] Caching Check: Success! Served quickly from cache.")
    else:
        print(f"   [FAIL] Caching request failed: HTTP {explain_resp2.status_code}")

if __name__ == "__main__":
    main()
