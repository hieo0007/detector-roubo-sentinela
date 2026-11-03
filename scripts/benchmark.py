import os
import sys
import csv
import json
import time
import argparse
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
    max_videos: int = None,
    tag: str = "benchmark",
    prompt_version: str = "v3"
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
    model_version = f"YOLOv8n + Gemini 3.5 Flash Lite (prompt: {prompt_version})"

    print("\n" + "="*80)
    print(f"  BENCHMARK SENTINELA - EXECUCAO EM CENARIOS DE TESTE")
    print(f"  Modelo: {model_version} | Tag: {tag} | Gabarito: {os.path.basename(abs_gabarito)}")
    print("="*80 + "\n")

    results: List[Dict[str, Any]] = []
    erros_ia_list: List[Dict[str, Any]] = []

    tp = 0
    tn = 0
    fp = 0
    fn = 0
    erros_classe = 0

    tempos_totais: List[float] = []
    tempos_gemini: List[float] = []

    for idx, row in enumerate(rows, start=1):
        filename = row["arquivo"].strip()
        expected = row["esperado"].strip().upper()
        origem = row.get("origem", "").strip()

        video_path = os.path.join(base_dir, "videos_teste", filename)
        if not os.path.exists(video_path):
            print(f"[{idx}/{len(rows)}] [PULADO] Arquivo nao encontrado: {filename}")
            continue

        print(f"[{idx}/{len(rows)}] Analisando: {filename} (Esperado: {expected})...")

        # Execucao com retentativa automatica de ate 2 vezes caso ocorra erro na IA
        report = None
        elapsed_total = 0.0
        max_attempts = 3  # tentativa inicial + 2 retentativas

        for attempt in range(1, max_attempts + 1):
            t0 = time.time()
            try:
                report = analyzer.analyze_clip(video_path, prompt_version=prompt_version)
                elapsed_total = round(time.time() - t0, 2)
            except Exception as e:
                elapsed_total = round(time.time() - t0, 2)
                print(f"  [AVISO] Excecao na tentativa {attempt}/{max_attempts}: {e}")
                report = None

            if report and not report.erro and report.tipo_evento != EventType.ERRO_ANALISE:
                break

            if attempt < max_attempts:
                print(f"  [AVISO] Tentativa {attempt}/{max_attempts} falhou com ERRO_IA. Retentando em 2 segundos...")
                time.sleep(2.0)

        # Trata falha persistente da IA
        if report is None or report.erro or report.tipo_evento == EventType.ERRO_ANALISE:
            status = "ERRO_IA"
            erro_msg = report.erro_detalhe if report else "Falha de comunicacao ou excecao nao tratada"
            print(f"  Status: {status} | Falha na IA persistiu apos {max_attempts} tentativas.")
            item_data = {
                "arquivo": filename,
                "esperado": expected,
                "classificacao": "ERRO_ANALISE",
                "risco": report.nivel_risco.value if report else "SUSPEITO",
                "confianca": report.confianca if report else 0.0,
                "tempo_total_segundos": elapsed_total,
                "tempo_gemini_segundos": getattr(report, "tempo_ia_segundos", None),
                "status": status,
                "detalhe": erro_msg,
                "origem": origem
            }
            results.append(item_data)
            erros_ia_list.append(item_data)
            continue

        # Tempos medidos
        tempo_gemini = getattr(report, "tempo_ia_segundos", None)
        tempos_totais.append(elapsed_total)
        if tempo_gemini is not None:
            tempos_gemini.append(tempo_gemini)

        # Regras estritas de avaliacao:
        # Acerto positivo exige classificacao exatamente igual ao esperado
        got_type = report.tipo_evento.value
        is_crime_expected = (expected != "NORMAL")
        is_crime_detected = report.evento_detectado and (
            report.nivel_risco in [RiskLevel.ALERTA_MAXIMO, RiskLevel.SUSPEITO]
        )

        if is_crime_expected:
            if got_type == expected:
                status = "ACERTO_POSITIVO"
                tp += 1
            elif is_crime_detected:
                status = "ERRO_CLASSE"
                erros_classe += 1
            else:
                status = "FALSO_NEGATIVO"
                fn += 1
        else:
            if got_type == "NORMAL" and not is_crime_detected:
                status = "ACERTO_NEGATIVO"
                tn += 1
            else:
                status = "FALSO_POSITIVO"
                fp += 1

        t_gemini_str = f"{tempo_gemini}s" if tempo_gemini is not None else "N/A"
        print(f"  Status: {status} | Tipo: {got_type} | Risco: {report.nivel_risco.value} | Conf: {report.confianca:.1f}%")
        print(f"  Tempo Total: {elapsed_total}s | Tempo Gemini: {t_gemini_str}")
        print(f"  Laudo: {report.descricao_acao[:80]}...")

        results.append({
            "arquivo": filename,
            "esperado": expected,
            "classificacao": got_type,
            "risco": report.nivel_risco.value,
            "confianca": report.confianca,
            "tempo_total_segundos": elapsed_total,
            "tempo_gemini_segundos": tempo_gemini,
            "status": status,
            "timestamp_segundo": report.timestamp_segundo,
            "descricao": report.descricao_acao,
            "origem": origem
        })

    # Metricas excluem ERRO_IA (mostrado a parte conforme diretriz)
    total_valid = tp + tn + fp + fn + erros_classe
    acertos = tp + tn
    accuracy = round((acertos / total_valid * 100.0), 2) if total_valid > 0 else 0.0

    # Precisao: acertos positivos sobre todos os crimes sinalizados (TP + FP + ERRO_CLASSE)
    denom_precisao = tp + fp + erros_classe
    precision = round((tp / denom_precisao * 100.0), 2) if denom_precisao > 0 else 0.0

    # Recall: acertos positivos sobre todos os crimes esperados (TP + FN + ERRO_CLASSE)
    denom_recall = tp + fn + erros_classe
    recall = round((tp / denom_recall * 100.0), 2) if denom_recall > 0 else 0.0

    avg_total_time = round(sum(tempos_totais) / len(tempos_totais), 2) if tempos_totais else 0.0
    avg_gemini_time = round(sum(tempos_gemini) / len(tempos_gemini), 2) if tempos_gemini else 0.0

    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    timestamp_str = now.strftime("%Y-%m-%d_%H%M")
    file_prefix = f"benchmark_{timestamp_str}_{tag}"

    output_data = {
        "timestamp": timestamp_str,
        "tag": tag,
        "versao_prompt": prompt_version,
        "data_execucao": today_str,
        "versao_modelo": model_version,
        "total_videos_processados": len(results),
        "total_videos_validos": total_valid,
        "erros_ia_total": len(erros_ia_list),
        "acertos_totais": acertos,
        "acertos_positivos": tp,
        "acertos_negativos": tn,
        "erros_classe": erros_classe,
        "falsos_positivos": fp,
        "falsos_negativos": fn,
        "acuracia_percentual": accuracy,
        "precisao_percentual": precision,
        "recall_percentual": recall,
        "tempo_medio_total_segundos": avg_total_time,
        "tempo_medio_gemini_segundos": avg_gemini_time,
        "resultados": results
    }

    # Salva JSON com nome unico contendo data, hora e rotulo/tag
    json_path = os.path.join(abs_output, f"{file_prefix}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    # Salva Markdown com nome unico contendo data, hora e rotulo/tag
    md_path = os.path.join(abs_output, f"{file_prefix}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Relatório de Benchmark - Sentinela CCTV\n\n")
        f.write(f"- **Data de Execução**: {timestamp_str}\n")
        f.write(f"- **Rótulo / Tag**: `{tag}`\n")
        f.write(f"- **Versão do Prompt**: `{prompt_version}`\n")
        f.write(f"- **Versão do Modelo**: {model_version}\n")
        f.write(f"- **Total de Vídeos Válidos Avaliados**: {total_valid}\n")
        f.write(f"- **Erros de Comunicação / API (ERRO_IA)**: {len(erros_ia_list)} (excluídos das métricas de acurácia)\n")
        f.write(f"- **Acurácia Global**: {accuracy}%\n")
        f.write(f"- **Precisão (Precision)**: {precision}%\n")
        f.write(f"- **Sensibilidade (Recall)**: {recall}%\n")
        f.write(f"- **Erros de Classe (Crime Detectado com Tipo Errado)**: {erros_classe}\n")
        f.write(f"- **Falsos Positivos**: {fp}\n")
        f.write(f"- **Falsos Negativos**: {fn}\n")
        f.write(f"- **Tempo Médio Total por Vídeo**: {avg_total_time}s\n")
        f.write(f"- **Tempo Médio da Chamada ao Gemini**: {avg_gemini_time}s\n\n")
        f.write("## Tabela Detalhada por Cenário\n\n")
        f.write("| Arquivo | Esperado | Classificação | Risco | Confiança | Tempo Total (s) | Tempo Gemini (s) | Status | Origem |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for r in results:
            tg_str = f"{r['tempo_gemini_segundos']}s" if r.get('tempo_gemini_segundos') is not None else "-"
            f.write(f"| `{r['arquivo']}` | {r['esperado']} | {r['classificacao']} | {r['risco']} | {r['confianca']:.1f}% | {r['tempo_total_segundos']}s | {tg_str} | {r['status']} | {r.get('origem', '')} |\n")

    print("\n" + "="*80)
    print("  RESUMO CONSOLIDADO DO BENCHMARK")
    print("="*80)
    print(f"Tag / Rotulo            : {tag}")
    print(f"Versao do Prompt        : {prompt_version}")
    print(f"Total de Videos Validos : {total_valid}")
    print(f"Falhas na IA (ERRO_IA)  : {len(erros_ia_list)}")
    print(f"Acertos Totais          : {acertos} ({accuracy}%)")
    print(f"Erros de Classe         : {erros_classe}")
    print(f"Falsos Positivos        : {fp}")
    print(f"Falsos Negativos        : {fn}")
    print(f"Precisao                : {precision}%")
    print(f"Recall                  : {recall}%")
    print(f"Tempo Medio Total       : {avg_total_time}s / video")
    print(f"Tempo Medio Gemini      : {avg_gemini_time}s / chamada")
    print(f"Relatorios Salvos :")
    print(f"  - {json_path}")
    print(f"  - {md_path}")
    print("="*80 + "\n")

    return output_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark Sentinela CCTV")
    parser.add_argument("--gabarito", type=str, default="videos_teste/gabarito.csv", help="Caminho do CSV de gabarito")
    parser.add_argument("--tag", type=str, default="benchmark", help="Rotulo identificador da rodada")
    parser.add_argument("--prompt-version", "--prompt_version", type=str, default="v3", choices=["v3", "novo", "legacy", "antigo"], help="Versao do prompt (v3/novo ou legacy/antigo)")
    parser.add_argument("--max-videos", "--max_videos", type=int, default=None, help="Limite maximo de videos a processar")
    parser.add_argument("legacy_max_videos", nargs="?", type=int, default=None, help="Argumento posicional retrocompativel para max_videos")

    args = parser.parse_args()
    limit = args.max_videos if args.max_videos is not None else args.legacy_max_videos

    run_benchmark(
        gabarito_path=args.gabarito,
        max_videos=limit,
        tag=args.tag,
        prompt_version=args.prompt_version
    )
