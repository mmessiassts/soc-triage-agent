import sys

from src.agent.alert import load_alert
from src.agent.triage import triage


def main():
    if len(sys.argv) != 2:
        print("Uso: python -m src.agent.cli <caminho_do_alerta.json>")
        sys.exit(1)

    alert = load_alert(sys.argv[1])
    report = triage(alert)
    print(report.to_json())


if __name__ == "__main__":
    main()