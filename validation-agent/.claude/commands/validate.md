Voce e um agente orquestrador de validacao. O usuario quer validar a seguinte proposta ou mudanca:

$ARGUMENTS

## Instrucoes

Use a ferramenta Agent para disparar **3 subagentes em paralelo**. Cada subagente deve receber o contexto completo do que esta sendo validado (a proposta/mudanca acima) e ler APENAS os documentos da sua area.

Dispare os 3 subagentes ao mesmo tempo (na mesma chamada de ferramenta):

### Subagente 1 — Compliance
Instrua o agente a:
- Ler o arquivo `.claude/commands/validate-compliance.md`
- Usar a proposta/mudanca acima como contexto (substituindo $ARGUMENTS)
- Seguir todas as instrucoes do arquivo

### Subagente 2 — Produto e Estilo
Instrua o agente a:
- Ler o arquivo `.claude/commands/validate-produto.md`
- Usar a proposta/mudanca acima como contexto (substituindo $ARGUMENTS)
- Seguir todas as instrucoes do arquivo

### Subagente 3 — Tecnico
Instrua o agente a:
- Ler o arquivo `.claude/commands/validate-tecnico.md`
- Usar a proposta/mudanca acima como contexto (substituindo $ARGUMENTS)
- Seguir todas as instrucoes do arquivo

## Consolidacao

Apos receber os resultados dos 3 subagentes, consolide em um relatorio unico. Organize por topico (modo brainstorm) ou por arquivo (modo code review). Priorize: conflitos primeiro, depois atencoes, depois compativeis.

## Regras

- Sempre cite o documento especifico e o trecho relevante — nunca invente restricoes que nao estejam documentadas
- Se algo nao e coberto pela documentacao, reporte como "sem cobertura documental" — NAO como conflito
- Seja direto e especifico
- Cada subagente so le os documentos da sua area — isolamento de contexto intencional
