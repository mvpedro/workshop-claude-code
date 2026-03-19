# Guia de estilo de codigo

> Ultima atualizacao: 2025-11-10
> Responsavel: Time de arquitetura
> Status: Vigente

## Contexto

Este documento define convencoes de nomenclatura e organizacao de arquivos do projeto. Complementa `padroes-formatacao.md` (regras de formatacao) e `convencoes-documentacao.md` (regras de documentacao).

## Nomenclatura

### Python

| Elemento | Convencao | Exemplo |
|---|---|---|
| Modulos | snake_case | `payment_service.py` |
| Classes | PascalCase | `PaymentService`, `OrderRepository` |
| Funcoes/metodos | snake_case | `calculate_discount()`, `get_by_id()` |
| Constantes | UPPER_SNAKE_CASE | `MAX_RETRY_ATTEMPTS`, `DEFAULT_TIMEOUT` |
| Variaveis | snake_case | `order_total`, `customer_segment` |
| Parametros | snake_case | `customer_id`, `include_inactive` |
| Tipos genericos | T, U ou nome descritivo | `T`, `EntityT`, `ResponseT` |

### Nomes de arquivos

| Tipo | Padrao | Exemplo |
|---|---|---|
| Service | `<dominio>_service.py` | `payment_service.py`, `pricing_service.py` |
| Repository | `<dominio>_repository.py` | `customer_repository.py` |
| Model | `<dominio>.py` | `customer.py`, `order.py` |
| Schema | `<dominio>.py` (em pasta schemas/) | `schemas/customer.py` |
| Route | `<dominio>.py` (em pasta routes/) | `routes/customers.py` (plural) |
| Teste | `test_<modulo>.py` | `test_customers.py`, `test_pricing_service.py` |
| Migration | `NNN_<descricao>.py` | `001_initial_schema.py` |

### Nomes de variaveis semanticos

Regras:
- Nomes devem revelar intencao: `customer_count` ao inves de `n`, `is_active` ao inves de `flag`
- Booleans: prefixar com `is_`, `has_`, `can_`, `should_`
- Listas: plural (`orders`, `customers`)
- Dicionarios: `<chave>_to_<valor>` ou `<chave>_by_<criterio>` (`status_to_label`, `orders_by_customer`)
- Evitar abreviacoes: `transaction` ao inves de `txn`, `customer` ao inves de `cust`
- Excecao: abreviacoes amplamente conhecidas sao aceitas (`id`, `url`, `api`, `db`, `cpf`)

## Organizacao de arquivos

### Estrutura de modulo Python

```python
"""Docstring do modulo (ver convencoes-documentacao.md)."""

from __future__ import annotations

# 1. Imports da standard library
import logging
from datetime import datetime
from typing import Any

# 2. Imports de terceiros
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# 3. Imports locais
from src.api.models.customer import Customer
from src.api.repositories.customer_repository import CustomerRepository
from src.api.schemas.customer import CustomerCreate, CustomerResponse
```

Regra: imports sempre organizados em 3 blocos (stdlib, terceiros, locais), separados por linha em branco. Ver `padroes-formatacao.md` para configuracao do isort.

### Estrutura de service

```python
class OrderService:
    """Orquestra operacoes de pedidos."""

    def __init__(self, repository: OrderRepository, event_bus: EventBus) -> None:
        self._repository = repository
        self._event_bus = event_bus

    async def create_order(self, data: OrderCreate) -> tuple[Order | None, str | None]:
        """Cria pedido: valida -> persiste -> emite evento."""
        # 1. Validacao (pura)
        # 2. Persistencia (side effect)
        # 3. Eventos (side effect)
```

Regra: services recebem dependencias no construtor (injecao de dependencia). Nunca instanciar dependencias internamente.

### Estrutura de route

```python
router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=CustomerResponse, status_code=201)
async def create_customer(
    data: CustomerCreate,
    session: AsyncSession = Depends(get_session),
) -> CustomerResponse:
    """Cria um novo cliente."""
    ...
```

Regra: routes sao finas — delegam para services. Nenhuma logica de negocio em routes.

---

*Ver tambem: `padroes-formatacao.md`, `convencoes-documentacao.md`*
