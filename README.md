# Workshop: Claude Code na Pratica

Repositorio de apoio ao workshop sobre Claude Code, cobrindo context engineering, agentes autonomos e automacao de workflows de desenvolvimento.

## Estrutura

```
.
├── demo/                      # Projeto de demonstracao
│   ├── src/                   # API REST (FastAPI + SQLAlchemy)
│   ├── dbt/                   # Transformacao de dados (DBT + DuckDB)
│   ├── tests/                 # Testes unitarios (pytest)
│   ├── prompts/               # Prompt templates para pipelines CI
│   ├── .claude/               # Configuracao do Claude Code (hooks, settings)
│   └── CLAUDE.md              # Instrucoes persistentes do projeto
│
├── validation-agent/          # Agente de validacao de propostas
│   ├── docs/                  # Base de conhecimento do projeto
│   │   ├── compliance/        # LGPD, politica de dados, restricoes
│   │   ├── produto/           # Decisoes de produto, roadmap, regras
│   │   ├── estilo/            # Guia de estilo, convencoes, formatacao
│   │   └── tecnico/           # Arquitetura, stack, principios, testes
│   ├── .claude/
│   │   ├── commands/          # Slash commands (/validate, /validate-tecnico, etc.)
│   │   └── skills/            # Skills invocaveis sob demanda
│   └── CLAUDE.md
│
└── .github/workflows/         # Pipelines de CI/CD
    ├── docs-full-scan.yml     # Geracao completa de documentacao
    ├── docs-incremental.yml   # Atualizacao incremental via PR
    └── code-validation.yml    # Validacao automatica de codigo
```

## Conceitos demonstrados

| Conceito | O que e | Onde ver |
|---|---|---|
| **CLAUDE.md** | Instrucoes persistentes, versionadas no repo | `demo/CLAUDE.md`, `validation-agent/CLAUDE.md` |
| **Hooks** | Comportamento deterministico (ex: rodar testes apos cada edicao) | `demo/.claude/settings.json` |
| **Prompt templates** | Prompts como codigo, versionados e revisaveis | `demo/prompts/` |
| **Modo CLI headless** | Claude Code rodando em pipeline, sem interface | `.github/workflows/` |
| **Custom slash commands** | Comandos personalizados do projeto | `validation-agent/.claude/commands/` |
| **Skills** | Instrucoes que o Claude invoca automaticamente quando o contexto pede | `validation-agent/.claude/skills/` |
| **Subagentes** | Tarefas decompostas com contexto isolado | `validation-agent/.claude/commands/validate.md` |

## Como usar

### Pre-requisitos

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) instalado
- Python 3.11+ (para o projeto demo)

### Demo: explorar o projeto

```bash
cd demo
claude
```

Experimente perguntar sobre a arquitetura, pedir testes ou gerar documentacao DBT.

### Validation agent: validar uma proposta

```bash
cd validation-agent
claude
```

Use o slash command para validar uma proposta contra a documentacao:

```
/project:validate Quero adicionar um endpoint que armazena CPF em uma tabela de analytics
```

Ou use os comandos individuais:

```
/project:validate-tecnico Quero usar a biblioteca requests para chamadas HTTP sincronas
/project:validate-compliance Quero armazenar dados de transacao incluindo CPF do cliente
/project:validate-produto Quero adicionar um modulo de pagamentos com gateway Pagar.me
```

### Pipelines CI/CD

Os workflows em `.github/workflows/` demonstram o Claude Code rodando em modo headless:

- **Full scan**: gera documentacao completa do projeto e abre PR
- **Incremental**: atualiza apenas a documentacao afetada por mudancas em PRs
- **Validacao**: valida codigo contra a documentacao do projeto e bloqueia PRs com conflitos
