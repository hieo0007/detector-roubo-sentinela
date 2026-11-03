import os
import sys
import csv
import urllib.request
import urllib.parse
from typing import List, Dict

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
videos_dir = os.path.join(base_dir, "videos_teste")
gabarito_csv = os.path.join(videos_dir, "gabarito.csv")
os.makedirs(videos_dir, exist_ok=True)

# Lista selecionada de 25 videos NORMAL e 25 videos FURTO_LOJA do dataset Centrique/tcc-shoplifting
DATASET_VIDEOS: List[Dict[str, str]] = [
    # 25 VIDEOS NORMAIS (MNNIT e Dataset 2.0)
    {"local": "mnnit_normal_01.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (1).mp4"},
    {"local": "mnnit_normal_02.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (2).mp4"},
    {"local": "mnnit_normal_03.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (3).mp4"},
    {"local": "mnnit_normal_04.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (4).mp4"},
    {"local": "mnnit_normal_05.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (5).mp4"},
    {"local": "mnnit_normal_06.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (6).mp4"},
    {"local": "mnnit_normal_07.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (7).mp4"},
    {"local": "mnnit_normal_08.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (8).mp4"},
    {"local": "mnnit_normal_09.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (9).mp4"},
    {"local": "mnnit_normal_10.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (10).mp4"},
    {"local": "mnnit_normal_11.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (11).mp4"},
    {"local": "mnnit_normal_12.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (12).mp4"},
    {"local": "mnnit_normal_13.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (13).mp4"},
    {"local": "ds2_normal_01.mp4", "cat": "NORMAL", "remote": "Shoplifting Dataset 2.0/normal/shop_lifter_n_1.mp4"},
    {"local": "ds2_normal_03.mp4", "cat": "NORMAL", "remote": "Shoplifting Dataset 2.0/normal/shop_lifter_n_3.mp4"},
    {"local": "ds2_normal_06.mp4", "cat": "NORMAL", "remote": "Shoplifting Dataset 2.0/normal/shop_lifter_n_6.mp4"},
    {"local": "ds2_normal_08.mp4", "cat": "NORMAL", "remote": "Shoplifting Dataset 2.0/normal/shop_lifter_n_8.mp4"},
    {"local": "ds2_normal_11.mp4", "cat": "NORMAL", "remote": "Shoplifting Dataset 2.0/normal/shop_lifter_n_11.mp4"},
    {"local": "mnnit_normal_14.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (14).mp4"},
    {"local": "mnnit_normal_15.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (15).mp4"},
    {"local": "mnnit_normal_16.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (16).mp4"},
    {"local": "mnnit_normal_17.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (17).mp4"},
    {"local": "mnnit_normal_18.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (18).mp4"},
    {"local": "mnnit_normal_19.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (19).mp4"},
    {"local": "mnnit_normal_20.mp4", "cat": "NORMAL", "remote": "Shoplifting - MNNIT/Normal/Normal (20).mp4"},

    # 25 VIDEOS DE FURTO (MNNIT e Dataset 2.0)
    {"local": "mnnit_theft_01.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (1).mp4"},
    {"local": "mnnit_theft_02.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (2).mp4"},
    {"local": "mnnit_theft_03.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (3).mp4"},
    {"local": "mnnit_theft_04.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (4).mp4"},
    {"local": "mnnit_theft_05.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (5).mp4"},
    {"local": "mnnit_theft_06.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (6).mp4"},
    {"local": "mnnit_theft_07.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (7).mp4"},
    {"local": "mnnit_theft_08.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (8).mp4"},
    {"local": "mnnit_theft_09.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (9).mp4"},
    {"local": "mnnit_theft_10.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (10).mp4"},
    {"local": "mnnit_theft_11.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (11).mp4"},
    {"local": "mnnit_theft_12.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (12).mp4"},
    {"local": "mnnit_theft_13.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (13).mp4"},
    {"local": "ds2_theft_01.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting Dataset 2.0/shoplifting/shop_lifter_0.mp4"},
    {"local": "ds2_theft_02.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting Dataset 2.0/shoplifting/shop_lifter_1.mp4"},
    {"local": "ds2_theft_03.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting Dataset 2.0/shoplifting/shop_lifter_2.mp4"},
    {"local": "ds2_theft_04.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting Dataset 2.0/shoplifting/shop_lifter_3.mp4"},
    {"local": "ds2_theft_05.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting Dataset 2.0/shoplifting/shop_lifter_4.mp4"},
    {"local": "ds2_theft_06.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting Dataset 2.0/shoplifting/shop_lifter_5.mp4"},
    {"local": "ds2_theft_07.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting Dataset 2.0/shoplifting/shop_lifter_6.mp4"},
    {"local": "ds2_theft_08.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting Dataset 2.0/shoplifting/shop_lifter_7.mp4"},
    {"local": "ds2_theft_09.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting Dataset 2.0/shoplifting/shop_lifter_8.mp4"},
    {"local": "ds2_theft_10.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting Dataset 2.0/shoplifting/shop_lifter_9.mp4"},
    {"local": "ds2_theft_11.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting Dataset 2.0/shoplifting/shop_lifter_10.mp4"},
    {"local": "ds2_theft_12.mp4", "cat": "FURTO_LOJA", "remote": "Shoplifting Dataset 2.0/shoplifting/shop_lifter_11.mp4"},
]

def make_url(remote_path: str) -> str:
    encoded = urllib.parse.quote(remote_path)
    return f"https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/{encoded}?download=true"

def setup_dataset():
    print(f"Configurando gabarito expandido de 50 videos ({len(DATASET_VIDEOS)} itens)...")
    
    # Escreve o novo gabarito.csv com links autenticos
    with open(gabarito_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["arquivo", "esperado", "origem"])
        for item in DATASET_VIDEOS:
            url = make_url(item["remote"])
            writer.writerow([item["local"], item["cat"], url])
    
    print(f"Gabarito gravado em: {gabarito_csv}")

    # Faz download dos que faltam
    total = len(DATASET_VIDEOS)
    downloaded = 0
    skipped = 0

    for idx, item in enumerate(DATASET_VIDEOS, 1):
        dest_path = os.path.join(videos_dir, item["local"])
        url = make_url(item["remote"])

        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000:
            skipped += 1
            continue

        print(f"[{idx}/{total}] Baixando: {item['local']}...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp, open(dest_path, "wb") as f_out:
                f_out.write(resp.read())
            size_mb = os.path.getsize(dest_path) / (1024 * 1024)
            print(f"  -> Concluido ({size_mb:.2f} MB)")
            downloaded += 1
        except Exception as e:
            print(f"  -> ERRO ao baixar {item['local']}: {e}")

    print(f"\nFinalizado: {downloaded} baixados, {skipped} ja existiam.")

if __name__ == "__main__":
    setup_dataset()
