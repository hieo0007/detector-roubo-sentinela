import os
import urllib.request
import urllib.parse
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
videos_dir = os.path.join(base_dir, "videos_teste")
os.makedirs(videos_dir, exist_ok=True)

downloads = [
    # Categoria: Pessoas Andando / Circulação Normal
    {
        "local": "pedestre_normal_01.mp4",
        "remote": "Shoplifting - MNNIT/Normal/Normal (1).mp4",
        "category": "NORMAL",
        "description": "Pedestres e clientes andando no ambiente (Normal 01)"
    },
    {
        "local": "pedestre_normal_02.mp4",
        "remote": "Shoplifting Dataset 2.0/normal/shop_lifter_n_1.mp4",
        "category": "NORMAL",
        "description": "Cliente circulando pelo corredor com mãos livres (Normal 02)"
    },
    {
        "local": "pedestre_normal_03.mp4",
        "remote": "Shoplifting - MNNIT/Normal/Normal (15).mp4",
        "category": "NORMAL",
        "description": "Movimentação contínua de pedestres em trânsito (Normal 03)"
    },
    # Categoria: Assalto e Furto Real
    {
        "local": "assalto_furto_01.mp4",
        "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (1).mp4",
        "category": "THEFT",
        "description": "Furto real de mercadoria em prateleira de comércio (Furto 01)"
    },
    {
        "local": "assalto_furto_02.mp4",
        "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (10).mp4",
        "category": "THEFT",
        "description": "Subtração rápida e ocultação sob jaqueta (Furto 02)"
    },
    {
        "local": "assalto_furto_03.mp4",
        "remote": "Shoplifting - MNNIT/Shoplifting/Shoplifting (15).mp4",
        "category": "THEFT",
        "description": "Furto por apropriação indevida e fuga do local (Furto 03)"
    }
]

print("Iniciando download dos videos da internet...")
for item in downloads:
    dest_path = os.path.join(videos_dir, item["local"])
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 100000:
        print(f"[OK] Ja baixado: {item['local']} ({os.path.getsize(dest_path)/(1024*1024):.2f} MB)")
        continue

    encoded = urllib.parse.quote(item["remote"])
    url = f"https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/{encoded}?download=true"
    print(f"Baixando: {item['local']} de {item['remote']}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp, open(dest_path, "wb") as f:
            f.write(resp.read())
        size_mb = os.path.getsize(dest_path) / (1024 * 1024)
        print(f" -> Concluido: {item['local']} ({size_mb:.2f} MB)")
    except Exception as e:
        print(f" -> Erro ao baixar {item['local']}: {e}")

print("\nTodos os downloads concluidos!")
