# Decisoes de arquitetura (ADR)

> Formato: Architecture Decision Record (ADR)
> Convencao: ADR-NNN com data e status

## Contexto

Este documento registra decisoes de arquitetura no formato ADR. Cada decisao inclui contexto, alternativas avaliadas e motivacao. Decisoes aqui registradas sao vinculantes — desvios requerem uma nova ADR que explicitamente substitua a anterior.

Ver tambem: `stack-definida.md` para tecnologias aprovadas, `principios-tecnicos.md` para principios de implementacao.

---

## ADR-001: Repository pattern para acesso a dados

**Data**: 2025-09-15
**Status**: Aceito
**Decisor**: Time de arquitetura

### Contexto

Routes acessavam o banco diretamente via SQLAlchemy, criando acoplamento forte entre a camada de apresentacao e a camada de persistencia. Dificultava testes unitarios e tornava mudancas no schema arriscadas.

### Decisao

Adotar o repository pattern com uma classe abstrata base (`AbstractRepository`) e implementacoes concretas por entidade (`CustomerRepository`, `ProductRepository`, `OrderRepository`).

### Alternativas avaliadas

1. **Active Record** (models com metodos de query): rejeitado por misturar responsabilidades
2. **DAO pattern**: similar ao repository, mas semanticamente diferente. Repository foi preferido por alinhar melhor com o domain model.
3. **Query objects**: considerado complementar, nao substituto. Pode ser adotado no futuro para queries complexas.

### Consequencias

- Routes injetam repositories, nunca criam sessions diretamente
- Testes de service podem usar repository mock (mas testes de integracao usam banco real — ver `padroes-testes.md`)
- Novas entidades devem seguir o mesmo padrao

---

## ADR-002: Event bus in-process

**Data**: 2025-10-01
**Status**: Aceito
**Decisor**: Time de arquitetura

### Contexto

O fluxo de criacao de pedido precisa disparar multiplas acoes: notificacao, atualizacao de analytics, reserva de estoque. Colocar tudo no service method criava um metodo de 200+ linhas com responsabilidades misturadas.

### Decisao

Implementar um event bus in-process (publish/subscribe) para desacoplar o fluxo principal das side effects. Eventos sao sincronos e in-process — nao ha filas externas.

### Alternativas avaliadas

1. **Celery + Redis**: overhead excessivo para o volume atual. Pode ser adotado no futuro se necessario.
2. **Background tasks do FastAPI**: adequado para fire-and-forget, mas nao para orquestracao de multiplos handlers.
3. **Event bus externo (RabbitMQ, Kafka)**: overengineering para o momento. Volume atual < 1000 eventos/dia.

### Consequencias

- Acoplamento reduzido: `OrderService` emite `OrderCreated`, nao sabe quem consome
- Handlers registrados em `events/handlers.py` — ponto unico de configuracao
- Trade-off: se um handler falhar, o evento se perde (sem dead letter queue). Aceitavel para o momento.
- Revisao planejada para Q3 2026 se volume crescer (ver `roadmap.md`)

---

## ADR-003: SQLite para desenvolvimento, PostgreSQL para producao

**Data**: 2025-08-20
**Status**: Aceito
**Decisor**: Time de arquitetura

### Contexto

Precisamos de um banco relacional que funcione sem setup para desenvolvimento local e testes, mas que seja robusto para producao.

### Decisao

- Desenvolvimento local: SQLite (arquivo)
- Testes: SQLite (in-memory)
- Producao: PostgreSQL 15+

### Consequencias

- SQLAlchemy como ORM garante portabilidade entre SQLite e PostgreSQL
- Testes rodam sem dependencias externas
- Queries especificas de PostgreSQL devem ser evitadas no ORM (ou ter fallback SQLite)
- Queries analiticas podem usar SQL raw — ver `principios-tecnicos.md`

---

## ADR-004: Criptografia com AWS KMS

**Data**: 2025-07-10
**Status**: Aceito
**Decisor**: Time de arquitetura + Compliance

### Contexto

Dados classificados como RESTRITO (CPF, dados de pagamento) precisam de criptografia em repouso. Ver `politica-dados.md`.

### Decisao

Usar AWS KMS para gerenciamento de chaves, com envelope encryption (chave de dados criptografada pela chave mestre do KMS).

### Consequencias

- Dependencia de AWS para gerenciamento de chaves
- Rotacao de chaves a cada 90 dias (automatizada)
- Fallback local para testes: chave fixa em configuracao de teste (nunca em producao)

---

## ADR-005: Middleware chain para cross-cutting concerns

**Data**: 2025-10-15
**Status**: Aceito
**Decisor**: Time de arquitetura

### Contexto

Autenticacao, logging, rate limiting e error handling estavam misturados nos routes. Codigo duplicado e inconsistente entre endpoints.

### Decisao

Implementar como middleware chain do FastAPI, na seguinte ordem:
1. Error handler (catch-all)
2. Logging (request/response com timing)
3. Rate limiter (in-memory, por IP)
4. Auth (API key no header)

### Consequencias

- Cross-cutting concerns centralizados e consistentes
- Ordem dos middlewares importa — error handler deve ser o mais externo
- Novos middlewares devem ser adicionados com cuidado a ordem

---

*Novas decisoes de arquitetura devem seguir o formato ADR.*
*Ver tambem: `stack-definida.md`, `principios-tecnicos.md`*
