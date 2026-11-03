# Relatório de Benchmark - Sentinela CCTV

- **Data de Execução**: 2026-11-03_2026
- **Rótulo / Tag**: `prompt_novo`
- **Versão do Prompt**: `v3`
- **Versão do Modelo**: YOLOv8n + Gemini 3.5 Flash Lite (prompt: v3)
- **Total de Vídeos Válidos Avaliados**: 50
- **Erros de Comunicação / API (ERRO_IA)**: 0 (excluídos das métricas de acurácia)
- **Acurácia Global**: 30.0%
- **Precisão (Precision)**: 4.0%
- **Sensibilidade (Recall)**: 4.0%
- **Erros de Classe (Crime Detectado com Tipo Errado)**: 13
- **Falsos Positivos**: 11
- **Falsos Negativos**: 11
- **Tempo Médio Total por Vídeo**: 4.55s
- **Tempo Médio da Chamada ao Gemini**: 1.8s

## Tabela Detalhada por Cenário

| Arquivo | Esperado | Classificação | Risco | Confiança | Tempo Total (s) | Tempo Gemini (s) | Status | Origem |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `mnnit_normal_01.mp4` | NORMAL | NORMAL | NORMAL | 99.5% | 7.63s | 2.0s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%281%29.mp4?download=true |
| `mnnit_normal_02.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 98.5% | 4.7s | 1.95s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%282%29.mp4?download=true |
| `mnnit_normal_03.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.5% | 4.35s | 1.62s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%283%29.mp4?download=true |
| `mnnit_normal_04.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 5.41s | 2.69s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%284%29.mp4?download=true |
| `mnnit_normal_05.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 3.65s | 1.51s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%285%29.mp4?download=true |
| `mnnit_normal_06.mp4` | NORMAL | NORMAL | NORMAL | 98.5% | 3.88s | 1.58s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%286%29.mp4?download=true |
| `mnnit_normal_07.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 98.5% | 4.37s | 1.58s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%287%29.mp4?download=true |
| `mnnit_normal_08.mp4` | NORMAL | NORMAL | NORMAL | 98.5% | 3.92s | 1.65s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%288%29.mp4?download=true |
| `mnnit_normal_09.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 3.88s | 1.8s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%289%29.mp4?download=true |
| `mnnit_normal_10.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 3.87s | 1.52s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2810%29.mp4?download=true |
| `mnnit_normal_11.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.5% | 4.42s | 1.51s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2811%29.mp4?download=true |
| `mnnit_normal_12.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 99.5% | 4.52s | 1.48s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2812%29.mp4?download=true |
| `mnnit_normal_13.mp4` | NORMAL | NORMAL | NORMAL | 99.5% | 3.4s | 1.51s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2813%29.mp4?download=true |
| `ds2_normal_01.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 5.58s | 1.48s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/normal/shop_lifter_n_1.mp4?download=true |
| `ds2_normal_03.mp4` | NORMAL | NORMAL | NORMAL | 95.5% | 5.05s | 1.54s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/normal/shop_lifter_n_3.mp4?download=true |
| `ds2_normal_06.mp4` | NORMAL | NORMAL | NORMAL | 95.5% | 5.41s | 1.79s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/normal/shop_lifter_n_6.mp4?download=true |
| `ds2_normal_08.mp4` | NORMAL | NORMAL | NORMAL | 98.5% | 5.54s | 2.21s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/normal/shop_lifter_n_8.mp4?download=true |
| `ds2_normal_11.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 5.46s | 1.55s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/normal/shop_lifter_n_11.mp4?download=true |
| `mnnit_normal_14.mp4` | NORMAL | NORMAL | NORMAL | 98.5% | 3.47s | 1.57s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2814%29.mp4?download=true |
| `mnnit_normal_15.mp4` | NORMAL | NORMAL | NORMAL | 95.0% | 3.45s | 1.57s | ACERTO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2815%29.mp4?download=true |
| `mnnit_normal_16.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 4.56s | 1.57s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2816%29.mp4?download=true |
| `mnnit_normal_17.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 99.5% | 3.63s | 1.42s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2817%29.mp4?download=true |
| `mnnit_normal_18.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.5% | 4.73s | 2.15s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2818%29.mp4?download=true |
| `mnnit_normal_19.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 98.5% | 3.62s | 1.51s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2819%29.mp4?download=true |
| `mnnit_normal_20.mp4` | NORMAL | INVASAO_PERIMETRO | ALERTA_MAXIMO | 99.5% | 3.86s | 1.64s | FALSO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Normal/Normal%20%2820%29.mp4?download=true |
| `mnnit_theft_01.mp4` | FURTO_LOJA | NORMAL | NORMAL | 98.5% | 3.82s | 1.94s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%281%29.mp4?download=true |
| `mnnit_theft_02.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 98.5% | 4.35s | 1.66s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%282%29.mp4?download=true |
| `mnnit_theft_03.mp4` | FURTO_LOJA | NORMAL | NORMAL | 98.5% | 4.65s | 2.57s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%283%29.mp4?download=true |
| `mnnit_theft_04.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.5% | 4.48s | 1.63s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%284%29.mp4?download=true |
| `mnnit_theft_05.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 4.39s | 1.55s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%285%29.mp4?download=true |
| `mnnit_theft_06.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 98.5% | 5.49s | 2.45s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%286%29.mp4?download=true |
| `mnnit_theft_07.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.5% | 3.75s | 1.64s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%287%29.mp4?download=true |
| `mnnit_theft_08.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 92.5% | 4.28s | 1.54s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%288%29.mp4?download=true |
| `mnnit_theft_09.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.5% | 3.67s | 1.47s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%289%29.mp4?download=true |
| `mnnit_theft_10.mp4` | FURTO_LOJA | FURTO_LOJA | ALERTA_MAXIMO | 98.5% | 4.57s | 1.77s | ACERTO_POSITIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%2810%29.mp4?download=true |
| `mnnit_theft_11.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 3.75s | 1.63s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%2811%29.mp4?download=true |
| `mnnit_theft_12.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 3.6s | 1.53s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%2812%29.mp4?download=true |
| `mnnit_theft_13.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 3.65s | 1.56s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20-%20MNNIT/Shoplifting/Shoplifting%20%2813%29.mp4?download=true |
| `ds2_theft_01.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.5% | 4.34s | 1.48s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_0.mp4?download=true |
| `ds2_theft_02.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 4.39s | 1.52s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_1.mp4?download=true |
| `ds2_theft_03.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.0% | 3.88s | 1.52s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_2.mp4?download=true |
| `ds2_theft_04.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 95.5% | 4.12s | 1.55s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_3.mp4?download=true |
| `ds2_theft_05.mp4` | FURTO_LOJA | INVASAO_PERIMETRO | ALERTA_MAXIMO | 99.5% | 4.39s | 1.68s | ERRO_CLASSE | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_4.mp4?download=true |
| `ds2_theft_06.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 5.5s | 1.52s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_5.mp4?download=true |
| `ds2_theft_07.mp4` | FURTO_LOJA | NORMAL | NORMAL | 98.5% | 4.12s | 1.42s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_6.mp4?download=true |
| `ds2_theft_08.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 4.31s | 1.54s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_7.mp4?download=true |
| `ds2_theft_09.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 4.83s | 1.59s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_8.mp4?download=true |
| `ds2_theft_10.mp4` | FURTO_LOJA | NORMAL | NORMAL | 98.5% | 4.79s | 1.57s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_9.mp4?download=true |
| `ds2_theft_11.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 5.09s | 1.63s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_10.mp4?download=true |
| `ds2_theft_12.mp4` | FURTO_LOJA | NORMAL | NORMAL | 95.0% | 10.92s | 7.72s | FALSO_NEGATIVO | https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/Shoplifting%20Dataset%202.0/shoplifting/shop_lifter_11.mp4?download=true |
