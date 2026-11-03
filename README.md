# Sentinela AI - Sistema de Monitoramento CFTV e Prevencao de Perdas (v2.4)

Plataforma inteligente de seguranca eletronica com **Visao Computacional no Edge e IA Multimodal na Nuvem**, desenvolvida para deteccao em tempo real de **furto (shoplifting)**, **invasao de perimetro** e **assalto a caixas**, com zero falsos alarmes em atividades normais de compras.

> **Documentacao Completa para Desenvolvedores e Agentes de IA:**  
> Consulte o arquivo [`CONTEXTO_AGENTE.md`](CONTEXTO_AGENTE.md) para detalhes de arquitetura, fluxo de dados, bateria de testes e guia de commits.

---

## Como Iniciar

Execute o arquivo:
**`iniciar_aplicativo.bat`**

O painel de monitoramento abrira automaticamente no navegador em: **`http://127.0.0.1:5000`**

---

## Modos de Vigilancia

| Modo | Cenario | O que o Sistema Detecta |
|---|---|---|
| **Varejo / Loja** | Mercados, farmacias e lojas de departamento | Gesto suspeito de pegar produto da gondola e ocultar em bolsos, bolsas, mochilas ou sob o casaco/jaqueta. |
| **Perimetro / Muro** | Residencias, quintais, galpoes e acessos | Cerca virtual poligonal desenhada com mouse: invasor pulando muro, cruzando linha restrita ou rondando o local. |
| **Ponto de Venda / Caixa** | Caixas de lojas, recepcoes e balcoes | Assaltos a mao armada, maos levantadas em rendicao ($y_{wrist} < y_{shoulder}$) e invasao da area do operador. |
| **Monitoramento Geral** | Vigilancia Integrada | Monitora simultaneamente os tres tipos de ocorrencia em tempo real. |

---

## Arquitetura Hibrida (Edge + Nuvem)

1. **Rastreamento Local (YOLOv8 + ByteTrack + Pose Detector):**
   * Processamento a 30 FPS no computador local.
   * Rastreia pessoas, caixas delimitadoras e esqueletos anatomicos sem gargalo de rede.
2. **Validacao Rapida por Storyboard Forense (Google Gemini 3.5 Flash Lite):**
   * Ao detectar movimento suspeito, gera uma tira horizontal de 6 fotos consecutivas (**Storyboard JPEG de ~60 KB**) com carimbos cronologicos legiveis.
   * A IA em nuvem avalia a sequencia temporal em **menos de 2 segundos** com veredito pericial.
3. **Custodia Forense e Evidencias:**
   * Cortador automatico de clipes pre e pos-ocorrencia transcodificados para **H.264 (avc1) web-ready com faststart**.
   * Streaming com suporte a Range requests (HTTP 206) para reproducao imediata com barra de rolagem no navegador.
   * Notificacoes sonoras suaves via Web Audio API.

---

## Benchmark Comparativo (Furto Real vs. Compras Normais)

| Video de Teste | Situacao Real | Modo | Classificacao IA | Risco | Confianca |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `furto_real_mercado_01.mp4` | **Furto Real** | Varejo | `FURTO_LOJA` | `ALERTA_MAXIMO` | **99%** |
| `furto_real_gondola_02.mp4` | **Furto Real** | Varejo | `FURTO_LOJA` | `ALERTA_MAXIMO` | **98%** |
| `assalto_furto_02.mp4` | **Furto (Mochila)** | Varejo | `FURTO_LOJA` | `ALERTA_MAXIMO` | **98%** |
| `cliente_normal_compras_04.mp4` | **Normal** | Varejo | `NORMAL` | `NORMAL` | **95%** |
| `atividade_normal_balcao_05.mp4` | **Normal** | Varejo | `NORMAL` | `NORMAL` | **95%** |
| `pedestre_normal_01.mp4` | **Normal** | Geral | `NORMAL` | `NORMAL` | **97%** |

---

## Estrutura do Repositorio

* `iniciar_aplicativo.bat`: Inicializador rapido para ambiente Windows.
* `requirements.txt`: Dependencias Python do projeto.
* `config.json` / `config.example.json`: Configuracoes de hardware e chaves de API.
* `CONTEXTO_AGENTE.md`: Documentacao tecnica completa para outros agentes e desenvolvedores.
* `videos_teste/`: Gravacoes reais de validacao e testes de estresse.
* `evidencias/`: Repositorio de videos de incidentes e relatorios JSON periciais.
* `src/`:
  * `app.py`: Servidor Flask e rotas de streaming e API.
  * `analyzer.py`: Orquestrador central (`SecurityAnalyzer`).
  * `storyboard.py`: Extrator de quadros e integracao com Gemini 3.5.
  * `video_buffer.py`: Cortador de evidencias com FFmpeg H.264.
  * `gesture_engine.py`: Detector de poses e maos em bolsos/mochila.
  * `virtual_fence.py`: Analise de cerca virtual poligonal.
  * `shelf_detector.py`: Monitoramento de zonas de prateleiras/gondolas.
  * `templates/index.html`: Dashboard CCTV corporativo responsivo.
