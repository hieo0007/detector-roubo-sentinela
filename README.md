# 🛡️ Sentinela AI — Sistema de Monitoramento CFTV e Prevenção de Perdas (v2.4)

Plataforma inteligente de segurança eletrônica com **Visão Computacional no Edge e IA Multimodal na Nuvem**, desenvolvida para detecção em tempo real de **furto (shoplifting)**, **invasão de perímetro** e **assalto a caixas**, com zero falsos alarmes em atividades normais de compras.

> 📄 **Documentação Completa para Desenvolvedores e Agentes de IA:**  
> Consulte o arquivo [`CONTEXTO_AGENTE.md`](CONTEXTO_AGENTE.md) para detalhes de arquitetura, fluxo de dados, bateria de testes e guia de commits.

---

## 🚀 Como Iniciar

Dê um duplo clique no arquivo executável:
👉 **`iniciar_aplicativo.bat`**

O painel de monitoramento abrirá automaticamente no navegador em: **`http://127.0.0.1:5000`**

---

## 🎯 Modos de Vigilância

| Modo | Cenário | O que o Sistema Detecta |
|---|---|---|
| 🛒 **Varejo / Loja** | Mercados, farmácias e lojas de departamento | Gesto suspeito de pegar produto da gôndola e ocultar em bolsos, bolsas, mochilas ou sob o casaco/jaqueta. |
| 🏡 **Perímetro / Muro** | Residências, quintais, galpões e acessos | Cerca virtual poligonal desenhada com mouse: invasor pulando muro, cruzando linha restrita ou rondando o local. |
| 💰 **Ponto de Venda / Caixa** | Caixas de lojas, recepções e balcões | Assaltos à mão armada, mãos levantadas em rendição ($y_{wrist} < y_{shoulder}$) e invasão da área do operador. |
| 🛡️ **Monitoramento Geral** | Vigilância Integrada | Monitora simultaneamente os três tipos de ocorrência em tempo real. |

---

## 🧠 Arquitetura Híbrida (Edge + Nuvem)

1. **Rastreamento Local (YOLOv8 + ByteTrack + Pose Detector):**
   * Processamento a 30 FPS no computador local.
   * Rastreia pessoas, caixas delimitadoras e esqueletos anatômicos sem gargalo de rede.
2. **Validação Rápida por Storyboard Forense (Google Gemini 3.5 Flash Lite):**
   * Ao detectar movimento suspeito, gera uma tira horizontal de 6 fotos consecutivas (**Storyboard JPEG de ~60 KB**) com carimbos cronológicos legíveis.
   * A IA em nuvem avalia a sequência temporal em **menos de 2 segundos** com veredito pericial.
3. **Custódia Forense e Evidências:**
   * Cortador automático de clipes pré e pós-ocorrência transcodificados para **H.264 (avc1) web-ready com faststart**.
   * Streaming com suporte a Range requests (HTTP 206) para reprodução imediata com barra de rolagem no navegador.
   * Notificações sonoras suaves via Web Audio API.

---

## 📊 Benchmark Comparativo (Furto Real vs. Compras Normais)

| Vídeo de Teste | Situação Real | Modo | Classificação IA | Risco | Confiança |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `furto_real_mercado_01.mp4` | **Furto Real** | Varejo | `FURTO_LOJA` | `ALERTA_MAXIMO` | **99%** |
| `furto_real_gondola_02.mp4` | **Furto Real** | Varejo | `FURTO_LOJA` | `ALERTA_MAXIMO` | **98%** |
| `assalto_furto_02.mp4` | **Furto (Mochila)** | Varejo | `FURTO_LOJA` | `ALERTA_MAXIMO` | **98%** |
| `cliente_normal_compras_04.mp4` | **Normal** | Varejo | `NORMAL` | `NORMAL` | **95%** |
| `atividade_normal_balcao_05.mp4` | **Normal** | Varejo | `NORMAL` | `NORMAL` | **95%** |
| `pedestre_normal_01.mp4` | **Normal** | Geral | `NORMAL` | `NORMAL` | **97%** |

---

## 📁 Estrutura do Repositório

* `iniciar_aplicativo.bat`: Inicializador rápido para ambiente Windows.
* `requirements.txt`: Dependências Python do projeto.
* `config.json` / `config.example.json`: Configurações de hardware e chaves de API.
* `CONTEXTO_AGENTE.md`: Documentação técnica completa para outros agentes e desenvolvedores.
* `videos_teste/`: Gravações reais de validação e testes de estresse.
* `evidencias/`: Repositório de vídeos de incidentes e relatórios JSON periciais.
* `src/`:
  * `app.py`: Servidor Flask e rotas de streaming e API.
  * `analyzer.py`: Orquestrador central (`SecurityAnalyzer`).
  * `storyboard.py`: Extrator de quadros e integração com Gemini 3.5.
  * `video_buffer.py`: Cortador de evidências com FFmpeg H.264.
  * `gesture_engine.py`: Detector de poses e mãos em bolsos/mochila.
  * `virtual_fence.py`: Análise de cerca virtual poligonal.
  * `shelf_detector.py`: Monitoramento de zonas de prateleiras/gôndolas.
  * `templates/index.html`: Dashboard CCTV corporativo responsivo.
