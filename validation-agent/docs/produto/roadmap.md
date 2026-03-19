# Roadmap de produto

> Ultima atualizacao: 2026-01-15
> Responsavel: Product Owner
> Horizonte: Q1 2026 — Q4 2026

## Contexto

Este roadmap define as prioridades trimestrais do produto. As decisoes registradas em `decisoes-produto.md` informam e restringem este planejamento. As regras de negocio em `regras-negocio.md` definem o comportamento esperado das features.

## Q1 2026 — Estabilizar o core (Janeiro - Marco)

**Tema**: Confiabilidade e resiliencia

Prioridades:
1. **Implementar circuit breaker no fluxo de pagamento** — Pagar.me com retry e fallback (ver `restricoes-integracao.md`)
2. **Refatorar chamadas externas para modo assincrono** — eliminar chamadas sincronas bloqueantes (ver `principios-tecnicos.md`)
3. **Implementar politica de retencao de dados** — jobs de limpeza para dados expirados (ver `requisitos-lgpd.md`)
4. **Aumentar cobertura de testes** — meta: 80% em services, 70% em routes (ver `padroes-testes.md`)
5. **Auditoria de dados pessoais em tabelas de analytics** — remover PII de tabelas analiticas (descoberto na auditoria de 2025-09)

Status: EM ANDAMENTO

## Q2 2026 — Dashboard de analytics (Abril - Junho)

**Tema**: Visibilidade para o time comercial

Prioridades:
1. **Dashboard de metricas de vendas** — receita por periodo, ticket medio, taxa de conversao
2. **Dashboard de clientes** — segmentacao, LTV, churn risk (dados anonimizados)
3. **Dashboard de produtos** — performance por categoria, estoque critico
4. **API de exportacao de relatorios** — CSV/Excel com dados agregados (nunca PII)

Dependencias:
- Q1 concluido (especialmente item 5 — PII removido de analytics)
- Stack de frontend React mantida (ver `decisoes-produto.md` DP-001)

Status: PLANEJADO

## Q3 2026 — Avaliar novas integracoes (Julho - Setembro)

**Tema**: Expansao controlada

Prioridades:
1. **Revisao da decisao de rewrite frontend** — reavaliar se migracao de framework faz sentido dado o estado do produto
2. **Avaliar novos gateways de pagamento** — Stripe, PayPal, Pix direto (ver `decisoes-produto.md` DP-002)
3. **Avaliar CDN** — Cloudflare vs AWS CloudFront (ver `restricoes-integracao.md`)
4. **Automacao de compliance** — reports automaticos para LGPD

Dependencias:
- Fluxo Pagar.me estavel por 3+ meses
- Dashboard de analytics entregue e validado

Status: PLANEJADO

## Q4 2026 — A definir (Outubro - Dezembro)

**Tema**: Sera definido com base nos resultados de Q2 e Q3.

Candidatos:
- Expansao do dashboard com metricas preditivas
- Novos canais de notificacao (WhatsApp Business API)
- Programa de fidelidade (se validado com time comercial)

Status: NAO PLANEJADO

## Principios de priorizacao

1. **Estabilidade antes de features novas** — Q1 foca em solidificar o que existe
2. **Dados antes de integracao** — Dashboard (Q2) antes de novos gateways (Q3)
3. **Decisoes de produto respeitadas** — nenhuma feature que contradiga `decisoes-produto.md` entra no roadmap sem revisao formal

---

*Roadmap revisado mensalmente. Proxima revisao: 2026-02-15.*
*Ver tambem: `decisoes-produto.md`, `regras-negocio.md`*
