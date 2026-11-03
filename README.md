# Atlas Patent

Alan adı: https://www.atlaspatent.com.tr/

Yayın klasörü `site` içindedir. Sayfalar hazır HTML’dir. İletişim formu ve ofis paneli için aynı klasörde Python sunucusu çalışır.

## Sunucuda

```bash
cd site
python -m pip install -r requirements.txt
python server.py
```

Sunucu yalnızca `127.0.0.1` adresini dinler. Dışarı varsayılan kapı `5500`’dür. `PORT` ortam değişkeniyle değişir.

DNS, alan adını bu makineye çevirir. Web sunucusu (nginx, Caddy veya panel) `atlaspatent.com.tr` ve `www.atlaspatent.com.tr` isteklerini `http://127.0.0.1:5500` adresine iletir.

## Forma gelen yazılar

SMTP tanımlı değilse mesaj sunucudaki veritabanında kalır. Panel adresi `/yonetim`. İlk çalıştırmada şifre sunucuda `site/data/YONETIM-SIFRE.txt` dosyasına yazılır. Bu dosya depoya konmaz.

Posta için ortam değişkenleri: `ATLAS_SMTP_HOST`, `ATLAS_SMTP_PORT`, `ATLAS_SMTP_USER`, `ATLAS_SMTP_PASSWORD`. Alıcı varsayılan olarak `info@atlaspatent.com.tr` (`ATLAS_MAIL_TO`).
