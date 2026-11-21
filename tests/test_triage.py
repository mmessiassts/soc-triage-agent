from dataclasses import replace

from src.agent.alert import load_alert
from src.agent.triage import triage


def test_triage_high_severity():
    alert = load_alert("samples/alerta_ssh_bruteforce.json")
    report = triage(alert)
    assert report.severity == "high"
    assert report.mitre_technique.startswith("T1110")
    assert report.requires_human_approval is True


def test_triage_medium_severity():
    alert = load_alert("samples/alerta_ssh_bruteforce.json")
    report = triage(replace(alert, failed_attempts=20))
    assert report.severity == "medium"