# Project: Workshop Demo — Sistema de Gestão

## Sobre o projeto
API REST em FastAPI para gestão de clientes, produtos e pedidos.
Arquitetura com repository pattern, event bus, middleware chain e hierarquia de exceptions.
Pydantic schemas separados dos models SQLAlchemy.
Projeto DBT para transformação de dados com camadas staging, intermediate e marts.

## Stack
- Python 3.11+, FastAPI, SQLAlchemy (async), Pydantic
- Repository pattern com base abstrata (AbstractRepository)
- Event bus in-process (publish/subscribe)
- Middleware: auth, logging, error handling, rate limiting
- DBT Core com adapter DuckDB
- Testes com pytest + httpx

## Convenções
- Docstrings em português
- Documentação em português
- Models DBT seguem convenção: stg_ (staging), int_ (intermediate), dim_/fct_ (marts)
- Testes de schema DBT em YAML
- snake_case para funções e variáveis, PascalCase para classes

## Regras para geração de documentação
- Gerar em markdown
- Incluir diagramas de dependência em mermaid
- Documentar todos os endpoints com método, path, parâmetros e response
- Documentar models DBT com descrição, colunas e testes
- Gerar changelog quando aplicável
- Sempre em português brasileiro
