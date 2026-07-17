import app.services.ai_service as ai_service
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


def test_generate_ai_explanation_falls_back_when_groq_raises(monkeypatch):
    class FakeCompletions:
        def create(self, **kwargs):
            raise RuntimeError("Groq is unavailable")

    class FakeChat:
        def __init__(self):
            self.completions = FakeCompletions()

    class FakeGroq:
        def __init__(self, api_key):
            self.chat = FakeChat()

    monkeypatch.setenv("GROQ_API_KEY", "fake-key")
    monkeypatch.setattr(ai_service, "Groq", FakeGroq)

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
    assert "fallback" in result["explanation"].lower() or "guidance" in result["explanation"].lower()
