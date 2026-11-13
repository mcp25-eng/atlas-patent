# -*- coding: utf-8 -*-
"""Eski ve güncel Atlas Patent sayfalarını PDF'e basar."""
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF
from playwright.sync_api import sync_playwright

ROOT = Path(r"C:\Users\Dell\Desktop\atlanspatent")
OUT = ROOT / "pdf"
TMP = OUT / "_tmp"
OUT.mkdir(exist_ok=True)
TMP.mkdir(exist_ok=True)

PAGE_W, PAGE_H = 1240, 1754
BAR = 52
FONT = Path(r"C:\Windows\Fonts\arial.ttf")
FONTB = Path(r"C:\Windows\Fonts\arialbd.ttf")

NEW = [
    ("index.html", "Ana sayfa"),
    ("hakkimizda.html", "Hakkımızda"),
    ("hizmetler.html", "Hizmetler"),
    ("marka-tescil.html", "Marka tescil"),
    ("patent-tescil.html", "Patent tescil"),
    ("tasarim-tescil.html", "Tasarım tescil"),
    ("faydali-model.html", "Faydalı model"),
    ("cografi-isaret.html", "Coğrafi işaret"),
    ("yurtdisi-tescil.html", "Yurt dışı tescil"),
    ("barkod.html", "Barkod"),
    ("iso-9001.html", "ISO 9001"),
    ("iso-22000.html", "ISO 22000"),
    ("iso-14001.html", "ISO 14001"),
    ("iso-45001.html", "ISO 45001"),
    ("iso-10002.html", "ISO 10002"),
    ("iso-50001.html", "ISO 50001"),
    ("iso-27001.html", "ISO 27001"),
    ("helal-gida.html", "Helal belgelendirme"),
    ("verbis-kvkk.html", "VERBİS ve KVKK"),
    ("yerli-mali-belgesi.html", "Yerli malı belgesi"),
    ("ce-belgesi.html", "CE belgesi (AT uygunluk beyanı)"),
    ("ce-akredite.html", "CE belgesi (akredite)"),
    ("ce-en-1090.html", "TS EN 1090-1 CE belgesi"),
    ("brcgs.html", "BRCGS danışmanlığı"),
    ("hak-akrediteli.html", "HAK akrediteli helal"),
    ("haccp.html", "HACCP"),
    ("tse-urun-belgesi.html", "TSE ürün belgelendirme"),
    ("referanslar.html", "Referanslar"),
    ("haberler.html", "Rehber"),
    ("konya-marka-tescil.html", "Konya'da marka tescili"),
    ("haccp-dosyasi-nedir.html", "HACCP dosyası"),
    ("ce-teknik-dosya.html", "CE teknik dosyasında neler bulunur"),
    ("yerli-mali-belgesi-kimler-icin.html", "Yerli malı belgesi kimler için"),
    ("tse-ve-ce-farki.html", "TSE ve CE farkı"),
    ("sss.html", "Sık sorulan sorular"),
    ("konya-marka-patent.html", "Ofisimiz"),
    ("iletisim.html", "İletişim"),
    ("gizlilik.html", "Kişisel veriler"),
]

FREEZE = """
() => {
  const css = document.createElement('style');
  css.textContent = `
    * { animation: none !important; transition: none !important; }
    .cover-copy > * { opacity: 1 !important; transform: none !important; }
    .cover-slide { opacity: 0 !important; }
    .cover-slide.is-in { opacity: 1 !important; }
  `;
  document.head.appendChild(css);
  const slides = document.querySelectorAll('.cover-slide');
  slides.forEach((slide, i) => slide.classList.toggle('is-in', i === 0));
}
"""


def font(size, bold=False):
    return ImageFont.truetype(str(FONTB if bold else FONT), size)


def text_page(title, lines, footer=""):
    im = Image.new("RGB", (PAGE_W, PAGE_H), "#f7f4ee")
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, PAGE_W, 18), fill="#9a7340")
    draw.text((64, 70), title, fill="#1c1915", font=font(36, True))
    y = 140
    body = font(20)
    for line in lines:
        if y > PAGE_H - 80:
            break
        draw.text((64, y), line, fill="#3a342c", font=body)
        y += 32
    if footer:
        draw.text((64, PAGE_H - 56), footer, fill="#6d655c", font=font(16))
    return im


def wrap(text, width=62):
    words = text.replace("\r", "").split()
    if not words:
        return [""]
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if len(trial) > width:
            if cur:
                lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def autoscroll(page):
    page.evaluate(
        """async () => {
      const delay = (ms) => new Promise((r) => setTimeout(r, ms));
      const height = () => Math.max(
        document.body.scrollHeight,
        document.documentElement.scrollHeight
      );
      for (let y = 0; y < height(); y += 900) {
        window.scrollTo(0, y);
        await delay(30);
      }
      window.scrollTo(0, 0);
    }"""
    )


def shoot(page, url, dest, settle=700):
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    try:
        page.wait_for_load_state("networkidle", timeout=12000)
    except Exception:
        pass
    page.wait_for_timeout(settle)
    try:
        page.evaluate(FREEZE)
    except Exception:
        pass
    try:
        autoscroll(page)
    except Exception:
        pass
    page.wait_for_timeout(200)
    page.screenshot(path=str(dest), full_page=True)
    return dest


def slices(src, label):
    im = Image.open(src).convert("RGB")
    ratio = PAGE_W / im.width
    im = im.resize((PAGE_W, max(1, int(im.height * ratio))), Image.Resampling.LANCZOS)
    room = PAGE_H - BAR
    count = max(1, math.ceil(im.height / room))
    pages = []
    y = 0
    n = 1
    while y < im.height:
        canvas = Image.new("RGB", (PAGE_W, PAGE_H), "#ffffff")
        draw = ImageDraw.Draw(canvas)
        draw.rectangle((0, 0, PAGE_W, BAR), fill="#f7f4ee")
        draw.rectangle((0, BAR - 3, PAGE_W, BAR), fill="#9a7340")
        caption = f"{label}   ·   {n}/{count}"
        draw.text((24, 14), caption, fill="#1c1915", font=font(18, True))
        crop = im.crop((0, y, PAGE_W, min(y + room, im.height)))
        canvas.paste(crop, (0, BAR))
        pages.append(canvas)
        y += room
        n += 1
    im.close()
    return pages


class Binder:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.n = 0

    def add(self, im):
        jpg = TMP / f"{self.name}-{self.n:04d}.jpg"
        im.convert("RGB").save(jpg, "JPEG", quality=78, optimize=True)
        im.close()
        self.files.append(jpg)
        self.n += 1

    def add_slices(self, src, label):
        for im in slices(src, label):
            self.add(im)

    def save(self, dest):
        pdf = FPDF(unit="pt", format="A4")
        pdf.set_auto_page_break(False)
        pdf.set_compression(True)
        for jpg in self.files:
            pdf.add_page()
            pdf.image(str(jpg), x=0, y=0, w=595.28, h=841.89)
        pdf.output(str(dest))
        print("yazildi", dest, "sayfa", len(self.files), flush=True)


def old_pages():
    data = json.loads((ROOT / "icerik" / "sayfalar.json").read_text(encoding="utf-8"))
    items = []
    for page in data["pages"]:
        path = page.get("path") or ""
        title = page.get("title") or path or "Ana sayfa"
        url = "https://www.atlaspatent.com.tr/" + path
        items.append((url, title, page.get("text") or ""))
    return items


def capture_new(page):
    shots = []
    base = "http://127.0.0.1:5500/"
    page.goto(base, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(900)
    page.evaluate(FREEZE)
    for i, name in enumerate(("Marka", "Patent", "Sistem", "Selçuklu")):
        page.evaluate(
            """(i) => {
              document.querySelectorAll('.cover-slide').forEach((slide, n) => {
                slide.classList.toggle('is-in', n === i);
              });
              document.querySelectorAll('.cover-tabs button').forEach((tab, n) => {
                tab.classList.toggle('on', n === i);
                tab.setAttribute('aria-selected', n === i ? 'true' : 'false');
              });
            }""",
            i,
        )
        page.wait_for_timeout(250)
        dest = TMP / f"kapak-{i}.png"
        page.locator(".cover").screenshot(path=str(dest))
        shots.append((dest, f"GÜNCEL kapak · {name}"))
    for i, (name, label) in enumerate(NEW):
        dest = TMP / f"yeni-{i:02d}.png"
        if dest.exists() and dest.stat().st_size > 20000:
            print("var", label, flush=True)
            shots.append((dest, f"GÜNCEL · {label}"))
            continue
        print("yeni", label, flush=True)
        shoot(page, base + name, dest)
        shots.append((dest, f"GÜNCEL · {label}"))
    return shots


def capture_old(page):
    shots = []
    ok = False
    try:
        resp = page.goto("https://www.atlaspatent.com.tr/", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(1500)
        title = page.title()
        status = resp.status if resp else 0
        body = page.inner_text("body")[:400]
        print("eski durum", status, title, flush=True)
        ok = status and status < 400 and "Attention Required" not in title and "Just a moment" not in title
        if "marka" not in body.lower() and "atlas" not in body.lower():
            ok = False
    except Exception as exc:
        print("eski acilamadi", exc, flush=True)
        ok = False
    if not ok:
        return shots, False
    for i, (url, title, _text) in enumerate(old_pages()):
        dest = TMP / f"eski-{i:02d}.png"
        print("eski", title, flush=True)
        try:
            shoot(page, url, dest, settle=900)
            shots.append((dest, f"ESKİ · {title}"))
        except Exception as exc:
            print("eski hata", title, exc, flush=True)
    return shots, True


def archive_pages():
    pages = []
    intro = [
        "Canlı eski site bu bilgisayardan görüntü olarak açılamadı.",
        "Aşağıdaki metin, siteden daha önce alınan arşivin aynısıdır.",
        "Yeni sayfa görüntüleri bu PDF'nin ikinci bölümündedir.",
        "",
    ]
    pages.append(text_page("Eski site · arşiv notu", intro))
    for url, title, text in old_pages():
        body = text.strip() or "(Bu sayfada gövde metni yoktu. İçerik görsel veya menüden oluşuyordu.)"
        lines = wrap(title) + [""] + wrap(url) + [""] + wrap(body)
        chunk = []
        for line in lines:
            chunk.append(line)
            if len(chunk) >= 42:
                pages.append(text_page("ESKİ · " + title[:42], chunk, url))
                chunk = []
        if chunk:
            pages.append(text_page("ESKİ · " + title[:42], chunk, url))
    return pages


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(
            viewport={"width": 1366, "height": 900},
            device_scale_factor=1,
            locale="tr-TR",
            ignore_https_errors=True,
        )
        page = context.new_page()
        old_shots, old_ok = capture_old(page)
        new_shots = capture_new(page)
        browser.close()

    note = [
        "Bu dosya iki bölümden oluşur.",
        "1. Eski site: atlaspatent.com.tr üzerinde duran hâlin görüntüsü.",
        "2. Yeni site: şu an yerelde çalışan güncel hâlin görüntüsü.",
        "",
        "Güncel sitenin sadece yeni hâlini içeren ayrı PDF de vardır:",
        "Atlas-Patent-GUNCEL-site.pdf",
        "",
        "Kapak slaytı hareketlidir. PDF'de dört slayt da ayrı kare olarak durur.",
        "Referans logoları eski galerideki 51 dosyanın aynısıdır.",
    ]
    if not old_ok:
        note[1] = "1. Eski site görüntüsü alınamadı; arşivdeki metin basıldı."
    compare = Binder("k")
    current = Binder("g")
    compare.add(text_page("Atlas Patent · eskiden ve şimdi", note))

    if old_ok:
        compare.add(text_page("Bölüm 1 · Eski site", ["atlaspatent.com.tr", "Aşağıdaki sayfalar eski sitenin ekran görüntüsüdür."]))
        for src, label in old_shots:
            compare.add_slices(src, label)
    else:
        for im in archive_pages():
            compare.add(im)

    compare.add(text_page("Bölüm 2 · Güncel site", [
        "http://127.0.0.1:5500",
        "Aşağıdaki sayfalar güncel sitenin tam sayfa görüntüsüdür.",
        "Aynı görüntüler Atlas-Patent-GUNCEL-site.pdf dosyasında da durur.",
    ]))
    current.add(text_page("Atlas Patent · güncel site", [
        "Bu PDF, sitenin şu anki hâlinin tamamıdır.",
        "Her HTML sayfası, ekranda göründüğü biçimde, kesilmeden basıldı.",
        "",
        "İlk dört kare ana sayfa kapağının dört slaytıdır.",
        "Sonraki sayfalar menü sırasıyla bütün sitedir.",
        "",
        "Sayfa sayısı: " + str(len(NEW)),
        "Adres: http://127.0.0.1:5500",
    ]))
    for src, label in new_shots:
        parts = slices(src, label)
        for im in parts:
            # aynı kare iki dosyaya girecek; ikinci kayıt için kopya
            copy = im.copy()
            compare.add(im)
            current.add(copy)

    current.save(OUT / "Atlas-Patent-GUNCEL-site.pdf")
    compare.save(OUT / "Atlas-Patent-ESKI-ve-YENI.pdf")
    print("PDF tamam", "eski_goruntu" if old_ok else "eski_arsiv", flush=True)


if __name__ == "__main__":
    main()
