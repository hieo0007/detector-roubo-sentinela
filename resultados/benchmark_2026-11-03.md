# Relatório de Benchmark - Sentinela CCTV

- **Data de Execução**: 2026-11-03
- **Versão do Modelo**: YOLOv8n + Gemini 3.5 Flash Lite
- **Total de Vídeos Válidos Avaliados**: 12
- **Erros de Comunicação / API (ERRO_IA)**: 0 (excluídos das métricas de acurácia)
- **Acurácia Global**: 50.0%
- **Precisão (Precision)**: 50.0%
- **Sensibilidade (Recall)**: 42.86%
- **Erros de Classe (Crime Detectado com Tipo Errado)**: 1
- **Falsos Positivos**: 2
- **Falsos Negativos**: 3
- **Tempo Médio Total por Vídeo**: 7.4s
- **Tempo Médio da Chamada ao Gemini**: 2.49s

## Tabela Detalhada por Cenário

| Arquivo | Esperado | Classificação | Risco | Confiança | Tempo Total (s) | Tempo Gemini (s) | Status | Origem |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `pedestre_normal_01.mp4` | NORMAL | NORMAL | NORMAL | 99.5% | 12.07s | 2.6s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20(1).mp4 |
| `pedestre_normal_02.mp4` | NORMAL | NORMAL | NORMAL | 95.5% | 7.95s | 2.01s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/normal/shop_lifter_n_1.mp4 |
| `pedestre_normal_03.mp4` | NORMAL | NORMAL | NORMAL | 95.5% | 4.7s | 1.7s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20(15).mp4 |
| `cliente_normal_compras_04.mp4` | NORMAL | ASSALTO_RENDICAO | ALERTA_MAXIMO | 99.5% | 10.85s | 2.12s | FALSO_POSITIVO | origem desconhecida |
| `atividade_normal_balcao_05.mp4` | NORMAL | FURTO_LOJA | ALERTA_MAXIMO | 98.5% | 8.06s | 6.87s | FALSO_POSITIVO | origem desconhecida |
| `assalto_furto_01.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.5% | 4.59s | 1.9s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20(1).mp4 |
| `assalto_furto_02.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 98.5% | 5.92s | 2.1s | ACERTO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20(10).mp4 |
| `assalto_furto_03.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 4.73s | 1.8s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20(15).mp4 |
| `furto_real_mercado_01.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 98.5% | 7.92s | 2.14s | ACERTO_POSITIVO | origem desconhecida |
| `furto_real_gondola_02.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 98.5% | 7.97s | 1.74s | ACERTO_POSITIVO | origem desconhecida |
| `roubo_mercado_01.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 6.98s | 3.0s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_0.mp4 |
| `roubo_mercado_02.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 7.11s | 1.95s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_1.mp4 |
