Os seguintes arquivos foram modificados neste PR:
${CHANGED_FILES}

Analise APENAS os arquivos modificados e atualize a documentação correspondente.

## Regras
- Atualizar APENAS os docs afetados pelas mudanças
- Não regenerar docs de arquivos não modificados
- Se um novo endpoint foi adicionado, adicionar ao doc da rota correspondente
- Se um model DBT foi modificado, atualizar o schema.yml e o diagrama de lineage
- Se um model de dados foi alterado, atualizar o diagrama ER
- Se um repositório foi modificado, atualizar docs/repositories/ correspondente
- Se um evento ou handler foi alterado, atualizar docs/events/
- Se um middleware foi modificado, atualizar docs/middleware/
- Se uma exception foi adicionada ou alterada, atualizar docs/exceptions/
- Se uma background task foi modificada, atualizar docs/tasks/
- Manter o formato e estilo dos docs existentes
- Tudo em português brasileiro
- Se a mudança afeta a arquitetura geral, atualizar docs/README.md também
- Marcar com "🆕 Novo" itens adicionados e "✏️ Atualizado" itens modificados
