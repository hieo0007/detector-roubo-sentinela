import os
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import cv2
import numpy as np
import time

def scan_available_cameras(max_to_test=5):
    """Verifica quais indices de camera estao disponiveis no sistema"""
    available = []
    print("\n[BUSCA] Escaneando portas de camera disponiveis...")
    for idx in range(max_to_test):
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                available.append(idx)
                print(f"  [OK] Camera encontrada no indice {idx}!")
            cap.release()
    if not available:
        print("  [AVISO] Nenhuma webcam USB ou integrada ativa encontrada nos indices 0-4.")
        print("  [DICA] Se voce estiver usando uma camera Wi-Fi/IP, configure o link RTSP ou HTTP no config.json.")
    return available

def create_synthetic_test_video(output_path=None, duration_seconds=5, fps=20):
    """Cria um video simulado com movimentacao para testar o pipeline sem precisar de camera fisica"""
    if output_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(base_dir, "videos_teste", "cenario_teste.mp4")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    total_frames = duration_seconds * fps
    print(f"\n[TESTE] Gerando video sintetico de teste: {output_path} ({duration_seconds}s)...")

    # Simula um cenario onde um retangulo se move e esconde um item
    for i in range(total_frames):
        frame = np.ones((height, width, 3), dtype=np.uint8) * 40 # Fundo escuro
        
        # Desenha balcao fixo
        cv2.rectangle(frame, (50, 350), (590, 450), (100, 100, 100), -1)
        cv2.putText(frame, "Balcao / Prateleira de Loja", (60, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # "Item na prateleira" (vermelho) antes do segundo 2.5
        if i < total_frames * 0.5:
            cv2.rectangle(frame, (280, 310), (320, 350), (0, 0, 255), -1)
            cv2.putText(frame, "Item", (280, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # "Pessoa" se aproximando
        x_pos = int(100 + (i / total_frames) * 350)
        cv2.circle(frame, (x_pos, 220), 40, (0, 255, 255), -1) # Cabeca/corpo
        
        # Mao se movendo em direcao ao item
        if i > total_frames * 0.3 and i < total_frames * 0.7:
            cv2.line(frame, (x_pos, 240), (300, 330), (0, 255, 0), 4)

        # Texto de status
        cv2.putText(frame, f"Simulacao de Movimento - Frame {i}/{total_frames}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        out.write(frame)

    out.release()
    print(f"[OK] Video de teste gerado com sucesso: {output_path}")
    return output_path

if __name__ == "__main__":
    scan_available_cameras()
    create_synthetic_test_video()

