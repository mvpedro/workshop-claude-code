# Padroes de formatacao

> Ultima atualizacao: 2025-11-10
> Responsavel: Time de arquitetura
> Status: Vigente — enforced via CI

## Contexto

Este documento define os padroes de formatacao de codigo do projeto. Estas regras sao enforced automaticamente no CI — PRs que violem sao bloqueados.

Ver tambem: `guia-estilo-codigo.md` para nomenclatura e organizacao, `convencoes-documentacao.md` para documentacao.

## Comprimento de linha

**Maximo: 100 caracteres por linha.**

Motivacao: 80 e muito restritivo para codigo com type annotations verbosas. 120 nao cabe confortavelmente em split view. 100 e o meio termo.

Configuracao:
```toml
# pyproject.toml
[tool.black]
line-length = 100

[tool.ruff]
line-length = 100
```

## Formatador: Black

Usamos Black como formatador automatico. Configuracao minima — Black e opinado por design.

```toml
# pyproject.toml
[tool.black]
line-length = 100
target-version = ["py311"]
```

Regra: nunca usar `# fmt: off` / `# fmt: on` exceto em matrizes de dados alinhadas manualmente (raro).

## Organizacao de imports: isort

```toml
# pyproject.toml
[tool.isort]
profile = "black"
line_length = 100
known_first_party = ["src"]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
```

Ordem:
1. `from __future__ import annotations`
2. Standard library (`import os`, `from datetime import datetime`)
3. Terceiros (`from fastapi import ...`, `from sqlalchemy import ...`)
4. Codigo local (`from src.api.models import ...`)

Cada secao separada por uma linha em branco.

## Linter: Ruff

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "ANN",  # flake8-annotations
    "B",    # flake8-bugbear
    "SIM",  # flake8-simplify
]
ignore = [
    "ANN101",  # missing type annotation for self
    "ANN102",  # missing type annotation for cls
]
```

## Type annotations: obrigatorias

**Regra**: todo codigo deve ter type annotations completas. `mypy` em modo strict.

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
```

Regras:
- Todas as funcoes devem ter tipos de parametro e retorno
- `Any` requer justificativa em comentario
- `type: ignore` requer justificativa em comentario
- Usar `from __future__ import annotations` em todos os modulos (avaliacao lazy de tipos)
- Generics com sintaxe moderna: `list[int]` ao inves de `List[int]`, `str | None` ao inves de `Optional[str]`

## Indentacao

- Python: 4 espacos (padrao PEP 8)
- YAML: 2 espacos
- JSON: 2 espacos
- Markdown: 2 espacos para listas aninhadas
- Nunca tabs

## Strings

- Preferir double quotes (`"texto"`) — convencao do Black
- f-strings para interpolacao: `f"Pedido {order_id} criado"`
- Strings longas: usar parenteses para quebra de linha, nunca `\`

```python
# Correto
message = (
    f"Pedido {order_id} criado com sucesso. "
    f"Total: R$ {total:.2f}. Status: {status}."
)

# Incorreto
message = f"Pedido {order_id} criado com sucesso. " \
          f"Total: R$ {total:.2f}. Status: {status}."
```

## Trailing commas

Sempre usar trailing comma em colecoes multilinhas:

```python
# Correto
config = {
    "host": "localhost",
    "port": 5432,
    "database": "app",
}

# Incorreto
config = {
    "host": "localhost",
    "port": 5432,
    "database": "app"
}
```

## CI enforcement

```yaml
# Em .github/workflows/lint.yml
- run: black --check --line-length 100 src/ tests/
- run: ruff check src/ tests/
- run: mypy src/ --strict
```

PRs que falhem em qualquer check de formatacao sao bloqueados automaticamente.

---

*Ver tambem: `guia-estilo-codigo.md`, `convencoes-documentacao.md`*
