# API — Produtos

Rotas para gestão de produtos. Prefixo: `/api/v1/products`.

---

## Endpoints

### `GET /api/v1/products`

Lista produtos com paginação e filtro opcional por categoria.

**Query Parameters**

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|-----------|
| `page` | `int` | Não | `1` | Página atual |
| `page_size` | `int` | Não | `20` | Itens por página |
| `category` | `string` | Não | — | Filtra por categoria |

**Response `200 OK`**

```json
{
  "items": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "name": "Notebook Pro",
      "description": "Notebook de alta performance",
      "price": 450000,
      "stock": 15,
      "category": "eletronicos",
      "sku": "NBK-PRO-001",
      "created_at": "2024-01-10T08:00:00",
      "updated_at": "2024-01-10T08:00:00"
    }
  ],
  "total": 50,
  "page": 1,
  "page_size": 20,
  "pages": 3
}
```

> **Nota:** O campo `price` é armazenado em centavos (inteiro).

---

### `GET /api/v1/products/low-stock`

Lista produtos com estoque baixo (≤ 5 unidades).

**Response `200 OK`** — Array de `ProductResponse` com os mesmos campos do endpoint de listagem.

---

### `GET /api/v1/products/{product_id}`

Retorna um produto pelo ID.

**Path Parameters**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `product_id` | `string` | UUID do produto |

**Response `200 OK`**

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": "Notebook Pro",
  "description": "Notebook de alta performance",
  "price": 450000,
  "stock": 15,
  "category": "eletronicos",
  "sku": "NBK-PRO-001",
  "created_at": "2024-01-10T08:00:00",
  "updated_at": "2024-01-10T08:00:00"
}
```

**Códigos de Erro**

| Código | Motivo |
|--------|--------|
| `404` | Produto não encontrado |

---

### `POST /api/v1/products`

Cria um novo produto.

**Request Body**

```json
{
  "name": "Notebook Pro",
  "description": "Notebook de alta performance",
  "price": 450000,
  "stock": 10,
  "category": "eletronicos",
  "sku": "NBK-PRO-001"
}
```

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `name` | `string` | Sim | — | Nome do produto |
| `description` | `string` | Não | `null` | Descrição detalhada |
| `price` | `float` | Sim | — | Preço em centavos |
| `stock` | `int` | Não | `0` | Quantidade em estoque |
| `category` | `string` | Sim | — | Categoria |
| `sku` | `string` | Sim | — | Código SKU único |

**Response `201 Created`** — Retorna o produto criado.

---

### `PUT /api/v1/products/{product_id}`

Atualiza os dados de um produto. Todos os campos são opcionais.

**Path Parameters**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `product_id` | `string` | UUID do produto |

**Request Body**

```json
{
  "name": "Notebook Pro X",
  "description": "Versão atualizada",
  "price": 480000,
  "stock": 20,
  "category": "eletronicos"
}
```

> **Nota:** O campo `sku` não pode ser alterado via PUT.

**Response `200 OK`** — Retorna o produto atualizado.

**Códigos de Erro**

| Código | Motivo |
|--------|--------|
| `404` | Produto não encontrado |

---

### `DELETE /api/v1/products/{product_id}`

Remove um produto.

**Path Parameters**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `product_id` | `string` | UUID do produto |

**Response `204 No Content`**

**Códigos de Erro**

| Código | Motivo |
|--------|--------|
| `404` | Produto não encontrado |

---

## Descontos por Volume

O `pricing_service` aplica descontos automáticos conforme a quantidade no momento da criação do pedido:

| Quantidade | Desconto |
|------------|----------|
| ≥ 100 | 15% |
| ≥ 50 | 10% |
| ≥ 10 | 5% |
| < 10 | Sem desconto |

---

## Modelo de Dados

Ver [docs/models/README.md](../models/README.md) para detalhes sobre o model `Product`.
