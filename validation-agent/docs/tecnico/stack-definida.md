# Stack tecnologica definida

> Ultima atualizacao: 2025-11-10
> Responsavel: Time de arquitetura
> Status: Vigente — desvios requerem ADR formal

## Contexto

Este documento define as tecnologias aprovadas para uso no projeto, bem como as explicitamente nao permitidas. A escolha de stack foi feita em setembro de 2025 com base na expertise do time, requisitos do produto e maturidade das ferramentas.

Ver tambem: `decisoes-arquitetura.md` para o racional de cada decisao, `principios-tecnicos.md` para principios de implementacao.

## Stack aprovada

### Backend

| Tecnologia | Versao | Uso |
|---|---|---|
| Python | 3.11+ | Linguagem principal do backend |
| FastAPI | 0.100+ | Framework web (escolhido por async nativo e tipagem) |
| SQLAlchemy | 2.x | ORM e query builder (2.x obrigatorio pelo novo style) |
| Pydantic | 2.x | Validacao de dados e schemas de API |
| Alembic | 1.12+ | Migrations de banco de dados |
| httpx | 0.25+ | Cliente HTTP assincrono (ver `principios-tecnicos.md`) |
| pytest | 7.x+ | Framework de testes |
| pytest-asyncio | 0.21+ | Suporte a testes async |

### Frontend

| Tecnologia | Versao | Uso |
|---|---|---|
| React | 18.x | Framework de UI (unico aprovado — ver nota abaixo) |
| TypeScript | 5.x | Linguagem (obrigatorio, nao usar JS puro) |
| Vite | 5.x | Build tool |

### Banco de dados

| Tecnologia | Ambiente | Uso |
|---|---|---|
| PostgreSQL | Producao | Banco principal |
| SQLite | Desenvolvimento/Testes | Banco local (ver `decisoes-arquitetura.md` ADR-003) |

### Infraestrutura

| Tecnologia | Uso |
|---|---|
| Docker | Containerizacao |
| GitHub Actions | CI/CD |
| AWS (SES, KMS, S3) | Servicos de nuvem aprovados |

## Tecnologias NAO permitidas

As seguintes tecnologias foram explicitamente avaliadas e rejeitadas. Usar qualquer uma delas requer uma ADR formal que justifique a mudanca.

### Frameworks web

| Tecnologia | Motivo da rejeicao | Data |
|---|---|---|
| Flask | Sem suporte nativo a async, tipagem fraca, menos estruturado que FastAPI | 2025-09 |
| Django | Overhead excessivo para o tipo de aplicacao (API-first, nao precisa de admin/ORM proprio) | 2025-09 |
| Express.js | Decisao de manter backend 100% Python | 2025-09 |

### Frameworks frontend

| Tecnologia | Motivo da rejeicao | Data |
|---|---|---|
| Vue.js | Time sem expertise, React ja consolidado, custo de migracao injustificavel | 2025-09 |
| Angular | Complexidade excessiva para o tamanho do time e do produto | 2025-09 |
| Svelte | Ecossistema ainda imaturo para as necessidades do projeto | 2025-09 |

### Bancos de dados

| Tecnologia | Motivo da rejeicao | Data |
|---|---|---|
| MongoDB | Modelo relacional e mais adequado para o dominio (pedidos, clientes, produtos com relacoes claras) | 2025-08 |
| Redis (como banco primario) | Aceito apenas como cache, nunca como store primario | 2025-08 |
| DynamoDB | Lock-in AWS excessivo para store primario | 2025-08 |

### Bibliotecas HTTP

| Tecnologia | Motivo da rejeicao | Data |
|---|---|---|
| requests | Sincrono, bloqueia a thread. Usar httpx com AsyncClient (ver `principios-tecnicos.md`) | 2025-10 |
| aiohttp | httpx preferido por API mais limpa e compatibilidade com sync/async | 2025-10 |
| urllib3 | Baixo nivel demais, usar httpx | 2025-10 |

## Processo de mudanca

Para propor uma mudanca na stack:
1. Criar ADR em `decisoes-arquitetura.md` com contexto, alternativas e justificativa
2. Revisao pelo time de arquitetura (minimo 2 aprovacoes)
3. Atualizar este documento apos aprovacao
4. Plano de migracao documentado se afetar codigo existente

---

*Este documento e a referencia canonica de tecnologias do projeto.*
*Ver tambem: `decisoes-arquitetura.md`, `principios-tecnicos.md`*
