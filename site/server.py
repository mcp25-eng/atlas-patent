# -*- coding: utf-8 -*-
"""Atlas Patent site server: pages, contact inbox, office login."""
import hashlib
import hmac
import json
import os
import re
import secrets
import smtplib
import sqlite3
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path

from flask import Flask, abort, jsonify, redirect, request, send_from_directory, session
from waitress import serve

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
DB_PATH = DATA / "atlas.db"
SECRET_PATH = DATA / "secret.key"
ADMIN_PATH = DATA / "yonetim.json"

TOPICS = {
    "Marka tescil",
    "Patent veya faydalı model",
    "Tasarım",
    "ISO ve yönetim sistemleri",
    "CE, TSE, yerli malı, HACCP",
    "VERBİS / KVKK",
    "İstek",
    "Şikayet",
    "Öneri",
    "İnsan kaynakları",
}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
BLOCKED = {
    "server.py",
    "build_site.py",
    "requirements.txt",
}

app = Flask(__name__)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    MAX_CONTENT_LENGTH=32 * 1024,
)


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                topic TEXT NOT NULL,
                message TEXT NOT NULL,
                ip TEXT NOT NULL,
                seen INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS hits (
                ip TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def load_secret():
    env = os.environ.get("ATLAS_SECRET_KEY", "").strip()
    if env:
        return env
    if SECRET_PATH.exists():
        return SECRET_PATH.read_text(encoding="utf-8").strip()
    key = secrets.token_hex(32)
    SECRET_PATH.write_text(key, encoding="utf-8")
    return key


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200_000)
    return salt, digest.hex()


def ensure_admin():
    env = os.environ.get("ATLAS_ADMIN_PASSWORD", "").strip()
    if env:
        salt, digest = hash_password(env)
        return {"salt": salt, "hash": digest, "source": "env"}
    if ADMIN_PATH.exists():
        return json.loads(ADMIN_PATH.read_text(encoding="utf-8"))
    password = secrets.token_urlsafe(9)
    salt, digest = hash_password(password)
    record = {"salt": salt, "hash": digest, "source": "file"}
    ADMIN_PATH.write_text(json.dumps(record), encoding="utf-8")
    (DATA / "YONETIM-SIFRE.txt").write_text(
        "Yonetim adresi: /yonetim\nSifre: " + password + "\nBu dosyayi kimseyle paylasmayin.\n",
        encoding="utf-8",
    )
    print("Yonetim sifresi olusturuldu. Dosya: data/YONETIM-SIFRE.txt")
    return record


def check_password(password, record):
    salt, digest = hash_password(password, record["salt"])
    return hmac.compare_digest(digest, record["hash"])


def client_ip():
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()[:64]
    return (request.remote_addr or "")[:64]


def too_many(ip):
    cutoff = datetime.now(timezone.utc).timestamp() - 3600
    with db() as conn:
        rows = conn.execute("SELECT created_at FROM hits WHERE ip = ?", (ip,)).fetchall()
        fresh = []
        for row in rows:
            try:
                stamp = datetime.fromisoformat(row["created_at"]).timestamp()
            except ValueError:
                continue
            if stamp >= cutoff:
                fresh.append(row["created_at"])
        conn.execute("DELETE FROM hits WHERE ip = ?", (ip,))
        conn.executemany("INSERT INTO hits (ip, created_at) VALUES (?, ?)", [(ip, item) for item in fresh])
        return len(fresh) >= 8


def remember_hit(ip):
    now = datetime.now(timezone.utc).isoformat()
    with db() as conn:
        conn.execute("INSERT INTO hits (ip, created_at) VALUES (?, ?)", (ip, now))


def send_mail(name, email, phone, topic, message):
    host = os.environ.get("ATLAS_SMTP_HOST", "").strip()
    user = os.environ.get("ATLAS_SMTP_USER", "").strip()
    password = os.environ.get("ATLAS_SMTP_PASSWORD", "").strip()
    recipient = os.environ.get("ATLAS_MAIL_TO", "info@atlaspatent.com.tr").strip()
    if not host or not user or not password:
        return False
    port = int(os.environ.get("ATLAS_SMTP_PORT", "587"))
    mail = EmailMessage()
    mail["Subject"] = "Web sitesi: " + topic
    mail["From"] = user
    mail["To"] = recipient
    mail["Reply-To"] = email
    mail.set_content(
        f"Ad soyad: {name}\nE-posta: {email}\nTelefon: {phone}\nKonu: {topic}\n\n{message}\n"
    )
    with smtplib.SMTP(host, port, timeout=20) as smtp:
        smtp.starttls()
        smtp.login(user, password)
        smtp.send_message(mail)
    return True


def page(title, body):
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{title}</title>
<link rel="stylesheet" href="/css/styles.css">
</head>
<body>
<main class="section"><div class="wrap" style="max-width:860px">
{body}
</div></main>
</body>
</html>"""


ADMIN = None


@app.post("/api/iletisim")
def iletisim():
    if not request.is_json:
        return jsonify(hata="Geçersiz istek."), 400
    data = request.get_json(silent=True) or {}
    if str(data.get("website") or "").strip():
        return jsonify(tamam=True)
    name = str(data.get("ad") or "").strip()
    email = str(data.get("eposta") or "").strip()
    phone = str(data.get("tel") or "").strip()
    topic = str(data.get("konu") or "").strip()
    message = str(data.get("mesaj") or "").strip()
    if not (2 <= len(name) <= 80):
        return jsonify(hata="Ad soyad 2 ile 80 karakter arasında olmalı."), 400
    if not EMAIL_RE.match(email) or len(email) > 120:
        return jsonify(hata="E-posta adresini kontrol edin."), 400
    if len(phone) > 30:
        return jsonify(hata="Telefon çok uzun."), 400
    if topic not in TOPICS:
        return jsonify(hata="Konu listeden seçilmeli."), 400
    if not (8 <= len(message) <= 4000):
        return jsonify(hata="Mesaj 8 ile 4000 karakter arasında olmalı."), 400
    ip = client_ip()
    if too_many(ip):
        return jsonify(hata="Çok fazla deneme. Bir saat sonra yeniden yazın veya arayın."), 429
    now = datetime.now(timezone.utc).isoformat()
    with db() as conn:
        conn.execute(
            """
            INSERT INTO messages (created_at, name, email, phone, topic, message, ip, seen)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
            """,
            (now, name, email, phone, topic, message, ip),
        )
    remember_hit(ip)
    mailed = False
    try:
        mailed = send_mail(name, email, phone, topic, message)
    except Exception:
        mailed = False
    return jsonify(tamam=True, eposta=mailed)


@app.get("/yonetim")
def yonetim():
    if not session.get("office"):
        return page(
            "Yönetim girişi",
            """
            <h1>Ofis girişi</h1>
            <p>Gelen talepler bu ekranda durur.</p>
            <form class="panel form" method="post" action="/yonetim/giris">
              <label>Şifre<input type="password" name="sifre" required autofocus></label>
              <button class="btn btn-gold" type="submit">Giriş</button>
            </form>
            """,
        )
    with db() as conn:
        rows = conn.execute(
            "SELECT * FROM messages ORDER BY id DESC LIMIT 200"
        ).fetchall()
    cards = []
    for row in rows:
        state = "Okundu" if row["seen"] else "Yeni"
        cards.append(
            f"""
            <article class="panel" style="margin-bottom:12px">
              <p><strong>{escape(row['topic'])}</strong> · {escape(state)} · {escape(row['created_at'][:19])}</p>
              <p>{escape(row['name'])}<br>{escape(row['email'])}<br>{escape(row['phone'] or '—')}</p>
              <p>{escape(row['message']).replace(chr(10), '<br>')}</p>
              <form method="post" action="/yonetim/mesaj/{row['id']}/okundu" style="display:inline">
                <button class="btn btn-ghost" type="submit">Okundu işaretle</button>
              </form>
              <form method="post" action="/yonetim/mesaj/{row['id']}/sil" style="display:inline" onsubmit="return confirm('Bu kayıt silinsin mi?')">
                <button class="btn btn-ghost" type="submit">Sil</button>
              </form>
            </article>
            """
        )
    empty = "<p>Henüz mesaj yok.</p>" if not cards else ""
    return page(
        "Gelen kutusu",
        f"""
        <div class="section-head">
          <h1>Gelen talepler</h1>
          <form method="post" action="/yonetim/cikis"><button class="btn btn-ghost" type="submit">Çıkış</button></form>
        </div>
        {empty}
        {''.join(cards)}
        """,
    )


def escape(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


@app.post("/yonetim/giris")
def giris():
    password = request.form.get("sifre", "")
    if not check_password(password, ADMIN):
        return page("Yönetim girişi", "<h1>Şifre uyuşmadı</h1><p><a href=\"/yonetim\">Yeniden dene</a></p>"), 401
    session["office"] = True
    session.permanent = False
    return redirect("/yonetim")


@app.post("/yonetim/cikis")
def cikis():
    session.clear()
    return redirect("/yonetim")


def office_only():
    if not session.get("office"):
        abort(401)


@app.post("/yonetim/mesaj/<int:message_id>/okundu")
def okundu(message_id):
    office_only()
    with db() as conn:
        conn.execute("UPDATE messages SET seen = 1 WHERE id = ?", (message_id,))
    return redirect("/yonetim")


@app.post("/yonetim/mesaj/<int:message_id>/sil")
def sil(message_id):
    office_only()
    with db() as conn:
        conn.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    return redirect("/yonetim")


@app.get("/")
def home():
    return send_from_directory(ROOT, "index.html")


@app.get("/<path:filename>")
def files(filename):
    if filename.startswith("data/") or filename in BLOCKED or ".." in filename:
        abort(404)
    target = (ROOT / filename).resolve()
    if not str(target).startswith(str(ROOT)) or not target.is_file():
        abort(404)
    return send_from_directory(target.parent, target.name)


def main():
    global ADMIN
    app.secret_key = load_secret()
    init_db()
    ADMIN = ensure_admin()
    port = int(os.environ.get("PORT", "5500"))
    print(f"Atlas Patent http://127.0.0.1:{port}")
    serve(app, host="127.0.0.1", port=port, threads=4)


if __name__ == "__main__":
    main()
