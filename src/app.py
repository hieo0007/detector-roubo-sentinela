import os
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import time
import json
import uuid
import threading
import cv2
from flask import Flask, render_template, request, jsonify, send_file, Response

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from src.analyzer import SecurityAnalyzer
from src.alert import AlertManager
from src.models import SecurityMode, RiskLevel, EventType

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)

analyzer = SecurityAnalyzer()
alert = AlertManager(evidencias_dir=os.path.join(base_dir, "evidencias"), play_sound=True)

VIDEOS_DIR = os.path.join(base_dir, "videos_teste")
os.makedirs(VIDEOS_DIR, exist_ok=True)

SNAPSHOTS_DIR = os.path.join(base_dir, "snapshots")
os.makedirs(SNAPSHOTS_DIR, exist_ok=True)

STORYBOARD_DIR = os.path.join(SNAPSHOTS_DIR, "storyboards")
os.makedirs(STORYBOARD_DIR, exist_ok=True)

EVIDENCIAS_DIR = os.path.join(base_dir, "evidencias")
os.makedirs(EVIDENCIAS_DIR, exist_ok=True)

jobs = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/config", methods=["GET", "POST"])
def handle_config():
    if request.method == "POST":
        data = request.get_json() or {}
        gemini_key = data.get("gemini_api_key", "").strip()
        tele_token = data.get("telegram_bot_token", "").strip()
        tele_chat = data.get("telegram_chat_id", "").strip()

        config = {}
        if os.path.exists(analyzer.config_path):
            try:
                with open(analyzer.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except Exception:
                pass

        if gemini_key:
            analyzer.set_api_key(gemini_key)
            config["gemini_api_key"] = gemini_key
        if tele_token:
            config["telegram_bot_token"] = tele_token
        if tele_chat:
            config["telegram_chat_id"] = tele_chat

        try:
            with open(analyzer.config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
        except Exception:
            pass

        return jsonify({
            "success": True,
            "has_gemini_key": bool(analyzer.client),
            "has_telegram": bool(config.get("telegram_bot_token") and config.get("telegram_chat_id"))
        })

    config = {}
    if os.path.exists(analyzer.config_path):
        try:
            with open(analyzer.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            pass

    return jsonify({
        "has_gemini_key": bool(analyzer.client),
        "has_telegram": bool(config.get("telegram_bot_token") and config.get("telegram_chat_id")),
        "telegram_chat_id": config.get("telegram_chat_id", "")
    })

@app.route("/api/telegram/test", methods=["POST"])
def test_telegram():
    data = request.get_json() or {}
    token = data.get("token", "").strip()
    chat_id = data.get("chat_id", "").strip()
    if not token or not chat_id:
        return jsonify({"success": False, "error": "Token e Chat ID são obrigatórios"}), 400

    ok, msg = analyzer.notifier.test_connection(token, chat_id)
    return jsonify({"success": ok, "message": msg})

@app.route("/api/fence", methods=["GET", "POST"])
def handle_fence():
    if request.method == "POST":
        data = request.get_json() or {}
        points = data.get("points", [])
        if points and len(points) >= 3:
            analyzer.set_fence_polygon([(float(p[0]), float(p[1])) for p in points])
            return jsonify({"success": True, "points": analyzer.virtual_fence.polygon})
        return jsonify({"success": False, "error": "Mínimo 3 pontos requeridos"}), 400
    return jsonify({"points": analyzer.virtual_fence.polygon})

@app.route("/api/shelf", methods=["GET", "POST"])
def handle_shelf():
    if request.method == "POST":
        data = request.get_json() or {}
        zones = data.get("zones", [])
        if zones:
            analyzer.set_shelf_zones(zones)
            return jsonify({"success": True, "zones": analyzer.shelf_detector.zones})
        return jsonify({"success": False, "error": "Nenhuma zona informada"}), 400
    return jsonify({"zones": analyzer.shelf_detector.zones})

@app.route("/api/test-videos")
def list_test_videos():
    descriptions = {
        "furto_real_mercado_01.mp4": {"tag": "FURTO REAL", "label": "Furto em Mercadinho (Ocultação Rápida)", "category": "loja"},
        "furto_real_gondola_02.mp4": {"tag": "FURTO REAL", "label": "Subtração em Gôndola de Supermercado", "category": "loja"},
        "cliente_normal_compras_04.mp4": {"tag": "NORMAL", "label": "Cliente Comprando em Loja (Sem Furto)", "category": "normal"},
        "atividade_normal_balcao_05.mp4": {"tag": "NORMAL", "label": "Movimentação Normal em Balcão (Sem Furto)", "category": "normal"},

        "assalto_furto_01.mp4": {"tag": "FURTO", "label": "Subtração e Ocultação de Objeto em Bolso", "category": "loja"},
        "assalto_furto_02.mp4": {"tag": "FURTO", "label": "Ocultação Sob Jaqueta / Casaco", "category": "loja"},
        "assalto_furto_03.mp4": {"tag": "FURTO", "label": "Furto Discreto de Mercadoria e Evasão", "category": "loja"},
        "novo_teste_roubo_06.mp4": {"tag": "FURTO", "label": "Furto e Ocultação Rápida em Loja", "category": "loja"},
        "roubo_mercado_01.mp4": {"tag": "FURTO", "label": "Furto em Prateleira de Mercado (Shoplifting)", "category": "loja"},

        "pedestre_normal_01.mp4": {"tag": "NORMAL", "label": "Pedestres em Calçada / Circulação Pacífica", "category": "normal"},
        "pedestre_normal_02.mp4": {"tag": "NORMAL", "label": "Cliente Circulando com Mãos Livres", "category": "normal"},
        "pedestre_normal_03.mp4": {"tag": "NORMAL", "label": "Trânsito Regular de Pessoas", "category": "normal"},
        "upload_1792883072_teste02.mp4": {"tag": "NORMAL", "label": "Pedestre com Sacola Verde na Rua", "category": "normal"},
        "cenario_teste.mp4": {"tag": "NORMAL", "label": "Cenário de Teste Limpo", "category": "normal"},

        "upload_1792882829_teste01.mp4": {"tag": "ASSALTO", "label": "Assalto a Loja de Celulares / Saque ao Cofre", "category": "assalto"}
    }

    files = []
    seen = set()

    priority_order = [
        "furto_real_mercado_01.mp4",
        "furto_real_gondola_02.mp4",
        "cliente_normal_compras_04.mp4",
        "atividade_normal_balcao_05.mp4",
        "assalto_furto_01.mp4",
        "assalto_furto_02.mp4",
        "roubo_mercado_01.mp4",
        "assalto_furto_03.mp4",
        "upload_1792882829_teste01.mp4",
        "novo_teste_roubo_06.mp4",
        "pedestre_normal_01.mp4",
        "pedestre_normal_02.mp4",
        "pedestre_normal_03.mp4",
        "upload_1792883072_teste02.mp4"
    ]

    for p in priority_order:
        if os.path.exists(os.path.join(VIDEOS_DIR, p)):
            meta = descriptions.get(p, {"tag": "VÍDEO", "label": p, "category": "geral"})
            files.append({
                "name": p,
                "path": p,
                "tag": meta["tag"],
                "description": meta["label"],
                "category": meta["category"]
            })
            seen.add(p)

    for f in os.listdir(VIDEOS_DIR):
        if f.lower().endswith((".mp4", ".avi", ".mkv", ".mov")) and f not in seen:
            tag = "GRAVAÇÃO"
            cat = "geral"
            files.append({
                "name": f,
                "path": f,
                "tag": tag,
                "description": f,
                "category": cat
            })

    return jsonify({"videos": files})

@app.route("/api/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"success": False, "error": "Nenhum arquivo enviado"}), 400

    file = request.files["video"]
    if file.filename == "":
        return jsonify({"success": False, "error": "Nome de arquivo vazio"}), 400

    filename = f"upload_{int(time.time())}_{file.filename}"
    save_path = os.path.join(VIDEOS_DIR, filename)
    file.save(save_path)
    return jsonify({"success": True, "path": filename})

@app.route("/videos/<path:filename>")
def serve_video(filename):
    file_path = os.path.join(VIDEOS_DIR, filename)
    if not os.path.exists(file_path):
        file_path = os.path.join(EVIDENCIAS_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype="video/mp4", conditional=True)
    return "Vídeo não encontrado", 404

@app.route("/api/snapshots/storyboards/<path:filename>")
def serve_storyboard(filename):
    file_path = os.path.join(STORYBOARD_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype="image/jpeg")
    return "Storyboard não encontrado", 404

@app.route("/snapshots/<path:filename>")
def serve_snapshot(filename):
    file_path = os.path.join(SNAPSHOTS_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype="image/jpeg")
    return "Snapshot não encontrado", 404

def generate_live_annotated_stream(video_path: str, start_sec: float = 0.0, speed: float = 1.0, mode: str = "TODOS"):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1

    if start_sec > 0:
        target_frame = min(total_frames - 1, int(start_sec * fps))
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)

    delay = 1.0 / max(12.0, min(60.0, fps * speed))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        h, w = frame.shape[:2]
        curr_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        current_sec = curr_frame / fps
        is_breached = False

        # 1. Desenho de Prateleiras se modo for Varejo ou Geral
        if mode in ["TODOS", "LOJA"]:
            try:
                frame = analyzer.shelf_detector.draw_overlay(frame)
            except Exception:
                pass

        # 2. Análise de Gestos e Esqueleto com ByteTrack
        telemetry = {}
        if analyzer.gesture_engine:
            try:
                frame, telemetry = analyzer.gesture_engine.analyze_frame(
                    frame,
                    draw_overlay=True,
                    imgsz=384,
                    current_sec=current_sec,
                    enable_tracking=True
                )
            except Exception:
                pass

        # 3. Análise e Desenho de Cerca Virtual
        if mode in ["TODOS", "PERIMETRO"]:
            try:
                for p in telemetry.get("persons", []):
                    kpts = p.get("keypoints")
                    invaded, _ = analyzer.virtual_fence.check_intrusion(None, kpts, w, h)
                    if invaded:
                        is_breached = True
                        break
                frame = analyzer.virtual_fence.draw_overlay(frame, is_breached=is_breached)
            except Exception:
                pass

        # 4. HUD de Alerta Minimalista (sem blocos neon vermelhos)
        alert_msg = None
        if telemetry.get("is_surrender"):
            alert_msg = "ALERTA: RENDICAO DETECTADA"
        elif is_breached:
            alert_msg = "ALERTA: VIOLACAO DE PERIMETRO"
        elif telemetry.get("is_shoplifting_suspicious") and mode in ["TODOS", "LOJA"]:
            alert_msg = "ALERTA: OCULTACAO DE MERCADORIA"

        if alert_msg:
            cv2.rectangle(frame, (12, 12), (280, 40), (18, 18, 22), -1)
            cv2.rectangle(frame, (12, 12), (280, 40), (60, 55, 120), 1)
            cv2.circle(frame, (24, 26), 4, (70, 70, 185), -1)
            cv2.putText(frame, alert_msg, (36, 29), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (225, 225, 230), 1, cv2.LINE_AA)

        small = cv2.resize(frame, (640, 360))
        ret, buffer = cv2.imencode('.jpg', small, [int(cv2.IMWRITE_JPEG_QUALITY), 78])
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(delay)

    cap.release()

@app.route("/video_feed/<path:filename>")
def video_feed(filename):
    file_path = os.path.join(VIDEOS_DIR, filename)
    if not os.path.exists(file_path):
        file_path = os.path.join(EVIDENCIAS_DIR, filename)
    if not os.path.exists(file_path):
        return "Arquivo não encontrado", 404

    start_sec = float(request.args.get("start", 0.0))
    speed = float(request.args.get("speed", 1.0))
    mode = request.args.get("mode", "TODOS")
    return Response(generate_live_annotated_stream(file_path, start_sec, speed, mode), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/api/video-info/<path:filename>")
def get_video_info(filename):
    file_path = os.path.join(VIDEOS_DIR, filename)
    if not os.path.exists(file_path):
        file_path = os.path.join(EVIDENCIAS_DIR, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "Vídeo não encontrado"}), 404

    cap = cv2.VideoCapture(file_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    duration = frames / fps
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return jsonify({
        "duration": round(duration, 2),
        "fps": round(fps, 2),
        "total_frames": frames,
        "width": w,
        "height": h
    })

def async_analyzer_worker(job_id: str, full_path: str, mode_str: str, fence_pts: list, shelf_zones: list):
    def on_progress(percent: float, current_frame: int, total_frames: int, stage_msg: str):
        if job_id in jobs:
            jobs[job_id]["percent"] = round(min(98.0, max(0.0, percent)), 1)
            jobs[job_id]["current_frame"] = current_frame
            jobs[job_id]["total_frames"] = total_frames
            jobs[job_id]["stage"] = stage_msg

    try:
        try:
            mode_enum = SecurityMode(mode_str)
        except Exception:
            mode_enum = SecurityMode.ALL

        report = analyzer.analyze_clip(
            video_path=full_path,
            mode=mode_enum,
            fence_points=fence_pts,
            shelf_zones=shelf_zones,
            progress_callback=on_progress
        )
        alert.trigger(full_path, report)

        if job_id in jobs:
            jobs[job_id]["percent"] = 100.0
            jobs[job_id]["status"] = "done"
            jobs[job_id]["stage"] = "Análise Forense Concluída!"
            jobs[job_id]["report"] = report.model_dump()
            jobs[job_id]["timeline"] = report.timeline

    except Exception as e:
        if job_id in jobs:
            jobs[job_id]["status"] = "error"
            jobs[job_id]["stage"] = f"Erro na análise: {str(e)}"

@app.route("/api/analyze-async", methods=["POST"])
def start_analyze_async():
    data = request.get_json() or {}
    rel_path = data.get("video_path")
    mode_str = data.get("mode", "TODOS")
    fence_pts = data.get("fence_points", [])
    shelf_zones = data.get("shelf_zones", [])

    if not rel_path:
        return jsonify({"error": "Caminho do vídeo não informado"}), 400

    full_path = os.path.join(VIDEOS_DIR, rel_path)
    if not os.path.exists(full_path):
        full_path = os.path.join(EVIDENCIAS_DIR, rel_path)
    if not os.path.exists(full_path):
        full_path = rel_path

    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "processing",
        "percent": 0.0,
        "current_frame": 0,
        "total_frames": 100,
        "stage": "Inicializando pipeline ByteTrack...",
        "report": None,
        "timeline": []
    }

    t = threading.Thread(
        target=async_analyzer_worker,
        args=(job_id, full_path, mode_str, fence_pts, shelf_zones),
        daemon=True
    )
    t.start()

    return jsonify({"job_id": job_id})

@app.route("/api/progress/<job_id>")
def get_job_progress(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"status": "not_found"}), 404
    return jsonify(job)

if __name__ == "__main__":
    print("\n" + "="*65)
    print(" SENTINELA - SISTEMA DE MONITORAMENTO E CONTROLE CCTV")
    print(" Painel de Operação: http://127.0.0.1:5000")
    print("="*65 + "\n")

    def auto_open_browser():
        time.sleep(1.2)
        import webbrowser
        webbrowser.open("http://127.0.0.1:5000")

    threading.Thread(target=auto_open_browser, daemon=True).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
