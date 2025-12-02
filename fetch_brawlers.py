import requests
import json
import os

API_URL = "https://api.brawlapi.com/v1/brawlers"

def slugify(name: str) -> str:
    """
    Dosya ismi için basit slug üretir.
    Örn: '8-Bit' -> '8-bit', 'El Primo' -> 'el-primo'
    """
    s = name.lower()
    for ch in [" ", "'", "’", "."]:
        s = s.replace(ch, "-")

    tr_map = {
        "ç": "c", "ğ": "g", "ı": "i",
        "ö": "o", "ş": "s", "ü": "u"
    }
    for k, v in tr_map.items():
        s = s.replace(k, v)

    while "--" in s:
        s = s.replace("--", "-")

    return s

print("⏳ Brawler verileri indiriliyor...")

response = requests.get(API_URL, timeout=15)

if response.status_code != 200:
    print("❌ API bağlantı hatası:", response.status_code)
    raise SystemExit()

data = response.json()
b_list = data.get("list", [])

output = []

for b in b_list:
    name = b["name"]
    rarity = b["rarity"]["name"]      # Örn: 'Rare', 'Legendary'
    bclass = b["class"]["name"]       # Örn: 'Damage Dealer', 'Tank'

    # API'de description pek yok, varsa alalım yoksa boş geçelim
    description = b.get("description", "")
    description = description.replace("\n", " ") if description else ""

    # Resim dosya adı: slugify(name).png
    # Örn: 'El Primo' -> 'el-primo.png'
    slug = slugify(name)
    image_filename = f"{slug}.png"

    item = {
        "name": name,
        "rarity": rarity,
        "role": bclass,          # Şimdilik rol = class, sonra elle düzeltebilirsin
        "class": bclass,
        "best_build": "",        # Sonradan dolduracağız
        "best_modes": [],        # Sonradan dolduracağız
        "description": description,
        "image": image_filename
    }

    output.append(item)

os.makedirs("data", exist_ok=True)

out_path = os.path.join("data", "brawlers.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✅ {len(output)} brawler başarıyla kaydedildi! → {out_path}")
