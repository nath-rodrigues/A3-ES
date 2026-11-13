# DespesaClara

Analisador de execução de despesa pública federal por órgão (CSV do Portal da Transparência).
Projeto da disciplina de Engenharia de Software (UTFPR).

- Sprint 1: `Descricao.MD`
- Sprint 2: `Historias_de_usuarios.md` e `test_despesaclara.py`
- Sprint 3: `despesaclara.py` e `docs/Arquitetura.md`

## Como rodar

```
python despesaclara.py exemplos/despesas_exemplo.csv
```

O programa valida o arquivo, pergunta os órgãos (nomes ou códigos separados por `;`, vazio = todos),
grava `relatorio_<data>.csv` na pasta atual e mostra o resumo no terminal.

## Testes

```
pip install pytest
python -m pytest -v
```
