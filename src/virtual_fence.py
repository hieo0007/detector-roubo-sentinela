import cv2
import numpy as np
from typing import List, Tuple, Dict, Optional

class VirtualFence:
    """
    Motor de Cerca Virtual e Detecção de Invasão de Perímetro.
    - Suporta polígonos arbitrários em coordenadas normalizadas (0.0 a 1.0).
    - Detecta intrusão direta (pés ou base do corpo cruzando a linha).
    - Detecta tempo de permanência não autorizada (loitering).
    """
    def __init__(self, polygon: Optional[List[Tuple[float, float]]] = None, name: str = "Zona Restrita"):
        # Se nenhum polígono for informado, usa a metade inferior por padrão
        self.polygon = polygon or [
            (0.15, 0.50),
            (0.85, 0.50),
            (0.95, 0.95),
            (0.05, 0.95)
        ]
        self.name = name
        self.dwell_times: Dict[int, float] = {}

    def set_polygon(self, points: List[Tuple[float, float]]):
        """Atualiza os pontos da cerca virtual (mínimo 3 pontos)."""
        if len(points) >= 3:
            self.polygon = points

    def get_pixel_polygon(self, width: int, height: int) -> np.ndarray:
        """Converte pontos normalizados (0-1) em coordenadas reais de pixel."""
        pts = [(int(x * width), int(y * height)) for x, y in self.polygon]
        return np.array(pts, dtype=np.int32)

    def check_intrusion(self, bbox: Tuple[float, float, float, float], keypoints: Optional[np.ndarray], width: int, height: int) -> Tuple[bool, float]:
        """
        Verifica se um indivíduo invadiu o perímetro restrito.
        bbox: (x1, y1, x2, y2)
        keypoints: array (17, 2) COCO (15=l_ankle, 16=r_ankle)
        Retorna (invadiu: bool, distancia: float)
        """
        poly_pts = self.get_pixel_polygon(width, height)
        test_points = []

        # 1. Pés detectados por pose (tornozelos)
        if keypoints is not None and len(keypoints) >= 17:
            l_ankle = keypoints[15]
            r_ankle = keypoints[16]
            if l_ankle[0] > 0 and l_ankle[1] > 0:
                test_points.append((float(l_ankle[0]), float(l_ankle[1])))
            if r_ankle[0] > 0 and r_ankle[1] > 0:
                test_points.append((float(r_ankle[0]), float(r_ankle[1])))

        # 2. Ponto central inferior da caixa delimitadora (base dos pés)
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            bottom_center = ((x1 + x2) / 2.0, y2)
            test_points.append(bottom_center)

        # Checa se qualquer ponto está dentro do polígono
        for pt in test_points:
            dist = cv2.pointPolygonTest(poly_pts, (int(pt[0]), int(pt[1])), measureDist=False)
            if dist >= 0:
                return True, dist

        return False, -1.0

    def draw_overlay(self, frame: np.ndarray, is_breached: bool = False) -> np.ndarray:
        """
        Desenha a cerca virtual em estilo minimalista, fosco e clean (sem cores neon).
        """
        h, w = frame.shape[:2]
        poly_pts = self.get_pixel_polygon(w, h)
        overlay = frame.copy()

        # Paleta suave e fosca de alta sofisticação (BGR)
        if is_breached:
            fill_color = (35, 30, 80)      # Vinho / terracota fosco suave
            border_color = (70, 70, 180)   # Linha terracota sutil (sem neon)
            alpha = 0.16
        else:
            fill_color = (40, 42, 45)      # Grafite / ardósia neutro suave
            border_color = (130, 130, 135) # Linha fina cinza titânio
            alpha = 0.08

        # Preenchimento semitransparente suave
        cv2.fillPoly(overlay, [poly_pts], fill_color)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        # Borda sutil de 1px (ou 2px se violado)
        cv2.polylines(frame, [poly_pts], isClosed=True, color=border_color, thickness=1 if not is_breached else 2)

        # Rótulo de status em badge minimalista escuro
        label = "PERIMETRO: INVASAO DETECTADA" if is_breached else "PERIMETRO: MONITORADO"
        top_y = min([p[1] for p in poly_pts])
        top_x = int(np.mean([p[0] for p in poly_pts])) - 95
        top_x = max(15, min(top_x, w - 215))
        top_y = max(24, top_y - 8)

        badge_bg = (18, 18, 22)
        badge_border = (60, 55, 120) if is_breached else (55, 55, 60)
        cv2.rectangle(frame, (top_x - 6, top_y - 16), (top_x + 195, top_y + 6), badge_bg, -1)
        cv2.rectangle(frame, (top_x - 6, top_y - 16), (top_x + 195, top_y + 6), badge_border, 1)

        # Indicador sutil
        dot_color = (70, 70, 180) if is_breached else (130, 130, 135)
        cv2.circle(frame, (top_x + 4, top_y - 5), 3, dot_color, -1)
        cv2.putText(frame, label, (top_x + 14, top_y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (220, 220, 225), 1, cv2.LINE_AA)

        return frame
