#!/usr/bin/env python3
"""Generate static HTML pages for the Monark catalog."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/workspace/monarquia")
PRODUCTS = json.loads((ROOT / "js/products.json").read_text(encoding="utf-8"))

ANNOUNCE = "Lançamentos e reposições Monark · Valores sob consulta"


def header(prefix: str, active: str = "") -> str:
    def nav(href, label, key):
        cls = ' class="active"' if active == key else ""
        return f'<a href="{prefix}{href}"{cls}>{label}</a>'

    return f"""<div class="announce">{ANNOUNCE}</div>
<header class="header">
  <div class="container header-main">
    <button class="icon-btn menu-toggle" id="menuOpen" aria-label="Abrir menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    <a class="logo" href="{prefix}"><img src="{prefix}assets/logo/logo-header.png" srcset="{prefix}assets/logo/logo-header.png 1x, {prefix}assets/logo/logo-header@2x.png 2x" alt="Monark Urban" width="220" height="67" decoding="async" /></a>
    <nav class="nav-desktop" aria-label="Principal">
      {nav("", "Início", "home")}
      {nav("tenis/", "Tênis", "tenis")}
      {nav("tenis/?tag=Lançamento", "Lançamentos", "lancamentos")}
      {nav("sobre/", "Sobre", "sobre")}
    </nav>
    <div class="header-actions">
      <form class="search-wrap" action="{prefix}tenis/" method="get" role="search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="11" cy="11" r="6.5"/><path d="M16.5 16.5 21 21" stroke-linecap="round"/></svg>
        <input type="search" name="q" placeholder="Buscar tênis..." aria-label="Buscar tênis" />
      </form>
      <button class="icon-btn" aria-label="Minha conta"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="8" r="3.2"/><path d="M5 19.2c1.6-3.2 4-4.8 7-4.8s5.4 1.6 7 4.8" stroke-linecap="round"/></svg></button>
      <button class="icon-btn" aria-label="Carrinho"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6.5 8.5h11l-1 10H7.5l-1-10Z" stroke-linejoin="round"/><path d="M9 8.5V7a3 3 0 0 1 6 0v1.5" stroke-linecap="round"/></svg><span class="badge">0</span></button>
    </div>
  </div>
  <div class="cat-bar">
    <div class="container">
      {nav("tenis/", "Tênis", "tenis")}
      <a href="{prefix}tenis/?marca=Nike">Nike</a>
      <a href="{prefix}tenis/?marca=Adidas">Adidas</a>
      <a href="{prefix}tenis/?tag=Lançamento">Lançamentos</a>
      {nav("sobre/", "Sobre", "sobre")}
      {nav("contato/", "Contato", "contato")}
    </div>
  </div>
</header>
<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer-backdrop" id="drawerBackdrop"></div>
  <aside class="drawer-panel" role="dialog" aria-label="Menu">
    <button class="drawer-close" id="menuClose" aria-label="Fechar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M7 7l10 10M17 7 7 17"/></svg></button>
    <a href="{prefix}">Início</a>
    <a href="{prefix}tenis/">Tênis</a>
    <a href="{prefix}tenis/?tag=Lançamento">Lançamentos</a>
    <a href="{prefix}sobre/">Sobre</a>
    <a href="{prefix}trocas-e-devolucoes/">Trocas e devoluções</a>
    <a href="{prefix}contato/">Contato</a>
  </aside>
</div>"""


def newsletter(prefix: str) -> str:
    return f"""<section class="newsletter">
  <div class="container newsletter-inner">
    <div>
      <h2>Fique por dentro dos lançamentos</h2>
      <p>Cadastre-se e receba novidades Monark em primeira mão.</p>
    </div>
    <form class="newsletter-form" id="newsletterForm">
      <input type="email" required placeholder="Seu e-mail" aria-label="E-mail" />
      <button class="btn btn-light" type="submit">Quero receber</button>
      <p class="newsletter-note" id="newsletterNote">Sem spam. Você pode sair quando quiser.</p>
    </form>
  </div>
</section>"""


def footer(prefix: str) -> str:
    return f"""<footer class="footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <a class="logo logo-footer" href="{prefix}"><img src="{prefix}assets/logo/logo-footer.png" srcset="{prefix}assets/logo/logo-footer.png 1x, {prefix}assets/logo/logo-footer@2x.png 2x" alt="Monark Urban" width="220" height="67" decoding="async" /></a>
      <p>Streetwear e cultura sneaker. Uma seleção cuidadosa de tênis para o dia a dia e para a rua.</p>
    </div>
    <div>
      <h3>Institucional</h3>
      <a href="{prefix}sobre/">Sobre a Monark</a>
      <a href="{prefix}trocas-e-devolucoes/">Trocas e devoluções</a>
      <a href="{prefix}contato/">Contato</a>
    </div>
    <div>
      <h3>Loja</h3>
      <a href="{prefix}tenis/">Tênis</a>
      <a href="{prefix}tenis/?tag=Lançamento">Lançamentos</a>
      <a href="{prefix}tenis/?marca=Nike">Nike</a>
      <a href="{prefix}tenis/?marca=Adidas">Adidas</a>
    </div>
    <div>
      <h3>Pagamento</h3>
      <div class="pay-row">
        <span class="pay-badge">Pix</span>
        <span class="pay-badge">Visa</span>
        <span class="pay-badge">Master</span>
        <span class="pay-badge">Elo</span>
      </div>
    </div>
  </div>
  <div class="container footer-bottom">
    <span>&copy; 2026 Monark. Todos os direitos reservados.</span>
    <span>Valores sob consulta.</span>
  </div>
</footer>
<script src="{prefix}js/products-data.js"></script>
<script src="{prefix}js/main.js"></script>"""


def page(title, description, prefix, body, active="", extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#111111" />
  <meta name="description" content="{description}" />
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <link rel="icon" href="{prefix}favicon.ico" sizes="any" />
  <link rel="icon" type="image/png" sizes="32x32" href="{prefix}favicon-32.png" />
  <link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png" />
  <meta property="og:site_name" content="Monark" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="{prefix}assets/logo/og-image.png" />
  <meta name="twitter:card" content="summary" />
  <link rel="stylesheet" href="{prefix}css/styles.css" />
  {extra_head}
</head>
<body>
{header(prefix, active)}
{body}
{newsletter(prefix)}
{footer(prefix)}
</body>
</html>
"""


def product_card(p, prefix, href=None):
    href = href or f"{prefix}tenis/{p['slug']}/"
    ncolors = len(p["colors"])
    colors = f'<p class="product-meta">{ncolors} cor' + ("es" if ncolors != 1 else "") + "</p>"
    tag = f'<span class="product-tag">{p["tag"]}</span>' if p.get("tag") else ""
    return f"""<a class="product-card" href="{href}" data-brand="{p["brand"]}" data-tag="{p.get("tag") or ""}" data-name="{p["name"]}">
  <div class="product-media">{tag}<img src="{prefix}{p["cover"]}" alt="{p["name"]}" width="800" height="800" loading="lazy" decoding="async" /></div>
  <div class="product-info">
    <p class="product-brand">{p["brand"]}</p>
    <h3>{p["name"]}</h3>
    {colors}
    <p class="product-price">Consulte</p>
  </div>
</a>"""


def home():
    cards = "\n".join(product_card(p, "") for p in PRODUCTS)
    tiles = [
        (PRODUCTS[0], "Tênis", "Ver coleção", "tenis/"),
        (PRODUCTS[4], "Lançamentos", "Nike Zoom X Run 3", f"tenis/{PRODUCTS[4]['slug']}/"),
        (PRODUCTS[2], "Botas", "Vans MTE Ultrarange", f"tenis/{PRODUCTS[2]['slug']}/"),
        (PRODUCTS[9], "Performance", "Adidas Adizero", f"tenis/{PRODUCTS[9]['slug']}/"),
    ]
    tile_html = ""
    for i, (p, label, sub, href) in enumerate(tiles, start=1):
        tile_html += (
            f'<a class="tile tile-photo tile-{i}" href="{href}" '
            f"style=\"background-image:url('{p['cover']}')\">"
            f"<div><strong>{label}</strong><span>{sub}</span></div></a>"
        )
    body = f"""<section class="hero">
  <div class="container hero-inner">
    <p class="hero-kicker">Nova marca · Cultura sneaker</p>
    <h1>Estilo urbano com identidade própria.</h1>
    <p>A Monark reúne tênis com atitude, conforto e visual limpo. Confira os lançamentos e as reposições — valores sob consulta.</p>
    <a class="btn btn-light" href="tenis/">Ver tênis</a>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-title">
      <h2>Explore</h2>
      <a href="tenis/">Ver tudo</a>
    </div>
    <div class="tiles">
      {tile_html}
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container">
    <div class="section-title">
      <h2>Catálogo</h2>
      <a href="tenis/">{len(PRODUCTS)} produtos</a>
    </div>
    <div class="product-grid">{cards}</div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container">
    <div class="benefits">
      <div class="benefit"><h3>Seleção cuidada</h3><p>Modelos escolhidos com foco em conforto, visual e cultura sneaker.</p></div>
      <div class="benefit"><h3>Valores sob consulta</h3><p>Fale com a gente para consultar valores e disponibilidade.</p></div>
      <div class="benefit"><h3>Fotos e vídeos reais</h3><p>Cada peça tem galeria e, quando houver, vídeo do produto.</p></div>
    </div>
  </div>
</section>"""
    return page(
        "Monark — Tênis & Streetwear",
        "Monark — loja de tênis streetwear. Lançamentos e reposições com fotos e vídeos.",
        "",
        body,
        "home",
    )


def listing():
    brands = sorted({p["brand"] for p in PRODUCTS})
    brand_chips = "".join(
        f'<button type="button" class="chip" data-filter="brand" data-value="{b}">{b}</button>'
        for b in brands
    )
    cards = "\n".join(product_card(p, "../") for p in PRODUCTS)
    body = f"""<section class="page-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../">Início</a><span>/</span><span>Tênis</span>
    </nav>
    <h1>Tênis</h1>
    <p>{len(PRODUCTS)} modelos no catálogo. Valores sob consulta.</p>
  </div>
</section>
<section class="container listing">
  <aside class="filters" aria-label="Filtros">
    <div class="filters-head">
      <h2>Filtros</h2>
      <button type="button" class="clear-filters" id="clearFilters">Limpar</button>
    </div>
    <div class="filter-group">
      <h3>Marca</h3>
      <div class="filter-options" id="brandFilters">{brand_chips}</div>
    </div>
    <div class="filter-group">
      <h3>Disponibilidade</h3>
      <div class="filter-options" id="tagFilters">
        <button type="button" class="chip" data-filter="tag" data-value="Lançamento">Lançamento</button>
        <button type="button" class="chip" data-filter="tag" data-value="Reposição">Reposição</button>
      </div>
    </div>
  </aside>
  <div class="listing-main">
    <div class="toolbar">
      <p class="count" id="productCount">{len(PRODUCTS)} produtos encontrados</p>
      <label>
        <span class="visually-hidden">Ordenar</span>
        <select id="sortSelect" aria-label="Ordenar">
          <option value="nome">A–Z</option>
          <option value="marca">Marca</option>
          <option value="lancamento">Lançamentos</option>
        </select>
      </label>
    </div>
    <div class="product-grid" id="productGrid">{cards}</div>
    <div class="empty" id="emptyState" hidden>
      <h2>Nenhum produto encontrado</h2>
      <p>Tente limpar os filtros ou buscar outro nome.</p>
    </div>
  </div>
</section>"""
    return page(
        "Tênis — Monark",
        "Catálogo de tênis Monark. Lançamentos e reposições com fotos e vídeos.",
        "../",
        body,
        "tenis",
    )


def pdp(p):
    prefix = "../../"
    colors = p["colors"]
    first = colors[0]
    thumbs = ""
    for i, img in enumerate(first["images"]):
        cls = " is-active" if i == 0 else ""
        thumbs += (
            f'<button type="button" class="thumb{cls}" data-kind="image" '
            f'data-src="{prefix}{img["src"]}" aria-label="Foto {i+1}">'
            f'<img src="{prefix}{img["thumb"]}" alt="" /></button>'
        )
    for i, vid in enumerate(first["videos"]):
        thumbs += (
            f'<button type="button" class="thumb thumb-video" data-kind="video" '
            f'data-src="{prefix}{vid}" aria-label="Vídeo {i+1}"><span>▶</span></button>'
        )
    color_btns = ""
    for i, c in enumerate(colors):
        cls = " is-active" if i == 0 else ""
        pressed = "true" if i == 0 else "false"
        color_btns += (
            f'<button type="button" class="color-swatch{cls}" data-color="{c["id"]}" '
            f'aria-pressed="{pressed}">{c["name"]}</button>'
        )
    video_block = ""
    if first["videos"]:
        video_block = (
            f'<video class="pdp-video" id="pdpVideo" controls playsinline '
            f'preload="metadata" src="{prefix}{first["videos"][0]}" hidden></video>'
        )
    media = {
        c["id"]: {
            "name": c["name"],
            "images": [{"src": prefix + im["src"], "thumb": prefix + im["thumb"]} for im in c["images"]],
            "videos": [prefix + v for v in c["videos"]],
        }
        for c in colors
    }
    media_json = json.dumps(media, ensure_ascii=False).replace("</", "<\\/")
    tag = f'<span class="pdp-tag">{p["tag"]}</span>' if p.get("tag") else ""
    ncolors = ", ".join(c["name"] for c in colors)
    body = f"""<section class="container pdp" data-product="{p["slug"]}">
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="../../">Início</a><span>/</span><a href="../">Tênis</a><span>/</span><span>{p["name"]}</span>
  </nav>
  <div class="pdp-grid">
    <div class="pdp-gallery">
      <div class="pdp-stage">
        <img id="pdpMain" src="{prefix}{first["images"][0]["src"]}" alt="{p["name"]} — {first["name"]}" />
        {video_block}
      </div>
      <div class="pdp-thumbs" id="pdpThumbs">{thumbs}</div>
    </div>
    <div class="pdp-buy">
      <p class="product-brand">{p["brand"]}</p>
      {tag}
      <h1>{p["name"]}</h1>
      <p class="pdp-price">Consulte</p>
      <p class="pdp-note">Valores sob consulta. Fale com a gente para consultar valor, tamanho e disponibilidade.</p>
      <div class="pdp-colors">
        <h2>Cores</h2>
        <div class="color-row" id="colorRow">{color_btns}</div>
        <p class="pdp-color-name" id="colorName">{first["name"]}</p>
      </div>
      <p class="pdp-sizes"><strong>Tamanhos:</strong> consulte disponibilidade.</p>
      <a class="btn btn-dark pdp-cta" href="../../contato/">Consultar este modelo</a>
    </div>
  </div>
  <div class="pdp-desc">
    <h2>Descrição</h2>
    <p>{p["description"]}</p>
    <p>Cores neste modelo: {ncolors}.</p>
  </div>
</section>
<script>window.MONARK_MEDIA = {media_json};</script>"""
    schema = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": p["name"],
            "brand": p["brand"],
            "description": p["description"],
            "image": prefix + p["coverFull"],
        },
        ensure_ascii=False,
    )
    extra = f'<script type="application/ld+json">{schema}</script>'
    return page(f'{p["name"]} — Monark', p["description"], prefix, body, "tenis", extra)


SOBRE = """<section class="container prose">
  <h1>Sobre a Monark</h1>
  <p>A Monark nasce da cultura streetwear e da paixão por tênis. Nosso objetivo é oferecer uma vitrine limpa, com modelos selecionados para quem vive a rua com estilo.</p>
  <p>O catálogo já está no ar, com fotos e vídeos dos primeiros modelos. Valores, tamanhos e canais oficiais de compra seguem sob consulta.</p>
</section>"""

CONTATO = """<section class="container prose">
  <h1>Contato</h1>
  <p>Ainda estamos montando os canais oficiais de atendimento. Enquanto isso, use o e-mail abaixo — é um placeholder até a operação começar.</p>
  <div class="contact-card">
    <p><strong>E-mail (placeholder):</strong> contato@monark</p>
    <p>Respostas e canais oficiais serão atualizados quando a loja abrir as vendas.</p>
  </div>
</section>"""

TROCAS = """<section class="container prose">
  <h1>Trocas e devoluções</h1>
  <p>As regras definitivas de troca e devolução serão publicadas junto com a abertura das vendas.</p>
  <h2>Diretrizes gerais (prévia)</h2>
  <ul>
    <li>Produtos sem uso, com etiquetas e na embalagem original</li>
    <li>Prazo e condições serão confirmados no momento da compra</li>
    <li>Em caso de defeito de fabricação, priorizamos a troca</li>
  </ul>
  <p>Dúvidas? Fale conosco pela página de contato.</p>
</section>"""


def main():
    files = {
        "index.html": home(),
        "tenis/index.html": listing(),
        "sobre/index.html": page("Sobre — Monark", "Sobre a Monark, loja de tênis streetwear.", "../", SOBRE, "sobre"),
        "contato/index.html": page("Contato — Monark", "Fale com a Monark.", "../", CONTATO, "contato"),
        "trocas-e-devolucoes/index.html": page(
            "Trocas e devoluções — Monark",
            "Trocas e devoluções Monark.",
            "../",
            TROCAS,
            "",
        ),
    }
    for p in PRODUCTS:
        files[f"tenis/{p['slug']}/index.html"] = pdp(p)
    for rel, html in files.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        print("wrote", rel, "bytes", len(html))
    data_js = "window.MONARK_PRODUCTS = " + json.dumps(PRODUCTS, ensure_ascii=False) + ";\n"
    (ROOT / "js/products-data.js").write_text(data_js, encoding="utf-8")
    print("wrote js/products-data.js")


if __name__ == "__main__":
    main()
