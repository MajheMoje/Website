/* corbel × majhe moje: story filter, add-to-bag drawer, scroll reveal */
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  /* reveal */
  var revealed = document.querySelectorAll(".mm-reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-visible"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -6% 0px" });
    revealed.forEach(function (el) { io.observe(el); });
  } else {
    revealed.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* filter stories by frame */
  var pills = document.querySelectorAll(".cx-frame-pill");
  var stories = document.querySelectorAll(".cx-story");
  pills.forEach(function (pill) {
    pill.addEventListener("click", function () {
      var f = pill.getAttribute("data-filter");
      pills.forEach(function (p) { p.classList.toggle("is-on", p === pill); });
      stories.forEach(function (s) { s.hidden = f !== "all" && s.getAttribute("data-frame") !== f; });
    });
  });

  /* add-to-bag drawer (prototype: counts locally, no checkout) */
  var overlay = document.getElementById("atc");
  var nameEl = document.getElementById("atc-name");
  var priceEl = document.getElementById("atc-price");
  var labelEl = document.getElementById("atc-label");
  var optsEl = document.getElementById("atc-options");
  var addBtn = document.getElementById("atc-add");
  var msgEl = document.getElementById("atc-msg");
  var bagEl = document.getElementById("bag-count");
  var bag = 0;

  function close() {
    overlay.classList.remove("is-open");
    overlay.setAttribute("aria-hidden", "true");
  }

  document.querySelectorAll("[data-product]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var p = JSON.parse(btn.getAttribute("data-product"));
      nameEl.textContent = p.name;
      priceEl.textContent = p.price;
      labelEl.textContent = p.label;
      msgEl.textContent = "";
      optsEl.innerHTML = "";
      addBtn.disabled = p.options.length > 0;
      p.options.forEach(function (o) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "mm-hd-drawer__pill";
        b.textContent = o;
        b.addEventListener("click", function () {
          optsEl.querySelectorAll(".mm-hd-drawer__pill").forEach(function (x) { x.classList.remove("is-on"); });
          b.classList.add("is-on");
          addBtn.disabled = false;
        });
        optsEl.appendChild(b);
      });
      overlay.classList.add("is-open");
      overlay.setAttribute("aria-hidden", "false");
      addBtn.focus();
    });
  });

  addBtn.addEventListener("click", function () {
    bag += 1;
    bagEl.textContent = bag;
    msgEl.textContent = "added. it's in your bag.";
    setTimeout(close, 900);
  });
  overlay.querySelector(".mm-hd-drawer__close").addEventListener("click", close);
  overlay.addEventListener("click", function (e) { if (e.target === overlay) close(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
})();
