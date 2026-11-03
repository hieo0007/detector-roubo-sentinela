import os
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
import time
from typing import Optional, List, Callable, Dict, Any, Tuple
import cv2
import numpy as np

from .models import SecurityMode, EventType, RiskLevel, SecurityAnalysisResult
from .gesture_engine import GestureActionEngine
from .virtual_fence import VirtualFence
from .shelf_detector import ShelfZoneDetector
from .storyboard import StoryboardVerifier
from .video_buffer import VideoClipCutter
from .notifier import TelegramNotifier

class SecurityAnalyzer:
    """
    Motor Híbrido Unificado Anti-Roubo, Invasão e Assalto:
    1. Detecção Local em Tempo Real com ByteTrack (IDs persistentes).
    2. Suporte a Zonas de Prateleira (Shelf ROI) para eliminação de falsos positivos de celular.
    3. Cerca Virtual Poligonal com detecção de intrusão e permanência (loitering).
    4. Verificador Inteligente por Storyboard Flash (Gemini 3.5 Flash Lite).
    5. Cortador Automático de Evidências Forenses (Clipe MP4 7s pré/pós-ocorrência).
    6. Despachante de Alertas para Telegram Bot.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.base_dir, "config.json")
        self.snapshots_dir = os.path.join(self.base_dir, "snapshots")
        self.evidencias_dir = os.path.join(self.base_dir, "evidencias")
        os.makedirs(self.snapshots_dir, exist_ok=True)
        os.makedirs(self.evidencias_dir, exist_ok=True)

        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or self._load_key_from_config()
        self.client = None
        self.yolo_model = None
        self.gesture_engine = None
        self.virtual_fence = VirtualFence(name="Perímetro de Segurança")
        self.shelf_detector = ShelfZoneDetector()
        self.storyboard_verifier = StoryboardVerifier(self.snapshots_dir, config_path=self.config_path)
        self.clip_cutter = VideoClipCutter(self.evidencias_dir)
        self.notifier = TelegramNotifier(self.config_path)

        self._init_gemini()
        self._init_yolo()
        self._init_gesture()

    def _load_key_from_config(self) -> Optional[str]:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("gemini_api_key")
            except Exception:
                pass
        return None

    def _init_gemini(self):
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                print("[ANALISADOR] [OK] IA Multimodal Gemini 3.5 conectada!")
            except Exception as e:
                print(f"[AVISO] Falha ao conectar Gemini: {e}")
                self.client = None

    def _init_yolo(self):
        try:
            from ultralytics import YOLO
            weights_path = os.path.join(self.base_dir, "yolov8n.pt")
            if not os.path.exists(weights_path):
                weights_path = "yolov8n.pt"
            self.yolo_model = YOLO(weights_path)
            print("[ANALISADOR] [OK] YOLOv8 (Objetos/Pessoas) carregado!")
        except Exception as e:
            print(f"[AVISO] Falha ao carregar YOLOv8: {e}")
            self.yolo_model = None

    def _init_gesture(self):
        try:
            self.gesture_engine = GestureActionEngine()
            print("[ANALISADOR] [OK] Motor de Gestos com ByteTrack carregado!")
        except Exception as e:
            print(f"[AVISO] Falha ao carregar Motor de Gestos: {e}")
            self.gesture_engine = None

    def set_api_key(self, key: str):
        self.api_key = key
        try:
            config = {}
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
            config["gemini_api_key"] = key
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
        except Exception:
            pass
        self._init_gemini()

    def set_fence_polygon(self, points: List[Tuple[float, float]]):
        self.virtual_fence.set_polygon(points)

    def set_shelf_zones(self, zones: List[List[Tuple[float, float]]]):
        self.shelf_detector.set_zones(zones)
        if self.gesture_engine:
            self.gesture_engine.shelf_detector.set_zones(zones)

    def analyze_clip(
        self,
        video_path: str,
        mode: SecurityMode = SecurityMode.ALL,
        fence_points: Optional[List[Tuple[float, float]]] = None,
        shelf_zones: Optional[List[List[Tuple[float, float]]]] = None,
        progress_callback: Optional[Callable[[float, int, int, str], None]] = None,
        prompt_version: str = "v3"
    ) -> SecurityAnalysisResult:
        """
        Executa o pipeline inteligente completo:
        1. Varredura local com ByteTrack (IDs únicos), Cerca Virtual e Zonas de Prateleira.
        2. Extração instantânea de Storyboard no momento crítico.
        3. Verificação com IA Gemini 3.5 Flash Lite sob demanda.
        4. Corte automático do clipe de evidência (7s) e despacho para o Telegram.
        """
        def update_progress(pct: float, cur: int, tot: int, msg: str):
            if progress_callback:
                try:
                    progress_callback(pct, cur, tot, msg)
                except Exception:
                    pass

        if not os.path.exists(video_path):
            update_progress(100.0, 0, 0, "Erro: Arquivo não encontrado")
            return SecurityAnalysisResult(
                evento_detectado=False,
                modo_analise=mode,
                tipo_evento=EventType.NORMAL,
                nivel_risco=RiskLevel.NORMAL,
                confianca=0.0,
                descricao_acao="Arquivo de vídeo não encontrado no disco.",
                recomendacao_acao="Verifique se o caminho do vídeo está correto."
            )

        if fence_points and len(fence_points) >= 3:
            self.set_fence_polygon(fence_points)

        if shelf_zones:
            self.set_shelf_zones(shelf_zones)

        update_progress(5.0, 0, 100, "Iniciando varredura com ByteTrack...")

        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
        duration = total_frames / fps
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 360
        cap.release()

        detected_objects = set()
        surrender_events = []      # timestamps de rendição
        intrusion_events = []      # timestamps de invasão de cerca
        shoplifting_events = []    # timestamps de furto com prateleira

        step = max(1, int(fps * 0.5))
        cap = cv2.VideoCapture(video_path)
        frame_idx = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % step == 0:
                sec = round(frame_idx / fps, 1)

                # 1. Análise de Gestos com ByteTrack e Prateleira
                telemetry = {}
                if self.gesture_engine:
                    try:
                        _, telemetry = self.gesture_engine.analyze_frame(
                            frame,
                            draw_overlay=False,
                            imgsz=320,
                            current_sec=sec,
                            enable_tracking=True
                        )
                        if telemetry.get("is_surrender"):
                            surrender_events.append(sec)
                        if telemetry.get("is_shoplifting_suspicious"):
                            shoplifting_events.append(sec)
                    except Exception:
                        pass

                # 2. Análise de Cerca Virtual
                if mode in [SecurityMode.ALL, SecurityMode.PERIMETER]:
                    persons = telemetry.get("persons", [])
                    for p in persons:
                        kpts = p.get("keypoints")
                        invaded, _ = self.virtual_fence.check_intrusion(None, kpts, w, h)
                        if invaded:
                            intrusion_events.append(sec)
                            break

                # 3. Rastreamento de Objetos (YOLOv8)
                if self.yolo_model:
                    try:
                        target_classes = [0, 24, 26, 28, 43, 67, 76]
                        res = self.yolo_model.predict(frame, classes=target_classes, imgsz=320, verbose=False, conf=0.3)
                        for r in res:
                            for c in r.boxes.cls:
                                detected_objects.add(self.yolo_model.names[int(c)])
                    except Exception:
                        pass

                pct = 5.0 + (frame_idx / total_frames) * 55.0
                update_progress(pct, frame_idx, total_frames, f"Rastreando indivíduos e zonas ({frame_idx}/{total_frames})...")

            frame_idx += 1
        cap.release()

        update_progress(65.0, total_frames, total_frames, "Verificando evidências com Storyboard...")

        # Escolhe o momento chave
        key_sec = 0.0
        if mode == SecurityMode.PERIMETER and intrusion_events:
            key_sec = intrusion_events[0]
        elif mode == SecurityMode.ROBBERY and surrender_events:
            key_sec = surrender_events[0]
        elif mode == SecurityMode.SHOPLIFTING and shoplifting_events:
            key_sec = shoplifting_events[0]
        elif surrender_events:
            key_sec = surrender_events[0]
        elif intrusion_events:
            key_sec = intrusion_events[0]
        elif shoplifting_events:
            key_sec = shoplifting_events[0]
        else:
            key_sec = duration * 0.5

        # Gera Storyboard de 5 quadros no momento crítico
        img_bytes, sb_path = self.storyboard_verifier.generate_storyboard(
            video_path=video_path,
            num_frames=5,
            target_sec=key_sec if (surrender_events or intrusion_events or shoplifting_events) else None
        )

        storyboard_rel_url = None
        if sb_path:
            storyboard_rel_url = f"/api/snapshots/storyboards/{os.path.basename(sb_path)}"

        # Etapa 3: Verificação com IA Gemini 3.5 (se disponível)
        if self.client and img_bytes:
            update_progress(75.0, total_frames, total_frames, "Consultando verificador analítico...")
            t_ai_start = time.time()
            ai_result = self.storyboard_verifier.verify_with_ai(self.client, img_bytes, mode=mode, prompt_version=prompt_version)
            ai_result.tempo_ia_segundos = round(time.time() - t_ai_start, 2)
            ai_result.storyboard_url = storyboard_rel_url

            # Se a IA falhou ou retornou erro, aciona o laudo de reserva do motor local
            if ai_result.erro or not ai_result.ia_respondeu or ai_result.tipo_evento == EventType.ERRO_ANALISE:
                print(f"[ANALISADOR] [ALERTA] Falha na comunicacao ou resposta invalida da IA: {ai_result.erro_detalhe or ai_result.descricao_acao}")
                print("[ANALISADOR] [CONTINGENCIA] Acionando laudo de reserva do motor local...")
                update_progress(85.0, total_frames, total_frames, "Falha na IA - Ativando laudo local de contingencia...")
                local_result = self._evaluate_local(
                    mode=mode,
                    surrender_events=surrender_events,
                    intrusion_events=intrusion_events,
                    shoplifting_events=shoplifting_events,
                    detected_objects=detected_objects,
                    duration=duration,
                    storyboard_url=storyboard_rel_url
                )
                local_result.erro = True
                local_result.ia_respondeu = False
                local_result.tempo_ia_segundos = ai_result.tempo_ia_segundos
                local_result.erro_detalhe = ai_result.erro_detalhe or ai_result.descricao_acao
                if not local_result.evento_detectado:
                    local_result.nivel_risco = RiskLevel.SUSPEITO
                    local_result.confianca = 0.0
                local_result.descricao_acao = f"[AVISO: Falha na IA - Laudo local de contingencia] {local_result.descricao_acao}"
                final_result = self._finalize_result(local_result, video_path, sb_path)
                update_progress(100.0, total_frames, total_frames, "Concluido com laudo local de contingencia.")
                return final_result

            for obj in detected_objects:
                if obj not in ai_result.itens_envolvidos:
                    ai_result.itens_envolvidos.append(f"{obj} (rastreado)")

            if mode in [SecurityMode.ALL, SecurityMode.PERIMETER] and len(intrusion_events) >= 2:
                if ai_result.tipo_evento == EventType.NORMAL:
                    ai_result.evento_detectado = True
                    ai_result.tipo_evento = EventType.INVASAO_PERIMETRO
                    ai_result.nivel_risco = RiskLevel.ALERTA_MAXIMO
                    ai_result.descricao_acao = f"Invasão confirmada da cerca virtual nos segundos {intrusion_events[:3]}."
                    ai_result.timestamp_segundo = intrusion_events[0]

            if mode in [SecurityMode.ALL, SecurityMode.ROBBERY] and len(surrender_events) >= 2:
                if ai_result.tipo_evento != EventType.ASSALTO_RENDICAO:
                    ai_result.evento_detectado = True
                    ai_result.tipo_evento = EventType.ASSALTO_RENDICAO
                    ai_result.nivel_risco = RiskLevel.ALERTA_MAXIMO
                    ai_result.descricao_acao = "Postura explícita de rendição com mãos para cima detectada pelo esqueleto."
                    ai_result.timestamp_segundo = surrender_events[0]

            final_result = self._finalize_result(ai_result, video_path, sb_path)
            update_progress(100.0, total_frames, total_frames, "Análise concluída com sucesso!")
            return final_result

        # Fallback Local (Offline)
        update_progress(85.0, total_frames, total_frames, "Gerando laudo do motor local...")
        local_result = self._evaluate_local(
            mode=mode,
            surrender_events=surrender_events,
            intrusion_events=intrusion_events,
            shoplifting_events=shoplifting_events,
            detected_objects=detected_objects,
            duration=duration,
            storyboard_url=storyboard_rel_url
        )
        local_result.ia_respondeu = False
        local_result.erro = False
        final_result = self._finalize_result(local_result, video_path, sb_path)
        update_progress(100.0, total_frames, total_frames, "Análise local concluída com sucesso!")
        return final_result

    def _finalize_result(
        self,
        result: SecurityAnalysisResult,
        video_path: str,
        sb_path: Optional[str]
    ) -> SecurityAnalysisResult:
        """Gera timeline, corta clipe de evidência forense de 7s e envia alerta via Telegram."""
        result.timeline = self._build_timeline(video_path, result)

        if result.evento_detectado and result.timestamp_segundo > 0:
            clip_path = self.clip_cutter.extract_incident_clip(
                input_video_path=video_path,
                incident_sec=result.timestamp_segundo,
                pre_sec=3.0,
                post_sec=4.0
            )
            if clip_path:
                result.clip_url = f"/videos/{os.path.basename(clip_path)}"

            # Dispara alerta para Telegram se configurado
            self.notifier.send_alert(
                event_type=result.tipo_evento.value,
                risk_level=result.nivel_risco.value,
                description=result.descricao_acao,
                timestamp_sec=result.timestamp_segundo,
                image_path=sb_path
            )

        return result

    def _evaluate_local(
        self,
        mode: SecurityMode,
        surrender_events: List[float],
        intrusion_events: List[float],
        shoplifting_events: List[float],
        detected_objects: set,
        duration: float,
        storyboard_url: Optional[str]
    ) -> SecurityAnalysisResult:
        is_breach = False
        event_type = EventType.NORMAL
        risk = RiskLevel.NORMAL
        conf = 85.0
        sec = 0.0
        desc = "Ambiente monitorado sem anomalias críticas detectadas pelo motor local."
        recom = "Manter monitoramento rotineiro ativo."

        if mode in [SecurityMode.ALL, SecurityMode.ROBBERY] and len(surrender_events) >= 2:
            is_breach = True
            event_type = EventType.ASSALTO_RENDICAO
            risk = RiskLevel.ALERTA_MAXIMO
            conf = 85.0
            sec = surrender_events[0]
            desc = "Rendição identificada: Indivíduo com mãos elevadas acima dos ombros de forma continuada."
            recom = "Acionar alarme silencioso e polícia imediatamente."
        elif mode in [SecurityMode.ALL, SecurityMode.PERIMETER] and len(intrusion_events) >= 2:
            is_breach = True
            event_type = EventType.INVASAO_PERIMETRO
            risk = RiskLevel.ALERTA_MAXIMO
            conf = 85.0
            sec = intrusion_events[0]
            desc = "Violação de Perímetro: Indivíduo cruzou a cerca virtual restrita."
            recom = "Verificar o setor invadido e acionar refletores/sirene perimetral."
        elif mode in [SecurityMode.ALL, SecurityMode.SHOPLIFTING] and len(shoplifting_events) >= 2:
            is_breach = True
            event_type = EventType.FURTO_LOJA
            risk = RiskLevel.ALERTA_MAXIMO
            conf = 85.0
            sec = shoplifting_events[0]
            desc = "Subtração detectada: Mão interagiu com prateleira de produtos e ocultou item em roupas/bolso."
            recom = "Acionar fiscal de salão para monitoramento do indivíduo."

        return SecurityAnalysisResult(
            evento_detectado=is_breach,
            modo_analise=mode,
            tipo_evento=event_type,
            nivel_risco=risk,
            confianca=conf,
            descricao_acao=desc,
            timestamp_segundo=sec,
            itens_envolvidos=list(detected_objects),
            recomendacao_acao=recom,
            storyboard_url=storyboard_url,
            erro=False,
            ia_respondeu=False
        )

    def _build_timeline(self, video_path: str, result: SecurityAnalysisResult) -> List[Dict[str, Any]]:
        timeline = []
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
        duration = total_frames / fps
        cap.release()

        sec_crime = result.timestamp_segundo
        is_crime = result.evento_detectado

        steps_def = [
            {"sec": 0.5, "title": "01. Início do Monitoramento", "icon": "fa-camera", "desc": "Câmera ativa rastreando área de interesse e pedestres."},
            {"sec": max(1.0, sec_crime * 0.5 if is_crime else duration * 0.4), "title": "02. Circulação & Análise de Intenção", "icon": "fa-person-walking", "desc": "Mapeamento contínuo de esqueleto e interação corporal."},
            {"sec": sec_crime if is_crime else duration * 0.8, "title": "03. Ponto Crítico da Ação" if is_crime else "03. Situação Normal", "icon": "fa-triangle-exclamation" if is_crime else "fa-circle-check", "desc": result.descricao_acao},
            {"sec": min(duration - 0.2, sec_crime + 2.0 if is_crime else duration * 0.95), "title": "04. Conclusão & Desfecho", "icon": "fa-shield-halved", "desc": result.recomendacao_acao}
        ]

        for s in steps_def:
            s_time = float(s["sec"])
            status = "alert" if (is_crime and abs(s_time - sec_crime) < 1.5) else "normal"
            timeline.append({
                "sec": round(s_time, 1),
                "title": s["title"],
                "status": status,
                "icon": s["icon"],
                "desc": s["desc"]
            })

        return timeline

# Alias de compatibilidade
TheftAnalyzer = SecurityAnalyzer
