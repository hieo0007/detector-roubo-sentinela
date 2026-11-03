import cv2
import numpy as np
from typing import List, Tuple, Dict, Optional

class ShelfZoneDetector:
    """
    Detector de Zonas de Prateleiras e Interação Mão-Mercadoria (Anti-Falsos-Positivos).
    - Permite definir regiões de interesse (ROI) onde ficam as mercadorias/produtos.
    - Rastreia se os pulsos do indivíduo (ID rastreado pelo ByteTrack) tocaram na prateleira.
    - Condição estrita: Movimentos em direção a bolsos ou casacos só são suspeitos se o
      indivíduo tiver interagido com uma prateleira nos últimos segundos.
    """
    def __init__(self, zones: Optional[List[List[Tuple[float, float]]]] = None):
        # Zona de prateleira padrão (região média/lateral direita de exposição)
        self.zones = zones or [
            [(0.50, 0.35), (0.95, 0.35), (0.95, 0.85), (0.50, 0.85)]
        ]
        # Histórico por ID de pessoa: { track_id: último_timestamp_em_que_tocou_prateleira }
        self.touch_history: Dict[int, float] = {}

    def set_zones(self, zones: List[List[Tuple[float, float]]]):
        if zones:
            self.zones = zones

    def check_hand_interaction(
        self,
        track_id: int,
        kpts: np.ndarray,
        width: int,
        height: int,
        current_sec: float
    ) -> bool:
        """
        Verifica se os pulsos (keypoints 9 e 10) do indivíduo estão dentro de alguma prateleira.
        """
        if kpts is None or len(kpts) < 17:
            return False

        l_wrist = kpts[9]
        r_wrist = kpts[10]
        hand_in_shelf = False

        for zone in self.zones:
            poly_px = np.array([(int(x * width), int(y * height)) for x, y in zone], dtype=np.int32)

            for wrist in [l_wrist, r_wrist]:
                if wrist[0] > 0 and wrist[1] > 0:
                    dist = cv2.pointPolygonTest(poly_px, (int(wrist[0]), int(wrist[1])), measureDist=False)
                    if dist >= 0:
                        hand_in_shelf = True
                        self.touch_history[track_id] = current_sec
                        break

            if hand_in_shelf:
                break

        return hand_in_shelf

    def has_touched_shelf_recently(self, track_id: int, current_sec: float, window_sec: float = 4.5) -> bool:
        """
        Retorna True se o indivíduo tocou na prateleira nos últimos `window_sec` segundos.
        """
        last_touch = self.touch_history.get(track_id)
        if last_touch is None:
            return False
        return (current_sec - last_touch) <= window_sec

    def draw_overlay(self, frame: np.ndarray, active_touches: bool = False) -> np.ndarray:
        """
        Desenha as zonas de prateleiras na tela em estilo minimalista de segurança.
        """
        h, w = frame.shape[:2]
        overlay = frame.copy()

        # Cores suaves e clean (estilo grafite técnico)
        fill_color = (45, 45, 50) if not active_touches else (40, 50, 65)
        border_color = (100, 100, 105) if not active_touches else (140, 130, 110)

        for zone in self.zones:
            poly_px = np.array([(int(x * w), int(y * h)) for x, y in zone], dtype=np.int32)
            cv2.fillPoly(overlay, [poly_px], fill_color)

        cv2.addWeighted(overlay, 0.08, frame, 0.92, 0, frame)

        for zone in self.zones:
            poly_px = np.array([(int(x * w), int(y * h)) for x, y in zone], dtype=np.int32)
            cv2.polylines(frame, [poly_px], isClosed=True, color=border_color, thickness=1)

            top_x = min([p[0] for p in poly_px])
            top_y = min([p[1] for p in poly_px])
            cv2.rectangle(frame, (top_x, max(15, top_y - 18)), (top_x + 150, top_y), (18, 18, 22), -1)
            cv2.rectangle(frame, (top_x, max(15, top_y - 18)), (top_x + 150, top_y), (55, 55, 60), 1)
            cv2.putText(
                frame,
                "ZONA DE MERCADORIA",
                (top_x + 8, max(26, top_y - 5)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.33,
                (175, 175, 180),
                1,
                cv2.LINE_AA
            )

        return frame
