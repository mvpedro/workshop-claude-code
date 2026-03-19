# Cenario 1 — Achados esperados: PaymentService sincrono com CPF em analytics

Este documento lista os conflitos que o agente de validacao DEVE identificar ao
analisar o codigo gerado pelo step-1 ou a proposta descrita no step-3.

## Conflitos esperados

### 1. Chamada HTTP sincrona (requests)

- **Documento**: `docs/tecnico/principios-tecnicos.md` — Principio 1
- **Trecho**: "Chamadas a servicos externos DEVEM ser assincronas (httpx.AsyncClient, nunca requests sincrono)."
- **Problema**: O step-1 pede para usar `requests` com timeout de 30s. Isso viola diretamente o principio de chamadas assincronas.
- **Contexto adicional**: `docs/tecnico/stack-definida.md` lista `requests` como tecnologia NAO permitida, com `httpx` como substituto aprovado.
- **Severidade**: ❌ Conflito

### 2. CPF em tabela de analytics

- **Documento**: `docs/compliance/requisitos-lgpd.md` — Secao 2 (Minimizacao de dados)
- **Trecho**: "Dados pessoais (CPF, nome, email) NAO devem ser armazenados em tabelas analiticas ou de reporting."
- **Problema**: O step-1 pede para armazenar CPF na tabela de analytics. Isso viola o principio de minimizacao de dados da LGPD.
- **Severidade**: ❌ Conflito

### 3. CPF e dado RESTRITO

- **Documento**: `docs/compliance/politica-dados.md` — Regra de armazenamento
- **Trecho**: "CPF e dado classificado como RESTRITO e so pode ser armazenado em tabelas transacionais com criptografia."
- **Problema**: O model `payment_analytics` armazena CPF sem criptografia em tabela analitica. Viola tanto a classificacao (RESTRITO so em transacional) quanto a criptografia obrigatoria.
- **Severidade**: ❌ Conflito

### 4. Falta de circuit breaker e retry

- **Documento**: `docs/compliance/restricoes-integracao.md` — Regra geral de resiliencia
- **Trecho**: "Toda integracao com gateway de pagamento deve implementar circuit breaker e retry com backoff exponencial."
- **Problema**: O codigo implementa uma chamada direta sem circuit breaker nem retry. O timeout de 30s tambem esta errado — o documento define timeout padrao de 5s.
- **Contexto adicional**: O documento especifica que Pagar.me deve ser usado em modo assincrono apenas.
- **Severidade**: ❌ Conflito

## Pontos de atencao adicionais

### 5. Timeout de 30 segundos

- **Documento**: `docs/compliance/restricoes-integracao.md` — Padroes obrigatorios
- **Trecho**: "Timeout por chamada: 5 segundos (nao 30s — aprendizado do incidente)"
- **Problema**: O step-1 especifica timeout de 30s. O padrao do projeto e 5s, justamente por causa do incidente de 2025-08.
- **Severidade**: ⚠️ Atencao

## Nuancias que o agente deve captar

- O agente deve identificar que sao 4 conflitos DISTINTOS, nao variantes do mesmo problema
- A questao do CPF aparece em DOIS documentos diferentes (LGPD e politica de dados) — o agente deve citar ambos
- A questao de async aparece em principios tecnicos E em restricoes de integracao (Pagar.me assincrono apenas) — citar ambos
- O agente NAO deve inventar conflitos que nao existem na documentacao
