from app.services.ai_service import generate_ai_explanation


def test_generate_ai_explanation_falls_back_without_api_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    finding = {
        "service": "EC2",
        "title": "Open SSH",
        "severity": "HIGH",
        "description": "Port 22 is open to the internet.",
        "evidence": {},
    }

    result = generate_ai_explanation(finding)

    assert "explanation" in result
    assert "danger" in result
    assert "real_world_impact" in result
    assert "remediation_steps" in result
    assert "estimated_effort" in result
    assert isinstance(result["remediation_steps"], list)
    assert len(result["remediation_steps"]) > 0