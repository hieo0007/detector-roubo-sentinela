# Relatório de Benchmark - Sentinela CCTV

- **Data de Execução**: 2026-11-03
- **Versão do Modelo**: YOLOv8n + Gemini 3.5 Flash Lite
- **Total de Vídeos Avaliados**: 12
- **Acurácia Global**: 66.67%
- **Precisão (Precision)**: 71.43%
- **Sensibilidade (Recall)**: 71.43%
- **Falsos Positivos**: 2
- **Falsos Negativos**: 2
- **Tempo Médio por Vídeo**: 17.98s

## Tabela Detalhada por Cenário

| Arquivo | Esperado | Classificação | Risco | Confiança | Tempo (s) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `pedestre_normal_01.mp4` | NORMAL | NORMAL | NORMAL | 99.0% | 8.42s | ACERTO_NEGATIVO |
| `pedestre_normal_02.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 7.68s | ACERTO_NEGATIVO |
| `pedestre_normal_03.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 61.4s | ACERTO_NEGATIVO |
| `cliente_normal_compras_04.mp4` | NORMAL | ASSALTO_RENDICAO | ALERTA_MAXIMO | 95.0% | 41.07s | FALSO_POSITIVO |
| `atividade_normal_balcao_05.mp4` | NORMAL | FURTO_LOJA | ALERTA_MAXIMO | 98.0% | 12.28s | FALSO_POSITIVO |
| `assalto_furto_01.mp4` | FURTO_LOJA | NORMAL | SUSPEITO | 0.0% | 33.61s | FALSO_NEGATIVO |
| `assalto_furto_02.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 98.0% | 8.47s | ACERTO_POSITIVO |
| `assalto_furto_03.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 98.0% | 8.31s | ACERTO_POSITIVO |
| `furto_real_mercado_01.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 99.0% | 8.2s | ACERTO_POSITIVO |
| `furto_real_gondola_02.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 99.0% | 8.79s | ACERTO_POSITIVO |
| `roubo_mercado_01.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 6.84s | FALSO_NEGATIVO |
| `roubo_mercado_02.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 10.68s | ACERTO_POSITIVO |
