import os
import sys
import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional, Any

from .shelf_detector import ShelfZoneDetector

class GestureActionEngine:
    """
    Motor Avançado de Gestos e Comportamentos Suspeitos com Rastreamento Persistente (ByteTrack):
    - Rastreia cada indivíduo com um ID único (ex: ID 1, ID 2) contínuo através dos quadros.
    - Integração com Detector de Prateleira (ShelfZoneDetector):
      Descarta movimentos normais em bolsos a menos que o indivíduo tenha tocado
      em uma prateleira de produtos nos últimos 4.5 segundos.
    - Detecção de Rendição / Mãos Elevadas com histórico de persistência.
    """
    def __init__(self, weights_path: Optional[str] = None):
        from ultralytics import YOLO
        if not weights_path:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            weights_path = os.path.join(base_dir, "yolov8n-pose.pt")
            if not os.path.exists(weights_path):
                weights_path = "yolov8n-pose.pt"
        self.model = YOLO(weights_path)

        # Histórico temporal por ID para persistência
        self.surrender_counter: Dict[int, int] = {}
        self.shelf_detector = ShelfZoneDetector()

    def analyze_frame(
        self,
        frame: np.ndarray,
        draw_overlay: bool = True,
        imgsz: int = 384,
        current_sec: float = 0.0,
        enable_tracking: bool = True
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Processa o frame com ByteTrack e telemetria comportamental por ID.
        """
        h, w = frame.shape[:2]

        if enable_tracking:
            try:
                results = self.model.track(frame, persist=True, tracker="bytetrack.yaml", imgsz=imgsz, verbose=False, conf=0.3)
            except Exception:
                results = self.model.predict(frame, imgsz=imgsz, verbose=False, conf=0.3)
        else:
            results = self.model.predict(frame, imgsz=imgsz, verbose=False, conf=0.3)

        r = results[0]
        annotated = frame.copy() if not draw_overlay else r.plot(line_width=1, font_size=0.35, kpt_radius=2)

        persons_data = []
        is_surrender_detected = False
        is_shoplifting_suspicious = False
        primary_action = "Nenhuma pessoa detectada"

        if len(r.keypoints) > 0:
            kpts_all = r.keypoints.xy.cpu().numpy()
            confs_all = r.keypoints.conf.cpu().numpy() if r.keypoints.conf is not None else None

            # Obtém IDs persistentes do ByteTrack se disponíveis
            track_ids = []
            if r.boxes is not None and r.boxes.id is not None:
                track_ids = r.boxes.id.int().cpu().tolist()
            else:
                track_ids = list(range(len(kpts_all)))

            for idx, kpts in enumerate(kpts_all):
                track_id = track_ids[idx] if idx < len(track_ids) else idx
                p_conf = confs_all[idx] if confs_all is not None else np.ones(17)

                # 0: nariz, 5: ombro esq, 6: ombro dir, 7: cotovelo esq, 8: cotovelo dir
                # 9: pulso esq, 10: pulso dir, 11: quadril esq, 12: quadril dir
                l_shoulder = kpts[5]
                r_shoulder = kpts[6]
                l_wrist = kpts[9]
                r_wrist = kpts[10]
                l_hip = kpts[11]
                r_hip = kpts[12]

                # ==============================================================
                # 1. VERIFICA INTERAÇÃO COM ZONA DE PRATELEIRA
                # ==============================================================
                hand_on_shelf = self.shelf_detector.check_hand_interaction(
                    track_id=track_id,
                    kpts=kpts,
                    width=w,
                    height=h,
                    current_sec=current_sec
                )
                touched_shelf_recently = self.shelf_detector.has_touched_shelf_recently(
                    track_id=track_id,
                    current_sec=current_sec,
                    window_sec=4.5
                )

                # ==============================================================
                # 2. DETECÇÃO DE RENDIÇÃO (Mãos ao alto / Assalto)
                # ==============================================================
                hands_raised = False
                l_raised = False
                r_raised = False

                if l_wrist[1] > 0 and l_shoulder[1] > 0 and p_conf[9] > 0.35 and p_conf[5] > 0.35:
                    if l_wrist[1] < l_shoulder[1] - 15:
                        l_raised = True

                if r_wrist[1] > 0 and r_shoulder[1] > 0 and p_conf[10] > 0.35 and p_conf[6] > 0.35:
                    if r_wrist[1] < r_shoulder[1] - 15:
                        r_raised = True

                if l_raised and r_raised:
                    hands_raised = True
                    self.surrender_counter[track_id] = self.surrender_counter.get(track_id, 0) + 1
                    if self.surrender_counter[track_id] >= 2:
                        is_surrender_detected = True
                        primary_action = f"Rendição Detectada (Indivíduo #{track_id})"
                else:
                    self.surrender_counter[track_id] = max(0, self.surrender_counter.get(track_id, 0) - 1)

                # ==============================================================
                # 3. DETECÇÃO DE FURTO / OCULTAÇÃO CONDICIONADA À PRATELEIRA
                # ==============================================================
                torso_top = min(l_shoulder[1], r_shoulder[1]) if (l_shoulder[1] > 0 and r_shoulder[1] > 0) else 0
                torso_bottom = max(l_hip[1], r_hip[1]) if (l_hip[1] > 0 and r_hip[1] > 0) else h
                torso_left = min(l_shoulder[0], r_shoulder[0], l_hip[0], r_hip[0])
                torso_right = max(l_shoulder[0], r_shoulder[0], l_hip[0], r_hip[0])
                torso_h = max(1.0, torso_bottom - torso_top)
                torso_w = max(1.0, torso_right - torso_left)

                l_in_pocket = False
                r_in_pocket = False

                if l_wrist[0] > 0 and l_wrist[1] > 0 and p_conf[9] > 0.35:
                    if (torso_bottom - 0.25 * torso_h) <= l_wrist[1] <= (torso_bottom + 0.35 * torso_h):
                        if (torso_left - 0.15 * torso_w) <= l_wrist[0] <= (torso_right + 0.15 * torso_w):
                            l_in_pocket = True

                if r_wrist[0] > 0 and r_wrist[1] > 0 and p_conf[10] > 0.35:
                    if (torso_bottom - 0.25 * torso_h) <= r_wrist[1] <= (torso_bottom + 0.35 * torso_h):
                        if (torso_left - 0.15 * torso_w) <= r_wrist[0] <= (torso_right + 0.15 * torso_w):
                            r_in_pocket = True

                # Condição de Furto: mão no bolso SÓ é suspeita se tocou na prateleira recentemente!
                if (l_in_pocket or r_in_pocket) and not hands_raised:
                    if touched_shelf_recently:
                        is_shoplifting_suspicious = True
                        if not is_surrender_detected:
                            primary_action = f"Furto em Andamento: Ocultação pós-manipulação (ID #{track_id})"
                    else:
                        if not is_surrender_detected:
                            primary_action = f"Manuseio Normal de Pertences (ID #{track_id})"

                persons_data.append({
                    "track_id": track_id,
                    "hands_raised": hands_raised,
                    "hand_on_shelf": hand_on_shelf,
                    "touched_shelf_recently": touched_shelf_recently,
                    "l_in_pocket": l_in_pocket,
                    "r_in_pocket": r_in_pocket,
                    "keypoints": kpts
                })

        telemetry = {
            "persons_count": len(persons_data),
            "is_surrender": is_surrender_detected,
            "is_shoplifting_suspicious": is_shoplifting_suspicious,
            "primary_action": primary_action,
            "persons": persons_data
        }

        return annotated, telemetry
