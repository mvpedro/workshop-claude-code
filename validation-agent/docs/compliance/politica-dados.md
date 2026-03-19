# Politica de classificacao e tratamento de dados

> Ultima revisao: 2025-10-20
> Responsavel: Equipe de Compliance + Arquitetura
> Aprovado por: Comite de Seguranca da Informacao

## Contexto

Esta politica define a classificacao de dados do sistema e os controles de seguranca associados a cada nivel. Complementa os `requisitos-lgpd.md` com regras operacionais de armazenamento e acesso. Ver tambem `decisoes-arquitetura.md` para decisoes de criptografia em repouso.

## Niveis de classificacao

### Publico

Dados que podem ser divulgados sem restricao.
- Exemplos: nome de produtos no catalogo, categorias, precos publicados
- Controles: nenhum controle adicional

### Interno

Dados de uso interno da organizacao, sem impacto regulatorio se vazados.
- Exemplos: metricas agregadas de vendas, contagem de pedidos por periodo, dashboards internos
- Controles: autenticacao basica, log de acesso

### Confidencial

Dados com impacto operacional ou contratual se vazados.
- Exemplos: email de clientes, historico de pedidos vinculado a cliente, regras de precificacao detalhadas
- Controles: criptografia em transito (TLS), controle de acesso por perfil, auditoria de leitura

### Restrito

Dados com impacto regulatorio (LGPD) e/ou financeiro se vazados.
- Exemplos: CPF, dados de pagamento, tokens de gateway
- Controles: criptografia em repouso + transito, acesso restrito a servicos especificos, log de cada acesso individual

## Regras de armazenamento por classificacao

**REGRA CRITICA**: CPF e dado classificado como RESTRITO e so pode ser armazenado em tabelas transacionais com criptografia. Nunca em tabelas analiticas, caches, logs ou exports.

| Classificacao | Tabelas transacionais | Tabelas analiticas | Logs | Exports |
|---|---|---|---|---|
| Publico | ✅ | ✅ | ✅ | ✅ |
| Interno | ✅ | ✅ | ✅ com mascara | ✅ com aprovacao |
| Confidencial | ✅ com criptografia | ❌ (apenas ID anonimizado) | ❌ | ❌ sem aprovacao |
| Restrito | ✅ com criptografia AES-256 | ❌ | ❌ | ❌ |

## Tratamento especifico de PII

Dados pessoais identificaveis (PII) no sistema:

| Dado | Classificacao | Onde pode existir | Criptografia |
|---|---|---|---|
| CPF | Restrito | `customers.cpf`, `payments.customer_cpf` | AES-256 |
| Nome completo | Confidencial | `customers.name` | AES-256 |
| Email | Confidencial | `customers.email` | AES-256 |
| Telefone | Confidencial | `customers.phone` | AES-256 |
| Endereco | Confidencial | `customers.address` | AES-256 |
| Data nascimento | Confidencial | `customers.birth_date` | AES-256 |

Regra: qualquer novo campo que armazene PII deve passar por revisao de compliance antes de ser criado. A equipe de desenvolvimento deve abrir um ticket de classificacao de dados antes de adicionar colunas com PII.

## Acesso a dados restritos

Servicos que tem permissao para acessar dados classificados como RESTRITO:
- `payment_service` — para processar transacoes
- `customer_service` — para gestao de cadastro
- `compliance_service` — para auditoria e exclusao de dados

Nenhum outro servico deve acessar dados restritos diretamente. Se um servico de analytics precisa correlacionar dados, deve usar o `transaction_id` ou `customer_hash` como chave, nunca o CPF ou dados pessoais.

## Criptografia

- Em repouso: AES-256 para dados restritos e confidenciais
- Em transito: TLS 1.2+ obrigatorio para todas as comunicacoes
- Chaves gerenciadas via AWS KMS (decisao de 2025-07, ver `decisoes-arquitetura.md`)
- Rotacao de chaves: a cada 90 dias

---

*Este documento deve ser revisado semestralmente. Proxima revisao: 2026-04-20.*
*Ver tambem: `requisitos-lgpd.md`, `decisoes-arquitetura.md`*
