# Workshop Demo Implementation — Design Spec

## Overview

This spec defines the implementation of two projects for the "Claude Code na Prática" workshop for Clínica do Leite:

1. **`demo/`** — A FastAPI + DBT application used for Bloco 1 (Claude Code intro), Bloco 2 (docs pipeline) demos
2. **`validation-agent/`** — A validation agent with subagents used for Bloco 3 (asteroid demo)

Both live in the same repository (`workshop-claude-code`), in separate folders. During demo time, separate Claude Code terminal windows are opened in each folder to isolate context — which itself becomes a teaching moment.

### Execution approach

Sequential, depth-first (Approach A): build the demo repo completely first (API + DBT + workflows + MkDocs), test end-to-end, then build the validation agent. Each piece is solid and testable before moving to the next.

### Deviations from workshop-spec.md

This design spec intentionally deviates from the original workshop spec in the following areas:

1. **DBT adapter: DuckDB instead of PostgreSQL** — The workshop spec (line 573) mentions "DBT Core com adapter PostgreSQL." This design uses DuckDB instead, which runs locally with zero server dependencies. This is a deliberate upgrade for demo reliability — no database server to configure or fail during the live demo. All references in CLAUDE.md, profiles.yml, and requirements should use DuckDB.

2. **Validation agent: 4 doc folders instead of 3** — The workshop spec has 3 folders (compliance, produto, tecnico). This design adds `docs/estilo/` for style/formatting compliance, as requested during brainstorming. The subagent dispatch changes from 3 independent subagents to: (1) compliance, (2) product + style, (3) technical. The orchestrator CLAUDE.md must reflect this grouping.

3. **Enhanced FastAPI architecture** — The workshop spec describes a simple CRUD app. This design adds repository pattern, event bus, middleware chain, exceptions hierarchy, and background tasks to make Claude's analysis non-trivial.

4. **Python version: 3.11+** — Consistent with workshop spec line 573. All code must target Python 3.11+.

### Teaching moments embedded in demos

| Demo block | Concept | What to show on screen |
|---|---|---|
| 1.3 — Claude Code intro | CLAUDE.md + context management | Open CLAUDE.md, contrast with ChatGPT |
| 1.4 — Guardrails | Hooks as deterministic behavior | Show settings.json hook example |
| 2.3 — Full scan | Skills / prompt templates | Open full-scan.md, "the prompt is code" |
| 2.4 — Incremental | CLI headless mode (`-p`) | Open workflow YAML, show `claude -p` line |
| 3.2 — Validation agent | Subagents + context isolation | Open CLAUDE.md, show subagent dispatch |

---

## Section 1: Demo repo — FastAPI application

### Architecture

A real, functional FastAPI application with SQLAlchemy + SQLite. Domain: customer/product/order management. The architecture is intentionally layered with indirection, events, and cross-cutting concerns to make Claude's analysis non-trivial.

### Structure

```
demo/
├── src/
│   └── api/
│       ├── main.py                     # FastAPI app, middleware registration, router includes
│       ├── config.py                   # Pydantic BaseSettings, environment-based config
│       ├── database.py                 # SQLAlchemy async engine + session factory (SQLite)
│       │
│       ├── models/
│       │   ├── base.py                 # Base model with id, created_at, updated_at
│       │   ├── customer.py             # name, email, phone, segment, is_active
│       │   ├── product.py              # name, description, price, stock, category, sku
│       │   ├── order.py                # customer_id (FK), status (state machine), total, notes
│       │   └── order_item.py           # order_id (FK), product_id (FK), quantity, unit_price
│       │
│       ├── schemas/                    # Pydantic request/response schemas (separate from DB models)
│       │   ├── customer.py
│       │   ├── product.py
│       │   ├── order.py
│       │   └── pagination.py           # Reusable PaginatedResponse[T] generic
│       │
│       ├── repositories/
│       │   ├── base.py                 # AbstractRepository with CRUD interface
│       │   ├── customer_repository.py  # Concrete, adds search_by_email, get_by_segment
│       │   ├── product_repository.py   # Concrete, adds filter_by_category, low_stock
│       │   └── order_repository.py     # Concrete, adds get_by_customer, get_by_status
│       │
│       ├── services/
│       │   ├── order_service.py        # Orchestrates: validate stock -> create order -> emit events
│       │   ├── inventory_service.py    # Stock reservation, stock release on cancel
│       │   ├── notification_service.py # Listens to events, logs (simulates email/SMS)
│       │   ├── analytics_service.py    # top_products, revenue_by_period, customer_ltv
│       │   └── pricing_service.py      # Discount rules, bulk pricing, calculates order total
│       │
│       ├── events/
│       │   ├── bus.py                  # Simple in-process event bus (publish/subscribe)
│       │   ├── types.py                # Event dataclasses: OrderCreated, OrderStatusChanged, StockLow
│       │   └── handlers.py             # Maps events -> service methods
│       │
│       ├── middleware/
│       │   ├── auth.py                 # API key validation from header
│       │   ├── logging.py              # Request/response logging with timing
│       │   ├── error_handler.py        # Maps exceptions -> HTTP responses
│       │   └── rate_limiter.py         # Simple in-memory rate limiter
│       │
│       ├── routes/
│       │   ├── customers.py            # CRUD + search + segment filtering
│       │   ├── products.py             # CRUD + category filter + low stock alert
│       │   ├── orders.py               # Create, get, list + status transitions (state machine)
│       │   └── analytics.py            # Dashboard endpoints using analytics_service
│       │
│       ├── exceptions/
│       │   ├── base.py                 # AppException hierarchy
│       │   ├── business.py             # InsufficientStock, InvalidStatusTransition, DuplicateEmail
│       │   └── infrastructure.py       # DatabaseError, ExternalServiceError
│       │
│       └── tasks/
│           ├── background.py           # FastAPI BackgroundTasks wrappers
│           └── order_processing.py     # Async post-order work: confirm, notify, update analytics
│
├── alembic.ini                            # Alembic config (at project root, standard placement)
├── migrations/                         # Alembic
│   ├── env.py
│   └── versions/
│       ├── 001_initial_schema.py
│       └── 002_add_order_items.py
│
├── tests/
│   ├── conftest.py                     # In-memory SQLite, test client, fixtures
│   ├── test_customers.py
│   ├── test_products.py
│   ├── test_orders.py                  # Including state machine transitions
│   ├── test_pricing_service.py
│   ├── test_inventory_service.py
│   └── test_event_bus.py
│
├── requirements.txt                    # fastapi, uvicorn, sqlalchemy, pytest, httpx, alembic, pydantic-settings
└── pyproject.toml                      # Project metadata, Python 3.11+ target
```

**Note:** All packages under `src/api/` include `__init__.py` files for explicit Python packaging. This ensures consistent import behavior across environments.

### Key design decisions

- **SQLite file** for dev, **in-memory SQLite** for tests — zero external dependencies
- **Order -> Customer FK** and **Order -> OrderItem -> Product** gives Claude real relationships to discover and diagram
- **Repository pattern** with abstract base class — indirection between routes and DB that Claude must trace
- **Event-driven flow** — creating an order emits `OrderCreated`, which triggers notification + analytics + inventory update via an event bus. Claude needs to trace this indirection.
- **State machine** — order status transitions have rules (can't go from `cancelled` back to `processing`). Hidden business logic.
- **Middleware chain** — auth, logging, error handling, rate limiting as cross-cutting concerns
- **Separation of schemas vs models** — Pydantic schemas != SQLAlchemy models
- **Custom exception hierarchy** — business exceptions vs. infrastructure exceptions
- **Background tasks** — async order processing using FastAPI BackgroundTasks
- **All async but no real external calls** — no Redis, no Celery, no external services
- **Tests use `httpx.AsyncClient`** with a test DB fixture — `pytest` runs clean with no setup

### What makes this non-trivial for Claude to analyze

- Routes don't touch the DB directly — they go through services -> repositories
- Creating an order triggers a chain: validate stock -> reserve inventory -> create order -> emit event -> notification + analytics
- Middleware, exceptions, and background tasks span multiple modules
- The event bus creates implicit coupling that doesn't show up in imports

---

## Section 2: Demo repo — DBT project

### Architecture

Real DBT project with DuckDB adapter. Seeds provide sample data. Models follow the staging -> intermediate -> marts convention (equivalent to the bronze/silver/gold medallion architecture the client's team uses).

### Structure

```
demo/
├── dbt/
│   ├── dbt_project.yml                 # Project config, DuckDB adapter
│   ├── profiles.yml                    # Local DuckDB profile
│   ├── packages.yml                    # dbt-utils for generic tests
│   │
│   ├── seeds/
│   │   ├── raw_customers.csv           # ~20 rows, realistic BR names/emails
│   │   ├── raw_products.csv            # ~15 products with categories, prices
│   │   └── raw_orders.csv              # ~50 orders with statuses, dates, amounts
│   │
│   ├── models/
│   │   ├── sources.yml                 # Declares raw seeds as sources (undocumented)
│   │   ├── staging/
│   │   │   ├── stg_customers.sql       # Clean, cast types, rename columns
│   │   │   ├── stg_products.sql        # Normalize category, parse SKU
│   │   │   └── stg_orders.sql          # Cast dates, map status codes to labels
│   │   ├── intermediate/
│   │   │   ├── int_customer_orders.sql # Join customers + orders, add order_count, total_spent
│   │   │   └── int_product_performance.sql # Product sales metrics aggregation
│   │   └── marts/
│   │       ├── dim_customers.sql       # Customer dimension with segment, LTV, first/last order
│   │       └── fct_orders.sql          # Fact table, refs int_customer_orders + stg_products
│   │
│   ├── macros/
│   │   └── cents_to_reais.sql          # Reusable currency conversion macro
│   │
│   └── tests/                          # Initially empty — Claude generates these
```

### Key design decisions

- **DuckDB** — runs locally, no server, `dbt build` works out of the box (intentional deviation from workshop spec's PostgreSQL — see Deviations section)
- **Seeds as sources** — no external database needed; seeds act as `raw` tables
- **`sources.yml` present but undocumented** — gives Claude more to discover
- **5 models across 3 layers** — enough for a meaningful lineage diagram, not so many that the demo drags
- **Two intermediate models** — creates a real DAG, not just a linear chain
- **`fct_orders` refs both intermediates and staging** — non-trivial lineage
- **Macro** — `cents_to_reais` used across models; Claude finding and documenting it is a good moment
- **No `schema.yml`** — intentionally missing, so Claude generates it during the demo
- **Expandable** — adding more models later is just new `.sql` files + more seed rows

### Dependencies

```
dbt-core>=1.7,<1.9
dbt-duckdb>=1.7,<1.9
dbt-utils>=1.1
```

These are pinned to compatible ranges. DuckDB adapter compatibility is version-sensitive — the implementer should verify `dbt-duckdb` works with the installed `dbt-core` version before proceeding.

### Seed data distribution

Seeds should have intentional distribution to produce interesting analytics:
- **Customers**: mix of segments (bronze/silver/gold), some active, some inactive, varied signup dates
- **Products**: spread across 3-4 categories, varied price ranges, some low stock
- **Orders**: spread across statuses (pending/processing/shipped/delivered/cancelled), some customers with many orders and some with only one, dates spanning 6+ months

This ensures Claude generates meaningful documentation and the analytics service queries produce non-trivial results.

### DAG (lineage)

```
raw_customers -> stg_customers -> int_customer_orders -> dim_customers
                                        |
raw_orders ---> stg_orders -----> int_customer_orders -> fct_orders
                                                            ^
raw_products -> stg_products --> int_product_performance    |
                       \------------------------------------/
```

---

## Section 3: Prompt templates + CLAUDE.md + MkDocs

### Structure

```
demo/
├── CLAUDE.md                           # Project instructions for Claude Code
├── prompts/
│   ├── full-scan.md                    # Mode 1: generate all docs from scratch
│   ├── incremental.md                  # Mode 2: update docs based on diff
│   └── dbt-docs.md                     # Standalone DBT documentation generation
├── mkdocs.yml                          # MkDocs config (Material theme)
├── docs/                               # Empty — generated by demos
└── scripts/
    ├── run-docs-generation.sh          # Wrapper: calls claude -p with prompt file
    └── setup-mkdocs.sh                 # Installs mkdocs + material, serves locally
```

### CLAUDE.md

Shown on screen during Bloco 1.3 teaching moment. Must be:
- Concise enough to show in 30 seconds
- Rich enough that the audience sees real value
- Written in Portuguese

Content: project description, stack with versions, naming conventions, DBT layer conventions with prefixes, documentation rules (language, format, mermaid diagrams), test conventions.

### Prompt templates

These are the "skills" highlighted in Bloco 2.3 teaching moment. They must:
- Look structured and intentional (sections, rules, output format) — not like a chat message
- Produce consistent results when run with `claude -p`
- Reference `${CHANGED_FILES}` in the incremental template (injected by CI)
- Cover the enhanced app structure: repositories, events, middleware, exceptions

Content follows the spec's existing templates (workshop-spec.md), adjusted for the enhanced architecture.

### MkDocs

- Material theme
- Portuguese navigation
- Auto-generated from `docs/` folder
- Nav mirrors doc categories (Architecture, API, Models, DBT, Services)
- Mermaid plugin enabled for rendering diagrams inline
- Search enabled
- Served locally with `mkdocs serve` for the demo

---

## Section 4: GitHub Actions workflows

### Workflow file location

GitHub Actions only runs workflows from `.github/workflows/` at the **repo root**. Since the demo code lives in `demo/`, the workflows live at the root but use `working-directory: demo` in their steps and `paths` filters scoped to `demo/`:

```
workshop-claude-code/                   # repo root
├── .github/
│   └── workflows/
│       ├── docs-full-scan.yml          # Mode 1: manual trigger
│       └── docs-incremental.yml        # Mode 2: triggers on PRs touching demo/
```

### `docs-full-scan.yml`

- **Trigger**: `workflow_dispatch` (manual)
- **Steps** (all using `working-directory: demo`):
  1. Checkout repo
  2. Setup Node.js 20
  3. Install Claude Code CLI
  4. Run Claude in headless mode with prompt file (see CLI flags below)
  5. Create PR via `peter-evans/create-pull-request`
     - Branch: `docs/full-scan-{timestamp}`
     - Title: "docs: geracao completa de documentacao via Claude Code"

### `docs-incremental.yml`

- **Trigger**: `pull_request` on paths `demo/src/**`, `demo/dbt/**`
- **Steps** (all using `working-directory: demo`):
  1. Checkout with `fetch-depth: 0` (full history for diff)
  2. Compute changed files via `git diff origin/main...HEAD -- demo/`
  3. Setup Node.js 20
  4. Install Claude Code CLI
  5. Run Claude in headless mode with prompt file and `CHANGED_FILES` env var
  6. Commit updated docs back to PR branch (only if docs changed)

### CLI flags

The exact Claude Code CLI flags must be validated against the installed version before the workshop. The canonical invocation pattern is:

```bash
claude -p "$(cat prompts/full-scan.md)" --allowedTools Edit,Write,Read,Glob,Grep,Bash
```

**Important notes:**
- `-p` (alias for `--print`) runs Claude headless with no interactive UI. This is the teaching moment in Bloco 2.4.
- `-p` accepts a prompt string, not a file path. Use `$(cat prompts/file.md)` to pass file contents as the prompt.
- `--allowedTools` restricts what Claude can do in CI — a guardrail to mention during the demo.
- There is no `--output-dir` flag. Claude writes files directly via its Edit/Write tools.
- The incremental template's `${CHANGED_FILES}` is injected as a shell env var before the prompt is read.

**These flags MUST be tested end-to-end before the workshop.** Run `claude --help` to verify the exact flag names and syntax.

### Key design decisions

- **Headless mode** — no interactive UI in CI. Teaching moment in Bloco 2.4.
- **Tool restrictions** — `--allowedTools` limits Claude's CI capabilities. Guardrail.
- **Changed files as env var** — incremental prompt uses `${CHANGED_FILES}`. Claude only analyzes what changed.
- **PR-based output** — full scan creates new PR; incremental commits to existing PR branch. Both require human review.
- **`working-directory: demo`** — all steps run inside `demo/`, so Claude's context is scoped correctly.
- **Auth**: `ANTHROPIC_API_KEY` in GitHub Secrets for CI. Local demos use normal Claude Code subscription.

### Pre-workshop testing required

- Exact `claude` CLI flags (run `claude --help` to verify)
- Token limits for full scan on the repo
- PR creation permissions (`contents: write`, `pull-requests: write`)
- Incremental commit push-back to PR branch
- `working-directory` behavior with `peter-evans/create-pull-request`

---

## Section 5: Validation agent

### Architecture

An orchestrator agent (CLAUDE.md) that dispatches three subagents, each with isolated context. Supports two modes: reviewing existing code changes (guardrail) and evaluating proposals before implementation (decision partner).

### Structure

```
validation-agent/
├── CLAUDE.md                           # Orchestrator with dual mode (review + brainstorm)
│
├── docs/
│   ├── compliance/
│   │   ├── requisitos-lgpd.md          # LGPD: consent, data minimization, retention
│   │   ├── politica-dados.md           # Data classification, PII handling, anonymization
│   │   └── restricoes-integracao.md    # Approved external APIs, auth requirements
│   │
│   ├── produto/
│   │   ├── decisoes-produto.md         # Decisions taken: scope, priorities, what's out
│   │   ├── roadmap.md                  # Quarterly plans, dependencies
│   │   └── regras-negocio.md           # Business rules: pricing, discounts, order limits
│   │
│   ├── tecnico/
│   │   ├── decisoes-arquitetura.md     # ADR-style architecture decisions
│   │   ├── stack-definida.md           # Approved stack, versions, what's NOT allowed
│   │   ├── principios-tecnicos.md      # Async for external calls, functional core/imperative shell,
│   │   │                               # immutability by default, no ORM in analytics queries,
│   │   │                               # error handling (Result type over exceptions)
│   │   └── padroes-testes.md           # Test pyramid, coverage, no mocking DB,
│   │                                   # integration tests for external boundaries
│   │
│   └── estilo/
│       ├── guia-estilo-codigo.md       # Naming, file organization
│       ├── convencoes-documentacao.md   # Docstrings, READMEs, changelog rules
│       └── padroes-formatacao.md       # Line length, imports, type annotations
│
└── scenarios/
    ├── scenario-1/                     # Payment gateway (PRIMARY demo)
    │   ├── step-1-implement.md         # Prompt: build sync payment + CPF in analytics
    │   ├── step-2-validate.md          # Prompt: review the changes against docs
    │   ├── step-3-brainstorm.md        # Prompt: pre-implementation consultation
    │   └── expected-findings.md        # Reference: what should be caught
    ├── scenario-2/                     # React->Vue migration (backup)
    │   ├── step-1-implement.md
    │   ├── step-2-validate.md
    │   ├── step-3-brainstorm.md
    │   └── expected-findings.md
    └── scenario-3/                     # Raw SQL analytics (backup)
        ├── step-1-implement.md
        ├── step-2-validate.md
        ├── step-3-brainstorm.md
        └── expected-findings.md
```

### CLAUDE.md — Orchestrator

Dispatches three subagents (intentional deviation from workshop spec's 3-way split — see Deviations section):
1. **Compliance subagent** — reads `docs/compliance/`, checks LGPD, data policies, integration restrictions
2. **Product + Style subagent** — reads `docs/produto/` + `docs/estilo/`, checks product decisions, roadmap, style compliance
3. **Technical subagent** — reads `docs/tecnico/`, checks architecture, stack, principles, test standards

Each subagent only sees its assigned folders (context isolation). They run in parallel and return structured findings.

### Subagent dispatch mechanism

The CLAUDE.md instructs Claude to use the **Agent tool** (Claude Code's built-in subagent dispatch) to spawn three parallel agents. Each agent receives:
- A specific task description ("Analyze the following proposal/code against compliance documentation")
- Explicit file scope ("Read ONLY files in docs/compliance/")
- Output format (structured: compatible / attention / conflict with citations)

Example instruction in CLAUDE.md:
```
Quando o usuário pedir validação, use a ferramenta Agent para disparar 3 subagentes em paralelo:
- Subagente 1: Leia APENAS os arquivos em docs/compliance/ e valide contra requisitos regulatórios
- Subagente 2: Leia APENAS os arquivos em docs/produto/ e docs/estilo/ e valide contra decisões de produto e padrões de estilo
- Subagente 3: Leia APENAS os arquivos em docs/tecnico/ e valide contra decisões técnicas e princípios
```

This uses Claude Code's native Agent tool, which is visible in the terminal output — the audience can see the subagents being dispatched, which supports the teaching moment.

### Code directory for implementation scenarios

When the step-1 prompt asks Claude to implement code (e.g., PaymentService), Claude will create a `src/` directory on the fly inside `validation-agent/`. This is intentional — the directory doesn't exist beforehand because the validation agent project is a documentation-only project. Claude creating files demonstrates that it's a real implementation, not a mock. After the demo, these files can be cleaned up with `git checkout .` to reset for the next run.

### Dual mode support

**Mode 1: Code review** — when user asks to review changes or code:
- Identify new/modified files
- Analyze each against relevant documentation
- Report violations with document citations

**Mode 2: Proposal validation** — when user describes an idea before implementing:
- Analyze proposal against all documentation
- Identify potential conflicts
- Suggest aligned alternatives

### Document content guidelines

Each doc must be:
- **Credible** — reads like real company internal docs
- **Specific** — concrete decisions with dates and reasoning
- **Interconnected** — some decisions reference other docs
- **Opinionated** — clear "we do X, we don't do Y" statements

### Demo scenarios

| Scenario | Implementation prompt (step 1) | Expected conflicts |
|---|---|---|
| 1 (primary) | Build sync PaymentService + store CPF in analytics table | `principios-tecnicos.md` (async), `requisitos-lgpd.md` (data minimization), `restricoes-integracao.md` (circuit breaker) |
| 2 (backup) | Implement React->Vue migration + mock DB in tests | `stack-definida.md` (React), `padroes-testes.md` (no mocking DB), `decisoes-produto.md` (rewrite not in roadmap) |
| 3 (backup) | Add raw SQL analytics endpoint with PII | `requisitos-lgpd.md` (PII in analytics), `decisoes-arquitetura.md` (query patterns) |

### Scenario prompt content specification

Each `step-1-implement.md` must be a concrete implementation request that tells Claude exactly what to build. The prompt should:
- Specify file paths to create (e.g., `src/services/payment_service.py`, `src/routes/payments.py`)
- Describe the functionality in enough detail that Claude produces complete, runnable code
- Include the "wrong" decisions naturally (e.g., "use requests for simplicity" implies sync)
- NOT mention the project docs — the implementer Claude is just building what was asked

Each `step-2-validate.md` must:
- Ask Claude to review all new/modified files in the repository
- Reference the project documentation folders explicitly
- Request structured output (compatible/attention/conflict format)

Each `step-3-brainstorm.md` must:
- Describe the same idea as step-1 but as a proposal, not an implementation request
- Ask "does this align with our project decisions?"
- Be conversational in tone — simulating a developer thinking out loud

**Scenario 1 step-1 prompt content:**

```
Implementa um PaymentService para integração com o gateway da Pagar.me.

Cria os seguintes arquivos:
- src/services/payment_service.py — serviço que processa pagamentos
- src/models/payment_analytics.py — model para armazenar dados de transação
- src/routes/payments.py — rota POST /payments/process

Requisitos:
- Usar a biblioteca requests para fazer a chamada HTTP para a API da Pagar.me
- Timeout de 30 segundos na chamada
- Armazenar os dados da transação na tabela de analytics, incluindo:
  CPF do cliente, valor, status, timestamp
- Retornar o status da transação ao caller
- Tratar erros básicos (timeout, resposta inválida)
```

**Scenario 1 step-2 prompt content:**

```
Revisa todas as mudanças recentes neste repositório. Analisa todos os arquivos
novos ou modificados e valida contra a documentação do projeto nas pastas docs/.

Para cada arquivo, verifica conformidade com:
- Princípios técnicos e decisões de arquitetura
- Requisitos de compliance e LGPD
- Restrições de integrações externas
- Padrões de teste e estilo

Reporta no formato: compatível / atenção / conflito, sempre citando
o documento e trecho específico.
```

**Scenario 1 step-3 prompt content:**

```
Estou pensando em implementar a integração com um gateway de pagamento
(Pagar.me). Minha ideia inicial:
- Usar chamada HTTP síncrona com requests pra simplicidade
- Timeout de 30 segundos
- Guardar CPF do cliente junto com os dados da transação numa tabela
  de analytics pra facilitar reconciliação financeira

Antes de eu começar: isso bate com o que já foi decidido no projeto?
Tem alguma restrição que eu deveria considerar?
```

### Demo flow (Bloco 3)

1. Open Claude Code in `validation-agent/`
2. Paste scenario 1 step-1 prompt — Claude implements the wrong thing (may warn but proceeds)
3. Then paste step-2 prompt — validation agent subagents catch the violations
4. Verbal: explain the brainstorm mode (step-3) as pre-implementation consultation
5. Teaching moment: "What makes this reliable is the architecture — isolated context, clear instructions, decomposed tasks"

Audience takeaway: two use cases — **guardrail in the pipeline** (catches errors post-hoc) and **decision partner** (prevents errors before implementation).

---

## Section 6: Overall repo structure

### Top-level layout

```
workshop-claude-code/
├── workshop-spec.md                    # Workshop spec (not shown in demo)
│
├── .github/
│   └── workflows/                      # GitHub Actions (must be at repo root)
│       ├── docs-full-scan.yml          # Mode 1, uses working-directory: demo
│       └── docs-incremental.yml        # Mode 2, uses working-directory: demo
│
├── demo/                               # Bloco 1 + Bloco 2 demos
│   ├── CLAUDE.md
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── mkdocs.yml
│   ├── src/api/                        # FastAPI app (Section 1)
│   ├── migrations/                     # Alembic (Section 1)
│   ├── tests/                          # Pytest (Section 1)
│   ├── dbt/                            # DBT project (Section 2)
│   ├── prompts/                        # Prompt templates (Section 3)
│   ├── scripts/                        # Helper scripts (Section 3)
│   └── docs/                           # Empty — generated by demos
│
├── validation-agent/                   # Bloco 3 demo
│   ├── CLAUDE.md
│   ├── docs/                           # compliance/, produto/, tecnico/, estilo/
│   └── scenarios/                      # scenario-1/, scenario-2/, scenario-3/
│
└── docs/
    └── guia-rapido.md                  # Post-workshop deliverable
```

### Demo window mapping

| Demo moment | Terminal opens in | What it shows |
|---|---|---|
| Bloco 1.3 — Claude Code intro | `demo/` | CLAUDE.md, architecture analysis, test generation |
| Bloco 2.3 — Full scan | `demo/` | Prompt template -> docs generated -> PR |
| Bloco 2.4 — Incremental | `demo/` (+ GitHub browser) | Code change -> CI runs -> docs PR |
| Bloco 3.2 — Implement wrong thing | `validation-agent/` | Step 1: Claude builds violating code |
| Bloco 3.2 — Validate | `validation-agent/` | Step 2: Subagents catch the problems |

### Authentication

- **Local demos**: normal Claude Code subscription (interactive login)
- **GitHub Actions**: `ANTHROPIC_API_KEY` in GitHub Secrets (API billing)

### GitHub repo

- Needs to be public or client given access (shared as post-workshop deliverable)
- `ANTHROPIC_API_KEY` never in code, only in GitHub Secrets
- Fallback: pre-run PRs already open as backup if CI is slow during live demo
