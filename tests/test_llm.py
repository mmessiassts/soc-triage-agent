import json
from unittest.mock import MagicMock, patch

from src.agent.llm import analyze_with_llm

ALERT = {"alert_id": "ALT-0002", "source": "apache", "src_ip": "198.51.100.23"}

FAKE_REPORT = {
    "alert_id": "ALT-0002",
    "severity": "high",
    "classification": "Path traversal",
    "mitre_tactic": "Initial Access",
    "mitre_technique": "T1190 - Exploit Public-Facing Application",
    "iocs": [{"type": "ip", "value": "198.51.100.23", "enrichment": "pendente"}],
    "summary": "Requisição tentando ler /etc/passwd via path traversal.",
    "recommended_actions": ["Bloquear o IP de origem", "Revisar o endpoint /download"],
}


def fake_client(text):
    client = MagicMock()
    client.messages.create.return_value.content = [MagicMock(text=text)]
    return client


def run(payload_text):
    with patch("src.agent.llm.anthropic.Anthropic", return_value=fake_client(payload_text)):
        return analyze_with_llm(ALERT)


def test_llm_valid_response():
    report = run(json.dumps(FAKE_REPORT))
    assert report.classification == "Path traversal"
    assert report.severity == "high"


def test_llm_cannot_disable_human_approval():
    data = {**FAKE_REPORT, "severity": "critical", "requires_human_approval": False}
    report = run(json.dumps(data))
    assert report.requires_human_approval is True
    assert report.severity == "medium"


def test_llm_response_wrapped_in_markdown():
    report = run("```json\n" + json.dumps(FAKE_REPORT) + "\n```")
    assert report.mitre_technique.startswith("T1190")