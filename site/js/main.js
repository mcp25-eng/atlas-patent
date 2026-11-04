(function () {
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".menu-toggle");
  if (toggle && header) {
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  document.querySelectorAll(".nav-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (window.matchMedia("(max-width: 1160px)").matches) {
        var drop = btn.parentElement;
        var open = drop.classList.toggle("open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      }
    });
  });

  var searchForm = document.querySelector(".site-search");
  var searchInput = document.getElementById("site-q");
  var searchPanel = searchForm ? searchForm.querySelector(".search-panel") : null;
  var searchData = [];
  var searchBlob = document.getElementById("search-index");
  if (searchBlob) {
    try { searchData = JSON.parse(searchBlob.textContent); } catch (err) { searchData = []; }
  }
  function fold(value) {
    return String(value || "").toLocaleLowerCase("tr-TR");
  }
  function esc(value) {
    return String(value).replace(/[&<>"]/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[ch];
    });
  }
  function renderSearch() {
    if (!searchPanel || !searchInput) return;
    var query = fold(searchInput.value.trim());
    if (query.length < 2) {
      searchPanel.hidden = true;
      searchPanel.innerHTML = "";
      return;
    }
    var hits = searchData.filter(function (item) {
      return fold(item.t + " " + item.d + " " + item.g).indexOf(query) !== -1;
    }).slice(0, 8);
    if (!hits.length) {
      searchPanel.innerHTML = '<p class="search-empty">Eşleşme yok. <a href="iletisim.html">İletişimden yazın</a>.</p>';
    } else {
      searchPanel.innerHTML = hits.map(function (item) {
        return '<a href="' + esc(item.u) + '"><small>' + esc(item.g) + '</small><strong>' + esc(item.t) + '</strong></a>';
      }).join("");
    }
    searchPanel.hidden = false;
  }
  if (searchForm && searchInput) {
    searchForm.addEventListener("submit", function (event) {
      event.preventDefault();
      var first = searchPanel.querySelector("a[href]");
      if (first) window.location.href = first.getAttribute("href");
    });
    searchInput.addEventListener("input", renderSearch);
    document.addEventListener("click", function (event) {
      if (!searchForm.contains(event.target)) searchPanel.hidden = true;
    });
  }

  var stage = document.querySelector(".stage");
  if (stage && window.matchMedia("(pointer:fine)").matches) {
    stage.addEventListener("pointermove", function (event) {
      var box = stage.getBoundingClientRect();
      stage.style.setProperty("--mx", ((event.clientX - box.left) / box.width * 100) + "%");
      stage.style.setProperty("--my", ((event.clientY - box.top) / box.height * 100) + "%");
    });
  }

  window.addEventListener("scroll", function () {
    if (!header) return;
    header.classList.toggle("scrolled", window.scrollY > 8);
  }, { passive: true });

  var cover = document.querySelector(".cover");
  if (cover) {
    var slides = cover.querySelectorAll(".cover-slide");
    var dots = cover.querySelectorAll(".cover-tabs button");
    var bar = cover.querySelector(".cover-progress i");
    var track = cover.querySelector(".cover-track");
    var index = 0;
    var token = 0;
    var timer = null;
    var wait = 8000;
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    function arm() {
      if (!bar || reduce) return;
      bar.classList.remove("run");
      void bar.offsetWidth;
      bar.classList.add("run");
    }
    function go(next) {
      index = (next + slides.length) % slides.length;
      var mine = ++token;
      if (track) track.style.transform = "translate3d(" + (-index * 100) + "%,0,0)";
      slides[index].classList.add("is-in");
      dots.forEach(function (dot, i) {
        dot.classList.toggle("on", i === index);
        dot.setAttribute("aria-selected", i === index ? "true" : "false");
      });
      arm();
      window.setTimeout(function () {
        if (mine !== token) return;
        Array.prototype.forEach.call(slides, function (slide, i) {
          slide.classList.toggle("is-in", i === index);
        });
      }, reduce ? 0 : 1000);
    }
    function play() {
      if (reduce) return;
      stop();
      timer = setInterval(function () { go(index + 1); }, wait);
      arm();
    }
    function stop() {
      if (timer) clearInterval(timer);
      timer = null;
      if (bar) bar.classList.remove("run");
    }
    cover.querySelector(".cover-arrow.next").addEventListener("click", function () {
      go(index + 1);
      play();
    });
    cover.querySelector(".cover-arrow.prev").addEventListener("click", function () {
      go(index - 1);
      play();
    });
    dots.forEach(function (dot, i) {
      dot.addEventListener("click", function () {
        go(i);
        play();
      });
    });
    var startX = 0;
    cover.addEventListener("touchstart", function (event) {
      startX = event.changedTouches[0].clientX;
    }, { passive: true });
    cover.addEventListener("touchend", function (event) {
      var delta = event.changedTouches[0].clientX - startX;
      if (Math.abs(delta) < 40) return;
      go(index + (delta < 0 ? 1 : -1));
      play();
    });
    cover.addEventListener("mouseenter", stop);
    cover.addEventListener("mouseleave", play);
    cover.addEventListener("focusin", stop);
    cover.addEventListener("focusout", play);
    document.addEventListener("keydown", function (event) {
      if (!cover.contains(document.activeElement) && document.activeElement !== document.body) return;
      if (event.key === "ArrowRight") { go(index + 1); play(); }
      if (event.key === "ArrowLeft") { go(index - 1); play(); }
    });
    go(0);
    play();
  }

  var dock = document.getElementById("wa-dock");
  var panel = document.getElementById("wa-panel");
  var note = document.getElementById("wa-note");
  var topic = "marka tescili";
  function setOpen(open) {
    if (!dock) return;
    dock.classList.toggle("open", open);
    var launcher = dock.querySelector(".wa-launcher");
    if (launcher) launcher.setAttribute("aria-expanded", open ? "true" : "false");
    if (panel) {
      panel.toggleAttribute("inert", !open);
      panel.setAttribute("aria-hidden", open ? "false" : "true");
    }
    if (open && note) note.focus();
  }
  setOpen(false);
  document.querySelectorAll(".wa-open, .wa-launcher").forEach(function (btn) {
    btn.addEventListener("click", function (event) {
      event.stopPropagation();
      setOpen(!dock.classList.contains("open"));
    });
  });
  document.addEventListener("click", function (event) {
    if (!dock || !dock.classList.contains("open")) return;
    if (dock.contains(event.target) || event.target.closest(".wa-open")) return;
    setOpen(false);
  });
  document.querySelectorAll(".wa-chips button").forEach(function (chip) {
    chip.addEventListener("click", function () {
      document.querySelectorAll(".wa-chips button").forEach(function (item) {
        item.classList.remove("on");
      });
      chip.classList.add("on");
      topic = chip.getAttribute("data-topic") || topic;
    });
  });
  var go = document.getElementById("wa-go");
  if (go) {
    go.addEventListener("click", function () {
      var text = "Merhaba Atlas Patent, " + topic + " için yazıyorum.";
      var extra = note ? note.value.trim() : "";
      if (extra) text += " " + extra;
      window.open("https://wa.me/905556224422?text=" + encodeURIComponent(text), "_blank", "noopener");
    });
  }
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") setOpen(false);
  });

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var refQuery = document.getElementById("ref-q");
  if (refQuery) {
    var figures = document.querySelectorAll(".logo-grid figure");
    var refCount = document.getElementById("ref-count");
    refQuery.addEventListener("input", function () {
      var query = fold(refQuery.value.trim());
      var shown = 0;
      figures.forEach(function (figure) {
        var ok = !query || fold(figure.textContent).indexOf(query) !== -1;
        figure.hidden = !ok;
        if (ok) shown += 1;
      });
      if (refCount) refCount.textContent = shown + " firma";
    });
  }

  var rail = document.createElement("div");
  rail.className = "scroll-rail";
  rail.setAttribute("aria-hidden", "true");
  document.body.appendChild(rail);
  function paintRail() {
    var max = document.documentElement.scrollHeight - window.innerHeight;
    rail.style.transform = "scaleX(" + (max > 0 ? window.scrollY / max : 0) + ")";
  }
  window.addEventListener("scroll", paintRail, { passive: true });
  paintRail();

  document.querySelectorAll(".info-strip b").forEach(function (node) {
    var raw = node.textContent.trim();
    var match = raw.match(/^(\d+)(\+?)$/);
    if (!match || reduceMotion) return;
    var end = parseInt(match[1], 10);
    var suffix = match[2];
    node.textContent = "0" + suffix;
    var counter = new IntersectionObserver(function (entries) {
      if (!entries[0].isIntersecting) return;
      counter.disconnect();
      var start = performance.now();
      function tick(now) {
        var t = Math.min(1, (now - start) / 1100);
        var eased = 1 - Math.pow(1 - t, 3);
        node.textContent = Math.round(end * eased) + suffix;
        if (t < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    }, { threshold: 0.5 });
    counter.observe(node);
  });

  var stepRow = document.querySelector(".steps");
  if (stepRow && !reduceMotion && "IntersectionObserver" in window) {
    stepRow.classList.add("await");
    var lineWatch = new IntersectionObserver(function (entries) {
      if (!entries[0].isIntersecting) return;
      stepRow.classList.add("lined");
      lineWatch.disconnect();
    }, { threshold: 0.12 });
    lineWatch.observe(stepRow);
  }

  var revealNodes = document.querySelectorAll(".card, .step, .door, .story, .logo-grid figure, .section-head, .group-label, .dark-band, .faq details, .ticks li, .timeline li");
  if (!reduceMotion && "IntersectionObserver" in window && revealNodes.length) {
    revealNodes.forEach(function (node, i) {
      node.classList.add("reveal");
      node.style.transitionDelay = (i % 6) * 70 + "ms";
    });
    var seen = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("in");
        seen.unobserve(entry.target);
      });
    }, { threshold: 0.16, rootMargin: "0px 0px -8% 0px" });
    revealNodes.forEach(function (node) { seen.observe(node); });
  }

  var form = document.querySelector("#iletisim-formu");
  if (!form) return;
  var error = form.querySelector(".error");
  var done = form.querySelector(".done");
  var button = form.querySelector("button[type=submit]");
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (done) done.hidden = true;
    var data = new FormData(form);
    var payload = {
      ad: String(data.get("ad") || "").trim(),
      eposta: String(data.get("eposta") || "").trim(),
      tel: String(data.get("tel") || "").trim(),
      konu: String(data.get("konu") || "").trim(),
      mesaj: String(data.get("mesaj") || "").trim(),
      website: String(data.get("website") || "").trim()
    };
    if (!payload.ad || !payload.eposta || !payload.konu || !payload.mesaj) {
      error.textContent = "Ad, e-posta, konu ve mesaj alanlarını doldurun.";
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(payload.eposta)) {
      error.textContent = "E-posta adresini kontrol edin.";
      return;
    }
    if (payload.website) return;
    if (payload.mesaj.length < 8) {
      error.textContent = "Mesajı biraz daha açın.";
      return;
    }
    error.textContent = "";
    var text = "Merhaba Atlas Patent, " + payload.konu + " için yazıyorum. Adım " + payload.ad + ". E-posta: " + payload.eposta + ".";
    if (payload.tel) text += " Telefon: " + payload.tel + ".";
    text += " " + payload.mesaj;
    window.open("https://wa.me/905556224422?text=" + encodeURIComponent(text), "_blank", "noopener");
    form.reset();
    if (done) done.hidden = false;
  });
})();
