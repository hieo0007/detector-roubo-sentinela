import os
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional

class PoseActionDetector:
    """
    Detector de Ações e Gestos Suspeitos baseado em Esqueleto Humano (YOLOv8-Pose).
    Inspirado em projetos state-of-the-art do GitHub (Theft-Detection, PoseLift, AisleGuard).
    
    Rastreia 17 pontos anatômicos (COCO Keypoints):
    - Diferencia caminhada natural (balanço pendular dos braços / sacola lateral) de gestos
      reais de furto (mãos inseridas em bolsos/jaquetas, saque rápido e ocultação).
    """
    def __init__(self, weights_path: Optional[str] = None):
        from ultralytics import YOLO
        if not weights_path:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            weights_path = os.path.join(base_dir, "yolov8n-pose.pt")
            if not os.path.exists(weights_path):
                weights_path = "yolov8n-pose.pt"
        self.model = YOLO(weights_path)

    def analyze_frame(self, frame: np.ndarray, draw_overlay: bool = True, imgsz: int = 384) -> Tuple[np.ndarray, Dict]:
        """
        Processa um frame e retorna o frame anotado com esqueleto + HUD e telemetria comportamental.
        imgsz otimizado para inferência de alta velocidade em tempo real.
        """
        h, w = frame.shape[:2]
        results = self.model.predict(frame, imgsz=imgsz, verbose=False, conf=0.3)
        r = results[0]

        annotated = frame.copy()
        if draw_overlay:
            annotated = r.plot()

        persons_data = []
        is_suspicious_action = False
        highest_theft_score = 0.0
        primary_action = "Nenhuma pessoa detectada"

        if len(r.keypoints) > 0:
            kpts_all = r.keypoints.xy.cpu().numpy()
            confs_all = r.keypoints.conf.cpu().numpy() if r.keypoints.conf is not None else None

            for p_idx, kpts in enumerate(kpts_all):
                # kpts: (17, 2)
                # 0: nose, 5: l_shoulder, 6: r_shoulder, 7: l_elbow, 8: r_elbow
                # 9: l_wrist, 10: r_wrist, 11: l_hip, 12: r_hip, 15: l_ankle, 16: r_ankle
                
                l_wrist = kpts[9]
                r_wrist = kpts[10]
                l_hip = kpts[11]
                r_hip = kpts[12]
                l_shoulder = kpts[5]
                r_shoulder = kpts[6]

                # Calcula altura e largura do tronco
                torso_top = min(l_shoulder[1], r_shoulder[1]) if (l_shoulder[1] > 0 and r_shoulder[1] > 0) else 0
                torso_bottom = max(l_hip[1], r_hip[1]) if (l_hip[1] > 0 and r_hip[1] > 0) else h
                torso_left = min(l_shoulder[0], r_shoulder[0], l_hip[0], r_hip[0])
                torso_right = max(l_shoulder[0], r_shoulder[0], l_hip[0], r_hip[0])
                torso_height = max(1.0, torso_bottom - torso_top)
                torso_width = max(1.0, torso_right - torso_left)

                # Verifica mãos nos bolsos ou ocultação no peito/jaqueta
                l_concealed = False
                r_concealed = False

                # Mão esquerda próxima ao quadril ou peito
                if l_wrist[0] > 0 and l_wrist[1] > 0:
                    dist_to_l_hip = np.linalg.norm(l_wrist - l_hip)
                    dist_to_r_hip = np.linalg.norm(l_wrist - r_hip)
                    in_torso_x = (torso_left - 0.1 * torso_width) <= l_wrist[0] <= (torso_right + 0.1 * torso_width)
                    in_pocket_y = (torso_bottom - 0.25 * torso_height) <= l_wrist[1] <= (torso_bottom + 0.3 * torso_height)
                    in_chest_y = (torso_top + 0.1 * torso_height) <= l_wrist[1] <= (torso_bottom - 0.1 * torso_height)
                    
                    if (in_pocket_y or in_chest_y) and in_torso_x and (dist_to_l_hip < torso_height * 0.45 or dist_to_r_hip < torso_height * 0.45):
                        l_concealed = True

                # Mão direita próxima ao quadril ou peito
                if r_wrist[0] > 0 and r_wrist[1] > 0:
                    dist_to_l_hip = np.linalg.norm(r_wrist - l_hip)
                    dist_to_r_hip = np.linalg.norm(r_wrist - r_hip)
                    in_torso_x = (torso_left - 0.1 * torso_width) <= r_wrist[0] <= (torso_right + 0.1 * torso_width)
                    in_pocket_y = (torso_bottom - 0.25 * torso_height) <= r_wrist[1] <= (torso_bottom + 0.3 * torso_height)
                    in_chest_y = (torso_top + 0.1 * torso_height) <= r_wrist[1] <= (torso_bottom - 0.1 * torso_height)
                    
                    if (in_pocket_y or in_chest_y) and in_torso_x and (dist_to_r_hip < torso_height * 0.45 or dist_to_l_hip < torso_height * 0.45):
                        r_concealed = True

                # Classificação da postura corporal
                # Se as mãos estão abaixo do quadril (carregando sacola, penduradas naturalmente):
                hands_low = (l_wrist[1] > torso_bottom + 0.1 * torso_height) or (r_wrist[1] > torso_bottom + 0.1 * torso_height)

                if (l_concealed or r_concealed) and not hands_low:
                    action_label = "OCULTAÇÃO SUSPEITA (MÃO NO CORPO/BOLSO)"
                    theft_score = 78.0
                    is_suspicious_action = True
                elif hands_low:
                    action_label = "CAMINHADA REGULAR (MÃOS LIVRES / SACOLA BAIXA)"
                    theft_score = 5.0
                else:
                    action_label = "CIRCULAÇÃO PADRÃO (BRAÇOS EM REPOUSO)"
                    theft_score = 8.0

                if theft_score > highest_theft_score:
                    highest_theft_score = theft_score
                    primary_action = action_label

                persons_data.append({
                    "person_id": p_idx + 1,
                    "action": action_label,
                    "theft_score": theft_score,
                    "l_wrist_concealed": l_concealed,
                    "r_wrist_concealed": r_concealed
                })

                # Desenha marcadores visuais táticos nos pulsos
                if draw_overlay:
                    if l_wrist[0] > 0 and l_wrist[1] > 0:
                        pt_l = (int(l_wrist[0]), int(l_wrist[1]))
                        cv2.circle(annotated, pt_l, 8, (0, 0, 255) if l_concealed else (0, 255, 0), 2)
                        cv2.putText(annotated, "Mao Esq", (pt_l[0] + 10, pt_l[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

                    if r_wrist[0] > 0 and r_wrist[1] > 0:
                        pt_r = (int(r_wrist[0]), int(r_wrist[1]))
                        cv2.circle(annotated, pt_r, 8, (0, 0, 255) if r_concealed else (0, 255, 0), 2)
                        cv2.putText(annotated, "Mao Dir", (pt_r[0] + 10, pt_r[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        # Desenha HUD elegante no topo do frame
        if draw_overlay:
            hud_bg = (15, 23, 42) # Slate 900
            cv2.rectangle(annotated, (15, 15), (min(w - 15, 560), 80), hud_bg, -1)
            hud_border = (68, 68, 239) if is_suspicious_action else (74, 222, 128)
            cv2.rectangle(annotated, (15, 15), (min(w - 15, 560), 80), hud_border, 2)

            tag_title = "ALERTA: SUSPEITA DE FURTO" if is_suspicious_action else "STATUS: SEGURO (NORMAL)"
            tag_color = (0, 0, 255) if is_suspicious_action else (0, 255, 100)

            cv2.putText(annotated, f"IA ESQUELETO (YOLO-Pose): {tag_title}", (25, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.55, tag_color, 2, cv2.LINE_AA)
            cv2.putText(annotated, f"Acao Mapeada: {primary_action}", (25, 68), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (226, 232, 240), 1, cv2.LINE_AA)

        return annotated, {
            "persons_detected": len(persons_data),
            "primary_action": primary_action,
            "is_suspicious": is_suspicious_action,
            "highest_theft_score": highest_theft_score,
            "persons": persons_data
        }
