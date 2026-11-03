# AGENTS.md - System Context and Operational Guidelines for Autonomous Agents

This document provides system context, architecture boundaries, execution guidelines, and test instructions for autonomous AI agents (such as Claude Code, Antigravity, Codex, Cursor, or similar developer assistants) interacting with the Sentinela codebase.

---

## 1. Executive Summary

Sentinela is a production-grade CCTV loss prevention and security monitoring platform. It solves the high-false-positive problem of traditional edge motion systems and the latency bottleneck of full-video cloud analysis through a hybrid architecture:

* **Edge Layer (Local Sampling):** Frame sampling every 0.5s of recorded video (2 fps) for continuous object detection (YOLOv8), multi-object tracking (ByteTrack), pose estimation (YOLOv8-Pose), and ray-casting geometric fence intrusion.
* **Cloud Multimodal Layer (<2.0s):** Event-triggered temporal storyboard extraction (6 keyframes @ 480x270 with timestamp metadata, ~60 KB JPEG) verified against Google Gemini 3.5 Flash Lite using loss-prevention forensic prompts.
* **Evidence Custody Layer:** Immediate incident clipping, automated faststart H.264 transcoding via imageio-ffmpeg, and HTTP 206 range-request streaming.

---

## 2. Directory Structure and Module Responsibilities

```
detector_roubo/
├── config.json                 # Local runtime configuration (ignored by git)
├── config.example.json         # Sanitized configuration template
├── requirements.txt            # Locked Python dependencies
├── iniciar_aplicativo.bat      # Windows 1-click bootloader (manages port 5000)
├── README.md                   # Public documentation (Caddy-style)
├── AGENTS.md                   # This agent guidance file
├── CONTEXTO_AGENTE.md          # Detailed engineering handoff specification
├── AUTHORS                     # Project author and contributors
├── LICENSE                     # MIT license
├── SECURITY.md                 # Security and privacy policy
├── CONTRIBUTING.md             # Developer workflow guidelines
├── evidencias/                 # Output directory for incident clips and JSONs
├── snapshots/                  # Ephemeral JPEG storyboards
├── videos_teste/               # Curated benchmark video suite
└── src/
    ├── app.py                  # Flask web backend, REST endpoints, MJPEG stream
    ├── analyzer.py             # SecurityAnalyzer: central orchestration pipeline
    ├── storyboard.py           # StoryboardVerifier: temporal keyframe sampler & Gemini client
    ├── video_buffer.py         # VideoClipCutter: incident extraction with H.264 transcoding
    ├── gesture_engine.py       # Pose tracking: surrender detection & pocket/backpack proximity
    ├── virtual_fence.py        # Ray-casting point-in-polygon intrusion engine
    ├── shelf_detector.py       # Shelf zone definition and interaction tracker
    ├── alert.py                # Forensic JSON logger and event dispatcher
    ├── models.py               # Enums (SecurityMode, EventType, RiskLevel) and dataclasses
    └── templates/
        └── index.html          # High-performance CCTV UI (Tailwind CSS + Vanilla JS)
```

---

## 3. Core Working Invariants

When modifying or refactoring this codebase, any agent must preserve these non-negotiables:

1. **Zero UI Bloat:** The frontend in `src/templates/index.html` uses Tailwind CSS via CDN and vanilla JavaScript. Do not introduce heavy frontend frameworks (React/Vue/Webpack/Vite) unless explicitly instructed.
2. **Codec Compliance:** Browser video playback strictly requires H.264 (`libx264`, `yuv420p`, `-movflags +faststart`). Do not revert to raw OpenCV `mp4v` codec, as modern Chromium/Brave/Edge will fail to play it.
3. **HTTP 206 Streaming:** Any endpoint serving MP4 videos must use `conditional=True` in `send_file` to support byte-range requests for client-side timeline scrubbing.
4. **Clean Corporate Aesthetics:** Zero neon colors, zero emojis in system logs or UI, minimal zinc/titanium palette with subdued status indicators.
5. **Privacy by Design:** Full-length raw videos are never sent to third-party APIs. Only compressed multi-frame storyboards (~60 KB) of triggered intervals are transmitted for semantic validation.

---

## 4. Verification and Benchmark Protocol

To verify changes without running the full web GUI, execute the headless benchmark script:

```bash
python -c "
from src.analyzer import SecurityAnalyzer
from src.models import SecurityMode

analyzer = SecurityAnalyzer()
res = analyzer.analyze_clip('videos_teste/furto_real_mercado_01.mp4', mode=SecurityMode.SHOPLIFTING)
assert res.tipo_evento.value == 'FURTO_LOJA', f'Expected FURTO_LOJA, got {res.tipo_evento.value}'
assert res.nivel_risco.value == 'ALERTA_MAXIMO', f'Expected ALERTA_MAXIMO, got {res.nivel_risco.value}'
print('Benchmark passed: Confidence', res.confianca, '%')
"
```

Expected Ground Truth:
* `furto_real_mercado_01.mp4` -> `FURTO_LOJA` (Confidence >= 95%)
* `furto_real_gondola_02.mp4` -> `FURTO_LOJA` (Confidence >= 95%)
* `assalto_furto_02.mp4` -> `FURTO_LOJA` (Confidence >= 95%)
* `cliente_normal_compras_04.mp4` -> `NORMAL` (Confidence >= 90%)
