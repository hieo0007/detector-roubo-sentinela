# Relatório de Benchmark - Sentinela CCTV

- **Data de Execução**: 2026-11-03_2022
- **Rótulo / Tag**: `prompt_antigo`
- **Versão do Prompt**: `legacy`
- **Versão do Modelo**: YOLOv8n + Gemini 3.5 Flash Lite (prompt: legacy)
- **Total de Vídeos Válidos Avaliados**: 50
- **Erros de Comunicação / API (ERRO_IA)**: 0 (excluídos das métricas de acurácia)
- **Acurácia Global**: 38.0%
- **Precisão (Precision)**: 19.23%
- **Sensibilidade (Recall)**: 20.0%
- **Erros de Classe (Crime Detectado com Tipo Errado)**: 10
- **Falsos Positivos**: 11
- **Falsos Negativos**: 10
- **Tempo Médio Total por Vídeo**: 8.08s
- **Tempo Médio da Chamada ao Gemini**: 5.19s

## Tabela Detalhada por Cenário

| Arquivo | Esperado | Classificação | Risco | Confiança | Tempo Total (s) | Tempo Gemini (s) | Status | Origem |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `mnnit_normal_01.mp4` | NORMAL | NORMAL | NORMAL | 99.0% | 7.39s | 1.95s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%281%29.mp4?download=true |
| `mnnit_normal_02.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 5.2s | 2.13s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%282%29.mp4?download=true |
| `mnnit_normal_03.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 5.05s | 2.21s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%283%29.mp4?download=true |
| `mnnit_normal_04.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 23.36s | 20.46s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%284%29.mp4?download=true |
| `mnnit_normal_05.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 8.37s | 6.21s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%285%29.mp4?download=true |
| `mnnit_normal_06.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 4.81s | 2.56s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%286%29.mp4?download=true |
| `mnnit_normal_07.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 5.06s | 2.25s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%287%29.mp4?download=true |
| `mnnit_normal_08.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 4.49s | 2.18s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%288%29.mp4?download=true |
| `mnnit_normal_09.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 4.5s | 2.32s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%289%29.mp4?download=true |
| `mnnit_normal_10.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 4.72s | 2.05s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2810%29.mp4?download=true |
| `mnnit_normal_11.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 8.26s | 5.29s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2811%29.mp4?download=true |
| `mnnit_normal_12.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 98.0% | 8.9s | 6.15s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2812%29.mp4?download=true |
| `mnnit_normal_13.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 4.23s | 2.13s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2813%29.mp4?download=true |
| `ds2_normal_01.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 33.61s | 29.5s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/normal/shop_lifter_n_1.mp4?download=true |
| `ds2_normal_03.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 5.34s | 2.14s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/normal/shop_lifter_n_3.mp4?download=true |
| `ds2_normal_06.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 5.88s | 2.11s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/normal/shop_lifter_n_6.mp4?download=true |
| `ds2_normal_08.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 5.53s | 2.18s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/normal/shop_lifter_n_8.mp4?download=true |
| `ds2_normal_11.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 6.02s | 2.16s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/normal/shop_lifter_n_11.mp4?download=true |
| `mnnit_normal_14.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 3.92s | 2.0s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2814%29.mp4?download=true |
| `mnnit_normal_15.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 15.04s | 13.19s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2815%29.mp4?download=true |
| `mnnit_normal_16.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 21.35s | 18.34s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2816%29.mp4?download=true |
| `mnnit_normal_17.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 98.0% | 23.19s | 21.07s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2817%29.mp4?download=true |
| `mnnit_normal_18.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 98.0% | 4.81s | 2.16s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2818%29.mp4?download=true |
| `mnnit_normal_19.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 4.1s | 2.05s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2819%29.mp4?download=true |
| `mnnit_normal_20.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 4.11s | 1.93s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2820%29.mp4?download=true |
| `mnnit_theft_01.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 98.0% | 9.01s | 6.34s | ACERTO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%281%29.mp4?download=true |
| `mnnit_theft_02.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 12.26s | 9.48s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%282%29.mp4?download=true |
| `mnnit_theft_03.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 4.85s | 2.39s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%283%29.mp4?download=true |
| `mnnit_theft_04.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 5.4s | 2.42s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%284%29.mp4?download=true |
| `mnnit_theft_05.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 5.47s | 2.34s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%285%29.mp4?download=true |
| `mnnit_theft_06.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 5.6s | 2.2s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%286%29.mp4?download=true |
| `mnnit_theft_07.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 6.75s | 4.39s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%287%29.mp4?download=true |
| `mnnit_theft_08.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 6.48s | 3.58s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%288%29.mp4?download=true |
| `mnnit_theft_09.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 98.0% | 5.65s | 2.44s | ACERTO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%289%29.mp4?download=true |
| `mnnit_theft_10.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 98.0% | 20.15s | 17.39s | ACERTO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%2810%29.mp4?download=true |
| `mnnit_theft_11.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 98.0% | 5.76s | 2.58s | ACERTO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%2811%29.mp4?download=true |
| `mnnit_theft_12.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 98.0% | 6.84s | 3.23s | ACERTO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%2812%29.mp4?download=true |
| `mnnit_theft_13.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 5.23s | 2.11s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%2813%29.mp4?download=true |
| `ds2_theft_01.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 6.04s | 2.28s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_0.mp4?download=true |
| `ds2_theft_02.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 5.95s | 2.61s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_1.mp4?download=true |
| `ds2_theft_03.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 4.56s | 2.23s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_2.mp4?download=true |
| `ds2_theft_04.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 4.69s | 2.09s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_3.mp4?download=true |
| `ds2_theft_05.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 6.59s | 4.15s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_4.mp4?download=true |
| `ds2_theft_06.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 6.05s | 2.09s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_5.mp4?download=true |
| `ds2_theft_07.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 6.12s | 3.72s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_6.mp4?download=true |
| `ds2_theft_08.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 6.98s | 4.33s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_7.mp4?download=true |
| `ds2_theft_09.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 5.26s | 2.42s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_8.mp4?download=true |
| `ds2_theft_10.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 4.81s | 2.16s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_9.mp4?download=true |
| `ds2_theft_11.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 5.64s | 2.55s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_10.mp4?download=true |
| `ds2_theft_12.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 14.55s | 11.22s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_11.mp4?download=true |
