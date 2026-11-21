from src.agent.alert import Alert
from src.agent.report import Report


def triage(alert: Alert) -> Report:
    if alert.failed_attempts >= 50:
        severity = "high"
    elif alert.failed_attempts >= 10:
        severity = "medium"
    else:
        severity = "low"

    return Report(
        alert_id=alert.alert_id,
        severity=severity,
        classification="SSH brute force",
        mitre_tactic="Credential Access",
        mitre_technique="T1110 - Brute Force",
        iocs=[{"type": "ip", "value": alert.src_ip, "enrichment": "pendente"}],
        summary=(
            f"{alert.failed_attempts} tentativas de login SSH falhas para o usuário "
            f"{alert.username} em {alert.window_minutes} minutos, "
            f"vindas de {alert.src_ip}."
        ),
        recommended_actions=[
            "Bloquear o IP de origem no firewall",
            "Verificar se houve algum login bem-sucedido a partir desse IP",
            "Desabilitar login SSH direto como root",
        ],
    )