import os
import urllib.request
import urllib.parse

videos_to_download = [
    ("roubo_mercado_01.mp4", "Shoplifting Dataset 2.0/shoplifting/shop_lifter_0.mp4"),
    ("roubo_mercado_02.mp4", "Shoplifting Dataset 2.0/shoplifting/shop_lifter_1.mp4"),
    ("roubo_mercado_03.mp4", "Shoplifting Dataset 2.0/shoplifting/shop_lifter_10.mp4"),
    ("roubo_mercado_04.mp4", "Shoplifting Dataset 2.0/shoplifting/shop_lifter_11.mp4"),
    ("roubo_mercado_05.mp4", "Shoplifting Dataset 2.0/shoplifting/shop_lifter_100.mp4")
]

dest_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "videos_teste")
os.makedirs(dest_dir, exist_ok=True)

for local_name, hf_path in videos_to_download:
    dest_file = os.path.join(dest_dir, local_name)
    if os.path.exists(dest_file) and os.path.getsize(dest_file) > 100000:
        print(f"[PULADO] Ja existe: {local_name}")
        continue
    
    encoded_path = urllib.parse.quote(hf_path)
    url = f"https://huggingface.co/datasets/Centrique/tcc-shoplifting/resolve/main/{encoded_path}?download=true"
    print(f"[BAIXANDO] {local_name}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp, open(dest_file, "wb") as out:
            out.write(resp.read())
        size_mb = os.path.getsize(dest_file) / (1024 * 1024)
        print(f"  [SUCESSO] Salvo {local_name} ({size_mb:.2f} MB)")
    except Exception as e:
        print(f"  [ERRO] Falha ao baixar {local_name}: {e}")

print("\nProcesso de download dos 5 videos de roubo concluido com sucesso!")
