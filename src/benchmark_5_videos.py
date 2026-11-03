import os
import sys

# Redireciona a execucao legada para o novo motor unificado de benchmark
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from scripts.benchmark import run_benchmark

if __name__ == "__main__":
    print("[LEGACY WRAPPER] Redirecionando para scripts/benchmark.py (5 primeiros videos)...")
    run_benchmark(max_videos=5)
