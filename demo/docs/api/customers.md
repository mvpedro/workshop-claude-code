# API — Clientes

Rotas para gestão de clientes. Prefixo: `/api/v1/customers`.

---

## Endpoints

### `GET /api/v1/customers`

Lista clientes com paginação e filtros opcionais.

**Query Parameters**

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `page` | `int` | Não | `1` | Página atual |
| `page_size` | `int` | Não | `20` | Itens por página |
| `segment` | `string` | Não | — | Filtra por segmento (`bronze`, `silver`, `gold`) |
| `is_active` | `bool` | Não | — | Filtra por status ativo/inativo |

**Response `200 OK`**

```json
{
  "items": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "name": "Maria Silva",
      "email": "maria@exemplo.com",
      "phone": "11999990000",
      "segment": "gold",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "pages": 5
}
```

---

### `GET /api/v1/customers/{customer_id}`

Retorna um cliente pelo ID.

**Path Parameters**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `customer_id` | `string` | UUID do cliente |

**Response `200 OK`**

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": "Maria Silva",
  "email": "maria@exemplo.com",
  "phone": "11999990000",
  "segment": "gold",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Códigos de Erro**

| Código | Motivo |
|--------|--------|
| `404` | Cliente não encontrado |

---

### `POST /api/v1/customers`

Cria um novo cliente.

**Request Body**

```json
{
  "name": "Maria Silva",
  "email": "maria@exemplo.com",
  "phone": "11999990000",
  "segment": "bronze"
}
```

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `name` | `string` | Sim | — | Nome completo |
| `email` | `string` | Sim | — | E-mail único |
| `phone` | `string` | Não | `null` | Telefone |
| `segment` | `string` | Não | `"bronze"` | Segmento do cliente |

**Response `201 Created`**

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": "Maria Silva",
  "email": "maria@exemplo.com",
  "phone": "11999990000",
  "segment": "bronze",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Códigos de Erro**

| Código | Motivo |
|--------|--------|
| `409` | E-mail já cadastrado |

---

### `PUT /api/v1/customers/{customer_id}`

Atualiza os dados de um cliente. Todos os campos são opcionais (atualização parcial).

**Path Parameters**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `customer_id` | `string` | UUID do cliente |

**Request Body**

```json
{
  "name": "Maria Silva Santos",
  "email": "maria.santos@exemplo.com",
  "phone": "11988880000",
  "segment": "silver",
  "is_active": true
}
```

**Response `200 OK`** — Retorna o cliente atualizado (mesmo schema do GET).

**Códigos de Erro**

| Código | Motivo |
|--------|--------|
| `404` | Cliente não encontrado |

---

### `DELETE /api/v1/customers/{customer_id}`

Remove um cliente.

**Path Parameters**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `customer_id` | `string` | UUID do cliente |

**Response `204 No Content`**

**Códigos de Erro**

| Código | Motivo |
|--------|--------|
| `404` | Cliente não encontrado |

---

## Modelo de Dados

Ver [docs/models/README.md](../models/README.md) para detalhes sobre o model `Customer`.
