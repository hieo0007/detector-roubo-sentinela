# Diretrizes de Contribuicao

## Padrao de Desenvolvimento
1. **Estrutura de Commits:** Utilize o padrao *Conventional Commits* (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`).
2. **Qualidade de Codigo:** Mantenha a modularidade das classes em `src/`, respeitando a separacao de responsabilidades entre captura de frames, analise perimetral, inferencia multimodal e interface web.
3. **Auditoria e Logs:** Todo evento classificado deve manter compatibilidade com o formato JSON de evidencias para auditoria forense.

## Fluxo de Trabalho
1. Crie uma branch para sua funcionalidade ou correcao: `git checkout -b feat/nome-da-feature`.
2. Execute os testes de benchmark para garantir que nao haja regressao de falsos positivos.
3. Submeta um Pull Request detalhado com a descricao das mudancas.
