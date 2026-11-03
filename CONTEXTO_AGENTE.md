# CONTEXTO DE ENGENHARIA PARA AGENTES E DESENVOLVEDORES (HANDOFF)
> **Data do Handoff:** Novembro de 2026  
> **Sistema:** Sentinela CCTV AI — Monitoramento Inteligente e Prevenção de Perdas (v2.4)  
> **Status Operacional:** Estável e Coberto por Testes Automatizados (pytest)

Este documento foi elaborado para que **qualquer outro agente autônomo (Claude Code, Antigravity, Codex)** ou engenheiro de software **sem nenhum contexto prévio** possa compreender imediatamente a arquitetura, o estado atual do projeto, os testes executados, a estrutura de código e como continuar o desenvolvimento sem retrabalho.

---

## 1. Visão Geral do Produto e Problema Resolvido

O **Sentinela CCTV** é uma plataforma de monitoramento de segurança eletrônica com foco em **prevenção de perdas (loss prevention)** e **resposta a incidentes em tempo real**.

### O Problema dos Sistemas Tradicionais:
1. **Falsos Positivos Constantes:** Detectores puramente geométricos ou de movimento disparam alarmes com clientes pegando produtos para olhar, pedestres na calçada ou funcionários trabalhando.
2. **Latência Inaceitável:** Enviar vídeos pesados (30-50 MB) para modelos de nuvem tradicionais demora de 40 a 60 segundos por clipe, inviabilizando qualquer intervenção em tempo real.
3. **Reprodução Falha em Navegadores:** Gravações de CFTV em codecs brutos (como `mp4v` do OpenCV) travam em tela preta (0:00) nos navegadores modernos.

### A Solução Implementada (Arquitetura Híbrida Edge + Nuvem):
* **No Edge (Amostragem a cada 0.5s):** Rastreamento de pessoas com **YOLOv8 + ByteTrack**, estimativa de pose anatômica (mãos, ombros, quadris) e polígonos vetoriais de cerca virtual e prateleiras.
* **Na Nuvem (Verificação Multimodal sob Demanda):** Quando um padrão de interesse ocorre, o sistema gera um **Storyboard Forense Temporal** (tira JPEG horizontal ultra-leve de 6 quadros em 480x270 com carimbos `T=Xs`, ~60 KB) e envia ao **Google Gemini 3.5 Flash Lite**. A IA analisa a intencionalidade da ação e retorna o diagnóstico com precisão cirúrgica.
* **Custódia Forense Imediata:** Clipes de evidência cortados automaticamente (pré e pós-ocorrência) transcodificados para **H.264 (avc1) web-ready com faststart**, permitindo streaming com suporte a HTTP 206 (Range requests).

---

## 2. Modos de Vigilância Suportados

| Modo (`SecurityMode`) | Valor API | Foco da Análise | Ocorrência Monitorada |
| :--- | :--- | :--- | :--- |
| **Varejo / Loja** | `LOJA` | Gôndolas, prateleiras e balcões | Ocultação de produtos em bolsos, bolsas, mochilas ou sob roupas/jaquetas (`FURTO_LOJA`). |
| **Perímetro / Muro** | `PERIMETRO` | Portões, pátios, calçadas e muros | Invasão de polígono de cerca virtual, loitering e escalada (`INVASAO_PERIMETRO`). |
| **Ponto de Venda** | `ASSALTO` | Caixa registradora e atendimento | Assaltos à mão armada, agressão, mãos erguidas em rendição e invasão brusca do caixa (`ASSALTO_RENDICAO`). |
| **Monitoramento Geral** | `TODOS` | Todas as áreas simultaneamente | Varredura global dos 3 cenários de risco com priorização dinâmica. |

---

## 3. Estado Atual do Projeto (Fase e Entregas Concluídas)

O projeto está na **versão v2.4 estável**. As seguintes funcionalidades estão 100% implementadas e funcionais:

1. **Dashboard Web Minimalista Enterprise:**
   * Design escuro matte (zinc/titanium estilo Verkada/Linear), sem cores neon agressivas ou emojis na interface.
   * Layout dividido em grade 8/4: visualização do feed principal com telemetria visual na esquerda e painel de diagnóstico operacional, risco e linha do tempo na direita.
2. **Calibração Espacial Interativa (Mouse Drawing):**
   * Ferramenta de desenho vetorial no próprio canvas do vídeo para o operador traçar polígonos de cerca virtual com o mouse.
   * Presets rápidos: Cerca Inferior, Cerca Caixa, Prateleira Lateral e Prateleira Mesa.
3. **Notificação Sonora Cristalina:**
   * Síntese de áudio via **Web Audio API** do navegador (chime suave de dois tons senoidais em 880Hz e 1318Hz). Sem dependência de avisos sonoros do sistema operacional (Windows Beep).
4. **Player de Evidências Web com Scrubbing:**
   * Servidor Flask com suporte nativo a `Range: bytes` (HTTP 206 Partial Content), permitindo avançar e retroceder os clipes de infração diretamente no navegador.
5. **Prompt Pericial Refinado:**
   * Diretrizes periciais estritas em `storyboard.py` que diferenciam organização legítima de itens pessoais versus subtração e ocultação de bens corporativos em mochilas e bolsos.

---

## 4. Mapa da Estrutura de Código

```
detector_roubo/
│
├── config.json                     # Configuração ativa local (chaves e câmera)
├── config.example.json             # Modelo seguro para clonagem
├── requirements.txt                # Dependências Python homologadas
├── iniciar_aplicativo.bat          # Inicializador 1-clique (porta 5000)
├── README.md                       # Documentação geral de apresentação
├── CONTEXTO_AGENTE.md              # Este documento de handoff técnico
│
├── evidencias/                     # Clipes MP4 H.264 e laudos JSON salvos
├── snapshots/                      # Instantâneos e storyboards temporais
├── videos_teste/                   # Banco de vídeos de validação e benchmark
│
└── src/
    ├── app.py                      # Servidor Flask, APIs REST e streaming
    ├── analyzer.py                 # Orquestrador central (SecurityAnalyzer)
    ├── storyboard.py               # Extrator de Storyboard e cliente Gemini 3.5
    ├── video_buffer.py             # Cortador de clipes forenses com FFmpeg H.264
    ├── gesture_engine.py           # Análise de poses e correlação de membros
    ├── shelf_detector.py           # Zonas de gôndolas e interação com mercadoria
    ├── virtual_fence.py            # Polígonos de cerca virtual (Ray Casting)
    ├── alert.py                    # Gerenciador de alarmes e registro em log
    ├── models.py                   # Enums e dataclasses (SecurityMode, EventType, etc.)
    └── templates/
        └── index.html              # Painel CCTV único (Tailwind CSS + Vanilla JS)
```

---

## 5. Resultados de Benchmarks e Testes Realizados

Os testes automatizados com o gabarito oficial (`videos_teste/gabarito.csv`) são executados pelo script unificado `scripts/benchmark.py`, que salva os laudos em `resultados/benchmark_AAAA-MM-DD.json` e `.md`.

* **Data do Último Benchmark:** 2026-11-03
* **Versão Avaliada:** YOLOv8n + Gemini 3.5 Flash Lite
* **Total de Vídeos Válidos Avaliados:** 12 vídeos (5 normais / 7 ocorrências reais)
* **Acurácia Global:** 66,67% (8/12 acertos exatos de classe)
* **Precisão (Precision):** 62,50%
* **Sensibilidade (Recall):** 71,43%
* **Erros de Classe (Crime Detectado com Tipo Errado):** 1 (`roubo_mercado_02.mp4`)
* **Falsos Positivos:** 2 (`cliente_normal_compras_04.mp4` e `atividade_normal_balcao_05.mp4`)
* **Falsos Negativos:** 1 (`roubo_mercado_01.mp4`)
* **Falhas de IA (ERRO_IA):** 0
* **Tempo Médio Total:** 14,90s por vídeo
* **Tempo Médio da Chamada ao Gemini:** 3,60s por chamada
* **Arquivo Fonte:** `resultados/benchmark_2026-11-03.json` e `resultados/benchmark_2026-11-03.md`

Para rodar a bateria oficial de testes:
```bash
python scripts/benchmark.py
```

---

## 6. Como Executar e Testar

### Pré-requisitos
* Python 3.10 ou superior
* Chave de API Google Gemini (definida em `config.json` ou na variável `GEMINI_API_KEY`)

### Instalação de Dependências
```bash
pip install -r requirements.txt
```

### Iniciar o Servidor Web e Interface
```bash
# Opção 1: Via script bat
./iniciar_aplicativo.bat

# Opção 2: Linha de comando direta
python -m src.app
```
Acesse no navegador: **`http://127.0.0.1:5000`**

### Testar Análise via Terminal (Modo Headless / Script)
```python
from src.analyzer import SecurityAnalyzer
from src.models import SecurityMode

analyzer = SecurityAnalyzer()
resultado = analyzer.analyze_clip("videos_teste/furto_real_mercado_01.mp4", mode=SecurityMode.SHOPLIFTING)

print(f"Evento: {resultado.tipo_evento.value}")
print(f"Risco: {resultado.nivel_risco.value}")
print(f"Confiança: {resultado.confianca}%")
print(f"Laudo: {resultado.descricao_acao}")
```

---

## 7. Convenção Recomendada de Commits Git

Caso o projeto seja versionado em repositório Git pelo Claude Code ou por você, recomenda-se adotar o padrão **Conventional Commits** para separar as entregas de forma clara e granular:

1. **`feat(core): pipeline híbrido de visão computacional e storyboard temporal`**  
   Integração do YOLOv8, ByteTrack e StoryboardVerifier com Gemini 3.5.
2. **`feat(ui): dashboard cctv corporativo em tailwind com calibração interativa`**  
   Interface web minimalista, grade responsiva 8/4 e ferramenta de desenho de cercas com o mouse.
3. **`fix(video): transcodificação h264 faststart e streaming http 206 para evidências`**  
   Resolução de travamentos em tela preta no Chrome/Edge com suporte a range requests.
4. **`test(benchmarks): suite de validação comparativa furto vs normal`**  
   Banco de vídeos de teste e testes automatizados de acurácia sem falsos positivos.
5. **`docs: especificação técnica completa e guia de transição de contexto`**  
   `CONTEXTO_AGENTE.md`, `README.md` e `config.example.json`.

---

## 8. Próximos Passos Sugeridos no Backlog

Se forem solicitadas melhorias futuras neste módulo:
* [ ] Conectar fontes de câmera ao vivo via protocolo RTSP diretamente nas configurações (`config.json`).
* [ ] Notificação instantânea via bot do Telegram (código base já existente em `src/notifier.py`).
* [ ] Suporte a múltiplos canais simultâneos (mosaico de 4 câmeras na mesma tela).
