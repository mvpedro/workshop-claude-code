# Cenario 2 — Achados esperados: Migracao React para Vue.js + mock de banco

Este documento lista os conflitos que o agente de validacao DEVE identificar ao
analisar o codigo/proposta do cenario 2.

## Conflitos esperados

### 1. Vue.js nao e framework aprovado

- **Documento**: `docs/tecnico/stack-definida.md` — Frameworks frontend NAO permitidos
- **Trecho**: "Vue.js — Time sem expertise, React ja consolidado, custo de migracao injustificavel" (rejeitado em 2025-09)
- **Problema**: A proposta quer migrar para Vue.js, que foi explicitamente avaliado e rejeitado. React e o unico framework frontend aprovado.
- **Severidade**: ❌ Conflito

### 2. Rewrite de frontend fora do escopo

- **Documento**: `docs/produto/decisoes-produto.md` — DP-001
- **Trecho**: "Rewrite de frontend esta fora do escopo ate Q3 2026."
- **Problema**: A proposta e essencialmente um rewrite de frontend (trocar framework). Isso foi decidido como fora do escopo com razoes documentadas: frontend atual atende, time tem expertise em React, backlog de negocio tem prioridade.
- **Contexto adicional**: `docs/produto/roadmap.md` coloca revisao de frontend apenas em Q3 2026.
- **Severidade**: ❌ Conflito

### 3. Mock de banco de dados nos testes

- **Documento**: `docs/tecnico/padroes-testes.md` — Regra critica
- **Trecho**: "NUNCA mockar o banco de dados. Testes de integracao devem usar banco real (SQLite in-memory)."
- **Problema**: O step-1 pede para mockar o repository (e portanto o banco) nos testes de integracao. O documento explica por que isso e problematico: mocks nao reproduzem constraints, queries reais, ou problemas de migracao.
- **Severidade**: ❌ Conflito

## Pontos de atencao adicionais

### 4. Processo de mudanca de stack

- **Documento**: `docs/tecnico/stack-definida.md` — Processo de mudanca
- **Trecho**: "Para propor uma mudanca na stack: 1. Criar ADR em decisoes-arquitetura.md..."
- **Problema**: A proposta nao segue o processo formal. Nao foi criada uma ADR, nao houve revisao pelo time de arquitetura.
- **Severidade**: ⚠️ Atencao

## Nuancias que o agente deve captar

- O conflito de Vue.js vem de DOIS documentos: stack-definida.md (tecnologia rejeitada) E decisoes-produto.md (rewrite fora de escopo). Sao conflitos complementares mas distintos.
- O conflito de mock de banco e independente do conflito de framework — mesmo se a migracao fosse aprovada, os testes ainda estariam errados.
- O agente deve reconhecer que a motivacao do desenvolvedor (Vue e mais simples, testes mais rapidos) e valida, mas conflita com decisoes ja tomadas.
