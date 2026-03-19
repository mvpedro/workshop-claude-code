Cria um endpoint de analytics que retorna um relatório de vendas por cliente.

Cria os seguintes arquivos:
- src/services/analytics_service.py — serviço que executa queries analíticas
- src/routes/analytics.py — rota GET /analytics/sales-by-customer
- src/models/analytics_report.py — schema do relatório

Requisitos:
- Usar SQL raw (sem ORM) para a query de analytics — preciso de JOINs complexos
  e window functions que ficam mais claros em SQL direto
- A query deve retornar por cliente: nome, email, CPF, total de compras,
  número de pedidos, ticket médio, data do último pedido
- Incluir paginação (limit/offset)
- Formato de resposta: JSON com lista de clientes e métricas agregadas
- A query deve ser performática — usar índices e evitar N+1
