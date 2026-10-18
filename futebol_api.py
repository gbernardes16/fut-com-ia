import requests
from datetime import date

BASE = "https://sportapi7.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": "39043382e9msh5c4e55f670dceb8p108e9cjsna89f9cbdcce",
    "X-RapidAPI-Host": "sportapi7.p.rapidapi.com",
}

today = date.today().strftime("%Y-%m-%d")
timezone_offset = 0

# ── Step 1: Enumerate football categories with matches today ────────
url = f"{BASE}/api/v1/sport/football/{today}/{timezone_offset}/categories"
resp = requests.get(url, headers=HEADERS)

if resp.status_code == 200:
    dados = resp.json()
    
    # Usamos o .get() para evitar que dê KeyError caso a chave venha vazia
    categories = dados.get("categories", [])
    
    if len(categories) > 0:
        print(f"Futebol categorias com jogos hoje ({today}):\n")
        for cat in categories:
            cat_info = cat.get("category", {})
            print(f"  id={cat_info.get('id')}  {cat_info.get('name')}")
    else:
        print(f"A API retornou sucesso, mas não há categorias com jogos para a data {today}.")
        print("Dica: Você pode testar direto o ID do Brasil (13) como fizemos antes!")
else:
    print(f"Erro na requisição: {resp.status_code} - {resp.text}")