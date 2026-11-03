import os
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import time
import json
import argparse
import cv2

from .camera import VideoStreamBuffer
from .motion import MotionDetector
from .analyzer import SecurityAnalyzer
from .alert import AlertManager

def load_config(config_path: str = "config.json") -> dict:
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def run_system(camera_source=None, preview=True):
    config = load_config()

    src = camera_source if camera_source is not None else config.get("camera", {}).get("source", 0)
    fps = config.get("camera", {}).get("fps", 20)
    res = tuple(config.get("camera", {}).get("resolution", [1280, 720]))
    clip_duration = config.get("buffer", {}).get("clip_duration_seconds", 4)
    min_area = config.get("motion_filter", {}).get("min_area", 800)
    play_sound = config.get("detection", {}).get("play_sound_alert", True)

    print("\n" + "="*50)
    print("INICIANDO SISTEMA DE DETECCAO DE ROUBO VIA CAMERA")
    print(f"Fonte de Video: {src}")
    print(f"Buffer deslizante: {clip_duration}s | FPS: {fps}")
    print("="*50 + "\n")

    stream = VideoStreamBuffer(
        source=src,
        buffer_seconds=clip_duration,
        target_fps=fps,
        resolution=res
    )

    if not stream.start():
        print(f"[ERRO FATAL] Não foi possível conectar à câmera ou stream '{src}'.")
        print("Dica: Verifique se a webcam está conectada ou se o link RTSP está acessível na rede.")
        return

    motion_detector = MotionDetector(min_area=min_area)
    analyzer = SecurityAnalyzer()
    alert_manager = AlertManager(play_sound=play_sound)

    last_analysis_time = 0
    cooldown_seconds = config.get("motion_filter", {}).get("cooldown_seconds", 4.0)

    print("[INFO] Monitoramento ativo. Pressione 'q' na janela de video para encerrar.\n")

    try:
        while True:
            ret, frame = stream.read_frame()
            if not ret:
                time.sleep(0.01)
                continue

            has_motion, boxes, mask = motion_detector.detect(frame)
            current_time = time.time()

            # Desenha caixas de movimento no preview
            if preview:
                display_frame = frame.copy()
                for (x, y, w, h) in boxes:
                    cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                status_text = "MOVIMENTO DETECTADO!" if has_motion else "Ambiente Estavel"
                status_color = (0, 0, 255) if has_motion else (0, 255, 0)
                cv2.putText(display_frame, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, status_color, 2)
                cv2.imshow("Monitor de Seguranca - Anti-Roubo", display_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Se houver movimento e respeitar o cooldown, exporta e analisa o clipe
            if has_motion and (current_time - last_analysis_time >= cooldown_seconds):
                clip_path = stream.export_current_buffer()
                if clip_path:
                    last_analysis_time = current_time
                    print(f"\n[EVENTO] Movimento detectado! Analisando clipe: {clip_path}...")
                    
                    report = analyzer.analyze_clip(clip_path)
                    alert_manager.trigger(clip_path, report)

                    # Remove o clipe temporário após análise
                    try:
                        if os.path.exists(clip_path):
                            os.remove(clip_path)
                    except Exception:
                        pass

    except KeyboardInterrupt:
        print("\n[INFO] Monitoramento interrompido pelo usuário.")
    finally:
        stream.stop()
        cv2.destroyAllWindows()
        print("[INFO] Câmera e recursos liberados.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detector de Roubo via Câmera com Schema Tipado")
    parser.add_argument("--source", type=str, default=None, help="Fonte de vídeo: 0, 1 ou URL RTSP")
    parser.add_argument("--no-preview", action="store_true", help="Desativa janela gráfica do OpenCV")
    args = parser.parse_args()

    run_system(camera_source=args.source, preview=not args.no_preview)
