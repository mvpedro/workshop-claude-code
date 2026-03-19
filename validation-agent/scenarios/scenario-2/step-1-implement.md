Preciso migrar nosso frontend de React para Vue.js. Cria um plano de migração
e começa a implementar:

1. Atualiza o package.json: remove React e dependências, adiciona Vue 3, Vite com plugin Vue
2. Cria um componente de exemplo em src/frontend/components/OrderList.vue que lista pedidos
3. Cria src/frontend/App.vue como componente raiz
4. Atualiza os testes: cria tests/frontend/test_order_list.py que testa o
   endpoint de listagem de pedidos mockando o banco de dados para velocidade
   (usar unittest.mock.patch no repository para retornar dados fake)

Requisitos:
- Vue 3 com Composition API
- TypeScript
- Os testes devem ser rápidos, então mocka o banco de dados ao invés de
  usar banco real nos testes de integração
