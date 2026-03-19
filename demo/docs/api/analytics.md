# API — Analytics

Rotas para consultas analíticas. Prefixo: `/api/v1/analytics`.

> Todos os endpoints são somente leitura e executam queries de agregação diretamente no banco operacional.

---

## Endpoints

### `GET /api/v1/analytics/top-products`

Retorna os produtos mais vendidos, ordenados por quantidade total vendida.

**Query Parameters**

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `limit` | `int` | Não | `10` | Quantidade máxima de resultados |

**Response `200 OK`**

```json
[
  {
    "product_id": "prod001",
    "total_sold": 250,
    "total_revenue": 5625000.0
  },
  {
    "product_id": "prod002",
    "total_sold": 180,
    "total_revenue": 2700000.0
  }
]
```

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `product_id` | `string` | UUID do produto |
| `total_sold` | `int` | Quantidade total de unidades vendidas |
| `total_revenue` | `float` | Receita total gerada (em centavos) |

> **Nota:** A query agrupa por `product_id` nos itens de todos os pedidos, independentemente do status do pedido.

---

### `GET /api/v1/analytics/revenue`

Retorna a receita agrupada por período (mês), excluindo pedidos cancelados.

**Query Parameters**

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `group_by` | `string` | Não | `"month"` | Granularidade do agrupamento (⚠️ apenas `"month"` implementado) |

**Response `200 OK`**

```json
[
  {
    "period": "2024-01",
    "revenue": 12500000.0,
    "order_count": 45
  },
  {
    "period": "2024-02",
    "revenue": 18300000.0,
    "order_count": 62
  }
]
```

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `period` | `string` | Período no formato `YYYY-MM` |
| `revenue` | `float` | Receita total do período (em centavos) |
| `order_count` | `int` | Número de pedidos no período |

> **Nota:** Pedidos com status `cancelled` são excluídos do cálculo. O parâmetro `group_by` é recebido mas a implementação atual usa sempre agrupamento mensal via `strftime("%Y-%m", ...)`.

---

### `GET /api/v1/analytics/customer-ltv/{customer_id}`

Retorna o valor vitalício (Lifetime Value) de um cliente específico.

**Path Parameters**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `customer_id` | `string` | UUID do cliente |

**Response `200 OK`**

```json
{
  "customer_id": "cust456",
  "order_count": 12,
  "total_spent": 3400000.0,
  "first_order": "2023-06-15 09:30:00",
  "last_order": "2024-02-28 16:45:00"
}
```

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `customer_id` | `string` | UUID do cliente |
| `order_count` | `int` | Total de pedidos não cancelados |
| `total_spent` | `float` | Total gasto (em centavos) |
| `first_order` | `string\|null` | Data/hora do primeiro pedido |
| `last_order` | `string\|null` | Data/hora do último pedido |

> **Nota:** Pedidos cancelados são excluídos do cálculo. Se o cliente não tiver pedidos, retorna `order_count: 0`, `total_spent: 0.0` e datas `null`.
