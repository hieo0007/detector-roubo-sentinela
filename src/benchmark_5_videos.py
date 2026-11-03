import os
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from src.analyzer import TheftAnalyzer
from src.alert import AlertManager
from src.models import RiskLevel

videos = [
    ("roubo_mercado_01.mp4", "Furto em prateleira de mercado (CCTV 1)"),
    ("roubo_mercado_02.mp4", "Subtração rápida de item em balcão (CCTV 2)"),
    ("roubo_mercado_03.mp4", "Ocultação de produto em vestimenta (CCTV 3)"),
    ("roubo_mercado_04.mp4", "Apropriação indevida de mercadoria (CCTV 4)"),
    ("roubo_mercado_05.mp4", "Furto e evasão de corredor (CCTV 5)")
]

analyzer = TheftAnalyzer()
alert = AlertManager(evidencias_dir=os.path.join(base_dir, "evidencias"), play_sound=False)

print("\n" + "="*70)
print("  AVALIANDO DETECÇÃO DA IA NOS 5 VÍDEOS DE ROUBO REAIS")
print("="*70 + "\n")

total_videos = len(videos)
detected_thefts = 0
results_summary = []

for filename, description in videos:
    video_path = os.path.join(base_dir, "videos_teste", filename)
    print(f"▶️ Testando: {filename} ({description})...")
    
    report = analyzer.analyze_clip(video_path)
    is_theft = report.evento_detectado and (report.nivel_risco in [RiskLevel.ROUBO_CONFIRMADO, RiskLevel.SUSPEITO])
    
    if is_theft:
        detected_thefts += 1
        status = "✅ DETECTADO COM SUCESSO"
        # Registra a evidência automaticamente
        alert.trigger(video_path, report)
    else:
        status = "❌ FALHA NA DETECÇÃO"
        
    results_summary.append({
        "video": filename,
        "status": status,
        "risco": report.nivel_risco.value,
        "confianca": f"{report.confianca:.1f}%",
        "momento": f"{report.timestamp_segundo:.2f}s",
        "descricao": report.descricao_acao[:60] + "..."
    })

accuracy = (detected_thefts / total_videos) * 100.0

print("\n" + "="*70)
print("  RESUMO FINAL DE DESEMPENHO")
print("="*70)
print(f"Total de Vídeos Analisados : {total_videos}")
print(f"Roubos/Furtos Detectados   : {detected_thefts}")
print(f"Taxa de Detecção da IA     : {accuracy:.1f}%\n")

for r in results_summary:
    print(f" • {r['video']}: {r['status']} | Nível: {r['risco']} | Confiança: {r['confianca']} | Momento: {r['momento']}")

print("="*70 + "\n")
