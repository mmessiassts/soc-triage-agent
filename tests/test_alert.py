from src.agent.alert import load_alert


def test_load_alert():
    alert = load_alert("samples/alerta_ssh_bruteforce.json")
    assert alert.alert_id == "ALT-0001"
    assert alert.failed_attempts == 87
    assert alert.src_ip == "203.0.113.45"