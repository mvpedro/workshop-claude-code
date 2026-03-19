Tô querendo propor uma migração do frontend de React pra Vue.js. O Vue 3 com
Composition API parece mais simples e o time poderia se beneficiar. A ideia seria:
- Trocar React por Vue 3 gradualmente
- Aproveitar pra atualizar o tooling (Vite já suporta Vue nativamente)
- Nos testes de integração, mockar o banco de dados ao invés de usar banco
  real — os testes ficam muito mais rápidos

O que acham? Isso bate com as decisões do projeto? Tem algo que eu deveria
considerar antes de propor isso pro time?
