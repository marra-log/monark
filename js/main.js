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
        renderThumbs(color);
        if (color.images[0]) showImage(color.images[0].src, color.name);
      });
  }
})();
