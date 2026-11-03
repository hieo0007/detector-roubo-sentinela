import os
import io
import json
import re
import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Optional, Dict, Any

from .models import SecurityMode, EventType, RiskLevel, SecurityAnalysisResult

class StoryboardVerifier:
    """
    Gerador e Verificador de Storyboards Temporais Compactos:
    - Extrai 4 a 6 quadros-chave em sequencia continua com carimbos de tempo.
    - Compacta em uma unica imagem JPEG ultra-leve (~60 KB).
    - Envia para o Gemini para verificacao semantica em tempo real.
    """
    def __init__(self, snapshots_dir: str):
        self.snapshots_dir = snapshots_dir
        self.storyboard_dir = os.path.join(snapshots_dir, "storyboards")
        os.makedirs(self.storyboard_dir, exist_ok=True)

    def generate_storyboard(
        self,
        video_path: str,
        num_frames: int = 6,
        target_sec: Optional[float] = None,
        window_sec: float = 4.0,
        output_filename: Optional[str] = None
    ) -> Tuple[Optional[bytes], Optional[str]]:
        """
        Gera uma tira horizontal de quadros-chave do video com carimbos de tempo legiveis.
        Retorna (bytes_jpeg, caminho_arquivo_salvo).
        """
        if not os.path.exists(video_path):
            return None, None

        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
        duration = total_frames / fps

        # Determina os indices de quadros a extrair
        if target_sec is not None and target_sec > 0:
            start_sec = max(0.0, target_sec - (window_sec / 2.0))
            end_sec = min(duration, target_sec + (window_sec / 2.0))
            start_frame = int(start_sec * fps)
            end_frame = min(total_frames - 1, int(end_sec * fps))
            indices = np.linspace(start_frame, end_frame, num_frames, dtype=int)
        else:
            indices = np.linspace(0, max(1, total_frames - 1), num_frames, dtype=int)

        frames = []
        for idx in indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
            ret, frame = cap.read()
            if ret:
                # Resolucao ampliada (480x270) para nitidez visual de maos e objetos
                frame_resized = cv2.resize(frame, (480, 270))
                sec = round(idx / fps, 1)

                # Overlay sutil e limpo com carimbo de tempo
                cv2.rectangle(frame_resized, (6, 6), (95, 28), (18, 18, 22), -1)
                cv2.rectangle(frame_resized, (6, 6), (95, 28), (55, 55, 60), 1)
                cv2.putText(
                    frame_resized,
                    f"T={sec}s",
                    (12, 22),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.48,
                    (220, 220, 225),
                    1,
                    cv2.LINE_AA
                )
                frames.append(cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB))
        cap.release()

        if not frames:
            return None, None

        # Concatena os quadros horizontalmente em uma unica tira cronologica
        storyboard_img = np.hstack(frames)
        pil_img = Image.fromarray(storyboard_img)

        # Salva o arquivo no disco
        if not output_filename:
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            output_filename = f"storyboard_{base_name}_{int(target_sec or 0)}.jpg"

        save_path = os.path.join(self.storyboard_dir, output_filename)
        pil_img.save(save_path, format="JPEG", quality=88)

        buf = io.BytesIO()
        pil_img.save(buf, format="JPEG", quality=88)
        return buf.getvalue(), save_path

    def parse_ai_response(self, raw_text: str, mode: SecurityMode = SecurityMode.ALL) -> SecurityAnalysisResult:
        """
        Valida e desserializa o JSON retornado pela IA usando Pydantic.
        Trata respostas invalidas, campos faltantes ou markdown quebrado como ERRO_ANALISE.
        """
        if not raw_text or not raw_text.strip():
            return SecurityAnalysisResult(
                evento_detectado=False,
                modo_analise=mode,
                tipo_evento=EventType.ERRO_ANALISE,
                nivel_risco=RiskLevel.SUSPEITO,
                confianca=0.0,
                descricao_acao="A IA retornou uma resposta vazia.",
                recomendacao_acao="Verificar o modelo ou repetir o processamento.",
                erro=True,
                erro_detalhe="Resposta da IA vazia",
                ia_respondeu=False
            )

        clean_json = re.sub(r"^```(?:json)?\s*", "", raw_text.strip(), flags=re.MULTILINE)
        clean_json = re.sub(r"\s*```$", "", clean_json, flags=re.MULTILINE).strip()

        try:
            data = json.loads(clean_json)
            if not isinstance(data, dict):
                raise ValueError("O conteudo JSON retornado nao e um objeto.")
        except Exception as e:
            return SecurityAnalysisResult(
                evento_detectado=False,
                modo_analise=mode,
                tipo_evento=EventType.ERRO_ANALISE,
                nivel_risco=RiskLevel.SUSPEITO,
                confianca=0.0,
                descricao_acao=f"Formato JSON invalido retornado pela IA: {e}",
                recomendacao_acao="Verificar a saida gerada pelo modelo.",
                erro=True,
                erro_detalhe=f"Erro ao decodificar JSON: {e}",
                ia_respondeu=False
            )

        # Validacao estrita dos campos com enums
        t_evento_str = data.get("tipo_evento")
        if not t_evento_str or t_evento_str not in [e.value for e in EventType if e != EventType.ERRO_ANALISE]:
            return SecurityAnalysisResult(
                evento_detectado=False,
                modo_analise=mode,
                tipo_evento=EventType.ERRO_ANALISE,
                nivel_risco=RiskLevel.SUSPEITO,
                confianca=0.0,
                descricao_acao=f"Campo 'tipo_evento' ausente ou invalido: '{t_evento_str}'",
                recomendacao_acao="Verificar a consistencia do schema de resposta.",
                erro=True,
                erro_detalhe=f"Tipo de evento invalido: {t_evento_str}",
                ia_respondeu=False
            )

        tipo_evento = EventType(t_evento_str)

        n_risco_str = data.get("nivel_risco")
        if not n_risco_str or n_risco_str not in [r.value for r in RiskLevel]:
            return SecurityAnalysisResult(
                evento_detectado=False,
                modo_analise=mode,
                tipo_evento=EventType.ERRO_ANALISE,
                nivel_risco=RiskLevel.SUSPEITO,
                confianca=0.0,
                descricao_acao=f"Campo 'nivel_risco' ausente ou invalido: '{n_risco_str}'",
                recomendacao_acao="Verificar a consistencia do schema de resposta.",
                erro=True,
                erro_detalhe=f"Nivel de risco invalido: {n_risco_str}",
                ia_respondeu=False
            )

        nivel_risco = RiskLevel(n_risco_str)

        try:
            confianca_val = float(data.get("confianca", 80.0))
            confianca_val = max(0.0, min(100.0, confianca_val))
        except (ValueError, TypeError):
            confianca_val = 50.0

        try:
            ts_sec = float(data.get("segundo_chave", 0.0))
        except (ValueError, TypeError):
            ts_sec = 0.0

        descricao = str(data.get("descricao_acao", "")).strip()
        if not descricao:
            descricao = "Analise pericial estruturada realizada pela IA."

        recomendacao = str(data.get("recomendacao_acao", "Verificar gravacao do setor.")).strip()

        itens = data.get("itens_envolvidos", [])
        if not isinstance(itens, list):
            itens = [str(itens)]

        # Validacao com Pydantic
        try:
            return SecurityAnalysisResult(
                evento_detectado=(tipo_evento != EventType.NORMAL),
                modo_analise=mode,
                tipo_evento=tipo_evento,
                nivel_risco=nivel_risco,
                confianca=confianca_val,
                descricao_acao=descricao,
                timestamp_segundo=ts_sec,
                itens_envolvidos=[str(i) for i in itens],
                recomendacao_acao=recomendacao,
                erro=False,
                ia_respondeu=True
            )
        except Exception as e:
            return SecurityAnalysisResult(
                evento_detectado=False,
                modo_analise=mode,
                tipo_evento=EventType.ERRO_ANALISE,
                nivel_risco=RiskLevel.SUSPEITO,
                confianca=0.0,
                descricao_acao=f"Falha de validacao Pydantic no resultado: {e}",
                recomendacao_acao="Verificar estrutura de dados interna.",
                erro=True,
                erro_detalhe=str(e),
                ia_respondeu=False
            )

    def verify_with_ai(
        self,
        client: Any,
        img_bytes: bytes,
        mode: SecurityMode = SecurityMode.ALL
    ) -> SecurityAnalysisResult:
        """
        Envia o storyboard para a IA Gemini para verificacao pericial rapida e rigorosa.
        Retorna SecurityAnalysisResult com erro=True caso ocorra falha na chamada.
        """
        from google.genai import types

        prompt = f"""Você é um perito sênior em segurança patrimonial, prevenção de perdas e análise forense de CFTV.
Analise com atenção minuciosa aos detalhes a sequência contínua de quadros (storyboard com carimbos de tempo T=Xs).

FOCO PRIORITÁRIO DA CÂMERA: {mode.value}

Categorias de Classificação:
1. FURTO_LOJA:
   - Qualquer indivíduo pegando, subtraindo ou manipulando produtos, caixas ou objetos de mesas/prateleiras/expositores e colocando discretamente dentro de mochilas, bolsas pessoais, bolsos traseiros/dianteiros da calça ou sob casacos/jaquetas para ocultar.
   - Mesmo em ambientes de escritório ou balcão, a subtração de itens para dentro de mochilas/bolsos DEVE ser classificada como FURTO_LOJA (Risco ALERTA_MAXIMO ou SUSPEITO).
2. INVASAO_PERIMETRO: Indivíduo pulando muro/portão, forçando portas, transitando em calçadas/pátios em área de cerca restrita.
3. ASSALTO_RENDICAO: Ameaça ostensiva com armas, facas ou agressão, mãos erguidas em rendição, invasão brusca da área do operador do caixa.
4. NORMAL: Pessoas caminhando pacificamente com mãos visíveis, clientes retirando itens da prateleira e colocando na cesta/carrinho aberto para pagamento, operadores trabalhando rotineiramente sem ocultação de objetos.

Regras de Decisão Forense:
- Observe as mãos e os braços em cada quadro: para onde vai o objeto retirado da mesa/prateleira? Se o objeto sumiu para dentro de uma mochila, casaco ou bolso, é FURTO_LOJA.
- Independentemente do foco prioritário ({mode.value}), se houver furto evidente ou ocultação de itens, acione FURTO_LOJA imediatamente.
- Se for atividade regular pacífica de compras ou circulação livre, classifique como NORMAL.

Retorne EXCLUSIVAMENTE um objeto JSON válido:
{{
  "tipo_evento": "NORMAL" | "FURTO_LOJA" | "INVASAO_PERIMETRO" | "ASSALTO_RENDICAO",
  "nivel_risco": "NORMAL" | "SUSPEITO" | "ALERTA_MAXIMO",
  "confianca": 80 a 99,
  "descricao_acao": "detalhamento pericial preciso da conduta observada nos quadros",
  "segundo_chave": número em segundos exato do movimento crítico,
  "itens_envolvidos": ["objeto", "mochila"],
  "recomendacao_acao": "diretriz imediata de segurança patrimonial"
}}
"""
        try:
            resp = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=[
                    types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
                    prompt
                ]
            )
            raw_text = getattr(resp, "text", "") or ""
            return self.parse_ai_response(raw_text, mode=mode)
        except Exception as e:
            print(f"[STORYBOARD] [ERRO] Falha ao comunicar com IA Gemini: {e}")
            return SecurityAnalysisResult(
                evento_detectado=False,
                modo_analise=mode,
                tipo_evento=EventType.ERRO_ANALISE,
                nivel_risco=RiskLevel.SUSPEITO,
                confianca=0.0,
                descricao_acao=f"Falha na comunicação com IA Gemini: {e}",
                recomendacao_acao="Verificar conexão com a internet ou chave de API.",
                erro=True,
                erro_detalhe=str(e),
                ia_respondeu=False
            )
