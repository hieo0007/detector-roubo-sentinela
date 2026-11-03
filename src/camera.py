import cv2
import os
import time
from collections import deque
from typing import Optional, Union

class VideoStreamBuffer:
    """
    Gerenciador de captura de vídeo com buffer deslizante (sliding window).
    Mantém os últimos N segundos na memória e grava blocos temporários de vídeo
    para envio ao motor de inferência.
    """
    def __init__(
        self,
        source: Union[int, str] = 0,
        buffer_seconds: int = 4,
        target_fps: int = 20,
        resolution: tuple[int, int] = (1280, 720),
        temp_dir: str = "temp"
    ):
        self.source = source
        self.buffer_seconds = buffer_seconds
        self.target_fps = target_fps
        self.resolution = resolution
        self.temp_dir = temp_dir
        
        os.makedirs(self.temp_dir, exist_ok=True)
        
        self.max_frames = buffer_seconds * target_fps
        self.frame_buffer = deque(maxlen=self.max_frames)
        self.cap: Optional[cv2.VideoCapture] = None

    def start(self) -> bool:
        """Inicia a captura de vídeo"""
        if isinstance(self.source, str) and self.source.isdigit():
            self.source = int(self.source)

        # Em Windows com webcam USB, cv2.CAP_DSHOW acelera a inicialização
        if isinstance(self.source, int):
            self.cap = cv2.VideoCapture(self.source, cv2.CAP_DSHOW)
        else:
            self.cap = cv2.VideoCapture(self.source)

        if not self.cap.isOpened():
            # Tenta fallback sem backend específico
            self.cap = cv2.VideoCapture(self.source)

        if not self.cap.isOpened():
            return False

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        return True

    def read_frame(self) -> tuple[bool, Optional[object]]:
        """Lê um frame da câmera e armazena no buffer circular"""
        if self.cap is None or not self.cap.isOpened():
            return False, None

        ret, frame = self.cap.read()
        if ret and frame is not None:
            self.frame_buffer.append(frame.copy())
            return True, frame
        return False, None

    def export_current_buffer(self) -> Optional[str]:
        """
        Salva os frames acumulados no buffer em um arquivo de vídeo temporário (.mp4).
        Retorna o caminho do arquivo gerado.
        """
        if len(self.frame_buffer) < (self.target_fps * 1.5):
            # Buffer muito pequeno ainda
            return None

        timestamp = int(time.time() * 1000)
        output_path = os.path.join(self.temp_dir, f"clip_{timestamp}.mp4")

        frames_to_write = list(self.frame_buffer)
        h, w = frames_to_write[0].shape[:2]

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.target_fps, (w, h))

        for f in frames_to_write:
            out.write(f)

        out.release()
        return output_path

    def stop(self):
        """Libera a câmera"""
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None
