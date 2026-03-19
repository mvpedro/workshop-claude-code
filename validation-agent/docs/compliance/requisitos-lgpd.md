# Requisitos LGPD — Lei Geral de Protecao de Dados

> Ultima revisao: 2025-11-15
> Responsavel: Equipe de Compliance
> Referencia legal: Lei 13.709/2018

## Contexto

Este documento estabelece os requisitos de conformidade com a LGPD aplicaveis a todo o software desenvolvido internamente. Foi elaborado apos a auditoria de compliance de setembro de 2025 (ver tambem `politica-dados.md` para classificacao de dados e `restricoes-integracao.md` para requisitos de integracao com terceiros).

## 1. Consentimento e base legal

Toda coleta de dados pessoais deve ter base legal explicita (Art. 7, LGPD). As bases legais aceitas no sistema sao:

- **Consentimento explicito**: opt-in ativo, nunca pre-marcado
- **Execucao de contrato**: dados necessarios para entregar o servico contratado
- **Interesse legitimo**: apenas com DPIA (Data Protection Impact Assessment) documentado

Regra: nenhum dado pessoal pode ser coletado sem que a base legal esteja registrada no campo `legal_basis` da tabela de consentimentos.

## 2. Minimizacao de dados

**REGRA CRITICA**: Dados pessoais (CPF, nome, email) NAO devem ser armazenados em tabelas analiticas ou de reporting. Tabelas analiticas devem conter apenas dados anonimizados ou pseudonimizados.

Motivacao: a auditoria de setembro de 2025 identificou que dados de CPF estavam sendo replicados em 4 tabelas de analytics sem necessidade operacional. Isso viola o principio de minimizacao (Art. 6, III, LGPD) — dados pessoais so devem ser tratados na medida do necessario para a finalidade.

Implementacao:
- Tabelas transacionais (`orders`, `customers`, `payments`): podem conter dados pessoais com criptografia
- Tabelas analiticas (`*_analytics`, `*_reporting`, `*_metrics`): apenas IDs anonimizados, nunca dados pessoais
- Para reconciliacao financeira, usar `transaction_id` como chave, nunca CPF

## 3. Retencao de dados

Politica de retencao por categoria:

| Categoria | Retencao maxima | Apos expiracao |
|---|---|---|
| Dados transacionais | 5 anos (obrigacao fiscal) | Anonimizar e arquivar |
| Dados de navegacao | 6 meses | Deletar permanentemente |
| Logs de sistema | 12 meses | Deletar permanentemente |
| Dados de analytics | Indefinido (se anonimizados) | N/A |

Regra: toda tabela que armazena dados pessoais deve ter um campo `retention_expiry_date` ou ser coberta por um job de limpeza automatizado.

## 4. Direito a exclusao (Art. 18, VI)

O sistema deve suportar exclusao de dados pessoais mediante requisicao do titular. A exclusao deve:

- Remover dados de todas as tabelas transacionais
- Manter registros anonimizados em tabelas analiticas (pois nao sao mais dados pessoais)
- Gerar log de auditoria da exclusao (retido por 12 meses)
- Prazo: 15 dias uteis apos requisicao

## 5. Anonimizacao e pseudonimizacao

Tecnicas aceitas:
- **Hashing com salt rotativo** para pseudonimizacao (referencia cruzada possivel internamente)
- **Supressao** de campos sensiveis em exports e relatorios
- **Generalizacao** de dados demograficos (faixa etaria ao inves de data de nascimento)

Dados considerados pessoais no contexto deste sistema: CPF, nome completo, email, telefone, endereco, data de nascimento, IP de acesso.

## 6. Incidentes e notificacao

Em caso de vazamento de dados pessoais:
- Notificar a ANPD em ate 72 horas (Art. 48)
- Notificar titulares afetados em linguagem clara
- Registrar o incidente no sistema de gestao de incidentes

---

*Este documento deve ser revisado trimestralmente. Proxima revisao: 2026-02-15.*
*Ver tambem: `politica-dados.md`, `restricoes-integracao.md`*
