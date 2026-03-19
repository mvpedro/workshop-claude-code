# Decisoes de produto

> Ultima atualizacao: 2026-01-10
> Responsavel: Product Owner
> Formato: registro cronologico de decisoes com contexto

## Contexto

Este documento registra decisoes de produto ja tomadas, com data, contexto e motivacao. O objetivo e evitar que decisoes sejam rediscutidas sem novas informacoes e garantir que o time de desenvolvimento saiba o que esta (e o que nao esta) no escopo.

Ver tambem: `roadmap.md` para planejamento trimestral e `regras-negocio.md` para regras operacionais.

## Decisoes vigentes

### DP-001: Rewrite de frontend fora do escopo (2025-11-20)

**Decisao**: Rewrite de frontend esta fora do escopo ate Q3 2026.

**Contexto**: Em novembro de 2025, o time de desenvolvimento sugeriu migrar o frontend de React para um framework mais recente. A proposta foi avaliada e rejeitada pelo comite de produto pelas seguintes razoes:
- O frontend atual (React) atende aos requisitos funcionais
- O time tem expertise consolidada em React
- O backlog de features de negocio tem prioridade sobre refatoracao tecnica
- Estimativa de esforco do rewrite: 3-4 meses, inviavel dado o roadmap atual

**Impacto**: qualquer proposta de migracao de framework frontend deve ser adiada ate a revisao de Q3 2026 (ver `roadmap.md`). Melhorias incrementais no frontend React sao permitidas.

### DP-002: Novas integracoes de pagamento apos estabilizacao (2025-12-05)

**Decisao**: Novas integracoes de pagamento so apos estabilizacao do fluxo atual (Q2 2026).

**Contexto**: Apos o incidente de agosto de 2025 com o gateway Pagar.me (ver `restricoes-integracao.md`), decidiu-se que:
- O fluxo atual com Pagar.me precisa ser estabilizado com circuit breaker, retry e fallback
- Nenhum novo gateway sera integrado ate que o fluxo atual esteja estavel por pelo menos 3 meses
- A estabilizacao esta prevista para conclusao em Q1 2026, com 3 meses de observacao ate Q2 2026

**Impacto**: propostas de integrar Stripe, PayPal ou outros gateways devem aguardar Q2 2026. O foco e solidificar Pagar.me primeiro.

### DP-003: Dashboard de analytics como prioridade Q2 2026 (2026-01-10)

**Decisao**: Dashboard de analytics para o time comercial e a principal entrega de Q2 2026.

**Contexto**: O time comercial precisa de visibilidade sobre metricas de vendas, comportamento de clientes e performance de produtos. Hoje usam planilhas manuais. O dashboard deve:
- Mostrar metricas agregadas (nunca dados pessoais)
- Ser acessivel via web
- Atualizar diariamente (nao precisa ser real-time)

**Impacto**: features de analytics tem prioridade sobre novas integracoes no Q2 2026. Ver `roadmap.md`.

### DP-004: Internacionalizacao nao planejada (2025-10-15)

**Decisao**: Nao ha planos de internacionalizacao (i18n) para o sistema.

**Contexto**: O produto atende exclusivamente o mercado brasileiro. Todos os textos, moeda (BRL), formatos de data (dd/mm/yyyy) e documentos (CPF) sao brasileiros. Nao ha demanda de internacionalizacao no horizonte visivel.

**Impacto**: nao investir em abstraccoes de i18n. Strings podem ser hardcoded em portugues. Moeda sempre BRL.

### DP-005: Sem app mobile nativo (2025-09-20)

**Decisao**: O produto sera web-only. Sem app mobile nativo.

**Contexto**: O publico-alvo acessa via desktop (80%) e navegador mobile (20%). Um app nativo nao se justifica pelo custo de manutencao. O frontend web deve ser responsivo.

---

*Novas decisoes devem ser registradas neste documento com data e contexto.*
*Ver tambem: `roadmap.md`, `regras-negocio.md`*
