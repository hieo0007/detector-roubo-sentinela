import os
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from src.analyzer import SecurityAnalyzer
from src.alert import AlertManager
from src.models import RiskLevel

videos = [
    ("roubo_mercado_01.mp4", "Furto em prateleira de mercado (CCTV 1)"),
    ("roubo_mercado_02.mp4", "Subtracao rapida de item em balcao (CCTV 2)"),
    ("roubo_mercado_03.mp4", "Ocultacao de produto em vestimenta (CCTV 3)"),
    ("roubo_mercado_04.mp4", "Apropriacao indevida de mercadoria (CCTV 4)"),
    ("roubo_mercado_05.mp4", "Furto e evasao de corredor (CCTV 5)")
]

analyzer = SecurityAnalyzer()
alert = AlertManager(evidencias_dir=os.path.join(base_dir, "evidencias"), play_sound=False)

print("\n" + "="*70)
print("  AVALIANDO DETECCAO DA IA NOS 5 VIDEOS DE ROUBO REAIS")
print("="*70 + "\n")

total_videos = len(videos)
detected_thefts = 0
results_summary = []

for filename, description in videos:
    video_path = os.path.join(base_dir, "videos_teste", filename)
    print(f"[TESTE] Testando: {filename} ({description})...")
    
    report = analyzer.analyze_clip(video_path)
    is_theft = report.evento_detectado and (report.nivel_risco in [RiskLevel.ALERTA_MAXIMO, RiskLevel.SUSPEITO])
    
    if is_theft:
        detected_thefts += 1
        status = "[OK] DETECTADO COM SUCESSO"
        # Registra a evidencia automaticamente
        alert.trigger(video_path, report)
    else:
        status = "[FALHA] NAO DETECTADO"
        
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
print(f"Total de Videos Analisados : {total_videos}")
print(f"Roubos/Furtos Detectados   : {detected_thefts}")
print(f"Taxa de Deteccao da IA     : {accuracy:.1f}%\n")

for r in results_summary:
    print(f" * {r['video']}: {r['status']} | Nivel: {r['risco']} | Confianca: {r['confianca']} | Momento: {r['momento']}")

print("="*70 + "\n")
