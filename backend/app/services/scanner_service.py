from typing import Any, Dict, List

from app.cloud.localstack_client import collect_resources
from rules.rule_engine import run_scan


def scan_resources(resources: Dict[str, Any]) -> List[Dict[str, Any]]:
    return run_scan(resources)


def scan_localstack() -> List[Dict[str, Any]]:
    resources = collect_resources()
    return run_scan(resources)