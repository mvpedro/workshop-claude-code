# Padroes de testes

> Ultima atualizacao: 2025-11-25
> Responsavel: Time de arquitetura
> Status: Vigente

## Contexto

Este documento define os padroes de teste do projeto. Os principios aqui sao complementares aos `principios-tecnicos.md` e refletem aprendizados acumulados desde o inicio do projeto.

Ver tambem: `principios-tecnicos.md` para principios de implementacao, `stack-definida.md` para frameworks de teste aprovados.

## Regra critica: nunca mockar o banco de dados

**REGRA**: NUNCA mockar o banco de dados. Testes de integracao devem usar banco real (SQLite in-memory para testes, conforme `decisoes-arquitetura.md` ADR-003).

**Motivacao**: Mocks de banco de dados criam uma falsa sensacao de seguranca. O teste passa, mas o codigo quebra em producao porque:
- O mock nao reproduz o comportamento real de constraints (FK, unique, not null)
- O mock nao testa queries SQL reais (typos, joins incorretos)
- O mock nao detecta problemas de migracao

**Implementacao**:
- Usar SQLite in-memory para testes (`conftest.py` cria engine e session de teste)
- Cada teste roda em transacao que faz rollback ao final (isolamento)
- Fixtures criam dados reais no banco de teste
- Se o teste precisa de banco e nao pode usar SQLite, e um sinal de que o codigo tem dependencia excessiva de features especificas do PostgreSQL

**Excecoes aceitas**: mocks sao aceitos para servicos externos (APIs, gateways) — estes sim devem ser mockados nos testes (ver secao abaixo).

## Piramide de testes

```
        /  E2E  \          <- poucos, lentos, alto valor
       /  Integ  \         <- medianos, banco real
      /  Unitarios \       <- muitos, rapidos, funcoes puras
```

### Testes unitarios

- Testam funcoes puras: calculo de preco, validacao de regras, state machine
- Nao tocam banco, nao tocam API
- Devem ser rapidos (< 100ms cada)
- Cobertura alvo: 90% para funcoes puras em services

### Testes de integracao

- Testam fluxos completos: rota -> service -> repository -> banco
- Usam `httpx.AsyncClient` com `TestClient` do FastAPI
- Banco SQLite in-memory (nao mock)
- Cobertura alvo: 80% para services, 70% para routes

### Testes end-to-end

- Poucos, focados em fluxos criticos: criar pedido completo, fluxo de pagamento
- Usam banco real e podem ser lentos
- Rodam em CI mas nao bloqueiam merge (advisory)

## Metas de cobertura

| Camada | Meta | Obrigatorio em CI |
|---|---|---|
| Services | 80% | Sim — build falha abaixo |
| Routes | 70% | Sim — build falha abaixo |
| Repositories | 60% | Nao — advisory |
| Models | N/A | N/A — cobertos via integracao |

## Mocks: quando usar

Mocks sao aceitos APENAS para:
- **Servicos externos** (Pagar.me, AWS SES, Twilio) — nunca chamar APIs reais em testes
- **Clock/time** — para testar logica temporal (expiracoes, retencao de dados)
- **Geradores aleatorios** — para reprodutibilidade

Mocks NAO sao aceitos para:
- **Banco de dados** — usar banco real (SQLite in-memory)
- **Repositories** — testar com banco real, nao com mock de repository
- **Event bus** — testar com bus real in-process

## Convencoes de nomenclatura

```python
# Arquivo: test_<modulo>.py
# Funcao: test_<acao>_<cenario>_<resultado_esperado>

def test_create_order_with_insufficient_stock_returns_error():
    ...

def test_calculate_discount_for_gold_customer_applies_10_percent():
    ...

def test_cancel_order_already_shipped_raises_invalid_transition():
    ...
```

## Fixtures

- Definidas em `conftest.py` (compartilhadas) ou no proprio arquivo de teste (especificas)
- Factories para criar entidades: `create_customer()`, `create_product()`, `create_order()`
- Dados realistas (nomes brasileiros, CPFs validos, precos em BRL)
- Cleanup automatico via rollback de transacao

## CI/CD

- Testes rodam em todo PR (`pytest --cov --cov-report=term-missing`)
- Build falha se cobertura de services < 80% ou routes < 70%
- Testes E2E rodam mas nao bloqueiam merge
- Tempo maximo de execucao: 5 minutos (alerta se exceder)

---

*Padroes de teste revisados semestralmente.*
*Ver tambem: `principios-tecnicos.md`, `stack-definida.md`*
