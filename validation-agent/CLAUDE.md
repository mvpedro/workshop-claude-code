# Agente de Validacao de Propostas

Este projeto contem a documentacao de referencia de um produto e um agente que valida codigo e propostas contra essa documentacao.

## Estrutura do projeto

- `docs/compliance/` — Requisitos regulatorios: LGPD, politica de dados, restricoes de integracao com terceiros.
- `docs/produto/` — Decisoes de produto, roadmap, regras de negocio.
- `docs/estilo/` — Guia de estilo de codigo, convencoes de documentacao, padroes de formatacao.
- `docs/tecnico/` — Decisoes de arquitetura, stack definida, principios tecnicos, padroes de testes.
- `scenarios/` — Cenarios de teste para exercitar o agente de validacao.

## Como usar

### Slash commands (`.claude/commands/`)

- `/validate` — Orquestrador principal. Dispara 3 subagentes em paralelo (compliance, produto, tecnico) e consolida o resultado.
- `/validate-compliance` — Validacao isolada de compliance.
- `/validate-produto` — Validacao isolada de produto e estilo.
- `/validate-tecnico` — Validacao isolada tecnica.

### Skill (`.claude/skills/`)

- `validate` (`.claude/skills/validate/SKILL.md`) — Skill invocavel sob demanda para validar decisoes, perguntas ou propostas contra toda a base de conhecimento do projeto. Dispara os mesmos 3 agentes em paralelo e gera um relatorio consolidado com vereditos e acoes necessarias. Use quando quiser verificar se uma abordagem e aderente antes de implementar.
