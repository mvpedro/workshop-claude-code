# Restricoes de integracao com servicos externos

> Ultima revisao: 2025-12-01
> Responsavel: Equipe de Arquitetura + Compliance
> Contexto: Estabelecido apos incidente de cascading failure em agosto de 2025

## Contexto

Este documento define as restricoes e requisitos para integracao com servicos externos (APIs de terceiros, gateways de pagamento, provedores de comunicacao). Foi criado apos o incidente de producao de agosto de 2025, onde uma falha no gateway de pagamento causou timeout em cascata que derrubou o sistema por 2 horas (ver `principios-tecnicos.md` para mais detalhes sobre o incidente).

## Regra geral de resiliencia

**REGRA CRITICA**: Toda integracao com gateway de pagamento deve implementar circuit breaker e retry com backoff exponencial. Chamadas sem circuit breaker nao passam em code review.

Motivacao: o incidente de 2025-08 ocorreu porque a integracao com Pagar.me usava chamada sincrona sem circuit breaker. Quando o gateway ficou lento (resposta em 25-30s ao inves de 200ms), todas as threads do servidor ficaram bloqueadas aguardando resposta, causando indisponibilidade total.

## Padroes obrigatorios para integracoes

### Circuit breaker

Configuracao padrao:
- **Threshold de abertura**: 5 falhas consecutivas
- **Tempo de half-open**: 30 segundos
- **Timeout por chamada**: 5 segundos (nao 30s — aprendizado do incidente)
- Biblioteca recomendada: `circuitbreaker` (Python) ou implementacao propria com mesma interface

### Retry com backoff

Configuracao padrao:
- **Maximo de retries**: 3
- **Backoff**: exponencial — 1s, 2s, 4s
- **Jitter**: aleatorio de 0 a 500ms (evita thundering herd)
- Nunca fazer retry em erros 4xx (exceto 429 Too Many Requests)
- Sempre fazer retry em erros 5xx e timeouts

### Fallback

Toda integracao deve ter um comportamento de fallback definido:
- Gateway de pagamento: enfileirar para processamento posterior, retornar status "pendente"
- Email/SMS: enfileirar e retornar sucesso (eventual consistency)
- APIs de consulta: retornar dado cacheado (se disponivel) ou erro gracioso

## APIs externas aprovadas

| Servico | Provedor | Status | Modo | Restricoes |
|---|---|---|---|---|
| Gateway de pagamento | Pagar.me | ✅ Aprovado | Assincrono apenas | Circuit breaker obrigatorio, timeout 5s, retry com backoff |
| Email transacional | AWS SES | ✅ Aprovado | Assincrono | Rate limit: 14 emails/segundo, templates pre-aprovados |
| SMS | Twilio | ✅ Aprovado | Assincrono | Apenas para OTP e notificacoes criticas, nunca marketing |
| Analytics externo | — | ❌ Nao aprovado | — | Nenhum provedor aprovado ainda. Usar analytics interno |
| CDN | — | 🔄 Em avaliacao | — | Cloudflare e AWS CloudFront em avaliacao |

### Pagar.me — Detalhamento

- Ambiente: sandbox para dev/staging, producao com credenciais rotacionadas
- Autenticacao: API key no header, nunca em query string
- **Modo obrigatorio: assincrono**. Usar webhooks para confirmacao de pagamento
- Fluxo: enviar requisicao -> receber `transaction_id` -> aguardar webhook com status final
- Nunca bloquear a thread esperando resposta sincrona do gateway
- Dados de cartao: nunca trafegar pelo nosso sistema (usar tokenizacao Pagar.me)

### AWS SES — Detalhamento

- Regiao: sa-east-1 (Sao Paulo)
- Bounce handling: configurado via SNS, monitored pelo time de infra
- Templates: todo novo template deve ser aprovado por produto antes de ir pra producao

### Twilio — Detalhamento

- Uso restrito: OTP (verificacao de telefone) e notificacoes criticas (pedido confirmado, pagamento aprovado)
- Nunca usar para: marketing, lembretes, promocoes
- Rate limit interno: 1 SMS por usuario a cada 60 segundos (anti-abuse)

## Integracoes nao permitidas

As seguintes integracoes foram avaliadas e rejeitadas:

| Servico | Motivo da rejeicao | Data da decisao |
|---|---|---|
| Stripe | Sem operacao completa no Brasil, custos de FX | 2025-06 |
| SendGrid | Migrado para AWS SES por custo e confiabilidade | 2025-07 |
| Firebase Auth | Lock-in excessivo, preferencia por solucao propria | 2025-09 |

## Monitoramento

Toda integracao externa deve ter:
- Dashboard de latencia (p50, p95, p99)
- Alertas para taxa de erro > 5% em janela de 5 minutos
- Log estruturado de cada chamada (sem dados sensiveis — ver `politica-dados.md`)

---

*Este documento deve ser revisado a cada nova integracao proposta.*
*Ver tambem: `principios-tecnicos.md`, `politica-dados.md`*
