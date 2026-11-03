import os
import cv2
import numpy as np

videos = [
    "roubo_mercado_01.mp4",
    "roubo_mercado_02.mp4",
    "roubo_mercado_03.mp4",
    "roubo_mercado_04.mp4",
    "roubo_mercado_05.mp4"
]

base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "videos_teste")

for v_name in videos:
    path = os.path.join(base_dir, v_name)
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=25, detectShadows=False)
    motion_profile = []
    
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        small = cv2.resize(frame, (320, 240))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        fg = subtractor.apply(gray)
        
        # Ignora os primeiros 20 frames de aquecimento do background
        if frame_idx > 20:
            motion_score = np.sum(fg > 0)
            motion_profile.append((frame_idx / fps, motion_score))
        frame_idx += 1
        
    cap.release()
    
    motion_profile.sort(key=lambda x: x[1], reverse=True)
    peak_time, peak_score = motion_profile[0] if motion_profile else (0.0, 0)
    print(f"{v_name}: {duration:.1f}s | Pico de acao anomala: {peak_time:.2f}s (pixels em movimento: {peak_score})")
