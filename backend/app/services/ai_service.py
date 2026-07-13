
from __future__ import annotations

import json
import os
from typing import Any, Dict

from app.schemas.ai_schema import AIExplanationResponse
from app.services.report_service import build_fallback_remediation

try:
    from groq import Groq
except ImportError:
    Groq = None

DEFAULT_MODEL = os.getenv("GROQ_MODEL_NAME", "llama-3.1-70b-versatile")


def _build_prompt(finding: Dict[str, Any]) -> str:
    return (
        "You are a cloud security assistant.\n"
        "Return ONLY valid JSON with these keys:\n"
        "explanation, danger, real_world_impact, remediation_steps, estimated_effort\n\n"
        f"Service: {finding.get('service', 'Unknown')}\n"
        f"Title: {finding.get('title', 'Unknown')}\n"
        f"Severity: {finding.get('severity', 'LOW')}\n"
        f"Description: {finding.get('description', '')}\n"
        f"Evidence: {finding.get('evidence', {})}\n"
    )


def _strip_code_fences(text: str) -> str:
    cleaned_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.lower() == "json":
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines).strip()


def generate_ai_explanation(finding: Dict[str, Any]) -> Dict[str, Any]:
    fallback = build_fallback_remediation(finding)
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key or Groq is None:
        return fallback

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You explain cloud security findings in simple English.",
                },
                {
                    "role": "user",
                    "content": _build_prompt(finding),
                },
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content or ""
        payload = json.loads(_strip_code_fences(content))
        validated = AIExplanationResponse(**payload)
        return validated.model_dump()
    except Exception:
        return fallback