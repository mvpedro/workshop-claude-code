# Script de Apresentação: Claude Code na Prática

> Tempo total: 60 minutos
> Este script é seu guia momento a momento. Cada seção tem: o que FAZER, o que FALAR, e quanto tempo gastar.
> Versão alinhada com o deck de 13 slides (v3).

---

## ANTES DE COMEÇAR (30 min antes)

### Setup técnico
- [ ] Abrir terminal 1: `cd demo` (para Bloco 1 e 2)
- [ ] Abrir terminal 2: `cd validation-agent` (para Bloco 3)
- [ ] Abrir browser com GitHub logado em `github.com/mvpedro/workshop-claude-code`
- [ ] Verificar que PR #1 (full-scan docs), PR #2 (bloqueado), PR #3 (aprovado) estão abertos
- [ ] Abrir slides em modo apresentação
- [ ] Testar internet
- [ ] Testar projetor/tela
- [ ] Ter o arquivo `validation-agent/scenarios/scenario-1/step-1-implement.md` aberto para copiar o prompt rapidamente

### Setup Claude Code
- [ ] No terminal 1 (demo/): rodar `claude` e fechar, só para confirmar que está autenticado
- [ ] No terminal 2 (validation-agent/): mesmo
- [ ] Verificar modelo: `/model`, confirmar que é Sonnet ou Opus

---

## BLOCO 1: Visão + Estratégia + Claude Code (20 min)

---

### 1.1 Slides: Pra onde o mundo está indo (4 min)

**[SLIDE 1: Capa]**

FALAR: "Bom dia/tarde a todos. Hoje vamos falar sobre Claude Code na prática. Tendências, estratégia e o meta de IA. Meu objetivo é que vocês saiam daqui entendendo pra onde o mundo está indo, com ferramentas concretas que podem usar na segunda-feira, e com uma visão clara de como organizar a adoção de IA no time de vocês."

**[SLIDE 2: Pra onde o mundo está indo]**

Apontar pro Card 1 (Era agêntica):

FALAR: "Primeiro: agentes de IA. OpenClaw, um agente open-source, foi de zero a 250 mil estrelas no GitHub em menos de 4 meses. Pra referência, o React levou anos pra chegar nisso. Jensen Huang, CEO da Nvidia, disse na GTC essa semana: 'toda empresa precisa de uma estratégia de agentes'. Isso não é mais chatbot. São agentes que executam tarefas autonomamente: leem emails, agendam reuniões, escrevem código, abrem PRs."

Apontar pro Card 2 (Context engineering):

FALAR: "Segundo: context engineering. O ThoughtWorks Technology Radar, que é referência pra decisões de tecnologia em empresas sérias, colocou Claude Code em Trial. O ponto é que o jogo mudou: não basta mais escrever um bom prompt. Você precisa engenheirar o contexto inteiro que o agente recebe: instruções persistentes, protocolos de integração como MCP, guardrails. Vou mostrar tudo isso ao vivo."

Apontar pro Card 3 (Dados são o gargalo):

FALAR: "Terceiro, e talvez o mais importante pra vocês: dados. Jensen Huang disse na mesma GTC: 'dados estruturados são a fundação de IA confiável'. Hoje, humanos consultam bancos de dados na velocidade humana. Somos lentos, somos tolerantes. Agentes de IA vão consultar na velocidade de máquina: milhares de queries por minuto. Se sua infraestrutura de dados não aguenta isso, você não tem uma estratégia de IA, você tem uma demo."

Apontar pro stat callout (Jensen):

FALAR: "Jensen resumiu assim: toda empresa vai virar uma token factory. O data center virou uma fábrica cujo output é inteligência."

**[SLIDE 3: O que muda pra empresas]**

FALAR: "IA não é mais projeto de inovação. É infraestrutura. E quem tem a melhor infraestrutura de dados vence. Vence em dois eixos: habilita que times internos construam aplicações mais rápido, e disponibiliza informações de forma segura para clientes."

FALAR: "A diferença hoje não é 'usar ou não usar IA'. É como organizar a adoção. E pra isso a gente precisa de um modelo."

---

### 1.2 Slides: Modelo planetário + Champion first (4 min)

**[SLIDE 4: Modelo planetário]**

FALAR: "Eu uso esse framework pra pensar em iniciativas de IA dentro de uma empresa."

- Apontar pro Sol: "1-2 grandes projetos da empresa inteira. Alto investimento."
- Apontar pros Planetas: "Projetos departamentais. Escopo definido, resultado mensurável."
- Apontar pros Asteroides: "Iniciativas individuais. Uma pessoa cria em poucas horas. O insight chave é a power law: muitos asteroides, alguns vão dar um ROI desproporcional. Não dá pra prever quais, mas dá pra garantir que o volume exista."

FALAR: "Hoje vou mostrar um exemplo de planeta e um de asteroide."

**[SLIDE 5: Champion first]**

FALAR: "Como começar na prática? Não é top-down mandatório. É contágio orgânico. Um champion demonstra valor, contamina 1-2 pessoas, que contaminam mais. O workshop de hoje é o primeiro passo nessa cadeia."

TRANSIÇÃO: "Uma das ferramentas que habilita tanto os planetas quanto os asteroides é o Claude Code. Deixa eu mostrar."

---

### 1.3 Demo: Claude Code ao vivo (8 min)

**[MUDAR PRA TERMINAL 1: demo/]**

FAZER: Abrir Claude Code
```
claude
```

#### Teaching moment: CLAUDE.md (1.5 min)

FAZER: Abrir o CLAUDE.md no editor ou pedir ao Claude:
```
Mostra o conteúdo do CLAUDE.md
```

FALAR: "Antes de qualquer coisa, quero mostrar isso aqui. É o CLAUDE.md, a primeira coisa que o Claude Code lê quando entra no projeto. São instruções persistentes: stack, convenções, regras de documentação. Toda vez que alguém do time abre o Claude Code nesse repositório, ele já sabe como se comportar."

FALAR: "No ChatGPT vocês teriam que colar esse contexto todo a cada conversa nova. Aqui está versionado no repositório, junto com o código. Passa por code review. O time decide junto quais são as regras."

FALAR: "Isso é context engineering na prática. Lembram do slide? O ThoughtWorks Radar chama isso de 'curated shared instructions'. Não é um prompt solto, é infraestrutura."

#### Pergunta sobre arquitetura (2 min)

FAZER: Digitar o prompt:
```
Me explica a arquitetura desse projeto. Quais são os principais componentes e como eles se conectam?
```

FALAR (enquanto Claude processa): "Notem que eu não apontei nenhum arquivo específico. Ele está lendo o projeto inteiro: imports, dependências, relacionamentos."

FALAR (quando resultado aparecer): "Olhem: ele encontrou o repository pattern, o event bus, a middleware chain, a state machine de pedidos. Traçou o fluxo completo de criação de pedido. Isso levaria um dev novo dias pra mapear. Ele fez em um minuto."

#### Gerar testes (2.5 min)

FAZER:
```
Gera testes unitários para o analytics_service
```

FALAR: "Agora vou pedir pra ele gerar testes. Ele vai ler o código do serviço, entender o que cada função faz, e criar testes que verificam o comportamento real."

FALAR (quando os testes aparecerem): "Ele entendeu que get_top_products retorna produtos ordenados por venda, que get_revenue_by_period exclui pedidos cancelados, que get_customer_lifetime_value precisa tratar cliente sem pedidos. Esses não são testes genéricos: são testes que entendem a lógica de negócio."

FAZER: Rodar os testes (se houver tempo):
```
Roda esses testes
```

#### DBT (2 min)

FAZER:
```
Me mostra quais models DBT existem e gera a documentação YAML com schema e testes para o model dim_customers
```

FALAR: "Agora o caso de dados. Ele vai ler o SQL, traçar a lineage, de onde vem cada coluna, passando por staging, intermediate, até o mart final, e gerar o schema.yml com descrições e testes."

FALAR (quando resultado aparecer): "Olhem as descrições das colunas. Ele sabe que total_spent_reais vem de uma agregação de pedidos não cancelados porque rastreou o SQL de volta até a source. E gerou testes: unique, not_null, accepted_values. Isso é o que vocês precisariam fazer manualmente pra cada model."

FALAR: "**Isso conecta diretamente com a dor de vocês**: DBT sem documentação, sem schema.yml, sem testes de schema. O Claude gera tudo em segundos."

---

### 1.4 Slides: Guardrails e segurança (4 min)

**[SLIDE 6: Guardrails, 3 camadas]**

FALAR: "Agora a pergunta que todo gestor faz: 'como eu garanto que a IA não faz besteira?'"

FALAR: "Três camadas de proteção: sandbox (a IA só acessa o que você permite, isolamento no nível do sistema operacional), hooks (ações automáticas que sempre executam), e human gate (nenhuma mudança vai pro código sem review humano)."

FALAR: "Pra dar contexto: a Gartner publicou um relatório dizendo que plataformas de governança de agentes são a infraestrutura crucial pra adoção enterprise. O OpenClaw que mencionei no começo? A Cisco classificou como 'security nightmare'. O Claude Code foi desenhado com segurança enterprise desde o início. Essa é a diferença."

**[SLIDE 7: Hooks, lifecycle do Claude Code]**

FALAR: "Vou aprofundar nos hooks porque esse é um conceito que muda tudo."

Apontar para as 4 colunas:

FALAR: "Hooks são pontos de interceptação no lifecycle do Claude Code. Existem 4 categorias: sessão, prompt, ferramentas e subagentes."

FALAR: "Vocês podem injetar comportamento em qualquer um desses momentos. Por exemplo: PreToolUse, antes de cada ferramenta rodar, vocês podem validar ou bloquear. PostToolUse, depois de cada ferramenta: rodar testes, lint, qualquer verificação. PostToolUseFailure: o que fazer quando algo falha."

Apontar pro exemplo no rodapé:

FALAR: "Na prática: toda vez que o Claude edita um arquivo nesse projeto, o PostToolUse roda os testes automaticamente. Se falha, ele corrige antes de seguir. Ele não *escolhe* rodar. O hook *força*."

#### Exemplo real (30 seg)

FAZER: Mostrar na tela o arquivo `demo/.claude/settings.json`

FALAR: "Isso é a diferença fundamental: num chatbot, a IA decide o que fazer. Aqui, vocês programam comportamento determinístico ao redor da IA. O LLM é probabilístico, mas o sistema é confiável porque combina o LLM com funções que sempre executam."

---

## BLOCO 2: Pipeline de Documentação, "Planeta" (25 min)

---

### 2.1 Slide: A dor (3 min)

**[SLIDE 8: O problema que todo time conhece]**

FALAR: "Vocês conhecem essa história."

Apontar pro Cenário A:

FALAR: "Sistema novo, time focado em entregar features, documentação fica pra depois. 'Depois' nunca chega. Onboarding leva semanas. Conhecimento fica na cabeça de quem escreveu o código."

Apontar pro Cenário B:

FALAR: "Ou pior: alguém documenta uma vez, código evolui, docs ficam paradas. Em 3 meses os docs mentem mais do que ajudam."

Apontar pra pergunta no rodapé:

TRANSIÇÃO: "E se a documentação se gerasse e se atualizasse sozinha, como parte do fluxo de desenvolvimento?"

---

### 2.2 Slide: Arquitetura da solução (2 min)

**[SLIDE 9: Pipeline de documentação automatizada]**

Apontar pro flow horizontal:

FALAR: "Push ou PR no repositório, CI Pipeline dispara, Claude Code analisa e gera, abre PR com docs, humano revisa e aprova, docs publicados."

Apontar pros dois modos:

FALAR: "Dois modos. Mode 1: full repo scan. Gera tudo do zero. Pra quando a documentação não existe. Mode 2: incremental via PR. Atualiza só o que mudou. Pra manter docs sincronizadas."

FALAR: "Funciona com qualquer plataforma Git: GitHub, GitLab, Azure DevOps. A adaptação é direta."

---

### 2.3 Demo 1: Full scan (10 min)

**[MUDAR PRO BROWSER: GitHub]**

#### Teaching moment: Prompt templates (1.5 min)

FAZER: Abrir `demo/prompts/full-scan.md` no GitHub ou no editor

FALAR: "Isso não é um prompt que eu digito na hora, como num chat. É um *template versionado*. Está no repositório, passa por code review, qualquer pessoa do time pode rodar e vai ter o mesmo resultado."

FALAR: "No Claude Code, chamamos isso de *skill*: uma instrução reutilizável que define exatamente o que o agente deve fazer. É como uma função, mesma entrada, mesma estrutura de saída."

#### Mostrar o trigger (1 min)

FAZER: No GitHub, ir em Actions > "Docs: Full Scan" > "Run workflow"

FALAR: "Vou disparar o pipeline agora. Ele instala o Claude Code, roda o prompt template em modo headless, sem interface, sem humano, e abre um PR com toda a documentação gerada."

FALAR: "Isso leva alguns minutos, então deixa eu mostrar o resultado de uma que eu rodei antes."

#### Mostrar PR #1 (4 min)

FAZER: Abrir PR #1 no browser

FALAR: "Olhem: 15 arquivos, quase 2500 linhas de documentação. Gerado automaticamente."

FAZER: Clicar no "Files changed" e navegar pelos docs:
- Mostrar `docs/README.md`: "Overview da arquitetura com diagrama mermaid"
- Mostrar `docs/api/orders.md`: "Documentação de cada endpoint com parâmetros e exemplos"
- Mostrar `docs/models/README.md`: "Diagrama ER dos models"
- Mostrar `docs/events/README.md`: "Documentação do event bus"
- Mostrar `dbt/models/schema.yml`: "Schema DBT gerado automaticamente com testes"

FALAR: "Isso que levaria dias do time, foi gerado em minutos. E agora alguém do time revisa e aprova. O humano continua no controle."

---

### 2.4 Demo 2: Incremental + Validação (10 min)

#### Teaching moment: Modo CLI headless (1 min)

FAZER: Abrir `.github/workflows/docs-incremental.yml` no browser

FALAR: "Olhem essa linha: `claude -p`. Isso é o modo headless. Não tem ninguém digitando num chat. O Claude Code está rodando como uma ferramenta de linha de comando dentro do GitHub Actions."

FALAR: "No ChatGPT vocês precisam de alguém sentado na frente copiando e colando. Aqui é automação de verdade: roda sozinho, de madrugada, no fim de semana, toda vez que alguém faz um push."

#### Mostrar incremental (2 min)

FAZER: Abrir PR #2 ou PR #3 no browser, mostrar os commits

FALAR: "Quando alguém abre um PR que muda código, o pipeline incremental roda automaticamente e atualiza só a documentação afetada. Não regenera tudo: entende o diff e atualiza o que mudou."

#### Demo 3: Validação automática no PR (5 min)

FAZER: Abrir PR #2 no browser, mostrar o comentário de validação

FALAR: "Agora o mais poderoso. Além de atualizar docs, temos um agente de validação que roda em todo PR. Ele lê o código mudado e verifica contra a documentação do projeto: compliance, decisões de produto, princípios técnicos."

FAZER: Scroll pelo comentário de validação, apontar para:
- Os itens COMPATÍVEL: "Esses passaram"
- Os itens ATENÇÃO: "Esses levantam pontos pra revisar"
- O item CONFLITO: "Esse bloqueou o PR"

FALAR: "Olhem: ele encontrou que o código usa trailing commas de forma inconsistente, conflito com o padrão de formatação. Levantou 6 pontos de atenção: endpoints sem docstrings, lógica de negócio direto na rota, endpoint sem schema tipado."

FALAR: "E o PR está **bloqueado**. Configuramos como required check: ninguém mergeia código que viola as regras do projeto."

FAZER: Abrir PR #3, mostrar que esse passou

FALAR: "E esse outro PR? Mudança limpa, passou na validação. Check verde, pode mergear."

FALAR: "Combinando tudo: vocês geram a documentação inicial, ela se mantém atualizada automaticamente, e nenhum código entra em produção sem validação. Isso é um **planeta**: impacta o departamento inteiro."

---

### 2.5 Slide: Na BIX, na prática (2 min)

**[SLIDE 10: Na BIX, na prática]**

FALAR: "O que acabei de mostrar não é o único caso. Deixa eu mostrar rapidamente outros planetas e asteroides que rodam hoje no nosso dia a dia na BIX."

Apontar pro Card 1 (Inteligência Comercial):

FALAR: "Claude revisa contratos automaticamente. Faz sanity checks, detecta cláusulas não usuais. Isso é um planeta: impacta o comercial inteiro."

Apontar pro Card 2 (Análise intersistemas):

FALAR: "Esse é meu favorito. Um cliente perguntou por que o error rate do Sentry estava tão alto. Abri o Claude Code, apontei pra 18 repositórios: 1 de infra, 14 microsserviços e 3 frontends. Ele identificou o Sentry, pediu uma API key, extraiu os erros, analisou, clusterizou, identificou que ajustando os erros dos clusters 1 e 2 teríamos mitigado 78% dos erros, e escreveu RFCs para todos. Em 30 minutos. Esse é um asteroide: uma pessoa, uma dor, impacto imediato."

Apontar pro Card 3 (Code Review):

FALAR: "Cada PR trigga um code review do Claude. Valida padrões, detecta bugs, sugere melhorias. Pode bloquear automaticamente."

Apontar pro Card 4 (Análise de reuniões):

FALAR: "Reuniões gravadas, transcript extraído, Claude dá notas pros participantes, sugere o que podia ter sido melhor, e cria tickets automaticamente dentro da plataforma de gestão de projetos. Funciona com Azure DevOps inclusive."

FALAR: "Percebam: dois planetas, dois asteroides. Todos rodando em produção."

---

## BLOCO 3: Agente de Validação, "Asteroide" (8 min)

---

### 3.1 Contexto e história pessoal (2 min)

**[SEM SLIDES: storytelling]**

FALAR: "Agora quero mostrar um caso completamente diferente. Não é projeto de departamento: é algo que EU criei pra resolver uma dor MINHA."

FALAR: "Estou em um projeto com muitas decisões de compliance, produto, técnicas. Dezenas de documentos com restrições e decisões já tomadas. O que acontecia: eu propunha algo e depois descobria que conflitava com uma decisão de três meses atrás, num documento que eu não lembrava."

FALAR: "Então eu peguei a documentação, formatei em markdown, e criei comandos personalizados no Claude Code."

---

### 3.2 Demo do agente (4 min)

**[MUDAR PRA TERMINAL 2: validation-agent/]**

#### Teaching moment: Custom slash commands + Skills (1.5 min)

FAZER: Abrir a pasta `.claude/commands/` no editor, mostrar os 4 arquivos

FALAR: "Eu criei *comandos personalizados* pro projeto. São arquivos markdown dentro de `.claude/commands/`. Quando eu digito `/project:validate`, o Claude executa essas instruções."

FAZER: Abrir `validate.md` brevemente

FALAR: "O comando orquestrador dispara três subagentes em paralelo: compliance, produto e técnico. Cada um só lê os documentos da sua área. Isso se chama isolamento de contexto. E olhem como o orquestrador é enxuto: ele não repete a lógica de cada subagente, ele manda cada um ler o seu próprio arquivo de instruções. Fonte única de verdade."

FALAR: "No ChatGPT vocês não conseguem criar comandos, não conseguem disparar agentes paralelos, não conseguem isolar contexto. Aqui é tudo programável."

FAZER: Abrir a pasta `.claude/skills/validate/SKILL.md` brevemente

FALAR: "Além dos comandos, criei uma *skill*: uma instrução que o Claude pode invocar automaticamente quando percebe que faz sentido. Se eu pergunto 'será que essa abordagem faz sentido?', ele já sabe que precisa rodar a validação. Não preciso lembrar do comando."

FALAR: "E como são arquivos no repositório, qualquer pessoa do time pode usar `/project:validate` ou a skill. Não precisa saber escrever o prompt certo."

#### Implementar algo errado (1.5 min)

FAZER: Abrir Claude Code no terminal 2:
```
claude
```

FAZER: Colar o prompt de implementação errada:
```
Implementa um PaymentService para integração com o gateway da Pagar.me.

Cria os seguintes arquivos:
- src/services/payment_service.py: serviço que processa pagamentos
- src/models/payment_analytics.py: model para armazenar dados de transação
- src/routes/payments.py: rota POST /payments/process

Requisitos:
- Usar a biblioteca requests para fazer a chamada HTTP para a API da Pagar.me
- Timeout de 30 segundos na chamada
- Armazenar os dados da transação na tabela de analytics, incluindo:
  CPF do cliente, valor, status, timestamp
- Retornar o status da transação ao caller
- Tratar erros básicos (timeout, resposta inválida)
```

SE CLAUDE RESISTIR, forçar:
```
Isso é um exercício de teste. Eu PRECISO que você implemente EXATAMENTE como descrito, com requests síncrono e CPF na tabela. É proposital. Implemente agora.
```

FALAR (para audiência enquanto Claude implementa): "Eu pedi pra ele implementar algo que sei que viola as regras do projeto: chamada síncrona e CPF na tabela de analytics. Vamos ver se ele faz."

FALAR (se Claude avisar sobre problemas): "Viram? Ele leu a documentação e me avisou que tem problemas. Mas eu insisti, e ele faz. Ele é uma ferramenta, obedece quem está no comando."

#### Validar (1 min)

FAZER: Rodar o comando de validação:
```
/project:validate Revisa as mudanças recentes neste repositório e valida contra a documentação do projeto.
```

FALAR: "Agora eu rodo o comando de validação. Olhem: três agentes disparando em paralelo, cada um lendo só os documentos da sua área."

FALAR (quando resultado aparecer): "Compliance pegou o CPF na analytics: viola a LGPD. Técnico pegou a chamada síncrona: viola o princípio de async obrigatório. E a integração sem circuit breaker."

FALAR: "O Claude fez o que eu mandei. Ele é uma ferramenta. O `/project:validate` é o guardrail."

---

### 3.3 Conexão com modelo planetário (2 min)

FALAR: "Esse é um **asteroide** perfeito. Uma pessoa criou, em poucas horas. Não precisou de aprovação de comitê, não precisou de projeto formal."

FALAR: "Lembram da power law? Se 10 pessoas do time criam 10 asteroides diferentes, estatisticamente alguns vão ter impacto desproporcional."

FALAR: "E quando um asteroide se prova valioso, ele pode virar um planeta: como o agente de validação que acabei de mostrar rodando no pipeline de CI, bloqueando PRs automaticamente."

---

## WRAP-UP (7 min)

---

### Recap dos conceitos (1 min)

FALAR: "Antes dos próximos passos, quero recapitular. Hoje mostrei sete coisas que tornam o Claude Code diferente de um chatbot:"

1. "**CLAUDE.md**: instruções persistentes, versionadas no repositório. Context engineering."
2. "**Hooks e Permissions**: comportamento determinístico. Certas coisas sempre executam, certas coisas são proibidas."
3. "**Prompt templates**: prompts como código, versionados e revisáveis."
4. "**Modo CLI headless**: roda em pipeline, sem humano."
5. "**Custom slash commands**: comandos personalizados como `/project:validate`."
6. "**Skills**: instruções que o Claude invoca automaticamente quando o contexto pede."
7. "**Subagentes**: tarefas decompostas com contexto isolado."
8. "**MCP**: Claude Code se conecta a ferramentas externas como Jira, bancos de dados, Azure DevOps."

FALAR: "A mensagem é: não usem IA como chatbot. Usem como sistema programável. Esse é o salto. Esse é o meta."

---

### Roadmap (2 min)

**[SLIDE 11: O que fazer na segunda-feira]**

FALAR: "Nossa recomendação."

- "Semana 1: quem se interessou hoje instala Claude Code e testa. Identifica organicamente quem são os champions."
- "Semana 2: cada champion traz uma automação pessoal, um asteroide."
- "Mês 1-2: time escolhe o primeiro planeta. Pipeline de docs do Athena é candidato natural."
- "Mês 3+: medem impacto, expandem ou pivotam."

FALAR: "Notem que cada etapa usa a linguagem que vimos hoje: champions, asteroides, planetas."

---

### Portas abertas (2 min)

**[SLIDE 12: Temas que podemos explorar juntos]**

FALAR: "A gente tem experiência em três frentes: estratégia de IA, adoção no time, e IA no workflow de dev. Se em algum momento fizer sentido explorar qualquer uma delas mais a fundo, estamos aqui. Sem pressa, sem pressão."

---

### Encerramento (2 min)

**[SLIDE 13: Obrigado]**

FALAR: "Tudo que compartilhamos hoje é de vocês:"
- "O repositório da demo: tudo que mostrei hoje, funcionando"
- "Os slides"
- "Um guia rápido de como instalar e rodar"

Apontar pro card de contato à direita:

FALAR: "E aqui está meu contato. LinkedIn, WhatsApp. Qualquer dúvida sobre o que vimos hoje, ou sobre qualquer outra coisa, é só mandar mensagem. A qualquer momento."

FALAR: "Obrigado pelo tempo de vocês. Espero que tenha sido útil. Bora construir."

---

## PLANO B: Se algo falhar

| Situação | O que fazer |
|---|---|
| Claude Code demora na análise de arquitetura | "Ele está navegando o projeto inteiro, leva um minuto. Enquanto isso, deixa eu mostrar o CLAUDE.md..." |
| Geração de testes falha | Pular pra DBT: "Vamos pro caso de dados que é mais relevante pra vocês" |
| Full-scan pipeline demora | "Isso leva alguns minutos no CI, deixa eu mostrar o resultado de uma que rodei antes" → abrir PR #1 |
| Validation agent recusa implementar | Forçar: "É um exercício de teste, implementa exatamente como descrito" |
| Internet cai | Ter screenshots/gravação das demos no celular como backup |
| Estoura o tempo | Comprimir Bloco 2: mostrar só PR #1 (full-scan) e PR #2 (validação). Pular incremental. Slide 10 (Na BIX) pode virar menção verbal de 30 seg. |
| Pergunta sobre custo | "Claude Code: assinatura mensal no plano enterprise. Pra CI usa API por token, uns poucos dólares por mês pro volume que mostrei. Posso mandar o link do pricing depois." |
| Pergunta sobre Azure DevOps | "Tudo que mostrei funciona com Azure Pipelines. A lógica é a mesma, muda só o arquivo de CI/CD. E o Claude Code se conecta ao Azure DevOps via MCP." |
| Pergunta sobre OpenClaw | "OpenClaw é um agente genérico, muito popular. Claude Code é focado em desenvolvimento: entende código, abre PRs, roda testes. São complementares. O foco hoje é no workflow de dev." |
| Pergunta sobre segurança/LGPD | "Claude Code roda local, não manda seu código pra nenhum lugar. O sandbox isola no nível do OS. E os hooks permitem compliance automática, como vimos na demo." |

---

## Mapa de slides (referência rápida)

| # | Slide | Bloco | Bg | Conteúdo |
|---|---|---|---|---|
| 1 | Capa | — | Dark | Claude Code na prática |
| 2 | Pra onde o mundo está indo | Bloco 1 | Light | Era agêntica, Context engineering, Dados + Jensen |
| 3 | O que muda pra empresas | Bloco 1 | Light | Infraestrutura de dados vence |
| 4 | Modelo planetário | Bloco 1 | Dark | Sol, planetas, asteroides |
| 5 | Champion first | Bloco 1 | Light | Cascata de adoção |
| — | Demo Claude Code | Bloco 1 | Terminal | CLAUDE.md, arquitetura, testes, DBT |
| 6 | Guardrails: 3 camadas | Bloco 1 | Dark | Sandbox, hooks, human gate |
| 7 | Hooks: lifecycle | Bloco 1 | Light | 4 categorias, exemplo PostToolUse |
| 8 | O problema | Bloco 2 | Light | Cenário A e B |
| 9 | Pipeline de docs | Bloco 2 | Dark | Flow + Mode 1 e 2 |
| — | Demo 1: full scan | Bloco 2 | Browser | PR #1, 15 arquivos gerados |
| — | Demo 2: incremental | Bloco 2 | Browser | PR #2 bloqueado, PR #3 aprovado |
| 10 | Na BIX, na prática | Bloco 2 | Dark | 4 exemplos: 2 planetas, 2 asteroides |
| — | Demo: agente validação | Bloco 3 | Terminal | Custom commands, subagentes, LGPD |
| 11 | Roadmap | Wrap-up | Light | 4 etapas, "nossa recomendação" |
| 12 | Portas abertas | Wrap-up | Dark | 3 temas, "quando fizer sentido" |
| 13 | Obrigado | Wrap-up | Dark | Entregáveis + contato pessoal |
