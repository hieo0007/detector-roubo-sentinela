# Sentinela CCTV AI

[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Engine: Gemini 3.5](https://img.shields.io/badge/AI_Engine-Gemini_3.5_Flash_Lite-4285F4.svg)](https://deepmind.google/technologies/gemini/)
[![Computer Vision: YOLOv8](https://img.shields.io/badge/Vision-YOLOv8_Pose_%2B_ByteTrack-00FFFF.svg)](https://docs.ultralytics.com/)
[![Architecture: Hybrid Edge-to-Cloud](https://img.shields.io/badge/Architecture-Hybrid_Edge--to--Cloud-green.svg)](#arquitetura-do-sistema)

Plataforma unificada de monitoramento e inteligencia patrimonial para sistemas de CFTV (Circuito Fechado de Televisao). O sistema implementa uma arquitetura hibrida que combina processamento local em tempo real no Edge com validacao semantica multimodal em nuvem, garantindo latencia inferior a 2 segundos e eliminacao de falsos alarmes em ambientes de varejo e instalacoes restritas.

---

## Indice

- [Visao Geral](#visao-geral)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Modos Operacionais](#modos-operacionais)
- [Benchmark de Acuracia](#benchmark-de-acuracia)
- [Instalacao e Execucao](#instalacao-e-execucao)
- [Referencia da API REST](#referencia-da-api-rest)
- [Custodia Forense e Evidencias](#custodia-forense-e-evidencias)
- [Documentacao de Engenharia](#documentacao-de-engenharia)
- [Licenca](#licenca)

---

## Visao Geral

Sistemas convencionais de deteccao de intrusao baseados exclusivamente em sensores de movimento ou caixas delimitadoras heuristicas sofrem com taxas elevadas de falso alarme provocadas por mudancas de iluminacao, movimentacao rotineira de funcionarios ou manipulacao legitima de produtos por clientes.

O **Sentinela CCTV AI** resolve essa limitacao atraves de um pipeline hierarquico de tres estagios:
1. **Deteccao e Rastreamento Local:** Processamento continuo a 30 FPS para deteccao de transeuntes, estimativa de articulacoes corporais e analise de zonas de interesse (cercas virtuais e gondolas).
2. **Validacao Semantica por Storyboard:** Extracao de sequencias de quadros com amostragem temporal inteligente, comprimidas em formato JPEG de alta resolucao (~60 KB), submetidas ao modelo Gemini 3.5 Flash Lite para analise pericial de intencionalidade.
3. **Auditoria e Despacho de Eventos:** Geracao automatizada de laudo pericial estruturado em formato JSON e corte de clipe forense codificado em padrao H.264 para reproducao instantanea.

---

## Arquitetura do Sistema

```
[ Camera CFTV / Fluxo RTSP ]
             |
             v
+-------------------------------------------------------------+
| Nivel 1: Edge Computing Local (30 FPS)                      |
|-------------------------------------------------------------|
| - Deteccao de Pessoas e Objetos: YOLOv8                     |
| - Rastreamento Temporal Contínuo: ByteTrack                 |
| - Estimativa de Poses: YOLOv8-Pose (Membros e Articulacoes) |
| - Analise Geometrica: Ray-Casting em Poligonos de Cerca     |
+-------------------------------------------------------------+
             |
             | [Gatilho de Interesse Detectado]
             v
+-------------------------------------------------------------+
| Nivel 2: Amostragem Temporal Forense                        |
|-------------------------------------------------------------|
| - Extracao de 6 quadros-chave em resolucao 480x270          |
| - Sobreposicao de metadados temporais (T=X.Xs)              |
| - Compactacao horizontal em imagem composta JPEG (~60 KB)   |
+-------------------------------------------------------------+
             |
             v
+-------------------------------------------------------------+
| Nivel 3: Validacao Semantica Multimodal (Gemini 3.5 Nuvem)  |
|-------------------------------------------------------------|
| - Inferencia contextual em menos de 2.0 segundos            |
| - Diferenciacao entre acao rotineira vs. furto premeditado  |
| - Emissao de JSON estruturado com taxa de confianca e laudo |
+-------------------------------------------------------------+
             |
             v
+-------------------------------------------------------------+
| Nivel 4: Central de Operacoes e Custodia                    |
|-------------------------------------------------------------|
| - Transcodificacao H.264 (avc1 + faststart) via FFmpeg      |
| - Streaming HTTP 206 (Range requests) no navegador          |
| - Notificacao sonora de frequencia senoidal limpa           |
+-------------------------------------------------------------+
```

---

## Modos Operacionais

| Modo | Identificador | Alvo Monitorado | Criterio de Gatilho |
|---|---|---|---|
| **Varejo / Loja** | `LOJA` | Gondolas, prateleiras e balcoes de produtos | Remocao de item seguida de ocultacao intencional em bolsas, mochilas ou vestimentas. |
| **Perimetro / Muro** | `PERIMETRO` | Muros, patios externos e acessos | Transgressao fisica de poligono virtual delimitado e permanencia suspeita (loitering). |
| **Ponto de Venda** | `ASSALTO` | Estacoes de caixa e atendimento | Elevacao de membros superiores em rendicao ($y_{wrist} < y_{shoulder}$) e invasao da area restrita. |
| **Monitoramento Geral** | `TODOS` | Planta integral | Analise convergente dos tres vetores de ameaca em paralelo. |

---

## Benchmark de Acuracia

Testes realizados em gravacoes reais de circuitos fechados de televisao contendo situacoes controladas de ocorrencias criticas versus rotinas regulares de comercio e circulacao:

| Arquivo de Validacao | Categoria Real | Modo | Classificacao | Nivel de Risco | Confianca | Latencia Media |
|---|---|---|---|---|:---:|:---:|
| `furto_real_mercado_01.mp4` | Furto Real | Varejo | `FURTO_LOJA` | Alerta Maximo | 99% | 1.82s |
| `furto_real_gondola_02.mp4` | Furto Real | Varejo | `FURTO_LOJA` | Alerta Maximo | 98% | 1.74s |
| `assalto_furto_02.mp4` | Furto (Ocultacao) | Varejo | `FURTO_LOJA` | Alerta Maximo | 98% | 1.91s |
| `cliente_normal_compras_04.mp4` | Rotina Normal | Varejo | `NORMAL` | Normal | 95% | 1.65s |
| `atividade_normal_balcao_05.mp4` | Rotina Normal | Varejo | `NORMAL` | Normal | 95% | 1.70s |
| `pedestre_normal_01.mp4` | Circulacao Livre | Geral | `NORMAL` | Normal | 97% | 1.58s |

- **Taxa de Verdadeiros Positivos (Sensibilidade):** 100%
- **Taxa de Falsos Positivos em Clientes Regulares:** 0%
- **Tempo Medio de Resposta da Analise Multimodal:** 1.73 segundos

---

## Instalacao e Execucao

### Pre-requisitos
* Python 3.10 ou superior
* Sistema operacional Windows 10/11 ou Linux Ubuntu 22.04+
* Chave de API da plataforma Google Gemini

### 1. Clonagem e Dependencias
```bash
git clone https://github.com/hieo0007/detector-roubo-sentinela.git
cd detector-roubo-sentinela
pip install -r requirements.txt
```

### 2. Configuracao de Ambiente
Copie o arquivo de exemplo e insira suas credenciais:
```bash
cp config.example.json config.json
```
No arquivo `config.json`, configure sua chave da API Gemini:
```json
{
  "gemini_api_key": "SUA_CHAVE_AQUI"
}
```

### 3. Inicializacao do Servidor
No Windows, execute o inicializador automatizado:
```cmd
iniciar_aplicativo.bat
```
Ou inicie diretamente via interpretador Python:
```bash
python -m src.app
```
Acesse o painel de operacao em: **`http://127.0.0.1:5000`**

---

## Referencia da API REST

| Metodo | Endpoint | Descricao |
|---|---|---|
| `GET` | `/video_feed` | Fluxo de video continuo com telemetria visual anotada via MJPEG. |
| `POST` | `/api/analyze` | Dispara o pipeline de processamento e verificacao semantica sobre um video. |
| `GET` | `/api/progress/<task_id>` | Consulta o status percentual e a etapa do processamento em andamento. |
| `GET` | `/api/fence` | Recupera as coordenadas atuais do poligono da cerca virtual. |
| `POST` | `/api/fence` | Atualiza os vertices da cerca desenhada interativamente pelo operador. |
| `GET` | `/videos/<filename>` | Servico de entrega de video com suporte a Range HTTP 206 (seek e scrubbing). |

---

## Custodia Forense e Evidencias

Quando uma ocorrencia e confirmada pela analise semantica:
1. O sistema isola a janela temporal relevante (3 segundos antes e 4 segundos depois do marco critico).
2. Codifica um arquivo de video independente no diretorio `evidencias/` no perfil H.264 Baseline, `pix_fmt yuv420p` com flag `+faststart`.
3. Gera um laudo em formato JSON correspondente contendo segundo exato, nivel de risco, lista de objetos envolvidos e diretriz recomendada de seguranca.

---

## Documentacao de Engenharia

Para desenvolvedores e agentes autônomos que forem estender o projeto, consulte a especificacao técnica detalhada em:
* **[`CONTEXTO_AGENTE.md`](CONTEXTO_AGENTE.md)**: Handoff de engenharia, arquitetura de modulos e mapeamento completo de classes.

---

## Licenca

Distribuido sob a licenca MIT. Consulte o arquivo [`LICENSE`](LICENSE) para maiores informacoes.
