# Documentação de Serviços

Os serviços contêm a lógica de negócio da aplicação. São chamados pelas rotas e colaboram com repositórios, o event bus e entre si.

---

## order_service (`src/api/services/order_service.py`)

Orquestra a criação e o ciclo de vida de pedidos.

### `create_order(session, data) -> Order`

Cria um novo pedido com todas as validações e efeitos colaterais.

**Parâmetros:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `session` | `AsyncSession` | Sessão de banco de dados |
| `data` | `OrderCreate` | Schema com `customer_id`, `items[]` e `notes` |

**Fluxo de execução:**
1. Para cada item, busca o `Product` — lança `NotFound` se não existir.
2. Reserva estoque de todos os produtos via `inventory_service.reserve_stock()`.
3. Calcula o total com descontos via `pricing_service.calculate_order_total()`.
4. Cria o registro `Order` e os registros `OrderItem` no banco.
5. Publica evento `OrderCreated` no bus.

**Exceções lançadas:**
- `NotFound` — produto não encontrado
- `InsufficientStock` — estoque insuficiente (propagada do `inventory_service`)

---

### `transition_status(session, order_id, new_status) -> Order`

Realiza a transição de status de um pedido.

**Parâmetros:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `session` | `AsyncSession` | Sessão de banco de dados |
| `order_id` | `str` | UUID do pedido |
| `new_status` | `str` | Status destino |

**Fluxo de execução:**
1. Busca o pedido com eager loading dos itens.
2. Valida a transição via `order.can_transition_to()`.
3. Atualiza o status.
4. Se `new_status == "cancelled"`, devolve estoque de todos os itens via `inventory_service.release_stock()`.
5. Publica evento `OrderStatusChanged` no bus.

**Exceções lançadas:**
- `NotFound` — pedido não encontrado
- `InvalidStatusTransition` — transição não permitida

---

## inventory_service (`src/api/services/inventory_service.py`)

Gerencia a reserva e liberação de estoque de produtos.

### `reserve_stock(session, product, quantity) -> None`

Reserva estoque para um item de pedido.

**Parâmetros:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `session` | `AsyncSession` | Sessão de banco de dados |
| `product` | `Product` | Instância do produto |
| `quantity` | `int` | Quantidade a reservar |

**Comportamento:**
- Lança `InsufficientStock` se `product.stock < quantity`.
- Decrementa `product.stock` e chama `session.flush()`.
- Se o estoque resultante for ≤ 5, publica evento `StockLow`.

---

### `release_stock(session, product, quantity) -> None`

Devolve estoque ao cancelar um pedido.

**Parâmetros:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `session` | `AsyncSession` | Sessão de banco de dados |
| `product` | `Product` | Instância do produto |
| `quantity` | `int` | Quantidade a devolver |

**Comportamento:** Incrementa `product.stock` e chama `session.flush()`. Não verifica limites.

---

## pricing_service (`src/api/services/pricing_service.py`)

Calcula preços com descontos por volume. Funções puras — sem acesso ao banco ou eventos.

### `calculate_item_price(product, quantity) -> float`

Calcula o preço de uma linha de pedido com desconto por volume.

| Quantidade | Desconto aplicado |
|------------|-------------------|
| ≥ 100 | 15% |
| ≥ 50 | 10% |
| ≥ 10 | 5% |
| < 10 | 0% |

**Retorno:** `product.price * quantity * (1 - desconto)`.

---

### `calculate_order_total(items) -> float`

Soma os preços de todos os itens do pedido.

**Parâmetros:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `items` | `list[tuple[Product, int]]` | Lista de pares (produto, quantidade) |

**Retorno:** Soma de `calculate_item_price(product, qty)` para cada par.

---

## analytics_service (`src/api/services/analytics_service.py`)

Consultas analíticas sobre pedidos e clientes.

### `get_top_products(session, limit) -> list[dict]`

Retorna os produtos mais vendidos.

**Parâmetros:** `session`, `limit: int = 10`

**Retorno:** Lista de `{"product_id", "total_sold", "total_revenue"}` ordenada por `total_sold` DESC.

---

### `get_revenue_by_period(session, group_by) -> list[dict]`

Retorna receita agrupada por mês.

**Parâmetros:** `session`, `group_by: str = "month"` (apenas `"month"` implementado)

**Retorno:** Lista de `{"period", "revenue", "order_count"}` para pedidos não cancelados.

---

### `get_customer_lifetime_value(session, customer_id) -> dict`

Calcula métricas de valor vitalício de um cliente.

**Retorno:** `{"customer_id", "order_count", "total_spent", "first_order", "last_order"}` excluindo pedidos cancelados.

---

## notification_service (`src/api/services/notification_service.py`)

Simula o envio de notificações para clientes. Registrado como subscriber do event bus no startup da aplicação.

### `handle_order_created(event: OrderCreated) -> None`

Handler para o evento `OrderCreated`. Loga simulação de envio de confirmação de pedido.

### `handle_status_changed(event: OrderStatusChanged) -> None`

Handler para o evento `OrderStatusChanged`. Loga simulação de envio de notificação de atualização.

> **Nota:** Ambos os handlers são simulações via `logger.info`. Uma implementação real integraria com provedores de e-mail/SMS/push notification.
