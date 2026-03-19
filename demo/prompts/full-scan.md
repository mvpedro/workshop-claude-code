Analise este repositório inteiro e gere documentação completa em português brasileiro.

## O que gerar

### 1. docs/README.md — Overview da arquitetura
- Descrição do projeto e seu propósito
- Diagrama de arquitetura em mermaid (componentes e como se conectam)
- Stack tecnológica
- Como rodar o projeto localmente

### 2. docs/api/ — Documentação de API
Para cada arquivo de rotas em src/api/routes/:
- Criar um arquivo markdown com todos os endpoints
- Para cada endpoint: método HTTP, path, parâmetros, body esperado, response, códigos de erro
- Incluir exemplos de request/response

### 3. docs/models/ — Documentação de models
Para cada model em src/api/models/:
- Campos com tipos e descrições
- Relacionamentos entre models
- Diagrama ER em mermaid

### 4. docs/repositories/ — Documentação de repositórios
Para cada repositório em src/api/repositories/:
- Descrever a interface abstrata (AbstractRepository) e seus métodos
- Documentar cada implementação concreta com seus métodos específicos
- Parâmetros, retornos e comportamentos de cada método
- Diagrama de herança em mermaid

### 5. docs/events/ — Documentação do sistema de eventos
Para os arquivos em src/api/events/:
- Descrever o event bus (mecanismo de publish/subscribe)
- Documentar cada tipo de evento (dataclasses) com seus campos
- Mapear handlers de eventos e quais serviços eles acionam
- Diagrama de fluxo de eventos em mermaid

### 6. docs/middleware/ — Documentação da cadeia de middleware
Para cada middleware em src/api/middleware/:
- Descrever a função de cada middleware (auth, logging, error handling, rate limiting)
- Ordem de execução na cadeia
- Configurações e comportamentos

### 7. docs/exceptions/ — Documentação da hierarquia de exceptions
Para os arquivos em src/api/exceptions/:
- Documentar a hierarquia de AppException
- Distinção entre exceptions de negócio e de infraestrutura
- Como cada exception é mapeada para respostas HTTP via middleware

### 8. docs/tasks/ — Documentação de background tasks
Para os arquivos em src/api/tasks/:
- Descrever as tarefas assíncronas disponíveis
- Quando são disparadas e por quem
- Fluxo de processamento pós-pedido

### 9. docs/dbt/ — Documentação DBT
Para cada model em dbt/models/:
- Descrição do que o model faz
- Schema YAML com descrição de cada coluna
- Testes de schema recomendados (unique, not_null, accepted_values, relationships)
- Diagrama de lineage em mermaid (dependências entre models)
- Gerar arquivo dbt/models/schema.yml se não existir

### 10. docs/services/ — Documentação de serviços
Para cada serviço em src/api/services/:
- O que o serviço faz
- Métodos públicos com parâmetros e retorno
- Dependências

### 11. docs/SUMMARY.md — Índice
- Links para todos os docs gerados
- Organizado por categoria

## Regras
- Tudo em português brasileiro
- Markdown com headers claros
- Diagramas em mermaid
- Ser específico e preciso — ler o código real, não inventar
- Se algo não está claro no código, marcar como "⚠️ Necessita revisão humana"
