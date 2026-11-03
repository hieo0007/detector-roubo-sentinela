# Relatório de Benchmark - Sentinela CCTV

- **Data de Execução**: 2026-11-03
- **Versão do Modelo**: YOLOv8n + Gemini 3.5 Flash Lite
- **Total de Vídeos Válidos Avaliados**: 12
- **Erros de Comunicação / API (ERRO_IA)**: 0 (excluídos das métricas de acurácia)
- **Acurácia Global**: 66.67%
- **Precisão (Precision)**: 62.5%
- **Sensibilidade (Recall)**: 71.43%
- **Erros de Classe (Crime Detectado com Tipo Errado)**: 1
- **Falsos Positivos**: 2
- **Falsos Negativos**: 1
- **Tempo Médio Total por Vídeo**: 14.9s
- **Tempo Médio da Chamada ao Gemini**: 3.6s

## Tabela Detalhada por Cenário

| Arquivo | Esperado | Classificação | Risco | Confiança | Tempo Total (s) | Tempo Gemini (s) | Status | Origem |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `pedestre_normal_01.mp4` | NORMAL | NORMAL | NORMAL | 99.0% | 10.68s | 2.13s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20(1).mp4 |
| `pedestre_normal_02.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 9.02s | 2.29s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/normal/shop_lifter_n_1.mp4 |
| `pedestre_normal_03.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 4.72s | 1.81s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20(15).mp4 |
| `cliente_normal_compras_04.mp4` | NORMAL | ASSALTO_RENDICAO | ALERTA_MAXIMO | 95.0% | 13.72s | 2.01s | FALSO_POSITIVO | origem desconhecida |
| `atividade_normal_balcao_05.mp4` | NORMAL | FURTO_LOJA | ALERTA_MAXIMO | 98.0% | 21.07s | 18.28s | FALSO_POSITIVO | origem desconhecida |
| `assalto_furto_01.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 98.0% | 15.17s | 3.45s | ACERTO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20(1).mp4 |
| `assalto_furto_02.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 98.0% | 8.11s | 2.13s | ACERTO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20(10).mp4 |
| `assalto_furto_03.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 98.0% | 10.75s | 2.13s | ACERTO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20(15).mp4 |
| `furto_real_mercado_01.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 99.0% | 18.59s | 2.07s | ACERTO_POSITIVO | origem desconhecida |
| `furto_real_gondola_02.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 99.0% | 18.12s | 1.96s | ACERTO_POSITIVO | origem desconhecida |
| `roubo_mercado_01.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 20.46s | 2.94s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_0.mp4 |
| `roubo_mercado_02.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 28.4s | 1.99s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_1.mp4 |
