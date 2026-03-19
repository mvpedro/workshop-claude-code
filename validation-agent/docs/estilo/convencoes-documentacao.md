# Convencoes de documentacao

> Ultima atualizacao: 2025-11-10
> Responsavel: Time de arquitetura
> Status: Vigente

## Contexto

Este documento define as convencoes de documentacao de codigo e projeto. O idioma oficial de toda documentacao e portugues brasileiro, exceto nomes de variaveis, funcoes e classes (que seguem convencao em ingles — ver `guia-estilo-codigo.md`).

## Docstrings

### Idioma

Docstrings devem ser escritas em portugues. Nomes tecnicos em ingles sao aceitos quando nao ha traducao natural (e.g., "endpoint", "middleware", "repository").

### Formato: Google style

Usamos o formato Google style para docstrings (compativel com ferramentas de geracao automatica como Sphinx e MkDocs).

```python
def calculate_discount(
    order_total: Decimal,
    customer_segment: str,
    coupon_code: str | None = None,
) -> tuple[Decimal, str]:
    """Calcula o desconto aplicavel ao pedido.

    Aplica regras de desconto por segmento de cliente e cupom,
    respeitando o limite maximo de 40% (ver regras-negocio.md).

    Args:
        order_total: Valor total do pedido em centavos.
        customer_segment: Segmento do cliente (bronze, silver, gold).
        coupon_code: Codigo do cupom, se aplicavel.

    Returns:
        Tupla com (valor_desconto, descricao). Valor em centavos.

    Raises:
        ValueError: Se order_total for negativo.

    Exemplo:
        >>> calculate_discount(Decimal("10000"), "gold")
        (Decimal("1000"), "Desconto fidelidade Gold 10%")
    """
```

### Regras

- Toda funcao publica deve ter docstring
- Funcoes privadas (`_prefixo`): docstring opcional, mas recomendada se a logica nao for obvia
- Primeira linha: resumo em uma frase (imperativo: "Calcula...", "Retorna...", "Valida...")
- Secoes `Args`, `Returns`, `Raises`: obrigatorias se aplicavel
- Secao `Exemplo`: recomendada para funcoes de calculo e validacao
- Referenciar documentos relevantes quando a logica implementa uma regra de negocio

### Classes

```python
class OrderService:
    """Orquestra operacoes de pedidos.

    Responsavel por coordenar a criacao, atualizacao e cancelamento
    de pedidos, incluindo validacao de estoque, calculo de preco e
    emissao de eventos.

    Dependencias:
        - OrderRepository: persistencia de pedidos
        - EventBus: emissao de eventos (ver decisoes-arquitetura.md ADR-002)
        - PricingService: calculo de descontos
    """
```

### Modulos

Todo modulo (arquivo `.py`) deve ter docstring no topo explicando seu proposito:

```python
"""Servico de precificacao.

Implementa as regras de desconto definidas em regras-negocio.md:
cupons, desconto por volume e desconto por fidelidade.
"""
```

## Documentacao de projeto

### Markdown

- Todo documento de projeto em markdown
- Titulos com hierarquia clara (# -> ## -> ###)
- Tabelas para dados estruturados
- Blocos de codigo com linguagem especificada (```python, ```sql)
- Links relativos entre documentos (nunca absolutos)

### Changelog

- Formato: Keep a Changelog (https://keepachangelog.com/)
- Categorias: Adicionado, Alterado, Corrigido, Removido
- Entrada para toda mudanca que afeta comportamento visivel
- Em portugues

### Commits

- Formato: Conventional Commits (feat, fix, refactor, docs, test, chore)
- Mensagem em ingles (convencao do time para commits)
- Corpo opcional em portugues se necessario explicar contexto

---

*Ver tambem: `guia-estilo-codigo.md`, `padroes-formatacao.md`*
