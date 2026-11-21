import json
from src.agent.report import Report


def test_report_requires_human_approval_by_default():
    report = Report(
        alert_id="ALT-0001",
        severity="high",
        classification="SSH brute force",
        mitre_tactic="Credential Access",
        mitre_technique="T1110",
    )
    assert report.requires_human_approval is True


def test_report_to_json():
    report = Report(
        alert_id="ALT-0001",
        severity="high",
        classification="SSH brute force",
        mitre_tactic="Credential Access",
        mitre_technique="T1110",
    )
    data = json.loads(report.to_json())
    assert data["alert_id"] == "ALT-0001"
    assert data["requires_human_approval"] is True