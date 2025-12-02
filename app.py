# app.py

from flask import Flask, render_template, request, abort
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")


# ------------ Yardımcı fonksiyonlar ------------

def load_maps():
    """data/maps.json dosyasını oku."""
    path = os.path.join(DATA_DIR, "maps.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_brawlers():
    """data/brawlers.json dosyasını oku."""
    path = os.path.join(DATA_DIR, "brawlers.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def slugify(name: str) -> str:
    """
    İsimden URL için slug üret.
    Örn: 'Larry & Lawrie' -> 'larry-lawrie'
    """
    s = name.lower()

    replacements = {
        "ş": "s",
        "ı": "i",
        "ö": "o",
        "ü": "u",
        "ğ": "g",
        "ç": "c",
        "&": "-",
        "'": "",
    }
    for old, new in replacements.items():
        s = s.replace(old, new)

    # Harf/rakam dışındaki her şeyi '-' yap, fazla '-'ları temizle
    result = []
    last_dash = False
    for ch in s:
        if ch.isalnum():
            result.append(ch)
            last_dash = False
        else:
            if not last_dash:
                result.append("-")
                last_dash = True

    s = "".join(result).strip("-")
    return s


# ------------ Ana sayfa ------------

@app.route("/")
def home():
    return render_template("index.html")


# ------------ Haritalar ------------

@app.route("/maps")
def maps():
    maps_data = load_maps()

    selected_mode = request.args.get("mode")

    if selected_mode and selected_mode != "ALL":
        maps_data = [
            m for m in maps_data
            if m.get("mode") == selected_mode
        ]

    return render_template(
        "maps.html",
        maps=maps_data,
        selected_mode=selected_mode,
    )


@app.route("/maps/<slug>")
def map_detail(slug):
    maps_data = load_maps()

    for m in maps_data:
        if slugify(m["name"]) == slug:
            m_detail = dict(m)
            m_detail["slug"] = slug
            return render_template("map_detail.html", map=m_detail)

    abort(404)


# ------------ Brawlers listesi ------------

@app.route("/brawlers")
def brawlers():
    raw_brawlers = load_brawlers()
    selected_rarity = request.args.get("rarity")

    brawlers_data = []
    for b in raw_brawlers:
        b_copy = dict(b)
        b_copy["slug"] = slugify(b_copy["name"])
        brawlers_data.append(b_copy)

    if selected_rarity and selected_rarity != "ALL":
        brawlers_data = [
            b for b in brawlers_data
            if b.get("rarity") == selected_rarity
        ]

    return render_template(
        "brawlers.html",
        brawlers=brawlers_data,
        selected_rarity=selected_rarity,
    )


# ------------ Tek brawler detayı ------------

@app.route("/brawlers/<slug>")
def brawler_detail(slug):
    raw_brawlers = load_brawlers()

    for b in raw_brawlers:
        if slugify(b["name"]) == slug:
            b_detail = dict(b)
            b_detail["slug"] = slug
            return render_template("brawler_detail.html", brawler=b_detail)

    abort(404)


# ------------ Çalıştır ------------

if __name__ == "__main__":
    app.run(debug=True)
