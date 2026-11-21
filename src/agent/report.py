import json
from dataclasses import dataclass, field, asdict


@dataclass
class Report:
    alert_id: str
    severity: str
    classification: str
    mitre_tactic: str
    mitre_technique: str
    iocs: list = field(default_factory=list)
    summary: str = ""
    recommended_actions: list = field(default_factory=list)
    requires_human_approval: bool = True

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)