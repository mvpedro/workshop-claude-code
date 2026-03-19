# Índice da Documentação

Documentação completa do **Workshop Demo — Sistema de Gestão**.

---

## Visão Geral

- [README — Arquitetura e Configuração](./README.md)
  - Diagrama de arquitetura geral
  - Stack tecnológica
  - Como rodar localmente
  - Variáveis de ambiente

---

## API REST

- [Clientes](./api/customers.md) — CRUD de clientes, paginação, filtros por segmento
- [Produtos](./api/products.md) — CRUD de produtos, filtro por categoria, low stock
- [Pedidos](./api/orders.md) — Criação, máquina de estados, transição de status
- [Analytics](./api/analytics.md) — Top produtos, receita por período, LTV de cliente

---

## Models SQLAlchemy

- [Models](./models/README.md)
  - `BaseModel` — campos comuns (id, created_at, updated_at)
  - `Customer` — clientes com segmento e status ativo
  - `Product` — produtos com estoque e SKU
  - `Order` — pedidos com máquina de estados
  - `OrderItem` — itens de pedido com preço snapshot
  - Diagrama ER completo

---

## Repositórios

- [Repositórios](./repositories/README.md)
  - `AbstractRepository[T]` — CRUD genérico (get_by_id, list, count, create, update, delete)
  - `CustomerRepository` — busca por email, filtro por segmento
  - `ProductRepository` — filtro por categoria, low stock
  - `OrderRepository` — eager loading de itens, filtros por cliente e status
  - Diagrama de herança

---

## Serviços

- [Serviços](./services/README.md)
  - `order_service` — criação de pedidos e transição de status
  - `inventory_service` — reserva e liberação de estoque
  - `pricing_service` — cálculo de preços com descontos por volume
  - `analytics_service` — consultas analíticas agregadas
  - `notification_service` — handlers de eventos para notificações

---

## Sistema de Eventos

- [Events](./events/README.md)
  - Event bus pub/sub in-process
  - `OrderCreated` — criação de pedido
  - `OrderStatusChanged` — mudança de status
  - `StockLow` — alerta de estoque baixo
  - Diagrama de fluxo de eventos sequencial

---

## Middleware

- [Middleware](./middleware/README.md)
  - `ErrorHandlerMiddleware` — converte exceções em respostas JSON
  - `LoggingMiddleware` — loga método, path, status e duração
  - `RateLimiterMiddleware` — limite por IP com janela deslizante
  - `AuthMiddleware` — validação de API Key via header `X-API-Key`
  - Ordem de execução na cadeia

---

## Exceptions

- [Exceptions](./exceptions/README.md)
  - `AppException` — base com `message` e `status_code`
  - Exceptions de negócio: `InsufficientStock`, `InvalidStatusTransition`, `DuplicateEmail`, `NotFound`
  - Exceptions de infraestrutura: `DatabaseError`, `ExternalServiceError`
  - Diagrama de hierarquia de classes

---

## Background Tasks

- [Tasks](./tasks/README.md)
  - `process_new_order` — processamento pós-criação de pedido
  - `process_status_change` — processamento pós-mudança de status
  - Fluxo esperado de integração com o event bus

---

## DBT

- [DBT](./dbt/README.md)
  - Diagrama de lineage completo
  - Macro `cents_to_reais`
  - Staging: `stg_customers`, `stg_products`, `stg_orders`
  - Intermediate: `int_customer_orders`, `int_product_performance`
  - Marts: `dim_customers`, `fct_orders`
- [schema.yml](../dbt/models/schema.yml) — testes de schema para todos os modelos DBT
