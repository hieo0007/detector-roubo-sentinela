import os
import sys
import csv
import json
import time
from datetime import datetime
from typing import List, Dict, Any

# Garante importacao do pacote src a partir da raiz do projeto
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from src.analyzer import SecurityAnalyzer
from src.models import RiskLevel, EventType


def run_benchmark(
    gabarito_path: str = "videos_teste/gabarito.csv",
    output_dir: str = "resultados",
    max_videos: int = None
) -> Dict[str, Any]:
    abs_gabarito = os.path.join(base_dir, gabarito_path) if not os.path.isabs(gabarito_path) else gabarito_path
    abs_output = os.path.join(base_dir, output_dir) if not os.path.isabs(output_dir) else output_dir
    os.makedirs(abs_output, exist_ok=True)

    if not os.path.exists(abs_gabarito):
        print(f"[ERRO] Gabarito nao encontrado em: {abs_gabarito}")
        sys.exit(1)

    with open(abs_gabarito, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if max_videos and max_videos > 0:
        rows = rows[:max_videos]

    analyzer = SecurityAnalyzer()
    model_version = "YOLOv8n + Gemini 3.5 Flash Lite"

    print("\n" + "="*80)
    print(f"  BENCHMARK SENTINELA - EXECUCAO EM CENARIOS DE TESTE")
    print(f"  Modelo: {model_version} | Gabarito: {os.path.basename(abs_gabarito)}")
    print("="*80 + "\n")

    results: List[Dict[str, Any]] = []
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total_time = 0.0

    for idx, row in enumerate(rows, start=1):
        filename = row["arquivo"].strip()
        expected = row["esperado"].strip().upper()
        origem = row.get("origem", "").strip()

        video_path = os.path.join(base_dir, "videos_teste", filename)
        if not os.path.exists(video_path):
            print(f"[{idx}/{len(rows)}] [PULADO] Arquivo nao encontrado: {filename}")
            continue

        print(f"[{idx}/{len(rows)}] Analisando: {filename} (Esperado: {expected})...")
        t0 = time.time()
        try:
            report = analyzer.analyze_clip(video_path)
            elapsed = round(time.time() - t0, 2)
        except Exception as e:
            elapsed = round(time.time() - t0, 2)
            print(f"  [FALHA DE PROCESSAMENTO] {e}")
            results.append({
                "arquivo": filename,
                "esperado": expected,
                "classificacao": "ERRO",
                "risco": "ERRO",
                "confianca": 0.0,
                "tempo_segundos": elapsed,
                "status": "ERRO_PROCESSAMENTO",
                "detalhe": str(e),
                "origem": origem
            })
            continue

        total_time += elapsed

        is_crime_expected = (expected != "NORMAL")
        is_crime_detected = report.evento_detectado and (
            report.nivel_risco in [RiskLevel.ALERTA_MAXIMO, RiskLevel.SUSPEITO]
        )

        if is_crime_expected and is_crime_detected:
            status = "ACERTO_POSITIVO"
            tp += 1
        elif not is_crime_expected and not is_crime_detected:
            status = "ACERTO_NEGATIVO"
            tn += 1
        elif not is_crime_expected and is_crime_detected:
            status = "FALSO_POSITIVO"
            fp += 1
        else:
            status = "FALSO_NEGATIVO"
            fn += 1

        print(f"  Status: {status} | Risco: {report.nivel_risco.value} | Conf: {report.confianca:.1f}% | Tempo: {elapsed}s")
        print(f"  Laudo: {report.descricao_acao[:80]}...")

        results.append({
            "arquivo": filename,
            "esperado": expected,
            "classificacao": report.tipo_evento.value,
            "risco": report.nivel_risco.value,
            "confianca": report.confianca,
            "tempo_segundos": elapsed,
            "status": status,
            "timestamp_segundo": report.timestamp_segundo,
            "descricao": report.descricao_acao,
            "origem": origem
        })

    total_valid = tp + tn + fp + fn
    accuracy = round(((tp + tn) / total_valid * 100.0), 2) if total_valid > 0 else 0.0
    precision = round((tp / (tp + fp) * 100.0), 2) if (tp + fp) > 0 else 0.0
    recall = round((tp / (tp + fn) * 100.0), 2) if (tp + fn) > 0 else 0.0
    avg_time = round(total_time / total_valid, 2) if total_valid > 0 else 0.0

    today_str = datetime.now().strftime("%Y-%m-%d")
    output_data = {
        "data_execucao": today_str,
        "versao_modelo": model_version,
        "total_videos": total_valid,
        "acertos": tp + tn,
        "acertos_positivos": tp,
        "acertos_negativos": tn,
        "falsos_positivos": fp,
        "falsos_negativos": fn,
        "acuracia_percentual": accuracy,
        "precisao_percentual": precision,
        "recall_percentual": recall,
        "tempo_medio_segundos": avg_time,
        "tempo_total_segundos": round(total_time, 2),
        "resultados": results
    }

    # Salva JSON
    json_path = os.path.join(abs_output, f"benchmark_{today_str}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    # Salva Markdown
    md_path = os.path.join(abs_output, f"benchmark_{today_str}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Relatório de Benchmark - Sentinela CCTV\n\n")
        f.write(f"- **Data de Execução**: {today_str}\n")
        f.write(f"- **Versão do Modelo**: {model_version}\n")
        f.write(f"- **Total de Vídeos Avaliados**: {total_valid}\n")
        f.write(f"- **Acurácia Global**: {accuracy}%\n")
        f.write(f"- **Precisão (Precision)**: {precision}%\n")
        f.write(f"- **Sensibilidade (Recall)**: {recall}%\n")
        f.write(f"- **Falsos Positivos**: {fp}\n")
        f.write(f"- **Falsos Negativos**: {fn}\n")
        f.write(f"- **Tempo Médio por Vídeo**: {avg_time}s\n\n")
        f.write("## Tabela Detalhada por Cenário\n\n")
        f.write("| Arquivo | Esperado | Classificação | Risco | Confiança | Tempo (s) | Status |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for r in results:
            f.write(f"| `{r['arquivo']}` | {r['esperado']} | {r['classificacao']} | {r['risco']} | {r['confianca']:.1f}% | {r['tempo_segundos']}s | {r['status']} |\n")

    print("\n" + "="*80)
    print("  RESUMO CONSOLIDADO DO BENCHMARK")
    print("="*80)
    print(f"Total de Videos   : {total_valid}")
    print(f"Acertos           : {tp + tn} ({accuracy}%)")
    print(f"Falsos Positivos  : {fp}")
    print(f"Falsos Negativos  : {fn}")
    print(f"Precisao          : {precision}%")
    print(f"Recall            : {recall}%")
    print(f"Tempo Medio       : {avg_time}s / video")
    print(f"Relatorios Salvos :")
    print(f"  - {json_path}")
    print(f"  - {md_path}")
    print("="*80 + "\n")

    return output_data


if __name__ == "__main__":
    max_v = None
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        max_v = int(sys.argv[1])
    run_benchmark(max_videos=max_v)
