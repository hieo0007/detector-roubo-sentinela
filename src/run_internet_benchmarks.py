import os
import sys
import json
import time

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from src.analyzer import SecurityAnalyzer

analyzer = SecurityAnalyzer()

test_cases = [
    # Categoria 1: Pessoas Andando / Circulação Normal
    {
        "filename": "pedestre_normal_01.mp4",
        "expected": "NORMAL",
        "label": "Pessoas Andando no Ambiente (CCTV 01)"
    },
    {
        "filename": "pedestre_normal_02.mp4",
        "expected": "NORMAL",
        "label": "Cliente Circulando com Maos Livres (CCTV 02)"
    },
    {
        "filename": "pedestre_normal_03.mp4",
        "expected": "NORMAL",
        "label": "Pedestres em Transito Regular (CCTV 03)"
    },
    # Categoria 2: Assalto e Furto Real
    {
        "filename": "assalto_furto_01.mp4",
        "expected": "FURTO_LOJA",
        "label": "Furto Real de Mercadoria em Prateleira (CCTV 04)"
    },
    {
        "filename": "assalto_furto_02.mp4",
        "expected": "FURTO_LOJA",
        "label": "Subtracao e Ocultacao sob Jaqueta (CCTV 05)"
    },
    {
        "filename": "assalto_furto_03.mp4",
        "expected": "FURTO_LOJA",
        "label": "Furto de Produto e Fuga (CCTV 06)"
    }
]

print("="*75)
print("INICIANDO BATERIA DE TESTES NOS VIDEOS DA INTERNET (YOLO-Pose + Gemini)")
print("="*75)

results = []

for idx, tc in enumerate(test_cases, 1):
    video_path = os.path.join(base_dir, "videos_teste", tc["filename"])
    if not os.path.exists(video_path):
        print(f"[{idx}/6] Arquivo nao encontrado: {tc['filename']}")
        continue

    print(f"\n[{idx}/6] Testando: {tc['label']} ({tc['filename']})...")
    t0 = time.time()
    
    def on_prog(pct, cur, tot, msg):
        pass # Silencioso para relatorio limpo

    try:
        report = analyzer.analyze_clip(video_path, progress_callback=on_prog)
        elapsed = time.time() - t0
        
        is_normal_expected = tc["expected"] == "NORMAL"
        is_normal_got = report.nivel_risco.value == "NORMAL"
        is_success = (is_normal_expected and is_normal_got) or (not is_normal_expected and not is_normal_got)

        status_icon = "[ACERTO]" if is_success else "[FALHA]"
        print(f"  {status_icon} Tempo: {elapsed:.1f}s | Risco: {report.nivel_risco.value} ({report.confianca:.1f}%)")
        print(f"  Acao: {report.descricao_acao[:90]}...")
        if report.timestamp_segundo > 0:
            print(f"  Instante Detectado: {report.timestamp_segundo:.1f}s")

        results.append({
            "test": tc["label"],
            "filename": tc["filename"],
            "expected": tc["expected"],
            "got": report.nivel_risco.value,
            "confidence": report.confianca,
            "elapsed": round(elapsed, 1),
            "timestamp": report.timestamp_segundo,
            "description": report.descricao_acao,
            "success": is_success
        })
    except Exception as e:
        print(f"  [ERRO] Falha ao testar {tc['filename']}: {e}")

print("\n" + "="*75)
print("RESUMO CONSOLIDADO DOS TESTES:")
print("="*75)
success_count = sum(1 for r in results if r["success"])
print(f"Taxa de Acerto: {success_count}/{len(results)} ({success_count/len(results)*100:.1f}%)")
for r in results:
    mark = "OK" if r["success"] else "ERRO"
    print(f" - [{mark}] {r['test']}: Esperado={r['expected']} | Obtido={r['got']} ({r['confidence']}%) em {r['elapsed']}s")
