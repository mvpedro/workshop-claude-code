Analise o projeto DBT neste repositório e gere documentação completa.

## Foco
1. Para cada model em dbt/models/:
   - Descrição clara do que o model faz e por que existe
   - Fonte de dados (de onde vem)
   - Transformações aplicadas
   - Schema com todas as colunas, tipos e descrições

2. Gerar/atualizar dbt/models/schema.yml:
   - Descrição de cada model
   - Descrição de cada coluna
   - Testes: unique, not_null para PKs; not_null para campos obrigatórios; accepted_values onde aplicável; relationships entre models

3. Gerar diagrama de lineage:
   - Diagrama mermaid mostrando: sources → staging → intermediate → marts
   - Dependências entre models

4. Gerar docs/dbt/data-dictionary.md:
   - Dicionário de dados completo
   - Organizado por camada (staging, intermediate, marts)
   - Cada model com suas colunas, tipos, descrições e regras de negócio inferidas

## Regras
- Português brasileiro
- Ler o SQL real, não inventar
- Se a lógica de negócio não é óbvia, marcar como "⚠️ Lógica a confirmar com o time"
- Ser específico nos nomes de colunas e tipos
