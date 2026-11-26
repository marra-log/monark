(function () {
  const drawer = document.getElementById("drawer");
  const openBtn = document.getElementById("menuOpen");
  const closeBtn = document.getElementById("menuClose");
  const backdrop = document.getElementById("drawerBackdrop");

  function openDrawer() {
    if (!drawer) return;
    drawer.classList.add("open");
    document.body.style.overflow = "hidden";
  }
  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove("open");
    document.body.style.overflow = "";
  }

  openBtn && openBtn.addEventListener("click", openDrawer);
  closeBtn && closeBtn.addEventListener("click", closeDrawer);
  backdrop && backdrop.addEventListener("click", closeDrawer);

  const form = document.getElementById("newsletterForm");
  form &&
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = form.querySelector('input[type="email"]');
      const note = document.getElementById("newsletterNote");
      if (!email || !email.value.trim()) return;
      if (note) note.textContent = "Obrigado! Em breve você receberá novidades Monark.";
      form.reset();
    });

  // Listing filters
  const grid = document.getElementById("productGrid");
  if (grid) {
    const params = new URLSearchParams(location.search);
    const countEl = document.getElementById("productCount");
    const emptyEl = document.getElementById("emptyState");
    const sortEl = document.getElementById("sortSelect");
    const chips = document.querySelectorAll(".filters .chip");

    function activeValues(kind) {
      return Array.from(document.querySelectorAll('.chip.active[data-filter="' + kind + '"]')).map(
        (c) => c.dataset.value
      );
    }

    function apply() {
      const brands = activeValues("brand");
      const tags = activeValues("tag");
      const cats = activeValues("category");
      const q = (params.get("q") || "").trim().toLowerCase();
      const cards = Array.from(grid.querySelectorAll(".product-card"));
      let visible = 0;
      cards.forEach((card) => {
        const brand = card.dataset.brand || "";
        const tag = card.dataset.tag || "";
        const category = card.dataset.category || "";
        const name = (card.dataset.name || card.textContent || "").toLowerCase();
        const okBrand = !brands.length || brands.includes(brand);
        const okTag = !tags.length || tags.includes(tag);
        const okCat = !cats.length || cats.includes(category);
        const okQ = !q || name.includes(q) || brand.toLowerCase().includes(q) || category.toLowerCase().includes(q);
        const show = okBrand && okTag && okCat && okQ;
        card.hidden = !show;
        if (show) visible += 1;
      });
      if (countEl) {
        countEl.textContent =
          visible === 1 ? "1 produto encontrado" : visible + " produtos encontrados";
      }
      if (emptyEl) emptyEl.hidden = visible > 0;
    }

    function sortCards() {
      const mode = sortEl ? sortEl.value : "nome";
      const cards = Array.from(grid.querySelectorAll(".product-card"));
      cards.sort((a, b) => {
        if (mode === "marca") {
          return (a.dataset.brand || "").localeCompare(b.dataset.brand || "", "pt-BR") ||
            (a.dataset.name || "").localeCompare(b.dataset.name || "", "pt-BR");
        }
        if (mode === "preco") {
          const ap = parseFloat(a.dataset.price) || Infinity;
          const bp = parseFloat(b.dataset.price) || Infinity;
          return ap - bp || (a.dataset.name || "").localeCompare(b.dataset.name || "", "pt-BR");
        }
        if (mode === "lancamento") {
          const aw = a.dataset.tag === "Lançamento" ? 0 : 1;
          const bw = b.dataset.tag === "Lançamento" ? 0 : 1;
          return aw - bw || (a.dataset.name || "").localeCompare(b.dataset.name || "", "pt-BR");
        }
        return (a.dataset.name || "").localeCompare(b.dataset.name || "", "pt-BR");
      });
      cards.forEach((c) => grid.appendChild(c));
    }

    chips.forEach((chip) => {
      chip.addEventListener("click", () => {
        // single-select per group
        const group = chip.parentElement;
        const already = chip.classList.contains("active");
        group.querySelectorAll(".chip").forEach((c) => c.classList.remove("active"));
        if (!already) chip.classList.add("active");
        apply();
      });
    });

    const clear = document.getElementById("clearFilters");
    clear &&
      clear.addEventListener("click", () => {
        chips.forEach((c) => c.classList.remove("active"));
        params.delete("q");
        params.delete("marca");
        params.delete("tag");
        params.delete("categoria");
        const search = document.querySelector('.search-wrap input[name="q"]');
        if (search) search.value = "";
        history.replaceState({}, "", location.pathname);
        apply();
      });

    sortEl && sortEl.addEventListener("change", () => { sortCards(); apply(); });

    // URL params
    const marca = params.get("marca");
    const tag = params.get("tag");
    const categoria = params.get("categoria");
    const q = params.get("q");
    if (marca) {
      document.querySelectorAll('.chip[data-filter="brand"]').forEach((c) => {
        if (c.dataset.value === marca) c.classList.add("active");
      });
    }
    if (tag) {
      document.querySelectorAll('.chip[data-filter="tag"]').forEach((c) => {
        if (c.dataset.value === tag) c.classList.add("active");
      });
    }
    if (categoria) {
      document.querySelectorAll('.chip[data-filter="category"]').forEach((c) => {
        if (c.dataset.value === categoria) c.classList.add("active");
      });
    }
    if (q) {
      const search = document.querySelector('.search-wrap input[name="q"]');
      if (search) search.value = q;
    }
    sortCards();
    apply();
  }

  // Product gallery / colors
  const media = window.MONARK_MEDIA;
  if (media) {
    const main = document.getElementById("pdpMain");
    const video = document.getElementById("pdpVideo");
    const thumbs = document.getElementById("pdpThumbs");
    const colorRow = document.getElementById("colorRow");
    const colorName = document.getElementById("colorName");

    function showImage(src, alt) {
      if (!main) return;
      main.hidden = false;
      main.src = src;
      if (alt) main.alt = alt;
      if (video) {
        video.pause();
        video.hidden = true;
      }
    }
    function videoSrc(v) {
      return typeof v === "string" ? v : (v && v.src) || "";
    }
    function videoPoster(v) {
      return typeof v === "string" ? "" : (v && v.poster) || "";
    }
    function showVideo(src, poster) {
      if (!video) return;
      video.hidden = false;
      if (poster) video.setAttribute("poster", poster);
      if (video.getAttribute("src") !== src) video.src = src;
      if (main) main.hidden = true;
    }

    function renderThumbs(color) {
      if (!thumbs) return;
      thumbs.innerHTML = "";
      color.images.forEach((img, i) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "thumb" + (i === 0 ? " is-active" : "");
        btn.dataset.kind = "image";
        btn.dataset.src = img.src;
        btn.setAttribute("aria-label", "Foto " + (i + 1));
        btn.innerHTML = '<img src="' + img.thumb + '" alt="" />';
        thumbs.appendChild(btn);
      });
      (color.videos || []).forEach((v, i) => {
        const src = videoSrc(v);
        const poster = videoPoster(v);
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "thumb thumb-video";
        btn.dataset.kind = "video";
        btn.dataset.src = src;
        if (poster) btn.dataset.poster = poster;
        btn.setAttribute("aria-label", "Vídeo " + (i + 1));
        btn.innerHTML = (poster ? '<img src="' + poster + '" alt="" />' : "") + "<span>▶</span>";
        thumbs.appendChild(btn);
      });
    }

    thumbs &&
      thumbs.addEventListener("click", (e) => {
        const btn = e.target.closest(".thumb");
        if (!btn) return;
        thumbs.querySelectorAll(".thumb").forEach((t) => t.classList.remove("is-active"));
        btn.classList.add("is-active");
        if (btn.dataset.kind === "video") showVideo(btn.dataset.src, btn.dataset.poster);
        else showImage(btn.dataset.src);
      });

    colorRow &&
      colorRow.addEventListener("click", (e) => {
        const btn = e.target.closest(".color-swatch");
        if (!btn) return;
        const color = media[btn.dataset.color];
        if (!color) return;
        colorRow.querySelectorAll(".color-swatch").forEach((c) => {
          c.classList.remove("is-active");
          c.setAttribute("aria-pressed", "false");
        });
        btn.classList.add("is-active");
        btn.setAttribute("aria-pressed", "true");
        if (colorName) colorName.textContent = color.name;
        const priceEl = document.getElementById("pdpPrice");
        if (priceEl && color.price) priceEl.textContent = color.price;
        renderThumbs(color);
        if (color.images[0]) showImage(color.images[0].src, color.name);
      });
  }
})();

// ---------- Carrinho e checkout ----------
(function () {
  const KEY = "monark_cart_v1";
  const prefix = document.body.dataset.prefix || "";
  const brl = (v) => "R$ " + v.toFixed(2).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, ".");

  function load() {
    try {
      const data = JSON.parse(localStorage.getItem(KEY) || "[]");
      return Array.isArray(data) ? data : [];
    } catch (e) {
      return [];
    }
  }
  function save(items) {
    try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) {}
    updateBadge(items);
  }
  function count(items) { return items.reduce((n, it) => n + it.qty, 0); }
  function updateBadge(items) {
    const el = document.getElementById("cartCount");
    if (el) el.textContent = String(count(items || load()));
  }
  function totals(items) {
    let subtotal = 0, pending = 0;
    items.forEach((it) => {
      if (it.price) subtotal += it.price * it.qty;
      else pending += it.qty;
    });
    return { subtotal, pending };
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }
  function toast(html) {
    let t = document.getElementById("toast");
    if (!t) {
      t = document.createElement("div");
      t.id = "toast";
      t.className = "toast";
      t.setAttribute("role", "status");
      document.body.appendChild(t);
    }
    t.innerHTML = html;
    t.classList.add("show");
    clearTimeout(t._h);
    t._h = setTimeout(() => t.classList.remove("show"), 3500);
  }

  updateBadge();

  // Página do produto: tamanho, quantidade e adicionar
  const addBtn = document.getElementById("addToCart");
  const media = window.MONARK_MEDIA;
  if (addBtn && media) {
    const sizeRow = document.getElementById("sizeRow");
    const hint = document.getElementById("sizeHint");
    const qtyInput = document.getElementById("qtyInput");
    let size = null;

    sizeRow && sizeRow.addEventListener("click", (e) => {
      const b = e.target.closest(".size-btn");
      if (!b) return;
      sizeRow.querySelectorAll(".size-btn").forEach((x) => { x.classList.remove("is-active"); x.setAttribute("aria-pressed", "false"); });
      b.classList.add("is-active");
      b.setAttribute("aria-pressed", "true");
      size = b.dataset.size;
      if (hint) { hint.classList.remove("is-error"); hint.textContent = "Tamanho " + size + " selecionado."; }
    });
    document.querySelectorAll("[data-qty-step]").forEach((b) =>
      b.addEventListener("click", () => {
        const v = Math.min(10, Math.max(1, (parseInt(qtyInput.value, 10) || 1) + parseInt(b.dataset.qtyStep, 10)));
        qtyInput.value = v;
      })
    );
    addBtn.addEventListener("click", () => {
      if (!size) {
        if (hint) { hint.classList.add("is-error"); hint.textContent = "Escolha um tamanho para adicionar ao carrinho."; }
        sizeRow && sizeRow.scrollIntoView({ behavior: "smooth", block: "center" });
        return;
      }
      const active = document.querySelector("#colorRow .color-swatch.is-active");
      const colorId = active ? active.dataset.color : Object.keys(media)[0];
      const color = media[colorId];
      const qty = Math.min(10, Math.max(1, parseInt(qtyInput.value, 10) || 1));
      const items = load();
      const id = addBtn.dataset.slug + "|" + colorId + "|" + size;
      const found = items.find((it) => it.id === id);
      if (found) found.qty = Math.min(10, found.qty + qty);
      else items.push({
        id, slug: addBtn.dataset.slug, name: addBtn.dataset.name,
        color: colorId, colorName: color.name, size, qty,
        price: color.priceValue || null, image: color.cover,
      });
      save(items);
      toast('Adicionado ao carrinho. <a href="' + prefix + 'carrinho/">Ver carrinho</a>');
    });
  }

  function itemRow(it, editable) {
    const price = it.price ? brl(it.price * it.qty) : "Consulte";
    const unit = it.price ? brl(it.price) + " cada" : "Valor a consultar";
    return (
      '<li class="cart-item" data-id="' + esc(it.id) + '">' +
      '<a class="cart-thumb" href="' + prefix + "tenis/" + esc(it.slug) + '/"><img src="' + prefix + esc(it.image) + '" alt="" /></a>' +
      '<div class="cart-info"><a class="cart-name" href="' + prefix + "tenis/" + esc(it.slug) + '/">' + esc(it.name) + "</a>" +
      '<p class="cart-meta">' + esc(it.colorName) + " · Tam. " + esc(it.size) + (editable ? "" : " · Qtd " + it.qty) + "</p>" +
      '<p class="cart-unit">' + unit + "</p>" +
      (editable
        ? '<div class="cart-actions"><div class="qty qty-sm"><button type="button" class="qty-btn" data-step="-1" aria-label="Diminuir">−</button><span>' + it.qty +
          '</span><button type="button" class="qty-btn" data-step="1" aria-label="Aumentar">+</button></div><button type="button" class="link-btn" data-remove>Remover</button></div>'
        : "") +
      "</div><p class=\"cart-price\">" + price + "</p></li>"
    );
  }
  function summaryHtml(items) {
    const t = totals(items);
    let h = '<div class="summary-line"><span>Subtotal</span><strong>' + brl(t.subtotal) + "</strong></div>";
    if (t.pending) h += '<p class="summary-note">+ ' + t.pending + (t.pending > 1 ? " itens" : " item") + " com valor a consultar.</p>";
    h += '<div class="summary-line"><span>Frete</span><span>A combinar</span></div>';
    h += '<p class="summary-note">O frete é calculado pelo CEP e confirmado no WhatsApp.</p>';
    return h;
  }

  // Página do carrinho
  const cartRoot = document.getElementById("cartRoot");
  if (cartRoot) {
    function render() {
      const items = load();
      if (!items.length) {
        cartRoot.innerHTML = '<div class="cart-empty"><p>Seu carrinho está vazio.</p><a class="btn btn-dark" href="' + prefix + 'tenis/">Ver catálogo</a></div>';
        return;
      }
      cartRoot.innerHTML =
        '<ul class="cart-list">' + items.map((it) => itemRow(it, true)).join("") + "</ul>" +
        '<aside class="cart-summary"><h2>Resumo</h2>' + summaryHtml(items) +
        '<a class="btn btn-dark cart-go" href="' + prefix + 'checkout/">Finalizar pedido</a>' +
        '<a class="cart-continue" href="' + prefix + 'tenis/">Continuar comprando</a></aside>';
    }
    cartRoot.addEventListener("click", (e) => {
      const li = e.target.closest(".cart-item");
      if (!li) return;
      const items = load();
      const it = items.find((x) => x.id === li.dataset.id);
      if (!it) return;
      const step = e.target.closest("[data-step]");
      if (step) it.qty = Math.min(10, Math.max(1, it.qty + parseInt(step.dataset.step, 10)));
      if (e.target.closest("[data-remove]")) items.splice(items.indexOf(it), 1);
      save(items);
      render();
    });
    render();
  }

  // Página de checkout
  const form = document.getElementById("checkoutForm");
  if (form) {
    const summary = document.getElementById("checkoutSummary");
    const errEl = document.getElementById("formError");
    const cepStatus = document.getElementById("cepStatus");
    const f = (n) => form.elements[n];

    function renderSummary() {
      const items = load();
      if (!items.length) {
        document.getElementById("checkoutRoot").innerHTML =
          '<div class="cart-empty"><p>Seu carrinho está vazio.</p><a class="btn btn-dark" href="' + prefix + 'tenis/">Ver catálogo</a></div>';
        return false;
      }
      summary.innerHTML = '<h2>Seu pedido</h2><ul class="cart-list compact">' + items.map((it) => itemRow(it, false)).join("") + "</ul>" +
        summaryHtml(items) + '<a class="cart-continue" href="' + prefix + 'carrinho/">Editar carrinho</a>';
      return true;
    }
    if (!renderSummary()) return;

    // Máscaras
    f("cep").addEventListener("input", (e) => {
      let d = e.target.value.replace(/\D/g, "").slice(0, 8);
      e.target.value = d.length > 5 ? d.slice(0, 5) + "-" + d.slice(5) : d;
      if (d.length === 8) buscarCep(d);
      else cepStatus.textContent = "";
    });
    f("telefone").addEventListener("input", (e) => {
      const d = e.target.value.replace(/\D/g, "").slice(0, 11);
      let v = d;
      if (d.length > 2) v = "(" + d.slice(0, 2) + ") " + d.slice(2);
      if (d.length > 7) v = "(" + d.slice(0, 2) + ") " + d.slice(2, d.length - 4) + "-" + d.slice(-4);
      e.target.value = v;
    });
    f("uf").addEventListener("input", (e) => { e.target.value = e.target.value.replace(/[^a-z]/gi, "").toUpperCase(); });

    form.addEventListener("input", (e) => { if (e.target.value.trim()) e.target.classList.remove("is-invalid"); });

    let lastCep = "";
    async function buscarCep(cep) {
      if (cep === lastCep) return;
      lastCep = cep;
      cepStatus.className = "cep-status";
      cepStatus.textContent = "Buscando endereço…";
      try {
        const r = await fetch("https://viacep.com.br/ws/" + cep + "/json/");
        const d = await r.json();
        if (d.erro) throw new Error("not found");
        if (d.logradouro) f("rua").value = d.logradouro;
        if (d.bairro) f("bairro").value = d.bairro;
        if (d.localidade) f("cidade").value = d.localidade;
        if (d.uf) f("uf").value = d.uf;
        cepStatus.textContent = "Endereço encontrado. Confira e informe o número.";
        f("numero").focus();
      } catch (e) {
        cepStatus.className = "cep-status is-error";
        cepStatus.textContent = "Não encontramos esse CEP. Preencha o endereço manualmente.";
        lastCep = "";
      }
    }

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      errEl.hidden = true;
      const required = ["nome", "telefone", "cep", "rua", "numero", "bairro", "cidade", "uf"];
      const missing = required.filter((n) => !f(n).value.trim());
      form.querySelectorAll(".is-invalid").forEach((x) => x.classList.remove("is-invalid"));
      missing.forEach((n) => f(n).classList.add("is-invalid"));
      if (f("cep").value.replace(/\D/g, "").length !== 8 && !missing.includes("cep")) { missing.push("cep"); f("cep").classList.add("is-invalid"); }
      if (f("telefone").value.replace(/\D/g, "").length < 10 && !missing.includes("telefone")) { missing.push("telefone"); f("telefone").classList.add("is-invalid"); }
      if (missing.length) {
        errEl.textContent = "Confira os campos destacados antes de enviar.";
        errEl.hidden = false;
        f(missing[0]).focus();
        return;
      }
      const items = load();
      const t = totals(items);
      const v = (n) => f(n).value.trim();
      const pay = form.querySelector('input[name="pagamento"]:checked');
      const lines = ["*Novo pedido — Monark*", ""];
      items.forEach((it, i) => {
        lines.push((i + 1) + ") " + it.name + " — " + it.colorName + " — Tam. " + it.size + " — Qtd " + it.qty + " — " + (it.price ? brl(it.price * it.qty) : "valor a consultar"));
      });
      lines.push("", "*Subtotal:* " + brl(t.subtotal) + (t.pending ? " (+ " + t.pending + " item(ns) a consultar)" : ""));
      lines.push("*Frete:* a combinar", "");
      lines.push("*Cliente:* " + v("nome"), "*WhatsApp:* " + v("telefone"));
      if (v("email")) lines.push("*E-mail:* " + v("email"));
      lines.push("", "*Entrega:* " + v("rua") + ", " + v("numero") + (v("complemento") ? " — " + v("complemento") : ""));
      lines.push(v("bairro") + " — " + v("cidade") + "/" + v("uf") + " — CEP " + v("cep"));
      lines.push("", "*Pagamento:* " + (pay ? pay.value : "Pix"));
      if (v("obs")) lines.push("*Observações:* " + v("obs"));
      const text = lines.join("\n");
      const num = String(window.MONARK_WHATSAPP || "").replace(/\D/g, "");
      const url = "https://wa.me/" + num + "?text=" + encodeURIComponent(text);
      save([]);
      document.getElementById("checkoutRoot").innerHTML =
        '<div class="order-done"><h2>Pedido pronto!</h2><p>Abrimos o WhatsApp com o seu pedido. Se não abriu, toque no botão abaixo.</p>' +
        '<a class="btn btn-dark" href="' + url + '" target="_blank" rel="noopener">Abrir WhatsApp</a>' +
        '<a class="cart-continue" href="' + prefix + 'tenis/">Voltar ao catálogo</a></div>';
      window.location.href = url;
    });
  }
})();
