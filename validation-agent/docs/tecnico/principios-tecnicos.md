# Principios tecnicos

> Ultima atualizacao: 2025-11-20
> Responsavel: Time de arquitetura
> Status: Vigente — estes principios guiam todas as decisoes de implementacao

## Contexto

Este documento define os principios tecnicos do projeto. Nao sao sugestoes — sao regras de implementacao que o time concordou em seguir. Desvios devem ser discutidos e, se aceitos, documentados como excecao explicita.

Ver tambem: `stack-definida.md` para tecnologias aprovadas, `decisoes-arquitetura.md` para decisoes formais, `padroes-testes.md` para padroes de teste.

---

## Principio 1: Chamadas externas DEVEM ser assincronas

**Regra**: Chamadas a servicos externos DEVEM ser assincronas (`httpx.AsyncClient`, nunca `requests` sincrono).

**Motivacao**: Timeout de 30s no gateway de pagamento causou cascading failures em producao (incidente 2025-08). O servidor tinha 4 workers. Quando o gateway ficou lento (25-30s por chamada), todas as 4 threads ficaram bloqueadas aguardando resposta sincrona. Nenhuma nova requisicao era processada. O sistema ficou indisponivel por 2 horas ate restart manual.

**Implementacao**:
- Usar `httpx.AsyncClient` para todas as chamadas HTTP externas
- Nunca importar ou usar a biblioteca `requests` — ela e sincrona por natureza
- Timeout padrao: 5 segundos (nao 30s — aprendizado do incidente)
- Sempre em conjunto com circuit breaker (ver `restricoes-integracao.md`)

**Excecoes aceitas**: nenhuma. Toda chamada externa e assincrona, sem excecao.

---

## Principio 2: Functional core, imperative shell

**Regra**: Logica de negocio deve ser implementada como funcoes puras sempre que possivel. Side effects (banco, APIs, notificacoes) ficam na camada externa (shell).

**Motivacao**: Funcoes puras sao mais faceis de testar, raciocinar e compor. O service layer orquestra side effects, mas a logica de calculo (pricing, validacao de regras, state machine) deve ser pura.

**Implementacao**:
- `PricingService.calculate_discount()` — funcao pura, recebe dados, retorna resultado
- `OrderService.create_order()` — shell, orquestra: valida (puro) -> persiste (side effect) -> emite evento (side effect)
- Regras de negocio (ver `regras-negocio.md`) implementadas como funcoes puras testadas unitariamente

---

## Principio 3: Imutabilidade por padrao

**Regra**: Preferir estruturas imutaveis. Dataclasses com `frozen=True`, Pydantic models com `model_config = ConfigDict(frozen=True)` onde possivel.

**Motivacao**: Imutabilidade elimina uma classe inteira de bugs (mutacao acidental de estado compartilhado). Especialmente importante em contexto async.

**Implementacao**:
- Eventos (`OrderCreated`, `StockLow`) sao dataclasses frozen
- Schemas de request sao imutaveis (Pydantic cuida disso por padrao)
- Schemas de response sao imutaveis
- Modelos SQLAlchemy sao mutaveis (necessidade do ORM), mas nunca expostos diretamente na API

---

## Principio 4: Error handling via Result types quando possivel

**Regra**: Para operacoes que podem falhar de forma esperada, preferir retorno de Result types (`tuple[valor, erro]` ou similar) ao inves de exceptions. Exceptions para erros inesperados.

**Motivacao**: Exceptions para controle de fluxo tornam o codigo dificil de raciocinar. Um `InsufficientStock` nao e uma "excecao" — e um resultado esperado que deve ser tratado explicitamente.

**Implementacao**:
- Service methods retornam `Result[T, Error]` para falhas esperadas
- Exceptions da hierarquia `AppException` para erros inesperados
- Routes fazem pattern matching no Result e retornam HTTP status apropriado
- Na pratica, usamos um tipo simples: `tuple[T | None, str | None]` — sem dependencia externa

---

## Principio 5: Queries analiticas podem usar SQL raw

**Regra**: Queries analiticas (dashboards, relatorios, metricas agregadas) podem usar SQL raw sem ORM. O ORM e obrigatorio para operacoes transacionais (CRUD).

**Motivacao**: O ORM adiciona overhead e complexidade em queries analiticas com multiplos JOINs, window functions e agregacoes. SQL raw e mais legivel e performante nesses casos.

**Implementacao**:
- `AnalyticsService` pode usar `session.execute(text(...))` com SQL raw
- Queries raw devem ser parametrizadas (nunca string concatenation — prevenir SQL injection)
- Queries CRUD usam SQLAlchemy ORM via repositories
- Queries raw devem ser documentadas com comentario explicando o que fazem

**Excecoes**: queries simples de analytics (contagem, soma) podem usar ORM se forem triviais.

---

## Principio 6: Tipagem estatica obrigatoria

**Regra**: Todo codigo Python deve ter type annotations. `mypy` em modo strict e parte do CI.

**Motivacao**: Type annotations documentam contratos entre modulos e pegam bugs em tempo de desenvolvimento. Com FastAPI + Pydantic, a tipagem e especialmente valiosa.

**Implementacao**:
- Todas as funcoes devem ter tipos de parametro e retorno anotados
- Usar `from __future__ import annotations` em todos os modulos
- `Any` e `type: ignore` devem ter justificativa em comentario
- Ver `padroes-formatacao.md` para convencoes de formatacao

---

*Estes principios sao revisados anualmente ou quando um incidente revela necessidade de ajuste.*
*Ver tambem: `stack-definida.md`, `padroes-testes.md`, `restricoes-integracao.md`*
