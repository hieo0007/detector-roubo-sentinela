import cv2
import numpy as np

class MotionDetector:
    """
    Filtro de movimento inteligente via OpenCV.
    Evita chamadas desnecessárias à IA quando o ambiente estiver vazio ou sem movimentação.
    """
    def __init__(self, min_area: int = 800, history: int = 500, var_threshold: int = 25):
        self.min_area = min_area
        self.subtractor = cv2.createBackgroundSubtractorMOG2(
            history=history,
            varThreshold=var_threshold,
            detectShadows=True
        )

    def detect(self, frame: np.ndarray) -> tuple[bool, list, np.ndarray]:
        """
        Retorna:
            - motion_detected (bool): True se houver movimento relevante
            - bounding_boxes (list): Caixas delimitadoras das áreas em movimento
            - fg_mask (np.ndarray): Máscara binária do movimento
        """
        if frame is None:
            return False, [], None

        # Reduz ruído inicial
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (21, 21), 0)

        # Aplica subtração de fundo
        fg_mask = self.subtractor.apply(blurred)

        # Remove sombras (geralmente valor 127) e ruídos pequenos
        _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        thresh = cv2.dilate(thresh, kernel, iterations=2)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        boxes = []
        motion_detected = False

        for c in contours:
            area = cv2.contourArea(c)
            if area >= self.min_area:
                motion_detected = True
                x, y, w, h = cv2.boundingRect(c)
                boxes.append((x, y, w, h))

        return motion_detected, boxes, fg_mask
