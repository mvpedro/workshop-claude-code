# Regras de negocio

> Ultima atualizacao: 2025-12-15
> Responsavel: Product Owner + Time Comercial
> Aprovado por: Diretoria

## Contexto

Este documento define as regras de negocio implementadas no sistema. Estas regras sao a fonte de verdade para o comportamento esperado — qualquer implementacao que desvie destas regras deve ser tratada como bug, nao como feature.

Ver tambem: `decisoes-produto.md` para decisoes de escopo e `roadmap.md` para priorizacao.

## 1. Precificacao

### Regras de preco

- Precos sempre em BRL (centavos internamente, reais na interface)
- Preco minimo por produto: R$ 0,01 (nunca zero — produtos gratuitos nao sao suportados)
- Preco maximo por produto: R$ 999.999,99
- Precos com no maximo 2 casas decimais
- Alteracao de preco nao afeta pedidos ja confirmados (snapshot no momento do pedido)

### Descontos

| Tipo | Descricao | Limite |
|---|---|---|
| Cupom percentual | Desconto % sobre o total | Maximo 30% |
| Cupom valor fixo | Desconto em R$ sobre o total | Maximo R$ 500,00 |
| Desconto por volume | Automatico acima de 10 unidades do mesmo produto | 5% |
| Desconto fidelidade | Para clientes Gold, automatico | 10% |

Regras de combinacao:
- Cupom percentual e cupom valor fixo NAO sao cumulativos (aplica o maior)
- Desconto por volume e desconto fidelidade SAO cumulativos entre si
- Desconto maximo total em qualquer pedido: 40% (trava de seguranca)
- Cupons expiram em 30 dias apos emissao

## 2. Pedidos

### Limites

- Minimo por pedido: R$ 10,00
- Maximo por pedido: R$ 50.000,00
- Maximo de itens distintos por pedido: 50
- Maximo de unidades por item: 100
- Maximo de pedidos pendentes por cliente: 5

### Estado do pedido (state machine)

```
pendente -> confirmado -> em_processamento -> enviado -> entregue
    |           |               |
    v           v               v
cancelado   cancelado       cancelado (com estorno)
```

Regras de transicao:
- `pendente -> confirmado`: apos confirmacao de pagamento (webhook Pagar.me)
- `confirmado -> em_processamento`: automatico, apos reserva de estoque confirmada
- `em_processamento -> enviado`: manual, pelo time de operacoes
- `enviado -> entregue`: manual ou automatico (tracking)
- Cancelamento: possivel ate `em_processamento`. Apos `enviado`, apenas devolucao
- Cancelamento com estorno: se pagamento ja foi capturado, gera solicitacao de estorno automatica

### Estoque

- Reserva de estoque no momento da confirmacao do pedido
- Liberacao de estoque automatica em cancelamento
- Alerta de estoque baixo: quando quantidade < 10 unidades
- Estoque negativo: NAO permitido (validacao sincrona antes de confirmar)

## 3. Segmentos de cliente

| Segmento | Criterio | Beneficios |
|---|---|---|
| Bronze | Padrao (todos os novos clientes) | Nenhum beneficio adicional |
| Silver | 5+ pedidos entregues OU R$ 1.000+ em compras | Frete gratis acima de R$ 200 |
| Gold | 15+ pedidos entregues OU R$ 5.000+ em compras | 10% desconto automatico + frete gratis |

Regras:
- Upgrade de segmento: avaliado mensalmente (job automatico)
- Downgrade: nao ocorre (uma vez Gold, sempre Gold)
- Segmento calculado com base nos ultimos 12 meses de pedidos entregues
- Excecao ao downgrade: se nao houver pedido em 24 meses, volta para Bronze

## 4. Notificacoes

| Evento | Canal | Obrigatorio |
|---|---|---|
| Pedido confirmado | Email + SMS | Sim |
| Pedido enviado | Email | Sim |
| Pedido entregue | Email | Nao (opt-in) |
| Estoque reposto (wishlist) | Email | Nao (opt-in) |
| Cupom proximo de expirar | Email | Nao (opt-in) |

Regra: notificacoes obrigatorias nao podem ser desativadas pelo usuario. Notificacoes opt-in respeitam preferencia do usuario (ver `requisitos-lgpd.md` sobre consentimento).

---

*Regras de negocio devem ser validadas com time comercial a cada trimestre.*
*Ver tambem: `decisoes-produto.md`, `roadmap.md`*
