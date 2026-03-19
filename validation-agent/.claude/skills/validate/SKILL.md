---
name: validate
description: Validate a decision, question, or proposal against all project knowledge — compliance, produto, estilo, and technical docs. Runs 3 parallel agents. Use when the user asks "will this work?", "is this approach right?", "does this conflict with anything?", or wants to check alignment before implementing.
---

The user wants to validate a decision, question, or direction against the full project knowledge base. Your job is to run **3 specialized agents in parallel**, collect their findings, and present a consolidated validation report.

**Input:** $ARGUMENTS

## 1. Launch All 3 Agents in Parallel

Spawn all of the following agents **simultaneously** using the Agent tool (subagent_type: "general-purpose"). Every agent receives the same user input but searches a different corpus.

### Agent 1 — Compliance
Instrua o agente a:
- Ler o arquivo `.claude/commands/validate-compliance.md`
- Usar o input acima como contexto (substituindo $ARGUMENTS)
- Seguir todas as instrucoes do arquivo
- Retornar no formato estruturado abaixo

### Agent 2 — Produto e Estilo
Instrua o agente a:
- Ler o arquivo `.claude/commands/validate-produto.md`
- Usar o input acima como contexto (substituindo $ARGUMENTS)
- Seguir todas as instrucoes do arquivo
- Retornar no formato estruturado abaixo

### Agent 3 — Tecnico
Instrua o agente a:
- Ler o arquivo `.claude/commands/validate-tecnico.md`
- Usar o input acima como contexto (substituindo $ARGUMENTS)
- Seguir todas as instrucoes do arquivo
- Retornar no formato estruturado abaixo

### Formato de retorno de cada agente

Cada agente deve retornar exatamente neste formato:

```
AGENTE: <nome>
VEREDITO: COMPATIVEL | CONFLITO | PARCIAL | ATENCAO | SEM_COBERTURA
FONTES: [arquivos e secoes onde encontrou informacao relevante]
RESUMO: [2-4 frases explicando o que encontrou ou o que esta faltando]
ITENS: [lista detalhada com classificacao por item, usando os emojis do validate]
```

## 2. Consolidate Results

After all 3 agents return, compile their findings into a single validation report:

```
## Relatorio de Validacao

**Input:** <a pergunta/decisao/proposta do usuario>

---

### Vereditos

| Agente | Veredito | Achado Principal |
|--------|----------|------------------|
| Compliance | <veredito> | <resumo de uma linha> |
| Produto e Estilo | <veredito> | <resumo de uma linha> |
| Tecnico | <veredito> | <resumo de uma linha> |

### Acao Necessaria

<Com base nos vereditos, liste proximos passos concretos:>
<- Se CONFLITO: "Resolver conflito entre X e Y antes de prosseguir">
<- Se SEM_COBERTURA: "Topico nao coberto pela documentacao — considere documentar antes de prosseguir">
<- Se ATENCAO: "Revisar com o time — [detalhe do risco]">
<- Se COMPATIVEL: "Seguro para prosseguir — ja coberto em [fonte]">

### Achados Detalhados

<Cole a resposta completa de cada agente aqui, em ordem>
```

## 3. Edge Cases

- **Input vago:** Se o input do usuario for generico demais para validar, diga isso e sugira uma formulacao mais especifica.
- **Sem achados em nenhum agente:** Reporte claramente — "Este topico parece ser inteiramente novo para o projeto. Considere documenta-lo antes de prosseguir."
- **Contradicoes entre agentes:** Destaque explicitamente na secao "Acao Necessaria" — ex: "Produto diz X mas Tecnico diz Y — precisa resolucao."

$ARGUMENTS
