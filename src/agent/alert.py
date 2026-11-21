import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Alert:
    alert_id: str
    timestamp: str
    source: str
    rule: str
    src_ip: str
    dest_host: str
    username: str
    failed_attempts: int
    window_minutes: int
    raw_log: str


def load_alert(path: str) -> Alert:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return Alert(**data)