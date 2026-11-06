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

  document.querySelectorAll(".chip").forEach((chip) => {
    chip.addEventListener("click", () => chip.classList.toggle("active"));
  });

  const clear = document.getElementById("clearFilters");
  clear &&
    clear.addEventListener("click", () => {
      document.querySelectorAll(".chip.active").forEach((c) => c.classList.remove("active"));
      document.querySelectorAll(".price-row input").forEach((i) => (i.value = ""));
    });

  const form = document.getElementById("newsletterForm");
  form &&
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = form.querySelector('input[type="email"]');
      const note = document.getElementById("newsletterNote");
      if (!email || !email.value.trim()) return;
      if (note) {
        note.textContent = "Obrigado! Em breve você receberá novidades Monark.";
      }
      form.reset();
    });
})();
