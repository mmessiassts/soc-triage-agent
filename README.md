\# SOC Triage Agent



Agente de triagem de alertas para SOC. Recebe um alerta em JSON, classifica a severidade, mapeia para o MITRE ATT\&CK e gera um relatório com ações recomendadas.



\## Princípio de design



O agente recomenda, mas nunca executa. Todo relatório sai com `requires\_human\_approval: true`, e esse valor é fixado no código: nem a resposta do modelo de IA consegue desativá-lo.



\## Como funciona



1\. \*\*Triagem por regras\*\* (`src/agent/triage.py`): classificação determinística e testável para alertas conhecidos, como brute force SSH.

2\. \*\*Camada de IA\*\* (`src/agent/llm.py`): para alertas que as regras não cobrem, o agente consulta um modelo de linguagem e valida a resposta (severidade inválida vira `medium`, JSON em markdown é tratado).



\## Como rodar



```

git clone https://github.com/mmessiassts/soc-triage-agent.git

cd soc-triage-agent

python -m venv .venv

.venv\\Scripts\\activate

pip install -r requirements.txt

```



Triagem por regras:



```

python -m src.agent.cli samples\\alerta\_ssh\_bruteforce.json

```



Camada de IA (requer a variável de ambiente `ANTHROPIC\_API\_KEY`):



```

python -m src.agent.llm samples\\alerta\_desconhecido.json

```



Testes:



```

python -m pytest

```



Os testes da camada de IA usam respostas simuladas, então rodam sem internet e sem custo.



\## Estrutura



```

src/agent/   código do agente

samples/     alertas de exemplo e relatório esperado

tests/       testes automatizados

```



\## Próximos passos



\- Integrar o enriquecimento de IOCs do \[threat-hunting-tool](https://github.com/mmessiassts/threat-hunting-tool)

\- Suportar mais tipos de alerta nas regras

\- Roteamento automático: regras primeiro, IA apenas quando nenhuma regra se aplica



\## Licença



MIT

