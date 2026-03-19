# Agente de Validacao de Propostas

Este projeto contem a documentacao de referencia de um produto e um agente que valida codigo e propostas contra essa documentacao.

## Estrutura do projeto

- `docs/compliance/` — Requisitos regulatorios: LGPD, politica de dados, restricoes de integracao com terceiros.
- `docs/produto/` — Decisoes de produto, roadmap, regras de negocio.
- `docs/estilo/` — Guia de estilo de codigo, convencoes de documentacao, padroes de formatacao.
- `docs/tecnico/` — Decisoes de arquitetura, stack definida, principios tecnicos, padroes de testes.
- `scenarios/` — Cenarios de teste para exercitar o agente de validacao.

## Como usar

Use os slash commands disponveis em `.claude/commands/`:

- `/validate` — Orquestrador principal. Dispara 3 subagentes em paralelo (compliance, produto, tecnico) e consolida o resultado.
- `/validate-compliance` — Validacao isolada de compliance.
- `/validate-produto` — Validacao isolada de produto e estilo.
- `/validate-tecnico` — Validacao isolada tecnica.
