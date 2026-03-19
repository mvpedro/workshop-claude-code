# Cenario 3 — Achados esperados: SQL raw analytics com PII de clientes

Este documento lista os conflitos que o agente de validacao DEVE identificar ao
analisar o codigo/proposta do cenario 3.

## Conflitos esperados

### 1. PII (nome, email) em endpoint de analytics

- **Documento**: `docs/compliance/requisitos-lgpd.md` — Secao 2 (Minimizacao de dados)
- **Trecho**: "Dados pessoais (CPF, nome, email) NAO devem ser armazenados em tabelas analiticas ou de reporting."
- **Problema**: O endpoint retorna nome e email de clientes em um relatorio analitico. Mesmo que nao armazene em tabela, expor PII em endpoint de analytics viola o principio de minimizacao.
- **Alternativa**: Usar IDs anonimizados ou hashes para identificar clientes no relatorio. Se o time comercial precisa do nome, o acesso deve ser via endpoint transacional com controle de acesso, nao via analytics.
- **Severidade**: ❌ Conflito

### 2. CPF em endpoint de analytics

- **Documento**: `docs/compliance/politica-dados.md` — Regra de armazenamento
- **Trecho**: "CPF e dado classificado como RESTRITO e so pode ser armazenado em tabelas transacionais com criptografia."
- **Problema**: CPF e dado RESTRITO. Retorna-lo em um endpoint de analytics viola a politica de classificacao de dados. Dados restritos nao devem ser expostos em contexto analitico.
- **Contexto adicional**: A tabela de politica de dados mostra que dados RESTRITOS tem ❌ em tabelas analiticas, logs e exports.
- **Severidade**: ❌ Conflito

## Nuanca critica: SQL raw E permitido

### 3. Uso de SQL raw para queries analiticas — COMPATIVEL

- **Documento**: `docs/tecnico/principios-tecnicos.md` — Principio 5
- **Trecho**: "Queries analiticas (dashboards, relatorios, metricas agregadas) podem usar SQL raw sem ORM."
- **Avaliacao**: O uso de SQL raw para a query de analytics esta CORRETO e alinhado com os principios tecnicos. O documento explicitamente permite SQL raw para queries analiticas com JOINs e window functions.
- **Condicao**: A query deve ser parametrizada (nunca string concatenation) para prevenir SQL injection.
- **Severidade**: ✅ Compativel

**IMPORTANTE**: Este e o ponto de nuanca principal do cenario 3. O agente deve identificar que SQL raw e permitido pela documentacao tecnica, ao mesmo tempo que o CONTEUDO da query (PII) e o problema. Sao duas dimensoes diferentes: a tecnica de acesso (SQL raw) esta correta, mas os dados retornados (PII em analytics) estao incorretos.

## Pontos de atencao adicionais

### 4. Dashboard de analytics previsto para Q2 2026

- **Documento**: `docs/produto/roadmap.md` — Q2 2026
- **Trecho**: Dashboard de metricas de vendas e a principal entrega de Q2 2026
- **Avaliacao**: A feature esta alinhada com o roadmap (analytics e prioridade Q2). Nao e um conflito, mas o agente pode notar que esta alinhado com o planejamento.
- **Severidade**: ✅ Compativel

### 5. Metricas devem ser agregadas, nunca PII

- **Documento**: `docs/produto/decisoes-produto.md` — DP-003
- **Trecho**: "Mostrar metricas agregadas (nunca dados pessoais)"
- **Problema**: A decisao de produto sobre o dashboard de analytics especifica que deve mostrar metricas AGREGADAS, nunca dados pessoais. Isso reforco a violacao de LGPD.
- **Severidade**: ⚠️ Atencao (reforco do conflito #1)

## Nuancias que o agente deve captar

- O cenario e desenhado para testar se o agente consegue distinguir entre "como" (SQL raw — OK) e "o que" (PII — nao OK)
- Um agente ruim diria "SQL raw e um problema" — isso esta ERRADO, a documentacao permite
- Um agente bom dira "SQL raw esta correto para analytics, MAS os dados retornados violam LGPD"
- Os conflitos de PII vem de DOIS documentos (requisitos-lgpd.md e politica-dados.md) — citar ambos
- O roadmap esta alinhado — o agente deve reconhecer isso como ponto positivo
