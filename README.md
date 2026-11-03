# Sentinela

Plataforma inteligente de monitoramento CFTV e prevencao de perdas com visao computacional e IA multimodal.

[Documentacao](CONTEXTO_AGENTE.md) | [Agentes de IA](AGENTS.md) | [Instalacao](#instalacao) | [Inicio Rapido](#inicio-rapido) | [Benchmarks](#benchmarks)

---

### Menu
[Destaques](#destaques) | [Arquitetura](#arquitetura) | [Modos de Operacao](#modos-de-operacao) | [Instalacao](#instalacao) | [Inicio Rapido](#inicio-rapido) | [Benchmarks](#benchmarks) | [API REST](#api-rest) | [Custodia Forense](#custodia-forense) | [Sobre](#sobre)

---

## Destaques

* **Processamento Hibrido Edge-to-Cloud:** Amostragem local a cada 0.5s de gravacao (2 quadros por segundo) com rastreamento de poses e validacao semantica sob demanda na nuvem.
* **Validação Semântica via Storyboard:** O modelo multimodal Gemini 3.5 Flash Lite avalia sequências compostas de quadros-chave sob demanda com telemetria cronológica.
* **Eliminacao de Falsos Positivos:** Distincao pericial entre clientes manuseando itens licitamente versus ocultacao premeditada em mochilas, bolsas ou vestimentas.
* **Calibracao Espacial com o Mouse:** Interface interativa no canvas para tracao de cercas virtuais poligonais em tempo real.
* **Custodia Forense H.264 Automatizada:** Exportacao imediata do clipe da ocorrencia (pre e pos-evento) codificado em H.264 (avc1 + faststart) compativel com navegadores.
* **Streaming Nativo HTTP 206:** Suporte completo a Range requests para navegacao fluida e controle temporal direto no navegador.
* **Auditoria Estruturada:** Emissao de relatorios periciais em JSON indexados com timestamp exato, nivel de risco e recomendacao imediata de seguranca.
* **Privacidade por Design:** Nenhum video continuo e transmitido para servidores externos; apenas storyboards compactados (~60 KB) de incidentes confirmados sao analisados.

---

## Arquitetura

O sistema opera em um modelo hierarquico de 4 camadas:

```
[ Camera CFTV / Fluxo RTSP ]
             |
             v
+-------------------------------------------------------------+
| Nivel 1: Edge Computing Local (1 quadro a cada 0.5s gravado)|
| - Deteccao de Pessoas e Objetos: YOLOv8                     |
| - Rastreamento Temporal Continuo: ByteTrack                 |
| - Estimativa de Poses: YOLOv8-Pose (Membros e Articulacoes) |
| - Analise Geometrica: Ray-Casting em Poligonos de Cerca     |
+-------------------------------------------------------------+
             |
             | [Gatilho de Interesse Detectado]
             v
+-------------------------------------------------------------+
| Nivel 2: Amostragem Temporal Forense                        |
| - Extracao de 6 quadros-chave em resolucao 480x270          |
| - Sobreposicao de metadados temporais legiveis (T=X.Xs)     |
| - Compactacao horizontal em imagem composta JPEG (~60 KB)   |
+-------------------------------------------------------------+
             |
             v
+-------------------------------------------------------------+
| Nivel 3: Validacao Semantica Multimodal (Gemini 3.5 Nuvem)  |
| - Inferencia contextual pericial sob demanda                 |
| - Diferenciacao entre acao rotineira vs. delito patrimonial |
| - Retorno estruturado em JSON com confianca e diretriz      |
+-------------------------------------------------------------+
             |
             v
+-------------------------------------------------------------+
| Nivel 4: Central de Operacoes e Custodia                    |
| - Transcodificacao H.264 Baseline (avc1 + faststart)        |
| - Streaming HTTP 206 (Range requests) no navegador          |
| - Alarme auditivo sintetizado via Web Audio API             |
+-------------------------------------------------------------+
```

---

## Modos de Operacao

| Modo | Identificador | Escopo Monitorado | Regra de Inferencia |
|---|---|---|---|
| **Varejo / Loja** | `LOJA` | Gondolas, prateleiras e balcoes de mercadoria | Retirada de mercadoria seguida de ocultacao deliberada em bolsos, bolsas ou sob vestimentas. |
| **Perimetro / Muro** | `PERIMETRO` | Portões, muros, calçadas e patios externos | Transgressao fisica de linha ou poligono virtual delimitado e permanencia suspeita (loitering). |
| **Ponto de Venda** | `ASSALTO` | Estacoes de caixa e atendimento | Elevacao de membros em rendicao ($y_{wrist} < y_{shoulder}$) e invasao da area restrita do operador. |
| **Monitoramento Geral** | `TODOS` | Planta integral | Varredura continua e simultanea de todos os vetores de risco. |

---

## Instalacao

### Requisitos de Sistema
* **Python:** Versao 3.10 ou superior
* **Sistema Operacional:** Windows 10/11 ou Linux (Ubuntu 22.04 LTS / Debian 12)
* **Credenciais:** Chave de API Google Gemini

### Passo 1: Obter o Codigo e Instalar Dependencias
```bash
git clone https://github.com/hieo0007/detector-roubo-sentinela.git
cd detector-roubo-sentinela
pip install -r requirements.txt
```

### Passo 2: Configuracao
Copie o modelo de configuracao e insira sua chave da API:
```bash
cp config.example.json config.json
```
No arquivo `config.json`, configure sua chave da API Gemini:
```json
{
  "camera": {
    "source": 0,
    "fps": 20,
    "resolution": [1280, 720]
  },
  "gemini_api_key": "SUA_CHAVE_GEMINI_AQUI"
}
```

---

## Inicio Rapido

### No Windows:
Basta executar o script automatizado com duplo clique:
```cmd
iniciar_aplicativo.bat
```

### Via Linha de Comando (Windows / Linux):
```bash
python -m src.app
```

O painel de monitoramento ficara acessivel imediatamente em:
**`http://127.0.0.1:5000`**

### Execucao Programatica (Headless):
```python
from src.analyzer import SecurityAnalyzer
from src.models import SecurityMode

analyzer = SecurityAnalyzer()
resultado = analyzer.analyze_clip("videos_teste/furto_real_mercado_01.mp4", mode=SecurityMode.SHOPLIFTING)

print("Status:", resultado.tipo_evento.value)
print("Confianca:", resultado.confianca)
print("Laudo:", resultado.descricao_acao)
```

---

## Benchmarks

Métricas de acurácia e desempenho medidas em execução real contra o gabarito oficial (`videos_teste/gabarito.csv`), com relatório salvo em `resultados/benchmark_2026-11-03.md`:

* **Data do Último Benchmark:** 2026-11-03
* **Versão Avaliada:** YOLOv8n + Gemini 3.5 Flash Lite (Saída Estruturada JSON)
* **Total de Vídeos Válidos Avaliados:** 12 vídeos (5 normais / 7 ocorrências reais)
* **Acurácia Global:** 50,00% (6/12 acertos exatos de classe)
* **Precisão (Precision):** 50,00%
* **Sensibilidade (Recall):** 42,86%
* **Erros de Classe (Crime Detectado com Tipo Errado):** 1 (`roubo_mercado_02.mp4`)
* **Falsos Positivos:** 2 (`cliente_normal_compras_04.mp4`, `atividade_normal_balcao_05.mp4`)
* **Falsos Negativos:** 3 (`assalto_furto_01.mp4`, `assalto_furto_03.mp4`, `roubo_mercado_01.mp4`)
* **Falhas de IA (ERRO_IA):** 0
* **Tempo Médio Total por Vídeo:** 7,40s
* **Tempo Médio da Chamada ao Gemini:** 2,49s

Para rodar novamente a bateria completa de benchmark e gerar novos relatórios em `resultados/`:

```bash
python scripts/benchmark.py
```

---

## API REST

| Metodo | Rota | Funcao |
|---|---|---|
| `GET` | `/` | Dashboard principal web da central Sentinela |
| `GET` | `/api/config` | Consulta o status da chave Gemini e do bot Telegram |
| `POST` | `/api/config` | Atualiza configuracoes de credenciais e chaves de API |
| `POST` | `/api/telegram/test` | Envia notificacao de teste para o canal Telegram configurado |
| `GET` | `/api/fence` | Retorna as coordenadas vetoriais atuais da cerca perimetral |
| `POST` | `/api/fence` | Define novo poligono de cerca desenhado interativamente |
| `GET` | `/api/shelf` | Retorna as zonas ativas de prateleiras e gondolas |
| `POST` | `/api/shelf` | Atualiza as zonas monitoradas de prateleiras |
| `GET` | `/api/test-videos` | Catalogo de videos de validacao indexados no servidor |
| `POST` | `/api/upload` | Envia novo arquivo de video para a fila de gravacoes |
| `GET` | `/videos/<filename>` | Servico de video com suporte a Range requests (HTTP 206) |
| `GET` | `/video_feed/<filename>` | Fluxo contínuo de video com telemetria e HUD anotado via MJPEG |
| `GET` | `/api/video-info/<filename>` | Retorna duracao, FPS e resolucao da gravacao |
| `POST` | `/api/analyze-async` | Inicia analise assincrona do video e devolve `job_id` |
| `GET` | `/api/progress/<job_id>` | Consulta o status percentual e o resultado final da analise |
| `GET` | `/api/snapshots/storyboards/<filename>` | Serve imagens compostas de storyboards temporais avaliados |
| `GET` | `/snapshots/<filename>` | Serve capturas instantaneas individuais da timeline |

---

## Custodia Forense

Apos a confirmacao de uma ocorrencia:
1. **Isolamento de Janela Temporal:** O sistema recorta automaticamente o intervalo de 3 segundos anteriores e 4 segundos posteriores ao evento critico.
2. **Transcodificacao Automatizada:** O trecho e codificado em H.264 Baseline (`libx264`, `pix_fmt yuv420p`, `-movflags +faststart`).
3. **Geracao de Laudo JSON:** Registro pericial estruturado e salvo em disco com hash de integridade e metadados forenses.

---

## Documentacao para Agentes e Desenvolvedores

Para agentes autonomos de IA (Claude Code, Cursor, Codex) e engenheiros de software:
* **[`AGENTS.md`](AGENTS.md)** / **[`CONTEXTO_AGENTE.md`](CONTEXTO_AGENTE.md)**: Especificacao completa da arquitetura interna, fluxo de estados, mapa de modulos e convencoes de codigo.

---

## Sobre

O Sentinela foi concebido como uma solucao de codigo aberto voltada para reducao de perdas no comercio varejista e protecao patrimonial perimetral, aliando velocidade computacional local a capacidade de compreensao contextual dos modelos fundacionais modernos.

Distribuido sob a licenca MIT. Consulte [`LICENSE`](LICENSE) para termos de uso.
