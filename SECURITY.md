# Politica de Seguranca da Informacao e Privacidade

## Escopo e Arquitetura de Privacidade
O sistema Sentinela adota o principio de privacidade por design (*Privacy by Design*):
1. **Processamento Local (Edge):** O processamento continuo de video em tempo real e executado inteiramente na infraestrutura local do cliente via YOLOv8 e ByteTrack. Nenhum fluxo de video ao vivo e transmitido para servidores externos.
2. **Transferencia Minima de Dados:** Apenas storyboards temporais comprimidos (amostras de quadros em JPEG de baixa resolucao) sao enviados temporariamente para inferencia semantica quando um gatilho de seguranca e disparado.
3. **Custodia de Evidencias:** Clipes forenses sao armazenados exclusivamente no diretorio local de evidencias do servidor, codificados em H.264 seguro.

## Reporte de Vulnerabilidades
Para reportar vulnerabilidades de seguranca ou falhas de isolamento, abra uma issue tecnica no repositorio ou encaminhe um relatorio detalhado diretamente a equipe de desenvolvimento.
