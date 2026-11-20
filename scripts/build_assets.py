#!/usr/bin/env python3
"""Optimize product photos and write catalog."""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image

ROOT = Path("/workspace/monarquia")
RAW = ROOT / "drive/raw"
IMG_OUT = ROOT / "assets/products"
VID_OUT = ROOT / "assets/videos"
IMG_OUT.mkdir(parents=True, exist_ok=True)

PRODUCTS = [
    {
        "slug": "nike-fit",
        "name": "Nike Fit",
        "brand": "Nike",
        "tag": "Lançamento",
        "description": "Tênis Nike Fit na cor marrom, com swoosh off-white e solado creme. Lançamento disponível.",
        "colors": [
            {
                "id": "marrom",
                "name": "Marrom",
                "images": ["IMG-20261115-WA0116.jpg", "IMG-20261115-WA0117.jpg", "IMG-20261115-WA0118.jpg"],
                "videos": [],
            }
        ],
    },
    {
        "slug": "new-balance-supercomp-elite-v6",
        "name": "New Balance Supercomp Elite V6",
        "brand": "New Balance",
        "tag": "Lançamento",
        "description": "Tênis New Balance Supercomp Elite V6, com entressola Infinion. Disponível nas cores limão e coral.",
        "colors": [
            {
                "id": "limao",
                "name": "Limão",
                "images": ["IMG-20261115-WA0120.jpg", "IMG-20261115-WA0122.jpg"],
                "videos": [],
            },
            {
                "id": "coral",
                "name": "Coral",
                "images": [
                    "IMG-20261115-WA0121.jpg",
                    "IMG-20261115-WA0123.jpg",
                    "IMG-20261115-WA0125.jpg",
                    "IMG-20261115-WA0126.jpg",
                ],
                "videos": [],
            },
        ],
    },
    {
        "slug": "vans-mte-ultrarange",
        "name": "Bota Vans MTE Ultrarange",
        "brand": "Vans",
        "tag": "Lançamento",
        "description": "Bota Vans MTE Ultrarange, cano médio, com solado tratorado. Disponível nas cores preto, preto e branco, e bege.",
        "colors": [
            {
                "id": "preto",
                "name": "Preto",
                "images": ["IMG-20261115-WA0128.jpg", "IMG-20261115-WA0130.jpg"],
                "videos": [],
            },
            {
                "id": "preto-branco",
                "name": "Preto e branco",
                "images": ["IMG-20261115-WA0129.jpg", "IMG-20261115-WA0132.jpg"],
                "videos": ["VID-20261115-WA0134.mp4"],
            },
            {
                "id": "bege",
                "name": "Bege",
                "images": ["IMG-20261115-WA0131.jpg"],
                "videos": [],
            },
        ],
    },
    {
        "slug": "adidas-slip-on",
        "name": "Adidas Slip On",
        "brand": "Adidas",
        "tag": "Reposição",
        "description": "Tênis Adidas Slip On na cor preta, com elástico cruzado, bico clássico e solado branco. Reposição disponível.",
        "colors": [
            {
                "id": "preto",
                "name": "Preto",
                "images": ["IMG-20261115-WA0136.jpg", "IMG-20261115-WA0137.jpg", "IMG-20261115-WA0138.jpg"],
                "videos": [],
            }
        ],
    },
    {
        "slug": "nike-zoom-x-run-3",
        "name": "Nike Zoom X Run 3",
        "brand": "Nike",
        "tag": "Lançamento",
        "description": "Tênis Nike Zoom X Run 3, com unidade visível no solado. Disponível nas cores off-white e rosa, marrom, preto e pink, e preto.",
        "colors": [
            {
                "id": "off-white-rosa",
                "name": "Off-white e rosa",
                "images": ["IMG-20261115-WA0141.jpg", "IMG-20261115-WA0142.jpg", "IMG-20261115-WA0143.jpg"],
                "videos": [],
            },
            {
                "id": "marrom",
                "name": "Marrom",
                "images": ["IMG-20261115-WA0144.jpg", "IMG-20261115-WA0145.jpg"],
                "videos": ["VID-20261115-WA0148.mp4"],
            },
            {
                "id": "preto-pink",
                "name": "Preto e pink",
                "images": ["IMG-20261115-WA0147.jpg"],
                "videos": ["VID-20261115-WA0146.mp4"],
            },
            {
                "id": "preto",
                "name": "Preto",
                "images": ["IMG-20261115-WA0149.jpg", "IMG-20261115-WA0150.jpg", "IMG-20261115-WA0151.jpg"],
                "videos": [],
            },
        ],
    },
    {
        "slug": "nike-air-force",
        "name": "Nike Air Force",
        "brand": "Nike",
        "tag": "Reposição",
        "description": "Tênis Nike Air Force. Disponível nas cores preto e branco com swoosh azul-marinho. Reposição disponível.",
        "colors": [
            {
                "id": "preto",
                "name": "Preto",
                "images": [
                    "IMG-20261115-WA0153.jpg",
                    "IMG-20261115-WA0154.jpg",
                    "IMG-20261115-WA0155.jpg",
                    "IMG-20261115-WA0156.jpg",
                ],
                "videos": ["VID-20261115-WA0158.mp4"],
            },
            {
                "id": "branco-navy",
                "name": "Branco e navy",
                "images": ["IMG-20261115-WA0176.jpg", "IMG-20261115-WA0177.jpg", "IMG-20261115-WA0178.jpg"],
                "videos": ["VID-20261115-WA0180.mp4", "VID-20261115-WA0181.mp4"],
            },
        ],
    },
    {
        "slug": "prada-thunder",
        "name": "Prada Thunder",
        "brand": "Prada",
        "tag": "Reposição",
        "description": "Tênis Prada Thunder na cor preta, com solado tratorado. Reposição disponível.",
        "colors": [
            {
                "id": "preto",
                "name": "Preto",
                "images": [
                    "IMG-20261115-WA0162.jpg",
                    "IMG-20261115-WA0161.jpg",
                    "IMG-20261115-WA0163.jpg",
                    "IMG-20261115-WA0159.jpg",
                ],
                "videos": ["VID-20261115-WA0164.mp4"],
            }
        ],
    },
    {
        "slug": "adidas-campus",
        "name": "Adidas Campus",
        "brand": "Adidas",
        "tag": "Reposição",
        "description": "Tênis Adidas Campus na cor preta, com três listras brancas e solado creme. Reposição disponível.",
        "colors": [
            {
                "id": "preto",
                "name": "Preto",
                "images": ["IMG-20261115-WA0165.jpg", "IMG-20261115-WA0166.jpg", "IMG-20261115-WA0167.jpg"],
                "videos": [],
            }
        ],
    },
    {
        "slug": "armani-exchange",
        "name": "Armani Exchange",
        "brand": "Armani Exchange",
        "tag": "Lançamento",
        "description": "Tênis Armani Exchange de malha, com solado branco. Disponível nas cores preto e branco. Lançamento disponível.",
        "colors": [
            {
                "id": "preto",
                "name": "Preto",
                "images": ["IMG-20261115-WA0172.jpg", "IMG-20261115-WA0169.jpg", "IMG-20261115-WA0170.jpg"],
                "videos": [],
            },
            {
                "id": "branco",
                "name": "Branco",
                "images": ["IMG-20261115-WA0171.jpg", "IMG-20261115-WA0173.jpg", "IMG-20261115-WA0174.jpg"],
                "videos": [],
            },
        ],
    },
    {
        "slug": "adidas-adizero",
        "name": "Adidas Adizero",
        "brand": "Adidas",
        "tag": "",
        "description": "Tênis Adidas Adizero com Lightstrike Pro no solado. Disponível nas cores preto e pink, branco e rose gold, branco e rosa, e azul e rosa. O nome segue o texto que aparece no próprio tênis (ADIZERO / LIGHTSTRIKE PRO).",
        "colors": [
            {
                "id": "preto-pink",
                "name": "Preto e pink",
                "images": ["IMG-20261117-WA0001.jpg"],
                "videos": ["VID-20261117-WA0007.mp4"],
            },
            {
                "id": "branco-rose",
                "name": "Branco e rose gold",
                "images": ["IMG-20261117-WA0002.jpg"],
                "videos": ["VID-20261117-WA0005.mp4"],
            },
            {
                "id": "branco-rosa",
                "name": "Branco e rosa",
                "images": ["IMG-20261117-WA0003.jpg"],
                "videos": ["VID-20261117-WA0009.mp4"],
            },
            {
                "id": "azul-rosa",
                "name": "Azul e rosa",
                "images": ["IMG-20261117-WA0006.jpg", "IMG-20261117-WA0008.jpg"],
                "videos": ["VID-20261117-WA0004.mp4"],
            },
        ],
    },
]



# Extra catalog fields from WhatsApp prints (OCR) and visual grouping.
# Prices were not present in any print, caption, filename or document.
LABELS = {
    "nike-fit": {
        "texts": ["LANÇAMENTOS DISPONÍVEIS", "NIKE FIT"],
        "files": ["IMG-20261115-WA0119.jpg"],
    },
    "new-balance-supercomp-elite-v6": {
        "texts": ["LANÇAMENTO DISPONÍVEL", "NEW BALANCE SUPERCOMP ELITE V6"],
        "files": ["IMG-20261115-WA0124.jpg"],
    },
    "vans-mte-ultrarange": {
        "texts": ["SUPER LANÇAMENTOS DISPONÍVEIS", "BOTA VANS MTE ULTRARANGE"],
        "files": ["IMG-20261115-WA0133.jpg"],
    },
    "adidas-slip-on": {
        "texts": ["REPOSIÇÃO DISPONÍVEL", "ADIDAS SLIP ON"],
        "files": ["IMG-20261115-WA0135.jpg"],
    },
    "nike-zoom-x-run-3": {
        "texts": [
            "LANÇAMENTO DISPONÍVEL — NIKE ZOOM X RUN 3",
            "LANÇAMENTOS DISPONÍVEIS — NIKE ZOOM X RUN 3",
        ],
        "files": ["IMG-20261115-WA0140.jpg", "IMG-20261115-WA0152.jpg"],
    },
    "nike-air-force": {
        "texts": [
            "REPOSIÇÃO DISPONÍVEL — NIKE AIR FORCE",
            "REPOSIÇÃO DISPONÍVEL — NIKE AIR FORCE",
        ],
        "files": ["IMG-20261115-WA0157.jpg", "IMG-20261115-WA0179.jpg"],
    },
    "prada-thunder": {
        "texts": ["REPOSIÇÃO DISPONÍVEL", "PRADA THUNDER"],
        "files": ["IMG-20261115-WA0160.jpg"],
    },
    "adidas-campus": {
        "texts": ["REPOSIÇÃO DISPONÍVEL", "ADIDAS CAMPUS"],
        "files": ["IMG-20261115-WA0168.jpg"],
    },
    "armani-exchange": {
        "texts": ["LANÇAMENTOS DISPONÍVEIS", "ARMANI EXCHANGE"],
        "files": ["IMG-20261115-WA0175.jpg"],
    },
    "adidas-adizero": {
        "texts": [],
        "files": [],
        "note": "Não havia print de WhatsApp com o nome. Identificado pelo texto no tênis: ADIZERO / LIGHTSTRIKE PRO.",
    },
}

def category_for(name: str, slug: str) -> str:
    if "bota" in name.lower() or slug.startswith("vans-"):
        return "Botas"
    return "Tênis"



def to_webp(src: Path, dest: Path, max_side: int, quality: int) -> tuple[int, int]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src)
    if im.mode != "RGB":
        im = im.convert("RGB")
    w, h = im.size
    if max(w, h) > max_side:
        if w >= h:
            nh = max(1, int(h * max_side / w))
            nw = max_side
        else:
            nw = max(1, int(w * max_side / h))
            nh = max_side
        im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    im.save(dest, "WEBP", quality=quality, method=6)
    return im.size


def optimize():
    catalog = []
    for p in PRODUCTS:
        slug = p["slug"]
        out_colors = []
        for color in p["colors"]:
            imgs = []
            for i, fname in enumerate(color["images"], start=1):
                src = RAW / fname
                if not src.exists():
                    raise SystemExit(f"missing image {src}")
                stem = f"{color['id']}-{i:02d}"
                gal = IMG_OUT / slug / f"{stem}.webp"
                thumb = IMG_OUT / slug / f"{stem}-thumb.webp"
                gw, gh = to_webp(src, gal, 1000, 80)
                to_webp(src, thumb, 800, 75)
                rel = f"assets/products/{slug}/{stem}.webp"
                rel_t = f"assets/products/{slug}/{stem}-thumb.webp"
                imgs.append({"src": rel, "thumb": rel_t, "w": gw, "h": gh})
            vids = []
            for vname in color["videos"]:
                if not (VID_OUT / vname).exists():
                    print(f"NOTE video not ready yet: {vname}")
                poster_src = ROOT / "drive/frames" / Path(vname).with_suffix(".jpg").name
                poster_rel = f"assets/videos/posters/{Path(vname).stem}.webp"
                poster_dest = ROOT / poster_rel
                if poster_src.exists():
                    to_webp(poster_src, poster_dest, 1000, 75)
                else:
                    print(f"NOTE missing poster frame for {vname}")
                    poster_rel = None
                vids.append({
                    "src": f"assets/videos/{vname}",
                    "poster": poster_rel,
                })
            out_colors.append({
                "id": color["id"],
                "name": color["name"],
                "images": imgs,
                "videos": vids,
            })
        first = out_colors[0]["images"][0]
        meta = LABELS.get(slug, {"texts": [], "files": []})
        label_imgs = []
        for i, fname in enumerate(meta.get("files") or [], start=1):
            src = RAW / fname
            if not src.exists():
                print("NOTE missing label", src)
                continue
            rel = f"assets/products/{slug}/label-{i:02d}.webp"
            to_webp(src, ROOT / rel, 1400, 80)
            label_imgs.append(rel)
        catalog.append({
            "slug": slug,
            "name": p["name"],
            "brand": p["brand"],
            "tag": p["tag"],
            "category": category_for(p["name"], slug),
            "price": None,
            "priceLabel": "Consulte",
            "description": p["description"],
            "labelTexts": meta.get("texts") or [],
            "labelNote": meta.get("note") or "",
            "labelImages": label_imgs,
            "cover": first["thumb"],
            "coverFull": first["src"],
            "colors": out_colors,
        })
    dest = ROOT / "js/products.json"
    dest.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", dest, "products", len(catalog))
    total = sum(f.stat().st_size for f in IMG_OUT.rglob("*.webp"))
    print(f"webp total {total/1e6:.1f} MB, files {len(list(IMG_OUT.rglob('*.webp')))}")


if __name__ == "__main__":
    optimize()
