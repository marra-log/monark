#!/usr/bin/env python3
"""Lote de 24/11/2026: novas fotos + preços enviados pelo WhatsApp.

Lê as fotos de drive/raw/ (pasta ignorada pelo git), gera os .webp no mesmo
padrão do build_assets.py e atualiza js/products.json com as cores e os preços.
Preço fica por cor ("price"); o generate_site.py calcula o preço do produto.

Rodar uma vez, depois: python3 scripts/generate_site.py
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "drive/raw"
IMG_OUT = ROOT / "assets/products"


def img(n: str) -> str:
    return f"IMG-20261124-WA{n}.jpg"


# Fotos novas em modelos que já existem no site.
EXISTING = {
    "nike-fit": {
        "description": "Tênis Nike Fit com swoosh em contraste e solado creme. Disponível nas cores marrom e branco.",
        "colors": [
            {"id": "marrom", "add": [img("0159")], "price": 180},
            {"id": "branco", "name": "Branco", "add": [img("0160")], "price": 180},
        ],
    },
    "adidas-slip-on": {
        "description": "Tênis Adidas Slip On com elástico cruzado e bico clássico. Disponível nas cores preto (solado branco) e marrom (solado off-white).",
        "colors": [
            {"id": "preto", "add": [img("0206")], "price": 250},
            {"id": "marrom", "name": "Marrom", "add": [img("0207"), img("0208")], "price": 250},
        ],
    },
    "adidas-adizero": {
        "description": "Tênis Adidas Adizero Pro 4 com Lightstrike Pro no solado. Disponível nas cores preto e pink, branco e rose gold, branco e rosa, azul e rosa, e turquesa.",
        "colors": [
            {"id": "branco-rose", "add": [img("0146")], "price": 220},
            {"id": "turquesa", "name": "Turquesa", "add": [img("0201")], "price": 190},
        ],
    },
    "nike-air-force": {
        "description": "Tênis Nike Air Force. Disponível nas cores preto, branco com swoosh azul-marinho, preto com cadarço de corda e bordô com rosa em verniz.",
        "colors": [
            {"id": "preto-corda", "name": "Preto com cadarço de corda", "add": [img("0143")], "price": 200},
            {"id": "bordo-rosa", "name": "Bordô e rosa (verniz)", "add": [img("0158")], "price": 250},
        ],
    },
}

# Modelos novos (entram no topo do catálogo).
NEW = [
    {
        "slug": "new-balance-9060",
        "name": "New Balance 9060",
        "brand": "New Balance",
        "description": "Tênis New Balance 9060, cabedal em camurça e mesh com solado robusto. Disponível nas cores branco e cinza, cinza claro, e creme com bordô.",
        "colors": [
            {"id": "branco-cinza", "name": "Branco e cinza", "images": [img("0136")], "price": 200},
            {"id": "cinza-claro", "name": "Cinza claro", "images": [img("0137")], "price": 250},
            {"id": "creme-bordo", "name": "Creme e bordô", "images": [img("0138")], "price": 240},
        ],
    },
    {
        "slug": "new-balance-fresh-foam-x",
        "name": "New Balance Fresh Foam X",
        "brand": "New Balance",
        "description": "Tênis New Balance Fresh Foam X, de corrida, com entressola macia. Disponível em seis cores.",
        "colors": [
            {"id": "cinza", "name": "Cinza e branco", "images": [img("0135")], "price": 180},
            {"id": "azul-laranja", "name": "Azul e laranja", "images": [img("0152")], "price": 180},
            {"id": "limao", "name": "Limão", "images": [img("0153")], "price": 180},
            {"id": "preto-turquesa", "name": "Preto e turquesa", "images": [img("0154")], "price": 180},
            {"id": "preto", "name": "Preto", "images": [img("0155")], "price": 180},
            {"id": "marinho-limao", "name": "Marinho e limão", "images": [img("0156")], "price": 180},
        ],
    },
    {
        "slug": "new-balance-rebel",
        "name": "New Balance Rebel",
        "brand": "New Balance",
        "description": "Tênis New Balance Rebel na cor off-white com rosa.",
        "colors": [
            {"id": "rosa", "name": "Off-white e rosa", "images": [img("0150")], "price": 180},
        ],
    },
    {
        "slug": "nike-creme",
        "name": "Nike Running Creme",
        "brand": "Nike",
        "description": "Tênis Nike de corrida na cor creme, com swoosh marrom e solado caramelo.",
        "colors": [
            {"id": "creme-marrom", "name": "Creme e marrom", "images": [img("0142")], "price": 190},
        ],
    },
    {
        "slug": "nike-bege-rose",
        "name": "Nike Bege e Rose",
        "brand": "Nike",
        "description": "Tênis Nike bege com swoosh rose e calcanhar caramelo.",
        "colors": [
            {"id": "bege-rose", "name": "Bege e rose", "images": [img("0203")], "price": 170},
        ],
    },
    {
        "slug": "miu-miu",
        "name": "Miu Miu Camurça",
        "brand": "Miu Miu",
        "description": "Tênis Miu Miu em camurça marrom, com solado plataforma off-white.",
        "colors": [
            {"id": "marrom", "name": "Marrom", "images": [img("0200")], "price": 220},
        ],
    },
    {
        "slug": "reserva-branco",
        "name": "Reserva Branco",
        "brand": "Reserva",
        "description": "Tênis Reserva branco com solado caramelo.",
        "colors": [
            {"id": "branco-caramelo", "name": "Branco e caramelo", "images": [img("0356")], "price": 190},
        ],
    },
    {
        "slug": "tenis-plataforma-branco",
        "name": "Tênis Plataforma Branco",
        "brand": "Casual",
        "description": "Tênis casual todo branco, em couro, com solado plataforma.",
        "colors": [
            {"id": "branco", "name": "Branco", "images": [img("0148")], "price": 380},
        ],
    },
    {
        "slug": "on-cloud",
        "name": "On Cloud",
        "brand": "On",
        "description": "Tênis On com solado Cloud vazado. Disponível nas cores off-white com preto e preto.",
        "colors": [
            {"id": "off-white-preto", "name": "Off-white e preto", "images": [img("0212")], "price": None},
            {"id": "preto", "name": "Preto", "images": [img("0213")], "price": None},
        ],
    },
]


def to_webp(src: Path, dest: Path, max_side: int, quality: int) -> tuple[int, int]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src)
    if im.mode != "RGB":
        im = im.convert("RGB")
    w, h = im.size
    if max(w, h) > max_side:
        if w >= h:
            nw, nh = max_side, max(1, int(h * max_side / w))
        else:
            nw, nh = max(1, int(w * max_side / h)), max_side
        im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    im.save(dest, "WEBP", quality=quality, method=6)
    return im.size


def convert(slug: str, color_id: str, start: int, files: list[str]) -> list[dict]:
    out = []
    for i, fname in enumerate(files, start=start):
        src = RAW / fname
        if not src.exists():
            raise SystemExit(f"missing image {src}")
        stem = f"{color_id}-{i:02d}"
        gw, gh = to_webp(src, IMG_OUT / slug / f"{stem}.webp", 1000, 80)
        to_webp(src, IMG_OUT / slug / f"{stem}-thumb.webp", 800, 75)
        out.append({
            "src": f"assets/products/{slug}/{stem}.webp",
            "thumb": f"assets/products/{slug}/{stem}-thumb.webp",
            "w": gw,
            "h": gh,
        })
    return out


def main():
    path = ROOT / "js/products.json"
    catalog = json.loads(path.read_text(encoding="utf-8"))
    by_slug = {p["slug"]: p for p in catalog}

    for slug, spec in EXISTING.items():
        p = by_slug[slug]
        p["description"] = spec["description"]
        colors = {c["id"]: c for c in p["colors"]}
        for cs in spec["colors"]:
            c = colors.get(cs["id"])
            if c is None:
                c = {"id": cs["id"], "name": cs["name"], "images": [], "videos": []}
                p["colors"].append(c)
                colors[cs["id"]] = c
            c["images"].extend(convert(slug, cs["id"], len(c["images"]) + 1, cs["add"]))
            c["price"] = cs["price"]

    new_entries = []
    for spec in NEW:
        if spec["slug"] in by_slug:
            raise SystemExit(f"slug already exists: {spec['slug']}")
        colors = []
        for cs in spec["colors"]:
            colors.append({
                "id": cs["id"],
                "name": cs["name"],
                "images": convert(spec["slug"], cs["id"], 1, cs["images"]),
                "videos": [],
                "price": cs["price"],
            })
        first = colors[0]["images"][0]
        new_entries.append({
            "slug": spec["slug"],
            "name": spec["name"],
            "brand": spec["brand"],
            "tag": "Novidade",
            "category": "Tênis",
            "price": None,
            "priceLabel": "Consulte",
            "description": spec["description"],
            "labelTexts": [],
            "labelNote": "",
            "labelImages": [],
            "cover": first["thumb"],
            "coverFull": first["src"],
            "colors": colors,
        })

    catalog = new_entries + catalog
    path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print("products", len(catalog), "new", len(new_entries))


if __name__ == "__main__":
    main()
