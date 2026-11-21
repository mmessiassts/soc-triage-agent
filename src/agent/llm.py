import json
import sys
from pathlib import Path

import anthropic

from src.agent.report import Report

MODEL = "claude-sonnet-5-5"

SYSTEM_PROMPT = """Você é um analista de SOC nível 1. Receberá um alerta de segurança em JSON.
Responda SOMENTE com um objeto JSON, sem texto extra e sem markdown, com estas chaves:
alert_id, severity (low, medium ou high), classification, mitre_tactic, mitre_technique,
iocs (lista de objetos com type, value e enrichment), summary, recommended_actions (lista de textos).
Escreva summary e recommended_actions em português.
Use apenas informações presentes no alerta. Não invente dados."""

VALID_SEVERITIES = {"low", "medium", "high"}


def analyze_with_llm(alert_data: dict) -> Report:
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": json.dumps(alert_data, ensure_ascii=False)}
        ],
    )
    text = response.content[0].text.strip()
    text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    data = json.loads(text)

    severity = data["severity"] if data["severity"] in VALID_SEVERITIES else "medium"

    return Report(
        alert_id=data["alert_id"],
        severity=severity,
        classification=data["classification"],
        mitre_tactic=data["mitre_tactic"],
        mitre_technique=data["mitre_technique"],
        iocs=data.get("iocs", []),
        summary=data["summary"],
        recommended_actions=data["recommended_actions"],
        requires_human_approval=True,
    )


if __name__ == "__main__":
    alert_data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(analyze_with_llm(alert_data).to_json())