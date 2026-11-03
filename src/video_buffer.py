import os
import cv2
import time
from typing import Optional

class VideoClipCutter:
    """
    Cortador de Evidências Forenses (Pré e Pós-Ocorrência):
    Extrai automaticamente um clipe enxuto (ex: 3s antes e 4s depois)
    do momento exato em que a infração ocorreu.
    """
    def __init__(self, evidencias_dir: str):
        self.evidencias_dir = evidencias_dir
        os.makedirs(self.evidencias_dir, exist_ok=True)

    def extract_incident_clip(
        self,
        input_video_path: str,
        incident_sec: float,
        pre_sec: float = 3.0,
        post_sec: float = 4.0,
        output_name: Optional[str] = None
    ) -> Optional[str]:
        """
        Corta e exporta um arquivo MP4 leve focado no momento da ação.
        Retorna o caminho absoluto do arquivo salvo.
        """
        if not os.path.exists(input_video_path):
            return None

        cap = cv2.VideoCapture(input_video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
        duration = total_frames / fps
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 360

        start_sec = max(0.0, incident_sec - pre_sec)
        end_sec = min(duration, incident_sec + post_sec)

        start_frame = int(start_sec * fps)
        end_frame = int(end_sec * fps)

        if not output_name:
            ts = time.strftime("%Y%m%d_%H%M%S")
            output_name = f"evidencia_clipe_{ts}.mp4"

        output_path = os.path.join(self.evidencias_dir, output_name)
        raw_temp_path = os.path.join(self.evidencias_dir, f"raw_{output_name}")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(raw_temp_path, fourcc, fps, (w, h))

        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        curr = start_frame
        while curr <= end_frame:
            ret, frame = cap.read()
            if not ret:
                break
            # Insere marca d'água forense de tempo no rodapé
            sec_now = round(curr / fps, 1)
            cv2.rectangle(frame, (10, h - 35), (200, h - 10), (10, 10, 12), -1)
            cv2.putText(
                frame,
                f"EVIDENCIA T={sec_now}s",
                (16, h - 18),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (220, 220, 220),
                1,
                cv2.LINE_AA
            )
            out.write(frame)
            curr += 1

        cap.release()
        out.release()

        # Converte para codec H.264 (avc1) web-ready com faststart para navegadores
        try:
            import subprocess
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            cmd = [
                ffmpeg_exe, "-y",
                "-i", raw_temp_path,
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                output_path
            ]
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res.returncode == 0 and os.path.exists(output_path):
                if os.path.exists(raw_temp_path):
                    try:
                        os.remove(raw_temp_path)
                    except Exception:
                        pass
                return output_path
        except Exception:
            pass

        if os.path.exists(raw_temp_path):
            try:
                os.replace(raw_temp_path, output_path)
            except Exception:
                pass

        return output_path if os.path.exists(output_path) else None
