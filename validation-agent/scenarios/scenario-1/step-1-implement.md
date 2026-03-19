Implementa um PaymentService para integração com o gateway da Pagar.me.

Cria os seguintes arquivos:
- src/services/payment_service.py — serviço que processa pagamentos
- src/models/payment_analytics.py — model para armazenar dados de transação
- src/routes/payments.py — rota POST /payments/process

Requisitos:
- Usar a biblioteca requests para fazer a chamada HTTP para a API da Pagar.me
- Timeout de 30 segundos na chamada
- Armazenar os dados da transação na tabela de analytics, incluindo:
  CPF do cliente, valor, status, timestamp
- Retornar o status da transação ao caller
- Tratar erros básicos (timeout, resposta inválida)
