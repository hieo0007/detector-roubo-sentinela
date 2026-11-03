import urllib.request
import urllib.parse
import json

path = urllib.parse.quote('DCSASS_Dataset')
url = f'https://huggingface.co/api/datasets/Centrique/tcc-shoplifting/tree/main/{path}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        for item in data:
            print(item.get('path'))
except Exception as e:
    print('Erro:', e)
