Estou pensando em implementar a integração com um gateway de pagamento
(Pagar.me). Minha ideia inicial:
- Usar chamada HTTP síncrona com requests pra simplicidade
- Timeout de 30 segundos
- Guardar CPF do cliente junto com os dados da transação numa tabela
  de analytics pra facilitar reconciliação financeira

Antes de eu começar: isso bate com o que já foi decidido no projeto?
Tem alguma restrição que eu deveria considerar?
