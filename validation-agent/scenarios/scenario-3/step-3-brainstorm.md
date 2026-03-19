Preciso criar um endpoint de analytics que mostre um relatório de vendas por
cliente pro time comercial. Tava pensando em:
- Fazer em SQL raw, porque a query vai ter JOINs e window functions que
  ficam muito mais claras fora do ORM
- Retornar nome, email e CPF do cliente junto com as métricas de venda
  (total, ticket médio, quantidade de pedidos) — o time comercial precisa
  identificar os clientes no relatório
- Usar paginação com limit/offset

Isso faz sentido com o que temos definido no projeto? Alguma restrição
que eu deveria levar em conta?
