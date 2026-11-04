# -*- coding: utf-8 -*-
"""Generate the Atlas Patent static site."""
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\Dell\Desktop\atlanspatent")
SITE = ROOT / "site"
IMG = ROOT / "icerik" / "gorseller"
BASE = "https://www.atlaspatent.com.tr/"
PHONE = "0555 622 44 22"
TEL = "tel:+905556224422"
WA = "https://wa.me/905556224422"
EMAIL = "info@atlaspatent.com.tr"
ADDRESS = "Binkonutlar Mh. Udi Sk. No:4/D D:1 Selçuklu/KONYA"
MAP = "https://maps.google.com/maps?q=37.946813,32.510319&z=16"

DISCLAIMER = (
    "Süreç süreleri başvuruya, itiraza ve kurumun iş yüküne göre değişir. "
    "Sayfalar genel bilgilendirme amaçlıdır. Atlas Patent belgelendirme kuruluşu, "
    "onaylanmış kuruluş veya akreditasyon kurumu değildir; ISO, CE, TSE, helal ve "
    "BRCGS süreçlerinde dokümantasyon ve başvuru danışmanlığı verir."
)

REFS = [
    ("ASİL CİVATA", "1668762482.jpg"),
    ("BEYAZSARAY MÜHENDİSLİK", "1668762791.jpg"),
    ("GROSS BU1 MARKET", "1668763193.jpg"),
    ("BSK LABORATUVAR", "1668763289.jpg"),
    ("CLİNODEVİCE", "1668763478.jpg"),
    ("DERMALİZ GÜZELLİK SALONU", "1668763561.jpg"),
    ("DİYAR KOLONYA", "1668764011.jpg"),
    ("ESELYA ECLAIR & DONUT", "1668764771.jpg"),
    ("ELEKTRO MEKANİK GARAJ", "1668764818.jpg"),
    ("ERDEM PREFABRİK", "1668764846.jpg"),
    ("EROL YAMAN SUCUKLARI AKŞEHİR", "1668764894.jpg"),
    ("GAZİANTEP SOKAK LEZZETLERİ", "1668764926.jpg"),
    ("CİELO BUTİK", "1668764959.jpg"),
    ("HC MOTOR", "1668765058.jpg"),
    ("HÇ MOTOR", "1668765071.jpg"),
    ("HKB GAZİANTEPLİ HACI KERİMOĞLU BAKLAVALARI", "1668765442.jpg"),
    ("KOLLEZYUM BİLİŞİM", "1668765478.jpg"),
    ("KONAK TEL ÇİT AKSARAY", "1668765533.jpg"),
    ("Coffee Marrón", "1668765641.jpg"),
    ("METİN YILMAZ SUCUKLARI", "1668765733.jpg"),
    ("MUSALLAT KORKU EVİ", "1668765820.jpg"),
    ("NEFA CATERİNG", "1668766001.jpg"),
    ("OTOLASTEK EKİPMAN", "1668766037.jpg"),
    ("ÖNAY HİDROLİK", "1668766063.jpg"),
    ("NRM HYDRAULIC", "1668766110.jpg"),
    ("POXY-E-POXY", "1668766230.jpg"),
    ("SAYAR CNC", "1668766614.jpg"),
    ("SEZER ŞEKERLEME", "1668766698.jpg"),
    ("SİNOP REALİST GAYRİMENKUL", "1668766786.jpg"),
    ("ŞAHİN PEN CAM BALKON", "1668766825.jpg"),
    ("TOSTÇU ŞAKİR", "1668766850.jpg"),
    ("TÜRKER SAUNA", "1668766874.jpg"),
    ("UKM UZMANLAR KALİBRASYON", "1668766942.jpg"),
    ("WHITE 8 OZ", "1668766971.jpg"),
    ("YER6 KORKU EVİ", "1668767052.jpg"),
    ("YUMURTACI MURAT", "1668767129.jpg"),
    ("KUŞATAN YEMEK & ORGANİZASYON", "1668767321.jpg"),
    ("4E PLASTİK", "1699619384.jpg"),
    ("KAPUZBAŞI ŞELALESİ", "1699619422.jpg"),
    ("BARNVİTA", "1699619450.jpg"),
    ("BE FİT CAFE", "1699619472.jpg"),
    ("BGHLİMON", "1699619494.jpg"),
    ("DEFNEM GROSS", "1699619519.jpg"),
    ("KDB KÜPE DAĞI BALI", "1699619558.jpg"),
    ("NEVTAT POLAT", "1699619594.jpg"),
    ("NORM HİDROLİK", "1699619623.jpg"),
    ("ORIGINAL ROCKET SHOT", "1699619652.jpg"),
    ("TATAR SAVATRA MARKET", "1699619679.jpg"),
    ("YAĞLIBAYAT SAVATRA", "1699619707.jpg"),
    ("TWISTED ORIGINAL PART", "1699619727.jpg"),
    ("KÖFTECİ SOFU", "1699619878.png"),
]


def e(text):
    return html.escape(text, quote=True)


def ul(items):
    return "<ul>" + "".join(f"<li>{html.escape(i)}</li>" for i in items) + "</ul>"


def h2(text):
    return f"<h2>{html.escape(text)}</h2>"


SERVICES = []


def add_service(slug, group, name, card, seo_title, description, lead, body, faq):
    SERVICES.append({
        "slug": slug,
        "group": group,
        "name": name,
        "card": card,
        "seo_title": seo_title,
        "description": description,
        "lead": lead,
        "body": body,
        "faq": faq,
    })


add_service(
    "marka-tescil", "Sınai mülkiyet", "Marka tescil",
    "İsim, logo ve ayırt edici işaretlerin tescili, yenilemesi ve takibi.",
    "Marka Tescil Konya | Atlas Patent",
    "Konya Atlas Patent ile marka araştırması, sınıf seçimi, TÜRKPATENT başvurusu, bülten takibi ve yenileme. Marka tescil danışmanlığı.",
    "Marka, mal veya hizmetlerinizi başkasınınkinden ayıran işarettir. Tescil, bu işareti sicile yazdırır ve kullanımı size bağlar.",
    h2("Marka nedir?") + """
<p>Kişi adları dahil sözcükler, şekiller, harfler, sayılar, sesler, renkler, malların biçimi veya ambalajı gibi işaretler marka olabilir. Ayırt edici olmalı ve sicilde korunacak konu anlaşılır biçimde gösterilebilmelidir. Güncel çerçeve 6769 sayılı Sınai Mülkiyet Kanunu'dur.</p>
""" + h2("Markayı seçerken") + ul([
        "Kolay okunmalı ve kulağa düzgün gelmeli.",
        "Akılda kalmalı, kolay taklit edilmemeli.",
        "İhracat varsa hedef ülkenin dilinde olumsuz anlam taşımamalı.",
        "Kullanmaya başlamadan önce benzer marka araştırması yapılmalı.",
        "Tescil yolu açıksa, kullanımdan önce başvuru yapılmalı.",
    ]) + """
<p>Tüketicinin güvendiği isme yaslanan taklidi durdurmanın ilk adımı tescildir. Tescilsiz kullanım, başkası aynı işareti önce tescil ettirirse risk doğurur.</p>
""" + h2("Başvuru nasıl ilerler?") + ul([
        "Ön görüşme: faaliyet, hedef pazar ve korunacak işaretler birlikte yazılır.",
        "Araştırma: benzer kelime, ses ve görseller taranır; risk size anlatılır.",
        "Sınıf: mal ve hizmetler Nice sınıflarına yerleştirilir. Dar liste korumayı eksik bırakır, gereksiz sınıf maliyeti artırır.",
        "Başvuru: marka örneği ve emtia listesi hazırlanır, başvuru elektronik ortamda yapılır.",
        "İnceleme ve bülten: eksiklik veya ret yazısı olursa süresi içinde cevaplanır. Yayından sonra iki aylık itiraz süresi izlenir.",
        "Tescil ve sonrası: belge teslim edilir, yenileme ve bülten takibi planlanır.",
    ]) + """
<p>İtiraz gelmezse süreç çoğu dosyada birkaç ay ile bir yıl arasında tamamlanır. Başvuru tarihi, rüçhan açısından önemlidir. Koruma süresi on yıldır ve onar yıllık dönemlerle yenilenebilir.</p>
""" + h2("Atlas Patent bu dosyada ne yapar?") + ul([
        "Tescil edilebilirlik ön araştırması",
        "Sınıf listesinin kurulması",
        "Başvuru ve eksiklik yazılarının takibi",
        "İtirazlara karşı görüş için dosya hazırlığı",
        "Yenileme tarihi takibi",
        "Yurt dışı başvuru seçeneklerinin anlatılması",
    ]),
    [
        ("Marka tescili ne kadar sürer?", "İtiraz ve eksiklik yoksa çoğu dosya birkaç ay ile bir yıl arasında sonuçlanır. Süre kurumun iş yüküne bağlıdır. Başvuru yapıldığı gün korumanın başlangıç tarihi oluşur."),
        ("Tescil kaç yıl geçerli?", "On yıldır. Süre bitmeden yenilenirse koruma devam eder."),
        ("Logo ve isim ayrı mı tescil edilir?", "Kelime, şekil veya ikisi birlikte başvurulabilir. Hangisinin size daha sağlam koruma verdiğini ön araştırmadan sonra konuşuruz."),
    ],
)

add_service(
    "patent-tescil", "Sınai mülkiyet", "Patent tescil",
    "Yenilik, buluş basamağı ve sanayiye uygulanabilirlik taşıyan buluşların korunması.",
    "Patent Tescil | Atlas Patent",
    "Buluşunuz için patentlenebilirlik değerlendirmesi, tarifname ve istem hazırlığı, ulusal patent başvurusu ve süreç takibi. Konya Atlas Patent.",
    "Patent, buluşu belirli süre üçüncü kişilerin izinsiz üretmesine, kullanmasına ve satmasına karşı korur.",
    h2("Patent ne sağlar?") + """
<p>Buluş sahibi emek, zaman ve para harcar. Buluş piyasaya çıkınca başkaları da görebilir. Patent, bu emeğe karşılık sınırlı bir süre tekel benzeri bir işletme hakkı verir: üretmek, kullanmak ve satmak gibi fiiller hak sahibinin iznine bağlanır.</p>
<p>Koruma yalnızca hak sahibine yaramaz. Tarifname yayımlandığı için teknik bilgi toplumla paylaşılır. Bu da yeni ürün ve yöntemlerin duyulmasını, Ar-Ge'nin teşvik edilmesini sağlar.</p>
""" + h2("Patentlenebilirlik") + ul([
        "Yenilik: buluş, başvuru tarihinden önce dünyanın herhangi bir yerinde kamuya sunulmamış olmalıdır.",
        "Buluş basamağı: ilgili alandaki uzmana göre aşikar olmamalıdır.",
        "Sanayiye uygulanabilirlik: üretilip kullanılabilir olmalıdır.",
    ]) + """
<p>Koruma, başvuru tarihinden itibaren yirmi yıla kadar sürebilir ve yıllık ücretler aksatılmamalıdır. Patent ülkeseldir. Başka ülkeler için ayrı başvuru veya PCT yoluyla uluslararası rota gerekir. Ayrıntı için <a href="yurtdisi-tescil.html">yurt dışı tescil</a> sayfasına bakın.</p>
<p>Küçük teknik geliştirmeler her zaman patente uygun olmayabilir. O dosyalarda <a href="faydali-model.html">faydalı model</a> daha doğru araç olabilir.</p>
""" + h2("Dosyada birlikte yürüdüğümüz adımlar") + ul([
        "Buluşun anlatılması ve ön değerlendirme",
        "Teknik tarifname, istem ve resimlerin düzenlenmesi",
        "Ulusal başvurunun hazırlanması",
        "Kurum yazılarının takibi",
        "Tescil sonrası yıllık ücret takviminin hatırlatılması",
    ]),
    [
        ("Patent ile faydalı model arasındaki fark nedir?", "Patentte yeniliğin yanında buluş basamağı da aranır ve koruma yirmi yıla kadar çıkar. Faydalı model daha kısa sürelidir ve daha çok somut ürünlerdeki teknik geliştirmeye uygundur."),
        ("Fikrimi anlattıktan sonra başkası başvurabilir mi?", "Kamuya açıklamadan önce başvuru stratejisini konuşmak gerekir. Açıklama, yeniliği ortadan kaldırabilir."),
    ],
)

add_service(
    "tasarim-tescil", "Sınai mülkiyet", "Tasarım tescil",
    "Ürünün görünümünü korur. Fonksiyonu değil, çizgi, biçim, renk ve dokuyu tescil eder.",
    "Tasarım Tescil | Endüstriyel Tasarım | Atlas Patent",
    "Endüstriyel tasarım tescili: yenilik, başvuru evrakı, beş yıllık koruma ve yirmi beş yıla kadar yenileme. Atlas Patent Konya.",
    "Tasarım tescili, ürünün görünüşünü korur. Patentte ortada teknik bir buluş vardır; tasarımda çizgi, şekil, renk, biçim, doku ve süsleme vardır.",
    h2("Ne tescil edilir?") + """
<p>Ürünün tamamının veya bir parçasının insan duyularıyla algılanan görünümü tescil edilir. Üçüncü kişilerin bu görünümü izinsiz kullanması engellenir. Tasarım yeni olmalıdır. Yenilik değerlendirmesinde, kamuya sunulmanın üzerinden uzun süre geçmiş bir görünüm sorun çıkarabilir. Eski sitede de belirttiğimiz gibi, kamuya sunuluşun üzerinden bir yılı aşmış olmak yeniliği zedeler.</p>
""" + h2("Süre ve süreç") + ul([
        "Koruma beş yıldır. Beşer yıllık yenilemelerle en fazla yirmi beş yıla çıkar.",
        "Başvuru aynı gün elektronik olarak yapılabilir. Başvuru tarihinden itibaren koruma hesabı işler.",
        "Kurum önce şekli inceleme yapar. Şartlar tamamsa tasarım tescil edilir ve bültende yayımlanır.",
        "Yayın sürecinde üçüncü kişiler itiraz edebilir. Bu yüzden kendi tasarımınız ve rakipler için bülten takibi faydalıdır.",
        "Tescil ülkeseldir. Başka ülkelerde koruma için ayrı başvuru gerekir.",
    ]) + """
<p>Eski dosyalarımızda sürecin yaklaşık sekiz ay sürdüğünü görüyoruz. Güncel süre, inceleme ve itiraza göre değişir.</p>
""" + h2("İstenen belgeler") + ul([
        "Tasarımın resimleri",
        "Başvuru sahibi ve tasarımcının bilgileri",
        "Vekaletname, temsil söz konusuysa",
    ]) + """
<p>Hak ihlalinde 6769 sayılı Kanun hukuk ve ceza yollarını düzenler. Somut yaptırım, fiile ve güncel kanuna göre belirlenir. Eski KHK metinlerindeki para ve hapis aralıklarını güncel ceza diye kullanmıyoruz.</p>
""",
    [
        ("Tasarım tescili patente benzer mi?", "Hayır. Patent teknik çözümü, tasarım ürünün görünümünü korur."),
        ("Kaç yıl korunur?", "Beş yıl. Yenilemelerle üst sınır yirmi beş yıldır."),
    ],
)

add_service(
    "faydali-model", "Sınai mülkiyet", "Faydalı model",
    "Üründeki teknik geliştirmeyi daha kısa ve daha sade bir korumayla tescil eder.",
    "Faydalı Model Tescil | Atlas Patent",
    "Faydalı model tescili: yenilik ve sanayiye uygulanabilirlik, on yıla kadar koruma. Konya Atlas Patent başvuru danışmanlığı.",
    "Faydalı model, patente göre daha kısa koruma isteyen ve buluş basamağı eşiğine takılmayan teknik geliştirmeler içindir.",
    """
<p>Buluş sahibi yine emek ve masraf harcar. Faydalı model, üçüncü kişilerin bu ürünü izinsiz üretmesini ve satmasını belirli süre engeller. Patentten farkı şudur: patente yenilik, buluş basamağı ve sanayiye uygulanabilirlik birlikte aranır. Faydalı modelde yenilik ve sanayiye uygulanabilirlik öne çıkar; koruma on yıldır.</p>
<p>Kimyasal maddeler ve usuller gibi bazı konular faydalı modele uygun değildir. Ürünün şeklinde veya parçasında somut bir teknik etki varsa bu yol daha hızlı ve daha ekonomik olabilir. Kararı, buluşu dinlemeden vermiyoruz.</p>
""" + h2("Ne zaman faydalı model?") + ul([
        "Mevcut bir üründe ölçülebilir teknik iyileştirme varsa",
        "Yirmi yıllık patent süresi gerekmiyorsa",
        "Buluş basamağı tartışmalı görünüp yenilik açıksa",
    ]) + """
<p>Tarifname ve resimler yine özen ister. Zayıf yazılmış bir istem, belge çıksa bile korumayı daraltır.</p>
""",
    [
        ("Faydalı model kaç yıl sürer?", "On yıldır ve patentteki gibi yirmi yıla uzamaz."),
        ("Her buluş faydalı model olur mu?", "Hayır. Konu ürünle ilgili olmalı ve kanunun faydalı model dışında bıraktığı alanlara girmemelidir."),
    ],
)

add_service(
    "cografi-isaret", "Sınai mülkiyet", "Coğrafi işaret",
    "Bir yörenin adıyla anılan ürünün menşe veya mahreç olarak tescili.",
    "Coğrafi İşaret Tescili | Atlas Patent",
    "Menşe ve mahreç coğrafi işaret başvurusu, denetim şartları ve TÜRKPATENT süreci. Atlas Patent Konya.",
    "Coğrafi işaret, bir ürünün belirli bir yöreyle ün, kalite veya diğer özellikler üzerinden bağını korur.",
    """
<p>İki tür vardır. Menşe adı, tüm üretim aşamalarının o yörede geçtiği ürünler içindir. Mahreç işareti, niteliklerinden en az birinin o yöreye bağlandığı, üretimin bir kısmının başka yerde olabildiği ürünler içindir.</p>
<p>Konya ve çevresinde gıda, el sanatları ve tarım ürünlerinde bu bağ sık görülür. Tescil, yöre adının başkalarınca gelişigüzel kullanılmasını sınırlar. Başvuruda ürünün tanımı, üretim yöntemi, coğrafi sınır ve denetim düzeni yazılır.</p>
<p>Atlas Patent, dosyanın kurulması ve kurum yazışmalarının takibinde yanınızdadır. Denetim kuruluşunun seçimi ve ürün standardı, başvurunun parçasıdır.</p>
""",
    [
        ("Menşe ile mahreç aynı mı?", "Değildir. Menşede üretim baştan sona o yörededir. Mahreçte karakteristik özelliklerin bir kısmı yöreye bağlıdır."),
    ],
)

add_service(
    "yurtdisi-tescil", "Sınai mülkiyet", "Yurt dışı tescil",
    "Markada Madrid sistemi, buluşta PCT ve ülke seçimine göre ulusal başvurular.",
    "Yurt Dışı Marka ve Patent | Atlas Patent",
    "Yurt dışı marka ve patent başvurusu: Madrid sistemi, PCT ve ülke seçimi. Atlas Patent danışmanlığı, Konya.",
    "Türkiye'deki tescil başka ülkede kendiliğinden koruma doğurmaz. Hedef pazar için ayrı bir rota gerekir.",
    """
<p>Markada Madrid Sistemi, tek başvuru üzerinden birden çok ülkede koruma istemeye yarar. Her ülkenin ofisi kendi incelemesini yapar. Hangi ülkelerin seçileceği, sattığınız veya satacağınız pazarla belirlenir.</p>
<p>Buluşta PCT, çok sayıda ülkede son tarihi koruyarak ulusal aşamaya geçmeden önce süre kazandırır. PCT belge vermez; asıl koruma, seçilen ülkelerin ofislerinde doğar. Tasarım için de hedef ülkeye göre ulusal veya bölgesel başvuru konuşulur.</p>
<p>Önce Türkiye başvurusunun tarihi ve rüçhan süresi hesaplanır. Süre kaçırılırsa yabancı ülkede yenilik veya öncelik kaybı olur. Atlas Patent bu takvimi dosya açılırken yazar.</p>
""",
    [
        ("Türkiye tescili Avrupa'da da geçerli mi?", "Hayır. Her ülke veya bölge için başvuru gerekir. Madrid veya PCT bu başvuruları tek çatı altında toplamaya yardım eder, incelemeyi ortadan kaldırmaz."),
    ],
)

add_service(
    "barkod", "Sınai mülkiyet", "Barkod",
    "GS1 barkod numarasının alınması ve ürünlerin numaralandırılması.",
    "Barkod Tescil | Atlas Patent Konya",
    "Ürün barkodu için GS1 numarası, firma öneki ve etiket danışmanlığı. Atlas Patent Konya.",
    "Barkod, marka tescili değildir. Market ve pazaryeri sistemlerinin ürünü tanıması için küresel bir numaradır.",
    """
<p>Türkiye'de firma öneki GS1 Türkiye üzerinden alınır. Önce şirket ve ürün çeşitliliği konuşulur, kaç numaraya ihtiyaç olduğu çıkarılır, ardından ürünler numaralandırılır. Yanlış kurulan bir önek, yeni ürün ekledikçe baştan dağıtılır.</p>
<p>Barkod, markanın taklit edilmesini engellemez. Rafta kimliğiniz için barkod, hukuki koruma için marka tescili gerekir. İkisini aynı dosyada yürütebiliriz.</p>
""",
    [
        ("Barkod markamı korur mu?", "Hayır. Barkod lojistik kimliktir. Koruma için marka tescili gerekir."),
    ],
)

ISO_STEPS = ul([
    "Kuruluşun yapısı ve sistem ihtiyacının belirlenmesi",
    "Standardın kuruluşun süreçlerine göre kurulması",
    "Uygulama ve kayıtların işletilmesi",
    "Akreditasyon kapsamına göre belgelendirme kuruluşunun seçilmesi",
    "Belgelendirme denetimi",
    "Belgenin alınması ve gözetim denetimlerine hazırlık",
])


def iso(what, who, benefits, extra=""):
    return h2("Standart ne işe yarar?") + what + h2("Kimler için?") + ul(who) + h2("Ne kazandırır?") + ul(benefits) + extra + h2("Nasıl ilerleriz?") + ISO_STEPS


add_service(
    "iso-9001", "Yönetim sistemleri", "ISO 9001",
    "Kalite yönetim sistemi kurulumu ve belgelendirme denetimine hazırlık.",
    "ISO 9001 Danışmanlığı | Atlas Patent",
    "ISO 9001:2015 kalite yönetim sistemi danışmanlığı, dokümantasyon ve belgelendirme denetimine hazırlık. Konya Atlas Patent.",
    "ISO 9001, üretim ve hizmette kalitenin kişiye değil sisteme bağlandığı uluslararası standarttır.",
    iso(
        "<p>İster üretim ister hizmet olsun, ISO 9001:2015 belgesi müşterinin ve tedarik zincirinin aradığı kalite göstergelerinden biridir. Büyüklük fark etmeksizin süreçlerin izlenmesini ve yönetilmesini kolaylaştırır.</p>",
        ["Üretim ve imalat kuruluşları", "Hizmet kuruluşları", "Belediyeler ve organize sanayi bölgeleri", "Kooperatif, dernek ve vakıflar", "Özel ve kamu kuruluşları"],
        ["Her ölçekte ve her ürün tipinde uygulanabilir.", "İhale şartnamelerinde sık istendiği için iş almayı kolaylaştırır.", "Hata ve tekrar iş azalır, kaynak daha iyi kullanılır.", "Çalışanlar sürece katılır.", "İhracatta ve iç pazarda ürünün kabulünü destekler.", "Kurumsallaşmaya somut bir adım olur."],
    ),
    [("Belgeyi siz mi veriyorsunuz?", "Hayır. Sistemi kurar, denetimden önce hazırlarız. Belgeyi akredite belgelendirme kuruluşu verir.")],
)

add_service(
    "iso-22000", "Yönetim sistemleri", "ISO 22000",
    "Gıda zincirinde çiftlikten tabağa gıda güvenliği yönetim sistemi.",
    "ISO 22000 Danışmanlığı | Atlas Patent",
    "ISO 22000:2018 gıda güvenliği yönetim sistemi ve HACCP temelli danışmanlık. Atlas Patent Konya.",
    "ISO 22000:2018, gıda zincirindeki işletmeler için gıda güvenliği şartlarını tanımlar. Temelinde HACCP vardır.",
    iso(
        "<p>Birincil üretimden sunuma, ambalaj ve katkı maddesine kadar zincirdeki işletmeler aynı çatı altında ele alınır. 2018 revizyonu, sistemi ISO 9001 ile yan yana kurmayı kolaylaştırır.</p>",
        ["Birincil ve ikincil gıda üreticileri", "Catering ve yemek sunan işletmeler", "Yem üreticileri", "Toptan ve perakende gıda satış noktaları", "Katkı, ambalaj, makine ve temizlik maddesi üreticileri"],
        ["Tehlike kontrolünü sistemli hale getirir.", "Mevzuata uyumu kolaylaştırır.", "İhracat ve yeni pazar kapısını destekler.", "Resmi denetimlere hazırlık sağlar.", "Gıda kaynaklı hastalık ve ekonomik kayıp riskini düşürür.", "Müşteri güvenini görünür kılar."],
    ),
    [("HACCP ile farkı nedir?", "HACCP tehlike analizi ve kritik kontrol planıdır. ISO 22000 bu planı bir yönetim sisteminin içine yerleştirir. İkisi birlikte yürür. Ayrıntı için HACCP sayfasına bakın.")],
)

add_service(
    "iso-14001", "Yönetim sistemleri", "ISO 14001",
    "Çevresel etkilerin yaşam döngüsü boyunca yönetilmesi.",
    "ISO 14001 Danışmanlığı | Atlas Patent",
    "ISO 14001:2015 çevre yönetim sistemi kurulumu ve belgelendirme hazırlığı. Atlas Patent Konya.",
    "ISO 14001, faaliyetin her adımında çevresel etkiyi görmeyi, atığı ve kaynak tüketimini azaltmayı sisteme bağlar.",
    iso(
        "<p>2015 revizyonu etkileri yaşam döngüsüyle ele alır ve ISO 9001 ile entegre kurulabilir. Çevre politikası, boyutlar, yükümlülükler ve acil durum hazırlığı dosyanın omurgasıdır.</p>",
        ["Üretim kuruluşları", "Hizmet kuruluşları", "Belediyeler ve organize sanayi bölgeleri", "Kooperatif, dernek ve vakıflar", "Çevresel etkisi olan özel ve kamu kuruluşları"],
        ["Yasal çevre yükümlülüklerine uyumu kolaylaştırır.", "Atık, enerji ve hammadde maliyetini görünür kılar.", "Çevresel kaza ihtimaline karşı hazırlık sağlar.", "Müşteriye çevre taahhüdünü göstermenizi sağlar.", "Her ölçekte uygulanabilir."],
    ),
    [],
)

add_service(
    "iso-45001", "Yönetim sistemleri", "ISO 45001",
    "İş kazası ve meslek hastalığını önleyen iş sağlığı ve güvenliği sistemi.",
    "ISO 45001 Danışmanlığı | Atlas Patent",
    "ISO 45001:2018 iş sağlığı ve güvenliği yönetim sistemi danışmanlığı. OHSAS 18001 yerine güncel standart. Atlas Patent.",
    "ISO 45001:2018, çalışanı merkeze alan uluslararası iş sağlığı ve güvenliği standardıdır. Eski OHSAS 18001'in yerini almıştır.",
    iso(
        "<p>Amaç sağlıklı bir işyeri, kazanın ve meslek hastalığının önlenmesi, çalışanların tehlikeyi bildirebilmesidir. ISO 9001 ve ISO 14001 ile aynı yapıda entegre edilebilir.</p>",
        ["Çalışanı olan işletmeler", "Üretim ve hizmet kuruluşları", "Alt yükleniciler", "Belediyeler ve organize sanayi bölgeleri", "Kooperatif, dernek, vakıf, özel ve kamu kuruluşları"],
        ["Kaza ve kayıp iş gününü azaltmaya yardım eder.", "Mevzuata uyumu düzene sokar.", "Çalışanın katılımını artırır.", "İhale ve müşteri denetimlerinde hazır olmanızı sağlar.", "Kurum itibarını korur."],
    ),
    [],
)

add_service(
    "iso-10002", "Yönetim sistemleri", "ISO 10002",
    "Şikayetin alınması, izlenmesi ve kapatılması için müşteri memnuniyeti sistemi.",
    "ISO 10002 Danışmanlığı | Atlas Patent",
    "ISO 10002 müşteri memnuniyeti ve şikayet yönetimi danışmanlığı. Atlas Patent Konya.",
    "ISO 10002, ürün ve hizmetle ilgili şikayetin nasıl alınacağını, izleneceğini ve kapatılacağını tarif eder.",
    iso(
        "<p>Her ölçekte, kamu, özel sektör ve gönüllü kuruluşlarda kullanılabilir. Şikayet süreci, kalite yönetim sisteminin bir parçası olarak da kurulur. Müşteriye önemsendiğini göstermek, şikayet nedenini tekrar etmemek ve çalışanı bu konuda eğitmek standardın pratik karşılığıdır.</p>",
        ["Üretim, servis ve teknik hizmet veren şirketler", "Kamu kurumları", "Vakıf, dernek ve STK'lar", "Esnaf ve e-ticaret işletmeleri"],
        ["Şikayet nedeni görünür olur, tekrar azalır.", "Yönetim kararını veriye dayandırır.", "Çalışanın farkındalığı artar.", "Marka itibarını korur."],
        "<p>Kurulumda şikayet kanalları, sorumlular, kayıt, analiz, iç tetkik ve yönetimin gözden geçirmesi birlikte yazılır.</p>",
    ),
    [],
)

add_service(
    "iso-50001", "Yönetim sistemleri", "ISO 50001",
    "Enerji tüketimini izleyen, hedef koyan ve tasarrufu kalıcı hale getiren sistem.",
    "ISO 50001 Danışmanlığı | Atlas Patent",
    "ISO 50001 enerji yönetim sistemi kurulumu. Enerji yoğun tesisler için Atlas Patent danışmanlığı, Konya.",
    "ISO 50001, enerji politikası, hedef ve performans takibini tek sistemde toplar.",
    iso(
        "<p>Enerji kullanan her ölçekte kuruluş uygulayabilir. Tek başına veya diğer yönetim sistemleriyle entegre yürür. Enerji yöneticisi bulundurmakla yükümlü binalar, üretim tesisleri ve organize sanayi bölgeleri için mevzuat ayrıca sistem kurmayı gündeme getirebilir. Yükümlülüğün sizin tesis için geçerli olup olmadığını başvuru öncesi birlikte kontrol ederiz. Eski metinlerde geçen 2023 tarihini güncel bir son gün olarak kullanmıyoruz.</p>",
        ["Kamu, ticari ve hizmet binaları", "Elektrik üretim tesisleri", "Organize sanayi bölgeleri", "Endüstriyel işletmeler", "Belirli enerji tüketimini aşan kuruluşlar"],
        ["Enerji kaybını ve faturayı izlenebilir kılar.", "Düşük maliyetli tasarruf fırsatlarını öne alır.", "Karbon ve sera gazı hesabına veri sağlar.", "Enerji fiyatı dalgalanmasından daha az etkilenmenize yardım eder.", "Çalışanda enerji farkındalığı oluşturur."],
    ),
    [],
)

add_service(
    "iso-27001", "Yönetim sistemleri", "ISO 27001",
    "Bilgi varlıklarının gizliliği, bütünlüğü ve erişilebilirliği için güvenlik sistemi.",
    "ISO 27001 Danışmanlığı | Atlas Patent",
    "ISO/IEC 27001 bilgi güvenliği yönetim sistemi danışmanlığı. Atlas Patent Konya.",
    "ISO/IEC 27001, finansal veriyi, fikri mülkiyeti ve müşteri bilgisini korumak için risk temelli bir çerçevedir.",
    iso(
        "<p>Sektör ve ülke fark etmeksizin uygulanır. Finans, sağlık, kamu, yazılım ve başkası adına veri tutan şirketlerde özellikle aranır. Bazı yetki ve ihale süreçlerinde belge şartı mevzuatla gelir. Şartın sizin faaliyetiniz için güncel olup olmadığını dosya açılırken kontrol ederiz.</p>",
        ["Yazılım, donanım ve entegratör firmalar", "İnternet ve elektronik haberleşme işletmecileri", "E-fatura özel entegratörlüğü hedefleyenler", "Kamu kurumları ve belediyeler", "Başkası adına bilgi işleyen kuruluşlar"],
        ["Riski görünür kılar ve gereksiz iş tekrarını azaltır.", "Bilginin doğruluğunu ve gizliliğini korur.", "Yasal güvenlik şartlarına hazırlık sağlar.", "Müşteriye verinin korunduğunu göstermenizi sağlar.", "İş sürekliliğine katkı verir."],
    ),
    [],
)

add_service(
    "helal-gida", "Belgelendirme ve uyum", "Helal belgelendirme",
    "OIC/SMIIC 1 helal gıda genel şartlarına göre sistem kurulumu ve belge denetimine hazırlık.",
    "Helal Belgelendirme Danışmanlığı | Atlas Patent",
    "Helal belgelendirme danışmanlığı: OIC/SMIIC 1, tedarik, üretim, etiket ve denetim hazırlığı. Atlas Patent Konya.",
    "Helal belgelendirme, gıda zincirinin alımdan servise kadar ilgili helal şartına göre denetlenmesidir. Belgeyi yetkili kuruluş verir.",
    """
<p>OIC/SMIIC 1, kuruluşun büyüklüğünden bağımsız olarak gıda zincirinin bir veya daha fazla aşamasında uygulanabilir. Belgelendirme, ayrı bir helal belgelendirme standardının denetimiyle tamamlanır. Atlas Patent sistemi kurar; belgeyi yetkili belgelendirme kuruluşu verir. Belgenin Helal Akreditasyon Kurumu tarafından akredite bir kuruluştan alınması ayrı bir dosyadır: <a href="hak-akrediteli.html">HAK akrediteli helal</a>.</p>
""" + h2("Kapsanan ürün grupları") + ul([
        "Et, süt, yumurta ve su ürünleri",
        "Tahıl, meyve, sebze ve mamulleri",
        "Bitkisel ve hayvansal yağlar",
        "Şekerleme, alkolsüz içecek, bal ve takviyeler",
        "Katkı maddeleri, enzimler ve mikroorganizmalar",
        "Ambalaj, gıda hizmeti ve tesisleri",
        "Su ve hayvansal kökenli gıdalar",
    ]) + """
<p>Tüketicinin dini hassasiyeti satın alma kararını etkiler. Sertifika ve logosu, ürünün bu şarta göre denetlendiğini göstermenin açık yoludur. İç pazarda ve ihracatta bu talep büyür.</p>
""",
    [],
)

add_service(
    "verbis-kvkk", "Belgelendirme ve uyum", "VERBİS ve KVKK",
    "6698 sayılı Kanun kapsamında veri sorumluları siciline hazırlık.",
    "VERBİS Kaydı ve KVKK Danışmanlığı | Atlas Patent",
    "VERBİS kayıt hazırlığı ve KVKK uyum danışmanlığı. Yükümlülük ölçütleri güncel Kurul kararına göre kontrol edilir. Atlas Patent Konya.",
    "VERBİS, veri sorumlularının sicil bilgi sistemidir. Her işletme otomatik olarak kayıtlı olmak zorunda değildir.",
    """
<p>6698 sayılı Kişisel Verilerin Korunması Kanunu, kişisel veriyi belirli veya belirlenebilir gerçek kişiye ilişkin bilgi olarak tanımlar. Sağlık verisi gibi özel nitelikli veriler daha sıkı şartlara tabidir.</p>
<p>Sicile kayıt yükümlülüğü, Kişisel Verileri Koruma Kurulu'nun belirlediği ölçütlere ve istisnalara bağlıdır. Çalışan sayısı, bilanço ve faaliyet konusuna göre muafiyet olabilir. Bu eşikler yıllar içinde değişti. Eski sitemizdeki pandemi ertelemesi ve 31 Aralık 2022 tarihi artık bir son gün değildir. Ceza tutarlarını da sabit rakam diye yazmıyoruz; idari para cezası kanunda ve güncel yeniden değerleme oranlarında yer alır.</p>
""" + h2("Birlikte baktığımız başlıklar") + ul([
        "Veri sorumlusu mu, veri işleyen mi olduğunuz",
        "Güncel kayıt yükümlülüğü ve istisna",
        "İşleme amaçları, veri kategorileri, alıcı grupları ve aktarım",
        "Saklama süreleri ve güvenlik tedbirlerinin sicil bildirimine yazılması",
        "İrtibat kişisi ve kayıt sonrası değişiklik bildirimi",
    ]) + """
<p>Kayıt, aydınlatma metninin ve iç süreçlerin yerine geçmez. Sicil bildirimi ile gerçek uygulamanın aynı olması gerekir.</p>
""",
    [("Herkes VERBİS'e kaydolmak zorunda mı?", "Hayır. Yükümlülük ve istisna güncel Kurul kararına göre belirlenir. Dosyayı açmadan önce sizin durumunuzu kontrol ederiz.")],
)

add_service(
    "yerli-mali-belgesi", "Belgelendirme ve uyum", "Yerli malı belgesi",
    "Kamu alımlarında yerli malı avantajı için dosya hazırlığı.",
    "Yerli Malı Belgesi | Atlas Patent Konya",
    "Yerli malı belgesi danışmanlığı: yerli katkı hesabı, evrak ve başvuru takibi. Atlas Patent Konya.",
    "Yerli malı belgesi, bir malın yerli katkı oranının ilgili tebliğdeki eşiği karşıladığını gösterir. Kamu alımlarında fiyat avantajı bu belgeye bağlanabilir.",
    """
<p>Belge, malın cinsine ve yürürlükteki yerli malı tebliğine göre düzenlenir. Başvuru genellikle ilgili oda veya borsa üzerinden yürür. İmalat süreci, girdi listesi ve yerli katkı hesabı dosyanın çekirdeğidir. Oran, sektöre göre değişir; sabit bir yüzdeyi her ürüne uygulamıyoruz.</p>
""" + h2("Dosyada neler olur?") + ul([
        "Ürünün ve üretim yerinin tarifi",
        "Girdi listesi ve yerli katkı hesabı",
        "Oda veya borsa başvurusu için evrak",
        "Eksik yazıların takibi",
    ]) + """
<p>Belge süresi ve kapsamı tebliğle belirlenir. Süresi dolan belge kendiliğinden uzamaz.</p>
""",
    [("Belgeyi siz mi düzenliyorsunuz?", "Hayır. Hesabı ve evrakı hazırlarız. Belgeyi yetkili oda, borsa veya ilgili kurum düzenler.")],
)

add_service(
    "ce-belgesi", "Belgelendirme ve uyum", "CE belgesi (AT uygunluk beyanı)",
    "Üreticinin kendi uygunluk beyanıyla CE işareti basabildiği ürünler için teknik dosya.",
    "CE Belgesi | AT Uygunluk Beyanı | Atlas Patent",
    "AT uygunluk beyanı ile CE işareti: teknik dosya, risk değerlendirmesi ve üretici beyanı. Atlas Patent Konya.",
    "AT uygunluk beyanı, mevzuatın izin verdiği ürünlerde üreticinin CE işaretini kendi beyanıyla kullanmasıdır. Bu bir kalite belgesi değildir.",
    """
<p>Hangi mevzuatın uygulanacağı ürüne göre değişir: makine, alçak gerilim, elektromanyetik uyumluluk gibi. Mevzuat üreticinin iç üretim kontrolüyle beyan vermesine izin veriyorsa dosya kurulur, üretici AB uygunluk beyanını imzalar ve işareti basar. Beyanı imzalayan üreticidir. Atlas Patent onaylanmış kuruluş değildir.</p>
<p>Onaylanmış kuruluşun zorunlu olduğu ürünler ayrı dosyadır: <a href="ce-akredite.html">CE belgesi (akredite)</a>. Çelik ve alüminyum yapı malzemesi için <a href="ce-en-1090.html">TS EN 1090-1</a> sayfasına bakın.</p>
""" + h2("Bu dosyada genellikle bulunanlar") + ul([
        "Ürün tarifi, çizim ve parça listesi",
        "Uygulanan mevzuat ve standartlar",
        "Risk değerlendirmesi",
        "Varsa test raporları",
        "Kullanım kılavuzu ve etiket",
        "AB uygunluk beyanı taslağı",
    ]) + """
<p>İşaret, dosya tamamlanmadan ve beyan imzalanmadan ürüne basılmaz.</p>
""",
    [("CE belgesini Atlas Patent mi veriyor?", "Hayır. Teknik dosyayı ve beyan taslağını hazırlarız. Beyanı üretici imzalar. Onaylanmış kuruluş gereken üründe incelemeyi o kuruluş yapar.")],
)

add_service(
    "ce-akredite", "Belgelendirme ve uyum", "CE belgesi (akredite)",
    "Onaylanmış kuruluş veya akredite laboratuvar incelemesi zorunlu ürünler için dosya.",
    "CE Belgesi (Akredite) | Atlas Patent",
    "Onaylanmış kuruluş ve akredite laboratuvar gerektiren CE süreci için teknik dosya danışmanlığı. Atlas Patent Konya.",
    "Bazı ürünlerde CE işareti, üreticinin tek başına beyanıyla tamamlanmaz. Mevzuat, onaylanmış kuruluşun incelemesini veya akredite bir laboratuvarın testini ister.",
    """
<p>Akredite yol, ürünün hangi direktif ve modüle girdiğine bağlıdır. Kişisel koruyucu donanım, bazı makineler ve yapı malzemeleri buna örnektir. Test raporunu ve inceleme sertifikasını yetkili kuruluş düzenler. Atlas Patent bu kuruluş değildir; dosyayı kurar, doğru kuruluşun seçilmesine yardım eder ve yazışmayı takip eder.</p>
<p>Mevzuat kendi beyanınıza izin veriyorsa <a href="ce-belgesi.html">AT uygunluk beyanı</a> sayfası yeterlidir. İkisini karıştırmak, gümrükte ve piyasada dosyayı düşürür.</p>
""" + h2("Birlikte yürüttüğümüz işler") + ul([
        "Ürünün hangi modüle girdiğinin ayrılması",
        "Teknik dosya ve risk değerlendirmesi",
        "Numune ve test planının hazırlanması",
        "Onaylanmış kuruluş veya akredite laboratuvar seçimi",
        "Bulgu kapatma ve beyanın tamamlanması",
    ]),
    [("Akredite CE belgesini siz mi düzenliyorsunuz?", "Hayır. İncelemeyi ve sertifikayı onaylanmış kuruluş veya akredite laboratuvar verir. Biz dosyayı ve süreci yürütürüz.")],
)

add_service(
    "ce-en-1090", "Belgelendirme ve uyum", "TS EN 1090-1 CE belgesi",
    "Çelik ve alüminyum yapı malzemesinde fabrika üretim kontrolü ve CE dosyası.",
    "TS EN 1090-1 CE Belgesi | Atlas Patent",
    "TS EN 1090-1 kapsamında çelik ve alüminyum yapı bileşenleri için CE ve fabrika üretim kontrolü danışmanlığı. Atlas Patent Konya.",
    "TS EN 1090-1, çelik ve alüminyum yapı bileşenlerinin CE işareti için fabrika üretim kontrolünü tarif eden standarttır.",
    """
<p>Yapı malzemesi pazara çıkacaksa ilgili yapı malzemeleri mevzuatı ve bu standart birlikte okunur. İmalatın hangi uygulama sınıfına gireceği projeye ve bileşene göre belirlenir; her atölyeye aynı sınıf yazılmaz. Fabrika üretim kontrolünün belgelendirilmesini onaylanmış kuruluş yapar. Atlas Patent onaylanmış kuruluş değildir.</p>
""" + h2("Dosyada baktığımız başlıklar") + ul([
        "Ürün ailesi ve uygulama sınıfının ayrılması",
        "Kaynak, kesim ve izlenebilirlik kayıtları",
        "Fabrika üretim kontrolü dokümanı",
        "Personel yetkinliği ve kaynak prosedürleri",
        "Onaylanmış kuruluş denetimine hazırlık",
    ]) + """
<p>Genel makine CE dosyası bu standardın yerine geçmez. Diğer CE yolları için <a href="ce-belgesi.html">AT uygunluk beyanı</a> ve <a href="ce-akredite.html">akredite CE</a> sayfalarına bakın.</p>
""",
    [("EN 1090 belgesini Atlas Patent mi veriyor?", "Hayır. Fabrika üretim kontrolünü belgeleyen onaylanmış kuruluştur. Biz dokümanı kurar ve denetimde yanınızda dururuz.")],
)

add_service(
    "brcgs", "Belgelendirme ve uyum", "BRCGS danışmanlığı",
    "Gıda, ambalaj ve depolamada BRCGS standartlarına göre sistem kurulumu.",
    "BRCGS Danışmanlığı | Atlas Patent",
    "BRCGS gıda güvenliği danışmanlığı. Piyasada BRGS veya BRC diye de aranır. Atlas Patent Konya.",
    "BRCGS, gıda güvenliği, ambalaj ve depolama için perakende zincirlerinin aradığı standart ailesidir. Piyasada BRGS veya BRC diye de geçer.",
    """
<p>Market, ihracat veya özel marka tedarikinde alıcı çoğu zaman bu standarda göre bir belge ister. Belgeyi, BRCGS tarafından tanınan belgelendirme kuruluşu düzenler. Atlas Patent bu kuruluş değildir. Sistemi, ön gereksinimleri ve kayıt düzenini kurar; denetim bulgularının kapatılmasına eşlik eder.</p>
""" + h2("Hangi başlıklara bakılır?") + ul([
        "Üst yönetim taahhüdü ve gıda güvenliği kültürü",
        "Tehlike analizi ve kritik kontrol planı",
        "Tesis, hijyen, alerjen ve izlenebilirlik",
        "Tedarikçi onayı ve spesifikasyon",
        "İç denetim ve düzeltici faaliyet",
    ]) + """
<p>Yalnızca HACCP klasörü ile BRCGS denetimi aynı iş değildir. Hangisinin istendiğini ilk görüşmede ayırırız. HACCP dosyası için <a href="haccp.html">HACCP</a> sayfasına bakın.</p>
""",
    [("BRCGS belgesini siz mi veriyorsunuz?", "Hayır. Belgeyi BRCGS tarafından tanınan belgelendirme kuruluşu verir. Biz sistemi kurar ve denetime hazırlarız.")],
)

add_service(
    "hak-akrediteli", "Belgelendirme ve uyum", "HAK akrediteli helal",
    "Helal Akreditasyon Kurumu tarafından akredite edilmiş kuruluştan belge alınması için hazırlık.",
    "HAK Akrediteli Helal Belgesi | Atlas Patent",
    "HAK akrediteli helal belgelendirme danışmanlığı. Belgeyi akredite kuruluş verir. Atlas Patent Konya.",
    "HAK akrediteli helal belgesi, Helal Akreditasyon Kurumu tarafından akredite edilmiş bir belgelendirme kuruluşunun denetimiyle verilir.",
    """
<p>Helal Akreditasyon Kurumu belgeyi kendisi basmaz; belgelendirme kuruluşlarını akredite eder. Atlas Patent ne bu kurumdur ne de akredite bir belgelendirme kuruluşudur. İstenen kapsam için sistemi, tedarik şartını, üretim kaydını ve etiketi hazırlarız. Denetimi akredite kuruluş yapar.</p>
<p>Genel helal gıda sistemi için <a href="helal-gida.html">helal belgelendirme</a> sayfasına bakın. Alıcınız özellikle HAK akrediteli bir belge istiyorsa bu dosya açılır.</p>
""" + ul([
        "Kapsamın ve ürün grubunun yazılması",
        "Helal kritik noktalar ve tedarikçi şartı",
        "Üretim, depolama ve etiket kayıtları",
        "Akredite belgelendirme kuruluşunun seçilmesi",
        "Denetim bulgularının kapatılması",
    ]),
    [("HAK belgesini Atlas Patent mi düzenliyor?", "Hayır. Belgeyi, Helal Akreditasyon Kurumu tarafından akredite edilmiş belgelendirme kuruluşu düzenler.")],
)

add_service(
    "haccp", "Belgelendirme ve uyum", "HACCP dosyası",
    "Tehlike analizi, kritik kontrol noktaları ve ön gereksinim programları.",
    "HACCP Dosyası | Atlas Patent",
    "HACCP planı ve ön gereksinim programları danışmanlığı. Gıda işletmeleri için Atlas Patent Konya.",
    "HACCP, gıda güvenliğinde tehlikeyi önceden görüp kritik noktada kontrol etmeye dayanan bir plandır.",
    """
<p>Codex esaslı yedi ilke etrafında kurulur: tehlike analizi, kritik kontrol noktaları, kritik limitler, izleme, düzeltici faaliyet, doğrulama ve kayıt. Plan tek başına yetmez. Hijyen, haşere, izlenebilirlik ve eğitim gibi ön gereksinim programları tesisinize göre yazılır.</p>
<p>ISO 22000 bu planı yönetim sistemine bağlar. Yalnızca HACCP dosyası isteyen bir denetim ile belge denetimi aynı iş değildir. Market ve ihracat alıcısı BRCGS istiyorsa <a href="brcgs.html">BRCGS danışmanlığı</a> ayrı bir dosyadır. İhtiyacınızı ilk görüşmede ayırırız.</p>
""" + h2("Dosyada birlikte yazdığımız parçalar") + ul([
        "Ürün tarifi ve amaçlanan kullanım",
        "Akış şeması ve yerinde doğrulama",
        "Tehlike analizi",
        "Kritik limit, izleme ve düzeltici faaliyet",
        "Doğrulama ve kayıt düzeni",
    ]),
    [],
)

add_service(
    "tse-urun-belgesi", "Belgelendirme ve uyum", "TSE ürün belgelendirme",
    "Türk standardına göre ürün belgelendirme başvurusuna hazırlık.",
    "TSE Ürün Belgelendirme | Atlas Patent",
    "TSE ürün belgelendirme danışmanlığı: standart seçimi, numune, doküman ve denetim hazırlığı. Atlas Patent Konya.",
    "TSE ürün belgesi, ürünün ilgili Türk standardına uygun bulunduğunu belgelendirme kuruluşunun denetimiyle gösterir.",
    """
<p>CE işareti Avrupa mevzuatına uygunluk beyanıdır. TSE ürün belgesi ise Türk standardı kapsamında bir ürün belgelendirmesidir. Birinin olması diğerinin yerine geçmez. İhale, market veya ihracat şartnamesi hangisini istiyorsa o dosya açılır.</p>
<p>Atlas Patent belgeyi düzenlemez. Standardın seçilmesi, üretim kayıtlarının ve numunenin hazırlanması, başvurunun ve denetim bulgularının takip edilmesi bizim tarafımızdadır.</p>
""" + ul([
        "İlgili standardın belirlenmesi",
        "Ürün ve üretim yeri bilgisi",
        "Kalite kayıtları ve varsa test geçmişi",
        "Numune ve denetim planı",
        "Uygunsuzlukların kapatılması",
    ]),
    [("TSE belgesi CE yerine geçer mi?", "Geçmez. İkisi farklı mevzuata bakar. Bazı ürünlerde ikisi de istenir.")],
)

ARTICLES = [
    {
        "slug": "konya-marka-tescil",
        "title": "Konya'da marka tescili neden ertelenmemeli?",
        "description": "Konya'daki üretici ve esnaf için marka araştırması, sınıf seçimi ve başvuru zamanı. Atlas Patent.",
        "html": """
<p>Konya sanayi, gıda ve ticaretle büyürken aynı isimle açılan ikinci tabela sık görülür. Marka araştırması yapılmadan tabela, tabela ve ambalaj bastırmak, sonra aynı ismi başkasının tescil ettirdiğini öğrenmek pahalı bir sıradır.</p>
<p>Atlas Patent Selçuklu'dadır ve on yıllık tecrübeyle Türkiye geneline dosya yürütür. Konya'da olmanın faydası, üretim yerini ve malın gerçekten ne olduğunu yerinde konuşabilmektir. Sınıf listesi broşürden değil, tezgahınızdan çıkar.</p>
<h2>Pratik sıra</h2>
<ul>
<li>İsim ve logoyu kullanmaya başlamadan araştırın.</li>
<li>Sadece kendi ilinizi değil, Türkiye sicilini tarayın. Tescil ülkeseldir.</li>
<li>Başvurudan sonra bülten iki ay açık kalır. Bu süreyi izleyin.</li>
<li>İhracat varsa yurt dışı takvimini başvuru günü yazın.</li>
</ul>
<p>Ayrıntılı süreç <a href="marka-tescil.html">marka tescil</a> sayfasında. Ofis için <a href="iletisim.html">iletişim</a>.</p>
""",
    },
    {
        "slug": "haccp-dosyasi-nedir",
        "title": "HACCP dosyasında olması gerekenler",
        "description": "Gıda işletmesi için HACCP planı, ön gereksinim programları ve ISO 22000 ilişkisi.",
        "html": """
<p>HACCP dosyası bir klasör dolusu genel hijyen fotokopisi değildir. Ürününüzün akışına göre tehlike analizi, kritik kontrol noktası, limit, izleme ve kayıt içerir.</p>
<p>Ön gereksinimler (temizlik, haşere, su, eğitim, izlenebilirlik) planın altına yazılır. Bunlar yoksa kritik kontrol noktası kağıt üzerinde kalır. ISO 22000 bu yapıyı yönetim sistemine bağlar. Yalnızca dosya mı, belge denetimi mi istediğinizi <a href="haccp.html">HACCP</a> sayfasında ayırıyoruz.</p>
""",
    },
    {
        "slug": "ce-teknik-dosya",
        "title": "CE teknik dosyasında neler bulunur?",
        "description": "CE işareti için teknik dosya, uygunluk beyanı ve onaylanmış kuruluş ayrımı.",
        "html": """
<p>CE işareti, ürünün ilgili Avrupa mevzuatına uyduğunun beyanıdır. Kalite ödülü değildir. Dosyada ürün tarifi, risk değerlendirmesi, uygulanan standart, test, kılavuz ve uygunluk beyanı aranır.</p>
<p>Her üründe bir onaylanmış kuruluş şart değildir. Şart olan üründe kuruluşu siz seçersiniz, dosyayı birlikte kurarız. Atlas Patent onaylanmış kuruluş değildir. Adımlar <a href="ce-belgesi.html">CE sayfasında</a>.</p>
""",
    },
    {
        "slug": "yerli-mali-belgesi-kimler-icin",
        "title": "Yerli malı belgesi kimler için anlamlı?",
        "description": "Kamu alımında yerli malı avantajı, katkı hesabı ve belgenin süresi.",
        "html": """
<p>Kamu ihalesine giren ve malı Türkiye'de üreten firmalar için yerli malı belgesi fiyat avantajı doğurabilir. Avantaj, belgenin kapsamındaki mal ile sınırlıdır. Her ürün aynı yüzdeyle yerli sayılmaz. Hesap, yürürlükteki tebliğe ve girdi listesine göre yapılır.</p>
<p>Belgeyi oda veya ilgili kurum düzenler. Biz hesabı ve evrakı hazırlarız. Süre dolunca belge kendiliğinden uzamaz. Süreç <a href="yerli-mali-belgesi.html">yerli malı belgesi</a> sayfasında.</p>
""",
    },
    {
        "slug": "tse-ve-ce-farki",
        "title": "TSE ürün belgesi ile CE işareti aynı şey değil",
        "description": "TSE ürün belgesi Türk standardına, CE Avrupa mevzuatına bakar. İkisi birbirinin yerine geçmez.",
        "html": """
<p>Şartnamede TSE yazıyorsa CE dosyası yetmeyebilir. CE yazıyorsa TSE belgesi Avrupa uygunluğunun yerine geçmez. Bazı ürünlerde ikisi de istenir.</p>
<p>TSE ürün belgesi, ilgili Türk standardına göre belgelendirme denetimidir. CE, üreticinin uygunluk beyanıdır ve bazı ürünlerde onaylanmış kuruluş devreye girer. Hangi kapıya başvuracağınızı <a href="tse-urun-belgesi.html">TSE</a> ve <a href="ce-belgesi.html">CE</a> sayfalarında ayırdık.</p>
""",
    },
]

FAQ = [
    ("Marka tescili ne kadar sürer?", "İtiraz yoksa çoğu dosya birkaç ay ile bir yıl arasında biter. İki aylık bülten süresi bu takvimin parçasıdır."),
    ("Tescil kaç yıl korur?", "Marka on yıl, yenilenebilir. Patent yirmi yıla kadar. Faydalı model on yıl. Tasarım beş yıl, yenilemelerle yirmi beş yıla kadar."),
    ("Patent ile faydalı model aynı mı?", "Değil. Patentte buluş basamağı da aranır. Faydalı model daha çok üründeki teknik geliştirmeye ve on yıllık korumaya uygundur."),
    ("Tasarım tescili neyi korur?", "Ürünün görünümünü. Teknik fonksiyonu değil."),
    ("ISO belgesini siz mi veriyorsunuz?", "Hayır. Sistemi kurarız. Belgeyi akredite belgelendirme kuruluşu verir."),
    ("CE belgesi ile TSE aynı mı?", "Hayır. CE Avrupa mevzuatına uygunluk beyanıdır. TSE ürün belgesi Türk standardına göre belgelendirmedir."),
    ("Herkes VERBİS'e kaydolur mu?", "Hayır. Yükümlülük ve istisna güncel Kurul kararına bağlıdır."),
    ("Yerli malı belgesini kim düzenler?", "İlgili oda, borsa veya yetkili kurum. Biz katkı hesabını ve evrakı hazırlarız."),
    ("Konya dışına da bakıyor musunuz?", "Evet. Ofis Selçuklu'dadır, dosyalar Türkiye geneline ve yurt dışı başvuru rotalarına gider."),
    ("Ön görüşme ücretli mi?", "İlk görüşmede neye ihtiyacınız olduğunu ayırırız. Ücret, işin kapsamı netleşince yazılır. Sitede sabit fiyat yayınlamıyoruz çünkü sınıf sayısı ve ülke seçimi dosyayı değiştirir."),
]


BRIEFS = {
    "marka-tescil": (
        "Marka tescil belgesi",
        "Marka Tescil Belgesi",
        "Marka tescil belgesi: isim, logo ve ayırt edici işaretin sicile yazılması.",
        "Marka Tescil Belgesi | Marka Danışmanlığı Konya",
        "Marka tescil belgesi için araştırma, sınıf seçimi, başvuru ve bülten takibi. Konya Atlas Patent marka danışmanlığı.",
    ),
    "patent-tescil": (
        "Patent belgesi",
        "Patent Belgesi",
        "Patent belgesi: buluşun tarifnamesi, istemi ve ulusal başvuru takibi.",
        "Patent Belgesi | Patent Başvurusu Danışmanlığı Konya",
        "Patent belgesi için buluş değerlendirmesi, tarifname ve başvuru takibi. Konya Atlas Patent patent danışmanlığı.",
    ),
    "tasarim-tescil": (
        "Endüstriyel tasarım tescili",
        "Endüstriyel Tasarım Tescili",
        "Endüstriyel tasarım tescili: ürünün görünümünü koruyan tasarım belgesi.",
        "Endüstriyel Tasarım Tescili | Tasarım Belgesi Konya",
        "Endüstriyel tasarım tescili ve tasarım belgesi danışmanlığı. Görünüm, başvuru ve yenileme. Konya Atlas Patent.",
    ),
    "faydali-model": (
        "Faydalı model belgesi",
        "Faydalı Model Belgesi",
        "Faydalı model belgesi: üründeki teknik geliştirme için on yıla kadar koruma.",
        "Faydalı Model Belgesi | Faydalı Model Tescili Konya",
        "Faydalı model belgesi danışmanlığı. Yenilik, sanayiye uygulanabilirlik ve başvuru takibi. Konya Atlas Patent.",
    ),
    "cografi-isaret": (
        "Coğrafi işaret tescili",
        "Coğrafi İşaret Tescili",
        "Coğrafi işaret tescili: menşe veya mahreç adı için yöresel ürün belgesi.",
        "Coğrafi İşaret Tescili | Menşe ve Mahreç Belgesi",
        "Coğrafi işaret tescili: menşe ve mahreç belgesi, denetim şartı ve başvuru. Konya Atlas Patent.",
    ),
    "yurtdisi-tescil": (
        "Yurt dışı marka ve patent",
        "Yurt Dışı Marka ve Patent",
        "Yurt dışı marka tescili ve patent: Madrid sistemi, PCT ve ülke başvurusu.",
        "Yurt Dışı Marka Tescili ve Patent | Madrid, PCT",
        "Yurt dışı marka tescili ve patent başvurusu. Madrid sistemi, PCT ve ülke seçimi. Konya Atlas Patent.",
    ),
    "barkod": (
        "Barkod numarası",
        "Barkod Numarası",
        "Barkod numarası: GS1 firma öneki ve ürün barkodu danışmanlığı.",
        "Barkod Numarası | GS1 Barkod Danışmanlığı Konya",
        "Barkod numarası ve GS1 ürün barkodu danışmanlığı. Market ve pazaryeri için firma öneki. Konya Atlas Patent.",
    ),
    "iso-9001": (
        "Kalite yönetim sistemi belgesi",
        "ISO 9001 Kalite Yönetim Sistemi",
        "ISO 9001 belgesi: kalite yönetim sistemi kurulumu ve denetim hazırlığı.",
        "ISO 9001 Belgesi | Kalite Yönetim Sistemi Danışmanlığı Konya",
        "ISO 9001 belgesi ve kalite yönetim sistemi danışmanlığı. Dokümantasyon, uygulama ve belgelendirme denetimine hazırlık. Konya Atlas Patent.",
    ),
    "iso-22000": (
        "Gıda güvenliği belgesi",
        "ISO 22000 Gıda Güvenliği Yönetim Sistemi",
        "ISO 22000 belgesi: gıda güvenliği yönetim sistemi ve HACCP temelli hazırlık.",
        "ISO 22000 Belgesi | Gıda Güvenliği Yönetim Sistemi Konya",
        "ISO 22000 belgesi ve gıda güvenliği yönetim sistemi danışmanlığı. HACCP temelli dokümantasyon ve denetim hazırlığı. Konya Atlas Patent.",
    ),
    "iso-14001": (
        "Çevre yönetim sistemi belgesi",
        "ISO 14001 Çevre Yönetim Sistemi",
        "ISO 14001 belgesi: çevre yönetim sistemi kurulumu ve denetim hazırlığı.",
        "ISO 14001 Belgesi | Çevre Yönetim Sistemi Danışmanlığı Konya",
        "ISO 14001 belgesi ve çevre yönetim sistemi danışmanlığı. Çevresel etki, atık ve mevzuat uyumu için denetim hazırlığı. Konya Atlas Patent.",
    ),
    "iso-45001": (
        "İş sağlığı ve güvenliği belgesi",
        "ISO 45001 İş Sağlığı ve Güvenliği",
        "ISO 45001 belgesi: iş sağlığı ve güvenliği yönetim sistemi. OHSAS 18001 yerine geçer.",
        "ISO 45001 Belgesi | İş Sağlığı ve Güvenliği Danışmanlığı Konya",
        "ISO 45001 belgesi ve iş sağlığı güvenliği yönetim sistemi danışmanlığı. OHSAS 18001 yerine güncel standart. Konya Atlas Patent.",
    ),
    "iso-10002": (
        "Müşteri memnuniyeti belgesi",
        "ISO 10002 Müşteri Memnuniyeti",
        "ISO 10002 belgesi: müşteri şikayetlerinin alınması, izlenmesi ve kapatılması.",
        "ISO 10002 Belgesi | Müşteri Memnuniyeti ve Şikayet Yönetimi",
        "ISO 10002 belgesi ve müşteri memnuniyeti danışmanlığı. Şikayet yönetimi sistemi kurulumu ve denetim hazırlığı. Konya Atlas Patent.",
    ),
    "iso-50001": (
        "Enerji yönetim sistemi belgesi",
        "ISO 50001 Enerji Yönetim Sistemi",
        "ISO 50001 belgesi: enerji tüketimini izleyen ve tasarrufu kalıcı kılan sistem.",
        "ISO 50001 Belgesi | Enerji Yönetim Sistemi Danışmanlığı Konya",
        "ISO 50001 belgesi ve enerji yönetim sistemi danışmanlığı. Enerji hedefi, izleme ve denetim hazırlığı. Konya Atlas Patent.",
    ),
    "iso-27001": (
        "Bilgi güvenliği belgesi",
        "ISO 27001 Bilgi Güvenliği",
        "ISO 27001 belgesi: bilgi güvenliği yönetim sistemi ve veri koruma hazırlığı.",
        "ISO 27001 Belgesi | Bilgi Güvenliği Yönetim Sistemi Konya",
        "ISO 27001 belgesi ve bilgi güvenliği yönetim sistemi danışmanlığı. Veri gizliliği, risk ve denetim hazırlığı. Konya Atlas Patent.",
    ),
    "helal-gida": (
        "Helal belgesi",
        "Helal Belgesi",
        "Helal belgesi: OIC/SMIIC 1 helal gıda şartına göre sistem ve denetim hazırlığı.",
        "Helal Belgesi | Helal Belgelendirme Danışmanlığı Konya",
        "Helal belgesi danışmanlığı. OIC/SMIIC 1, tedarik, üretim, etiket ve denetim hazırlığı. Belgeyi yetkili kuruluş verir. Konya Atlas Patent.",
    ),
    "verbis-kvkk": (
        "VERBİS kaydı",
        "VERBİS Kaydı ve KVKK",
        "VERBİS kaydı: 6698 sayılı KVKK kapsamında veri sorumluları siciline hazırlık.",
        "VERBİS Kaydı | KVKK Sicil Danışmanlığı Konya",
        "VERBİS kaydı ve KVKK danışmanlığı. Sicil yükümlülüğü güncel Kurul kararına göre kontrol edilir. Konya Atlas Patent.",
    ),
    "yerli-mali-belgesi": (
        "Kamu alımında yerli katkı belgesi",
        "Yerli Malı Belgesi",
        "Yerli malı belgesi: kamu alımlarında yerli katkı hesabı ve evrak hazırlığı.",
        "Yerli Malı Belgesi | Yerli Katkı Hesabı Danışmanlığı Konya",
        "Yerli malı belgesi danışmanlığı. Yerli katkı oranı, evrak ve oda başvurusu takibi. Belgeyi yetkili kurum düzenler. Konya Atlas Patent.",
    ),
    "ce-belgesi": (
        "CE belgesi, uygunluk beyanı",
        "CE Belgesi ve AT Uygunluk Beyanı",
        "CE belgesi: üreticinin AT uygunluk beyanıyla CE işareti için teknik dosya.",
        "CE Belgesi | AT Uygunluk Beyanı Danışmanlığı Konya",
        "CE belgesi ve AT uygunluk beyanı danışmanlığı. Teknik dosya, risk değerlendirmesi ve üretici beyanı. Konya Atlas Patent.",
    ),
    "ce-akredite": (
        "CE belgesi, onaylanmış kuruluş",
        "Akredite CE Belgesi",
        "Akredite CE belgesi: onaylanmış kuruluş veya akredite laboratuvar incelemesi.",
        "Akredite CE Belgesi | Onaylanmış Kuruluş Dosyası Konya",
        "Akredite CE belgesi danışmanlığı. Onaylanmış kuruluş ve akredite laboratuvar gerektiren ürünler için teknik dosya. Konya Atlas Patent.",
    ),
    "ce-en-1090": (
        "Çelik yapı CE belgesi",
        "TS EN 1090-1 CE Belgesi",
        "TS EN 1090-1 CE belgesi: çelik ve alüminyum yapıda fabrika üretim kontrolü.",
        "TS EN 1090-1 CE Belgesi | Çelik Yapı Danışmanlığı Konya",
        "TS EN 1090-1 CE belgesi danışmanlığı. Çelik ve alüminyum yapı bileşenlerinde fabrika üretim kontrolü hazırlığı. Konya Atlas Patent.",
    ),
    "brcgs": (
        "BRCGS gıda güvenliği belgesi",
        "BRCGS Gıda Güvenliği Belgesi",
        "BRCGS belgesi: gıda, ambalaj ve depolama. Piyasada BRC veya BRGS diye de aranır.",
        "BRCGS Belgesi | BRC ve BRGS Gıda Güvenliği Danışmanlığı",
        "BRCGS belgesi danışmanlığı. BRC ve BRGS diye de aranan gıda güvenliği standardı için sistem kurulumu ve denetim hazırlığı. Konya Atlas Patent.",
    ),
    "hak-akrediteli": (
        "HAK akrediteli helal belgesi",
        "HAK Akrediteli Helal Belgesi",
        "HAK akrediteli helal belgesi: Helal Akreditasyon Kurumu kapsamındaki denetim hazırlığı.",
        "HAK Akrediteli Helal Belgesi | Helal Danışmanlığı Konya",
        "HAK akrediteli helal belgesi danışmanlığı. Belgeyi akredite belgelendirme kuruluşu verir. Sistem ve denetim hazırlığı. Konya Atlas Patent.",
    ),
    "haccp": (
        "HACCP belgesi",
        "HACCP Belgesi ve Dosyası",
        "HACCP belgesi: tehlike analizi, kritik kontrol noktaları ve ön gereksinim programları.",
        "HACCP Belgesi | HACCP Dosyası Danışmanlığı Konya",
        "HACCP belgesi ve HACCP dosyası danışmanlığı. Tehlike analizi, kritik kontrol noktası ve hijyen ön koşulları. Konya Atlas Patent.",
    ),
    "tse-urun-belgesi": (
        "TSE ürün belgesi",
        "TSE Ürün Belgesi",
        "TSE ürün belgesi: Türk standardına göre ürün belgelendirme hazırlığı.",
        "TSE Ürün Belgesi | TSE Ürün Belgelendirme Danışmanlığı Konya",
        "TSE ürün belgesi danışmanlığı. Standart seçimi, numune, doküman ve denetim hazırlığı. Belgeyi TSE düzenler. Konya Atlas Patent.",
    ),
}


def apply_briefs():
    for s in SERVICES:
        row = BRIEFS.get(s["slug"])
        if not row:
            continue
        s["hint"], s["heading"], s["card"], s["seo_title"], s["description"] = row


apply_briefs()


def link_html(s):
    hint = f"<small>{e(s['hint'])}</small>" if s.get("hint") else ""
    return f'<a href="{s["slug"]}.html">{e(s["name"])}{hint}</a>'


def card_html(s, show_group=True):
    group = f"<small>{e(s['group'])}</small>" if show_group else ""
    hint = f"<em>{e(s['hint'])}</em>" if s.get("hint") else ""
    return (
        f'<a class="card" href="{s["slug"]}.html">{group}'
        f"<strong>{e(s['name'])}</strong>{hint}<span>{e(s['card'])}</span></a>"
    )


def service_schema(s):
    data = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": s.get("heading") or s["name"],
        "serviceType": s.get("hint") or s["name"],
        "description": s["description"],
        "url": BASE + s["slug"] + ".html",
        "areaServed": {"@type": "Country", "name": "Türkiye"},
        "provider": {"@type": "ProfessionalService", "name": "Atlas Patent", "url": BASE},
    }
    return json.dumps(data, ensure_ascii=False)


def service_by(slug):
    for s in SERVICES:
        if s["slug"] == slug:
            return s
    raise KeyError(slug)


def groups():
    order = []
    for s in SERVICES:
        if s["group"] not in order:
            order.append(s["group"])
    return order


def menu(active):
    blocks = []
    for group in groups():
        links = []
        for s in SERVICES:
            if s["group"] == group:
                links.append(link_html(s))
        blocks.append(f"<div><h3>{e(group)}</h3>{''.join(links)}</div>")
    current = ' aria-current="page"' if active == "hizmetler" else ""
    return f'''
    <div class="drop">
      <button class="nav-btn" type="button" aria-expanded="false" aria-haspopup="true"{current}>Hizmetler</button>
      <div class="drop-panel">{''.join(blocks)}</div>
    </div>'''


def header(active):
    def link(href, key, label):
        cur = ' aria-current="page"' if active == key else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    rehber = ' aria-current="page"' if active == "rehber" else ""
    return f'''
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html"><img src="assets/logo.png" alt="Atlas Patent" width="400" height="134"></a>
    <form class="site-search" role="search">
      <label class="sr" for="site-q">Sitede ara</label>
      <input id="site-q" type="search" placeholder="Marka, ISO, CE…" autocomplete="off" enterkeyhint="search">
      <div class="search-panel" hidden></div>
    </form>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="ana-menu" aria-label="Menüyü aç">
      <span></span><span></span><span></span>
    </button>
    <nav class="nav" id="ana-menu" aria-label="Ana menü">
      {link("index.html", "home", "Ana sayfa")}
      {link("hakkimizda.html", "hakkimizda", "Hakkımızda")}
      {menu(active)}
      {link("referanslar.html", "referanslar", "Referanslar")}
      <div class="drop">
        <button class="nav-btn" type="button" aria-expanded="false" aria-haspopup="true"{rehber}>Rehber</button>
        <div class="drop-panel is-single">
          <div>
            <h3>Bilgi</h3>
            <a href="haberler.html">Yazılar</a>
            <a href="sss.html">Sık sorulan sorular</a>
            <a href="konya-marka-patent.html">Konya ofisi</a>
          </div>
        </div>
      </div>
      {link("iletisim.html", "iletisim", "İletişim")}
      <a class="nav-cta" href="iletisim.html">Ön görüşme</a>
    </nav>
    <a class="header-cta" href="iletisim.html">Ön görüşme</a>
  </div>
</header>'''


def footer():
    cols = []
    for group in groups():
        links = "".join(f'<a href="{s["slug"]}.html">{e(s["name"])}</a>' for s in SERVICES if s["group"] == group)
        cols.append(f"<div><h2>{e(group)}</h2>{links}</div>")
    return f'''
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <a class="brand" href="index.html"><img src="assets/logo.png" alt="Atlas Patent" width="400" height="134"></a>
      <p>Selçuklu'dan Türkiye geneline marka, patent, tasarım ve yönetim sistemleri danışmanlığı. Belgeyi yetkili kuruluş verir; biz dosyayı kurar ve takip ederiz.</p>
      <p>{ADDRESS}<br><a href="{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{WA}">WhatsApp</a></p>
    </div>
    {''.join(cols)}
    <div>
      <h2>Kurumsal</h2>
      <a href="hakkimizda.html">Hakkımızda</a>
      <a href="hizmetler.html">Hizmetler</a>
      <a href="referanslar.html">Referanslar</a>
      <a href="haberler.html">Yazılar</a>
      <a href="sss.html">Sık sorulan sorular</a>
      <a href="konya-marka-patent.html">Konya ofisi</a>
      <a href="iletisim.html">İletişim</a>
      <a href="gizlilik.html">Kişisel veriler</a>
    </div>
  </div>
  <div class="wrap foot-map">
    <div class="map-frame">
      <iframe title="Atlas Patent ofisi, Binkonutlar Mahallesi Udi Sokak, Selçuklu Konya" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="{MAP}&amp;output=embed"></iframe>
      <p class="map-label">Atlas Patent</p>
    </div>
    <p><span>{ADDRESS}</span> <a href="{MAP}">Yol tarifi</a></p>
  </div>
  <div class="wrap legal">
    <p>{e(DISCLAIMER)}</p>
    <p>© Atlas Patent. Selçuklu / Konya.</p>
  </div>
</footer>'''


def org_schema():
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Atlas Patent",
        "url": BASE,
        "telephone": "+905556224422",
        "email": EMAIL,
        "image": BASE + "assets/logo.png",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Binkonutlar Mh. Udi Sk. No:4/D D:1",
            "addressLocality": "Selçuklu",
            "addressRegion": "Konya",
            "postalAddressCountry": "TR",
            "addressCountry": "TR",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 37.946813, "longitude": 32.510319},
        "hasMap": MAP,
        "areaServed": "TR",
        "description": "Marka, patent, tasarım, faydalı model ve yönetim sistemleri danışmanlığı. Selçuklu, Konya.",
    }
    return json.dumps(data, ensure_ascii=False)


def faq_schema(pairs):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }
    return json.dumps(data, ensure_ascii=False)


def crumbs_html(items):
    parts = ['<a href="index.html">Ana sayfa</a>']
    for href, label in items[:-1]:
        parts.append(f'<a href="{href}">{e(label)}</a>')
    parts.append(f'<span aria-current="page">{e(items[-1][1])}</span>')
    return '<nav class="crumbs" aria-label="Sayfa yolu">' + " / ".join(parts) + "</nav>"


def crumb_schema(items):
    elements = [{"@type": "ListItem", "position": 1, "name": "Ana sayfa", "item": BASE}]
    for i, (href, label) in enumerate(items, start=2):
        elements.append({"@type": "ListItem", "position": i, "name": label, "item": BASE + href})
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elements}, ensure_ascii=False)


def minutes_of(html_text):
    words = re.sub(r"<[^>]+>", " ", html_text).split()
    return max(1, round(len(words) / 170))


def story_card(article):
    mins = minutes_of(article["html"])
    return (
        f'<a class="story" href="{article["slug"]}.html">'
        f"<small>Rehber · {mins} dk okuma</small>"
        f"<strong>{e(article['title'])}</strong>"
        f"<span>{e(article['description'])}</span></a>"
    )


TOPICS = [
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
]


def topic_for(slug):
    if slug == "marka-tescil":
        return "Marka tescil"
    if slug in ("patent-tescil", "faydali-model"):
        return "Patent veya faydalı model"
    if slug == "tasarim-tescil":
        return "Tasarım"
    if slug.startswith("iso"):
        return "ISO ve yönetim sistemleri"
    if slug in ("ce-belgesi", "ce-akredite", "ce-en-1090", "yerli-mali-belgesi", "haccp", "tse-urun-belgesi", "brcgs", "helal-gida", "hak-akrediteli"):
        return "CE, TSE, yerli malı, HACCP"
    if slug == "verbis-kvkk":
        return "VERBİS / KVKK"
    return ""


def contact_form(preset=""):
    options = ['<option value="">Seçin</option>']
    for label in TOPICS:
        selected = " selected" if label == preset else ""
        options.append(f'<option value="{e(label)}"{selected}>{e(label)}</option>')
    return f'''
<form class="panel form" id="iletisim-formu">
  <h2>Yazın</h2>
  <label class="hp" aria-hidden="true">Web sitesi<input name="website" tabindex="-1" autocomplete="off"></label>
  <label>Ad soyad<input name="ad" autocomplete="name" required></label>
  <label>E-posta<input name="eposta" type="email" autocomplete="email" required></label>
  <label>Telefon <span class="note">(isteğe bağlı)</span><input name="tel" type="tel" autocomplete="tel"></label>
  <label>Konu
    <select name="konu" required>
      {''.join(options)}
    </select>
  </label>
  <label>Mesaj<textarea name="mesaj" rows="5" required></textarea></label>
  <p class="error" role="alert"></p>
  <button class="btn btn-gold" type="submit">WhatsApp'tan gönder</button>
  <p class="done note" hidden>WhatsApp açıldı. Mesaj hazır; göndermeyi orada tamamlayın.</p>
  <p class="note">Yazdıklarınız WhatsApp sohbetinde açılır. Site mesajın kopyasını tutmaz. Ayrıntı <a href="gizlilik.html">kişisel veriler</a> sayfasında.</p>
</form>'''


def search_index():
    items = []
    for s in SERVICES:
        items.append({"t": s["name"], "d": s["card"], "u": s["slug"] + ".html", "g": s["group"]})
    for a in ARTICLES:
        items.append({"t": a["title"], "d": a["description"], "u": a["slug"] + ".html", "g": "Rehber"})
    extras = [
        ("Hizmetler", "Tüm tescil ve belge başlıkları", "hizmetler.html", "Kurumsal"),
        ("Hakkımızda", "Selçuklu ofisi ve çalışma biçimi", "hakkimizda.html", "Kurumsal"),
        ("Referanslar", "Birlikte çalışılan firmalar", "referanslar.html", "Kurumsal"),
        ("Sık sorulan sorular", "Süre ve belgeyi kimin verdiği", "sss.html", "Rehber"),
        ("Konya ofisi", "Selçuklu'dan marka ve patent", "konya-marka-patent.html", "Kurumsal"),
        ("İletişim", "Telefon, e-posta ve ofis adresi", "iletisim.html", "Kurumsal"),
    ]
    for title, desc, url, group in extras:
        items.append({"t": title, "d": desc, "u": url, "g": group})
    return json.dumps(items, ensure_ascii=False).replace("<", "\\u003c")


def shell(filename, seo_title, description, body, active, schemas=None):
    canon = BASE if filename == "index.html" else BASE + filename
    scripts = [f'<script type="application/ld+json">{org_schema()}</script>']
    for raw in schemas or []:
        scripts.append(f'<script type="application/ld+json">{raw}</script>')
    doc = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(seo_title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(canon)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="tr_TR">
<meta property="og:title" content="{e(seo_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(canon)}">
<meta property="og:image" content="{BASE}assets/logo.png">
<meta name="twitter:card" content="summary">
<link rel="icon" href="assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,500;0,8..60,600;1,8..60,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css?v=26">
{''.join(scripts)}
</head>
<body class="page-{active}">
<a class="skip" href="#icerik">İçeriğe geç</a>
{header(active)}
<main id="icerik">
{body}
</main>
{footer()}
<div class="wa-dock" id="wa-dock">
  <div class="wa-panel" id="wa-panel" role="dialog" aria-labelledby="wa-title">
    <h2 id="wa-title">Bir cümle yeter.</h2>
    <p>Konuyu seçin, notunuzu yazın. Sohbet WhatsApp'ta açılır.</p>
    <div class="wa-chips">
      <button type="button" data-topic="marka tescili">Marka</button>
      <button type="button" data-topic="patent veya faydalı model">Patent</button>
      <button type="button" data-topic="ISO veya belgelendirme">ISO</button>
      <button type="button" data-topic="CE veya yerli malı">CE</button>
    </div>
    <textarea id="wa-note" placeholder="Kısaca ne lazım?"></textarea>
    <button class="btn wa-go" type="button" id="wa-go">Sohbeti aç</button>
  </div>
  <button class="wa-launcher" type="button" aria-expanded="false" aria-controls="wa-panel">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 11.5A8.5 8.5 0 0 1 6.7 18.6L4 20l1.5-2.6A8.5 8.5 0 1 1 20 11.5zm-8.5 6.8a7 7 0 1 0-6-3.4l.2.4-.8 1.5 1.6-.8.4.2a7 7 0 0 0 4.6 1.1zm3.8-5.2c-.2-.1-1.2-.6-1.4-.7s-.3-.1-.5.1-.5.7-.7.8-.2.2-.4.1a5.7 5.7 0 0 1-1.7-1 6.3 6.3 0 0 1-1.2-1.5c-.1-.2 0-.3.1-.4l.3-.4.1-.2a.4.4 0 0 0 0-.4c0-.1-.5-1.1-.6-1.5s-.3-.3-.5-.3h-.4a.8.8 0 0 0-.6.3 2.4 2.4 0 0 0-.8 1.8 4.1 4.1 0 0 0 .9 2.2 9.4 9.4 0 0 0 3.6 3.2 12 12 0 0 0 2.4.9 2 2 0 0 0 1.3-.1 1.6 1.6 0 0 0 1-.9 1.3 1.3 0 0 0 .1-.9c-.1-.1-.2-.1-.4-.2z"/></svg>
    <span class="wa-label">WhatsApp</span>
  </button>
</div>
<script id="search-index" type="application/json">{search_index()}</script>
<script src="js/main.js?v=17"></script>
</body>
</html>
'''
    (SITE / filename).write_text(doc, encoding="utf-8")
    return filename


def faq_html(pairs):
    blocks = []
    for q, a in pairs:
        blocks.append(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>")
    return '<div class="faq">' + "".join(blocks) + "</div>"


def side():
    links = "".join(link_html(s) for s in SERVICES)
    return f'''
<aside class="side">
  <h2>Ön görüşme</h2>
  <p>Dosyanızı dinleyip hangi işlemin gerektiğini ayıralım.</p>
  <button class="btn btn-wa wa-open" type="button">WhatsApp'tan yazın</button>
  <p><a href="{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <h2>Hizmetler</h2>
  {links}
</aside>'''


def logos(items):
    figs = []
    for name, filename in items:
        figs.append(
            f'<figure><img src="assets/referans/{e(filename)}" alt="{e(name)} logosu" loading="lazy" decoding="async"><figcaption>{e(name)}</figcaption></figure>'
        )
    return '<div class="logo-grid">' + "".join(figs) + "</div>"


def home():
    blocks = []
    for group in groups():
        inner = "".join(card_html(s) for s in SERVICES if s["group"] == group)
        blocks.append(f'<h3 class="group-label">{e(group)}</h3><div class="cards">{inner}</div>')
    steps = [
        ("01", "Dinleme", "Faaliyetinizi ve korunacak şeyi yerinde konuşuruz."),
        ("02", "Araştırma", "Benzer hakları ve riski yazılı olarak ayırırız."),
        ("03", "Dosya", "Sınıf, istem, resim veya sistem dokümanı hazırlanır."),
        ("04", "Başvuru", "İlgili kuruma başvuru yapılır, yazılar takip edilir."),
        ("05", "Sonrası", "Belge, yenileme ve izleme takvimi size kalır."),
    ]
    step_html = "".join(f'<article class="step"><em>{n}</em><h3>{e(t)}</h3><p>{e(p)}</p></article>' for n, t, p in steps)
    news = "".join(story_card(a) for a in ARTICLES[:3])
    body = f'''
<section class="cover" aria-roledescription="carousel" aria-label="Öne çıkanlar">
  <div class="cover-track">
  <article class="cover-slide is-in">
    <img class="cover-photo photo-marka" src="assets/hero/marka.jpg" alt="Evrak üzerinde çalışan danışman" width="1000" height="750" decoding="async" fetchpriority="high">
    <div class="cover-veil" aria-hidden="true"></div>
    <p class="cover-name" aria-hidden="true">Atlas</p>
    <div class="wrap cover-copy">
      <p class="kicker">Marka</p>
      <h1 class="slide-title">İsim, sicile yazılmadan <em>tabela olmasın.</em></h1>
      <p class="lede">Logo, isim ve ayırt edici işaret önce araştırılır, sonra dosyaya girer. Ofis Selçuklu'da, başvuru Türkiye genelinde.</p>
      <div class="actions">
        <a class="btn btn-gold" href="marka-tescil.html">Marka dosyası</a>
        <a class="btn btn-ghost" href="iletisim.html">Ön görüşme</a>
      </div>
    </div>
  </article>
  <article class="cover-slide">
    <img class="cover-photo photo-patent" src="assets/hero/patent.jpg" alt="Üretim alanında dosya inceleyen danışman" width="1000" height="750" decoding="async">
    <div class="cover-veil" aria-hidden="true"></div>
    <p class="cover-name" aria-hidden="true">Atlas</p>
    <div class="wrap cover-copy">
      <p class="kicker">Patent</p>
      <h2 class="slide-title">Buluş, anlatılmadan <em>dosyaya girer.</em></h2>
      <p class="lede">Yenilik, buluş basamağı ve sanayiye uygulanabilirlik aynı masada konuşulur. Faydalı model ayrı, daha kısa bir yoldur.</p>
      <div class="actions">
        <a class="btn btn-gold" href="patent-tescil.html">Patent dosyası</a>
        <a class="btn btn-ghost" href="faydali-model.html">Faydalı model</a>
      </div>
    </div>
  </article>
  <article class="cover-slide">
    <img class="cover-photo photo-sistem" src="assets/hero/sistem.jpg" alt="Toplantı masasında görüşen üç kişi" width="1000" height="750" decoding="async">
    <div class="cover-veil" aria-hidden="true"></div>
    <p class="cover-name" aria-hidden="true">Atlas</p>
    <div class="wrap cover-copy">
      <p class="kicker">Sistem</p>
      <h2 class="slide-title">Kalite, belge ve <em>uyum</em> aynı rafta.</h2>
      <p class="lede">ISO, helal, HACCP, CE teknik dosya ve yerli malı. Belgeyi veren kuruluş ayrıdır; biz dosyayı kurar, denetime hazırlarız.</p>
      <div class="actions">
        <a class="btn btn-gold" href="hizmetler.html">Hizmetlere bak</a>
        <a class="btn btn-ghost" href="iso-9001.html">ISO 9001</a>
      </div>
    </div>
  </article>
  <article class="cover-slide">
    <img class="cover-photo photo-konya" src="assets/hero/konya.jpg" alt="Cam cepheli ofiste çalışanlar" width="1000" height="750" decoding="async">
    <div class="cover-veil" aria-hidden="true"></div>
    <p class="cover-name" aria-hidden="true">Atlas</p>
    <div class="wrap cover-copy">
      <p class="kicker">Selçuklu</p>
      <h2 class="slide-title">Konya'dan, <em>Türkiye geneline.</em></h2>
      <p class="lede">{ADDRESS}. On yılı aşkın tecrübe, 51 referans firma. Dosyayı yerinde konuşmak için bir mesaj yeter.</p>
      <div class="actions">
        <a class="btn btn-gold" href="iletisim.html">Ofise yazın</a>
        <a class="btn btn-ghost" href="{TEL}">{PHONE}</a>
      </div>
    </div>
  </article>
  </div>
  <button class="cover-arrow prev" type="button" aria-label="Önceki slayt">‹</button>
  <button class="cover-arrow next" type="button" aria-label="Sonraki slayt">›</button>
  <div class="cover-tabs" role="tablist" aria-label="Slaytlar">
    <button type="button" role="tab" class="on" aria-label="Marka" aria-selected="true"></button>
    <button type="button" role="tab" aria-label="Patent" aria-selected="false"></button>
    <button type="button" role="tab" aria-label="Sistem" aria-selected="false"></button>
    <button type="button" role="tab" aria-label="Selçuklu" aria-selected="false"></button>
  </div>
  <div class="cover-progress" aria-hidden="true"><i></i></div>
</section>
<div class="info-strip">
  <div class="wrap">
    <span><b>10+</b> yıllık tecrübe</span>
    <span><b>51</b> referans firma</span>
    <span><b>{len(SERVICES)}</b> hizmet başlığı</span>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
  </div>
</div>
<section class="section">
  <div class="wrap split">
    <div>
      <p class="kicker">Hakkımızda</p>
      <h2>Büyük küçük ayırmadan, dosyayı sonuna kadar götürmek.</h2>
      <p>Marka, patent, faydalı model, tasarım ve coğrafi işaret işlemlerini yürütürüz. Yurt içi ve yurt dışı marka başvurularında, öncesi ve sonrasıyla sizi haberdar ederiz. Barkod, yerli malı belgesi, ISO, helal gıda, HACCP ve ürün belgelendirmede de aynı ciddiyet geçerlidir.</p>
      <p>Her firmaya ayrı bakar, işi benimseriz. Sürekli iyileştirme, yeni fikir ve samimi çalışma biçimimizdir.</p>
      <a class="btn btn-ghost" href="hakkimizda.html">Kurumsal metin</a>
    </div>
    <div>
      <p class="kicker">Neden Atlas Patent?</p>
      <ul class="ticks">
        <li>Başvurudan önce araştırma, sonra dosya.</li>
        <li>Eksik yazıyı süresi içinde cevaplamak.</li>
        <li>Yenileme tarihini kaçırmamak.</li>
        <li>Belge veren kuruluş ile danışmanı karıştırmamak.</li>
        <li>Konya'dan Türkiye geneline hizmet.</li>
      </ul>
    </div>
  </div>
</section>
<section class="section band">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="kicker">Çalışma yöntemi</p>
        <h2>Hangi dosya?</h2>
        <p>Ne aradığınız belli değilse buradan girin. Dört kapı yeter; gerisini ilk görüşmede ayırırız.</p>
      </div>
    </div>
    <div class="door-grid">
      <a class="door" href="marka-tescil.html">
        <em>01</em>
        <strong>Tabela ve isim</strong>
        <span>Marka tescili. Logo ve ayırt edici işaret, sicile yazılmadan tabela olmasın.</span>
      </a>
      <a class="door" href="patent-tescil.html">
        <em>02</em>
        <strong>Buluş</strong>
        <span>Patent veya faydalı model. Anlatılmadan önce dosyaya girer.</span>
      </a>
      <article class="door">
        <em>03</em>
        <strong>Gıda</strong>
        <span>Denetimden önce dosya kurulur. Belgeyi veren kuruluş ayrıdır.</span>
        <p><a href="iso-22000.html">ISO 22000</a><a href="haccp.html">HACCP</a><a href="helal-gida.html">Helal</a></p>
      </article>
      <article class="door">
        <em>04</em>
        <strong>İhale ve ihracat</strong>
        <span>Kamu alımı için yerli katkı, ürünün yurt dışına çıkışı için CE teknik dosya.</span>
        <p><a href="yerli-mali-belgesi.html">Yerli malı</a><a href="ce-belgesi.html">CE dosyası</a></p>
      </article>
    </div>
  </div>
</section>
<section class="section" id="hizmetler">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="kicker">Hizmetler</p>
        <h2>Ne için geldiniz?</h2>
        <p>Sınai mülkiyet, yönetim sistemleri ve belge dosyaları ayrı başlıklarda. Karışık duran işi ilk görüşmede ayırırız.</p>
      </div>
      <a href="hizmetler.html">Tüm hizmetler</a>
    </div>
    {''.join(blocks)}
  </div>
</section>
<section class="section band">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="kicker">Süreç</p>
        <h2>Dosya nasıl yürür?</h2>
        <p>Marka, patent ve ISO aynı takvime sığmaz. İskelet aynıdır: dinlemek, araştırmak, dosyayı kurmak, başvurmak, takip etmek.</p>
      </div>
    </div>
    <div class="steps">{step_html}</div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="kicker">Referanslar</p>
        <h2>Birlikte çalıştığımız yerler</h2>
      </div>
      <a href="referanslar.html">51 firmanın tamamı</a>
    </div>
    {logos(REFS[:12])}
  </div>
</section>
<section class="section band">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="kicker">Rehber</p>
        <h2>Kısa yazılar</h2>
      </div>
      <a href="haberler.html">Tüm yazılar</a>
    </div>
    <div class="news-grid">{news}</div>
  </div>
</section>
<section class="section">
  <div class="wrap narrow">
    <div class="section-head">
      <div>
        <p class="kicker">Sorular</p>
        <h2>Sık sorulanlar</h2>
      </div>
      <a href="sss.html">Tüm sorular</a>
    </div>
    {faq_html(FAQ[:6])}
  </div>
</section>
<section class="section flush">
  <div class="wrap">
    <div class="dark-band">
      <div>
        <h2>İsim basılmadan, buluş anlatılmadan önce konuşalım.</h2>
        <p>Tabela, ambalaj veya fuar, tescilsiz bir işareti kamuya açabilir. Bir telefon, sırayı değiştirir.</p>
      </div>
      <a class="btn btn-gold" href="iletisim.html">Ön görüşme</a>
    </div>
  </div>
</section>
'''
    shell(
        "index.html",
        "Atlas Patent | Marka, Patent ve Belgelendirme | Konya",
        "Konya Selçuklu Atlas Patent: marka tescil, patent, tasarım, faydalı model, ISO, CE teknik dosya, yerli malı ve VERBİS danışmanlığı.",
        body,
        "home",
        [faq_schema(FAQ[:6])],
    )


def about():
    trail = [("hakkimizda.html", "Hakkımızda")]
    body = f'''
<section class="page-hero"><div class="wrap">
{crumbs_html(trail)}
<p class="kicker">Kurumsal</p>
<h1>On yıldır dosyayı sonuna kadar götürüyoruz.</h1>
<p class="lede">Atlas Patent, Selçuklu'dan Türkiye geneline marka, patent ve yönetim sistemleri danışmanlığı verir.</p>
</div></section>
<section class="section"><div class="wrap layout">
<div class="prose">
<p>Firmamız marka tescil, patent, faydalı model, tasarım tescil ve coğrafi işaret işlemlerini yürütür. Fikri ve sınai hakların yurt içi ve yurt dışı marka başvurularında, işlem öncesi ve sonrasında müşteriyi bilgilendirir, süreci takip eder.</p>
<p>Barkod, yerli malı belgesi, ISO 9001, ISO 22000, ISO 45001, ISO 14001, helal gıda, HACCP, ürün belgelendirme ve standart belgelendirmede de aynı çizgide çalışırız.</p>
<p>On yıllık tecrübeyle Türkiye geneline hizmet vermeyi sürdürüyoruz. Hızlı olmak, kaliteden ödün vermek değildir. Sektörde iz bırakacak bir iş bilgisi ve sınai mülkiyet bilinci için sürekli çalışırız.</p>
<p>Her firmaya ayrı bakar, yenilikçi önlem önerir, üstlendiğimiz işi benimseriz. Sürekli iyileştirme, yeni fikir, güler yüz ve samimiyet çalışma biçimimizdir.</p>
<p>Genç ve işi bilen bir kadroyla, büyük küçük firma ayrımı yapmadan güvenilir bir hizmet anlayışıyla ilerleriz.</p>
<h2>Neyi üstleniriz, neyi üstlenmeyiz?</h2>
<p>Başvuru dosyasını, araştırmayı ve kurum yazışmalarının takibini üstleniriz. ISO, CE, TSE ve helal belgesini biz düzenlemeyiz. Belgeyi yetkili belgelendirme kuruluşu, onaylanmış kuruluş veya ilgili oda verir. Bu ayrım, sürpriz yaşamamanız içindir.</p>
<ol class="timeline">
<li><strong>Selçuklu ofisi</strong><span>{ADDRESS}</span></li>
<li><strong>On yılı aşkın dosya</strong><span>Türkiye geneline marka, patent ve yönetim sistemleri danışmanlığı.</span></li>
<li><strong>Sınai mülkiyet</strong><span>Marka, patent, faydalı model, tasarım ve coğrafi işaret.</span></li>
<li><strong>Sistem ve belge dosyası</strong><span>ISO, helal, HACCP, CE teknik dosya, yerli malı ve TSE hazırlığı.</span></li>
<li><strong>Sınır</strong><span>Belgeyi yetkili kuruluş verir. Atlas Patent dosyayı kurar ve takibini yapar.</span></li>
</ol>
</div>
{side()}
</div></section>
'''
    shell("hakkimizda.html", "Hakkımızda | Atlas Patent Konya", "Atlas Patent hakkında: Selçuklu Konya merkezli marka, patent, tasarım ve yönetim sistemleri danışmanlığı. On yıllık tecrübe.", body, "hakkimizda", [crumb_schema(trail)])


def services_page():
    trail = [("hizmetler.html", "Hizmetler")]
    blocks = []
    for group in groups():
        inner = "".join(card_html(s, show_group=False) for s in SERVICES if s["group"] == group)
        blocks.append(f'<h2 class="group-label">{e(group)}</h2><div class="cards">{inner}</div>')
    body = f'''
<section class="page-hero"><div class="wrap">
{crumbs_html(trail)}
<p class="kicker">Danışmanlık</p>
<h1>Hizmetler</h1>
<p class="lede">Sınai mülkiyet, yönetim sistemleri ve belge dosyaları. Hangisine ihtiyacınız olduğunu bilmiyorsanız iletişimden başlayın.</p>
</div></section>
<section class="section"><div class="wrap">
{''.join(blocks)}
</div></section>
'''
    shell(
        "hizmetler.html",
        "ISO, CE, TSE, Helal ve Marka Belgesi | Atlas Patent Konya",
        "Konya Atlas Patent: ISO 9001, 14001, 45001, 22000, 27001 ve 50001 belgesi, CE belgesi, TSE ürün belgesi, helal belgesi, yerli malı belgesi, VERBİS, HACCP ve BRCGS danışmanlığı.",
        body,
        "hizmetler",
        [crumb_schema(trail)],
    )


def service_pages():
    files = []
    for s in SERVICES:
        trail = [("hizmetler.html", "Hizmetler"), (s["slug"] + ".html", s["name"])]
        faq = faq_html(s["faq"]) if s["faq"] else ""
        related = [card_html(other, show_group=False) for other in SERVICES if other["group"] == s["group"] and other["slug"] != s["slug"]][:3]
        related_html = ""
        if related:
            related_html = f'''
<section class="section band"><div class="wrap">
<div class="section-head"><div><p class="kicker">Yakın başlıklar</p><h2>İlgili hizmetler</h2></div></div>
<div class="cards">{"".join(related)}</div>
</div></section>'''
        body = f'''
<section class="page-hero"><div class="wrap">
{crumbs_html(trail)}
<p class="kicker">{e(s["group"])}</p>
<h1>{e(s.get("heading") or s["name"])}</h1>
<p class="lede">{e(s["lead"])}</p>
</div></section>
<section class="section"><div class="wrap layout">
<article class="prose">
{s["body"]}
{('<h2>Sık sorulanlar</h2>' + faq) if faq else ''}
<p class="note">{e(DISCLAIMER)}</p>
</article>
{side()}
</div></section>
{related_html}
<section class="section"><div class="wrap split">
<div>
<p class="kicker">Ön görüşme</p>
<h2>Bu dosyayı birlikte ayıralım.</h2>
<p>Telefon <a href="{TEL}">{PHONE}</a>. Yazılı not için form, sohbeti WhatsApp'ta açar.</p>
</div>
{contact_form(topic_for(s["slug"]))}
</div></section>
'''
        schemas = [service_schema(s), crumb_schema(trail)]
        if s["faq"]:
            schemas.append(faq_schema(s["faq"]))
        files.append(shell(s["slug"] + ".html", s["seo_title"], s["description"], body, "hizmetler", schemas))
    return files


def refs_page():
    trail = [("referanslar.html", "Referanslar")]
    body = f'''
<section class="page-hero"><div class="wrap">
{crumbs_html(trail)}
<p class="kicker">Portföy</p>
<h1>Referanslar</h1>
<p class="lede">Marka ve belge dosyasında birlikte çalıştığımız 51 firma. Logolar firmalara aittir.</p>
</div></section>
<section class="section"><div class="wrap">
<div class="ref-tools">
<label>Firma ara<input id="ref-q" type="search" placeholder="Firma adı" autocomplete="off"></label>
<p class="note" id="ref-count">{len(REFS)} firma</p>
</div>
{logos(REFS)}
</div></section>
'''
    shell("referanslar.html", "Referanslar | Atlas Patent", "Atlas Patent referansları: Konya ve Türkiye genelinden 51 firma logosu.", body, "referanslar", [crumb_schema(trail)])


def article_schema(article):
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article["title"],
        "description": article["description"],
        "inLanguage": "tr",
        "timeRequired": f"PT{minutes_of(article['html'])}M",
        "author": {"@type": "Organization", "name": "Atlas Patent", "url": BASE},
        "publisher": {
            "@type": "Organization",
            "name": "Atlas Patent",
            "logo": {"@type": "ImageObject", "url": BASE + "assets/logo.png"},
        },
        "mainEntityOfPage": BASE + article["slug"] + ".html",
    }
    return json.dumps(data, ensure_ascii=False)


def news_pages():
    files = ["haberler.html"]
    trail = [("haberler.html", "Yazılar")]
    cards = "".join(story_card(a) for a in ARTICLES)
    body = f'''
<section class="page-hero"><div class="wrap">
{crumbs_html(trail)}
<p class="kicker">Rehber</p>
<h1>Kısa rehber</h1>
<p class="lede">Eski sitede başlığı olup metni boş kalan haberlerin yerine, işe yarayan kısa yazılar koyduk.</p>
</div></section>
<section class="section"><div class="wrap news-grid">{cards}</div></section>
'''
    shell("haberler.html", "Yazılar | Atlas Patent", "Marka tescili, HACCP, CE teknik dosya, yerli malı belgesi ve TSE-CE farkı üzerine kısa rehberler.", body, "rehber", [crumb_schema(trail)])
    for a in ARTICLES:
        item_trail = [("haberler.html", "Yazılar"), (a["slug"] + ".html", a["title"])]
        related = "".join(story_card(other) for other in ARTICLES if other["slug"] != a["slug"])
        article = f'''
<section class="page-hero"><div class="wrap">
{crumbs_html(item_trail)}
<p class="article-meta">Rehber · {minutes_of(a["html"])} dk okuma</p>
<h1>{e(a["title"])}</h1>
</div></section>
<section class="section"><div class="wrap layout">
<article class="prose">{a["html"]}<p class="note">{e(DISCLAIMER)}</p></article>
{side()}
</div></section>
<section class="section band"><div class="wrap">
<div class="section-head"><div><p class="kicker">Devamı</p><h2>İlgili yazılar</h2></div></div>
<div class="news-grid">{related}</div>
</div></section>
'''
        files.append(shell(
            a["slug"] + ".html",
            a["title"] + " | Atlas Patent",
            a["description"],
            article,
            "rehber",
            [article_schema(a), crumb_schema(item_trail)],
        ))
    return files


def sss():
    trail = [("sss.html", "Sık sorulan sorular")]
    body = f'''
<section class="page-hero"><div class="wrap">
{crumbs_html(trail)}
<p class="kicker">Sorular</p>
<h1>Sık sorulan sorular</h1>
<p class="lede">Süre, koruma ve kimin belge verdiği. Dosyanız farklıysa iletişimden netleştiririz.</p>
</div></section>
<section class="section"><div class="wrap narrow">
{faq_html(FAQ)}
</div></section>
'''
    shell("sss.html", "Sık Sorulan Sorular | Atlas Patent", "Marka, patent, tasarım, ISO, CE, VERBİS ve yerli malı belgesi hakkında kısa cevaplar.", body, "rehber", [faq_schema(FAQ), crumb_schema(trail)])


def contact():
    trail = [("iletisim.html", "İletişim")]
    body = f'''
<section class="page-hero"><div class="wrap">
{crumbs_html(trail)}
<p class="kicker">Ofis</p>
<h1>İletişim</h1>
<p class="lede">Dosyanızı iki cümleyle yazın. Aynı gün dönüş için telefon daha hızlıdır.</p>
</div></section>
<section class="section"><div class="wrap split">
<div>
  <h2>Genel merkez</h2>
  <p>{ADDRESS}</p>
  <p><a href="{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{WA}">WhatsApp</a></p>
  <p><a href="{MAP}">Yol tarifi</a></p>
  <div class="map-frame">
    <iframe class="map" title="Atlas Patent ofisi, Selçuklu Konya" loading="lazy" src="{MAP}&amp;output=embed"></iframe>
    <p class="map-label">Atlas Patent</p>
  </div>
</div>
{contact_form()}
</div></section>
'''
    shell("iletisim.html", "İletişim | Atlas Patent Konya", "Atlas Patent iletişim: Binkonutlar Mah. Udi Sk. No:4/D Selçuklu Konya, 0555 622 44 22, info@atlaspatent.com.tr.", body, "iletisim", [crumb_schema(trail)])


def privacy():
    trail = [("gizlilik.html", "Kişisel veriler")]
    body = f'''
<section class="page-hero"><div class="wrap">
{crumbs_html(trail)}
<p class="kicker">KVKK</p>
<h1>Kişisel veriler</h1>
</div></section>
<section class="section"><div class="wrap prose">
<p>Bu sayfa, web sitesi ve iletişim formu üzerinden Atlas Patent'e ulaşan kişiler içindir. Veri sorumlusu: Atlas Patent, {ADDRESS}, {EMAIL}, {PHONE}.</p>
<h2>Hangi veri, hangi amaç?</h2>
<p>Ad, e-posta, telefon ve mesaj, yalnızca talebinize cevap vermek ve randevu kurmak için işlenir. İnsan kaynakları konusunu seçerseniz özgeçmiş bilgisini de bu amaçla alırız. Veriyi reklam listesine kendiliğimizden eklemeyiz.</p>
<h2>Hukuki sebep ve süre</h2>
<p>İletişim, sözleşmenin kurulmasından önce talep üzerine adım atmak ve meşru menfaat kapsamında dosyayı yürütmek içindir. Site formdaki yazının kopyasını saklamaz. Yazışma WhatsApp ve e-posta üzerinden yürür; saklama süresi o kanalların kaydına göredir.</p>
<h2>Aktarım</h2>
<p>Formu gönderince ad, e-posta, telefon ve mesaj WhatsApp sohbetinde açılır. İletiyi siz tamamlarsınız. Harita, Google harita hizmetiyle gösterilir. Veri satılmaz ve reklam listesine eklenmez.</p>
<h2>Haklarınız</h2>
<p>6698 sayılı Kanun'un 11. maddesindeki haklarınız için {EMAIL} adresine yazabilirsiniz. Başvurunuz kimliğiniz doğrulanarak cevaplanır. Şikayet için Kişisel Verileri Koruma Kurulu'na da başvurabilirsiniz.</p>
</div></section>
'''
    shell("gizlilik.html", "Kişisel Veriler | Atlas Patent", "Atlas Patent web sitesi kişisel veriler aydınlatma metni. İletişim formu ve haklarınız.", body, "", [crumb_schema(trail)])


def konya():
    trail = [("konya-marka-patent.html", "Konya ofisi")]
    body = f'''
<section class="page-hero"><div class="wrap">
{crumbs_html(trail)}
<p class="kicker">Selçuklu</p>
<h1>Konya'da marka ve patent danışmanlığı</h1>
<p class="lede">Ofis Selçuklu'da. Dosya, Konya sanayisinden Türkiye geneline ve yurt dışı başvuru rotalarına gider.</p>
</div></section>
<section class="section"><div class="wrap layout">
<article class="prose">
<p>On yıllık tecrübeyle Türkiye geneline hizmet vermeyi amaçlayan firmamız, emin adımlarla büyümeye devam eder. Konya'da üreten, paketleyen ve ihraç eden firmalar için marka çoğu zaman tabeladan önce düşünülmesi gereken bir iştir.</p>
<p>Gıda, makine, mobilya ve perakendede aynı ismin ikinci kez seçilmesi sık görülür. Bu yüzden başvuru, tabela ve ambalaj siparişinden önce gelir. Sınıf listesini broşürden değil, ürettiğiniz maldan çıkarırız.</p>
<h2>Bu ofiste yürüyen işler</h2>
<ul>
<li><a href="marka-tescil.html">Marka tescil</a> ve yenileme</li>
<li><a href="patent-tescil.html">Patent</a> ve <a href="faydali-model.html">faydalı model</a></li>
<li><a href="tasarim-tescil.html">Tasarım tescil</a></li>
<li><a href="iso-9001.html">ISO</a>, <a href="haccp.html">HACCP</a> ve <a href="helal-gida.html">helal gıda</a></li>
<li><a href="ce-belgesi.html">CE teknik dosya</a>, <a href="yerli-mali-belgesi.html">yerli malı</a> ve <a href="tse-urun-belgesi.html">TSE</a></li>
</ul>
<p>{ADDRESS}. Telefon <a href="{TEL}">{PHONE}</a>.</p>
</article>
{side()}
</div></section>
'''
    shell("konya-marka-patent.html", "Konya Marka Patent | Atlas Patent Selçuklu", "Konya Selçuklu marka tescil, patent ve ISO danışmanlığı. Atlas Patent ofisi: Binkonutlar Mah. Udi Sk. No:4/D.", body, "rehber", [crumb_schema(trail)])


OLD_PATHS = {
    "atlas_patent": "hakkimizda.html",
    "hizmetlerimiz": "hizmetler.html",
    "marka_tescil": "marka-tescil.html",
    "patent_tescil": "patent-tescil.html",
    "tasarim_tescil": "tasarim-tescil.html",
    "faydali_model_tescil": "faydali-model.html",
    "iso_9001_yonetim_sistemleri_danismanligi": "iso-9001.html",
    "iso_22000_gida_yonetim_danismanligi": "iso-22000.html",
    "iso_14001_cevre_yonetim_sistemi_danismanligi": "iso-14001.html",
    "iso_45001_is_sagligi_ve_guvenligi_danismanligi": "iso-45001.html",
    "iso_10002_musteri_memnuniyeti_yonetim_sistemi_danismanligi": "iso-10002.html",
    "iso_50001_enerji_yonetim_sistemi_danismanligi": "iso-50001.html",
    "iso_27001_bilgi_guvenligi_yonetim_sistemi_danismanligi": "iso-27001.html",
    "helal_gida_danismanligi": "helal-gida.html",
    "yonetim_sistemleri_egitimi": "hizmetler.html",
    "verbis_hizmeti__kvkk_": "verbis-kvkk.html",
    "yerli_mali_belgesi": "yerli-mali-belgesi.html",
    "ce_belgesi": "ce-belgesi.html",
    "konya_marka_patent": "konya-marka-patent.html",
    "atlas_patent_konya": "konya-marka-patent.html",
    "atlas_patent_hizmetleri": "hizmetler.html",
    "haccp_dosyasi_": "haccp-dosyasi-nedir.html",
    "atlas_patent_marka_tescil_": "konya-marka-tescil.html",
    "ce_belgesi_": "ce-teknik-dosya.html",
    "urun_belgelendirme_": "tse-urun-belgesi.html",
    "hizli_cozumler_": "hizmetler.html",
    "tse_urun_belgesi_": "tse-urun-belgesi.html",
    "referanslar-2": "referanslar.html",
    "referanslar-3": "referanslar.html",
    "referanslar-4": "referanslar.html",
    "referanslar-5": "referanslar.html",
    "referanslar-6": "referanslar.html",
}


def old_redirects():
    for old, target in OLD_PATHS.items():
        page = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<link rel="canonical" href="{BASE}{target}">
<meta http-equiv="refresh" content="0; url=/{target}">
<title>Yönlendiriliyor</title>
<script>location.replace("/{target}");</script>
</head>
<body>
<p><a href="/{target}">Sayfa taşındı.</a></p>
</body>
</html>
'''
        (SITE / f"{old}.html").write_text(page, encoding="utf-8")


def sitemap(files):
    urls = []
    for name in files:
        loc = BASE if name == "index.html" else BASE + name
        urls.append(f"  <url><loc>{loc}</loc></url>")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    (SITE / "sitemap.xml").write_text(xml, encoding="utf-8")
    (SITE / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://www.atlaspatent.com.tr/sitemap.xml\n", encoding="utf-8")


def copy_assets():
    logo_src = IMG / "yuklemeler__W2__ayarlar__16520812481.png"
    shutil.copyfile(logo_src, SITE / "assets" / "logo.png")
    dest = SITE / "assets" / "referans"
    dest.mkdir(parents=True, exist_ok=True)
    for _name, filename in REFS:
        src = IMG / f"yuklemeler__W2__galeri_13__{filename}"
        if not src.exists():
            raise SystemExit(f"missing {src}")
        shutil.copyfile(src, dest / filename)


def main():
    copy_assets()
    files = ["index.html", "hakkimizda.html", "hizmetler.html", "referanslar.html", "haberler.html", "sss.html", "iletisim.html", "gizlilik.html", "konya-marka-patent.html"]
    home()
    about()
    services_page()
    files.extend(service_pages())
    refs_page()
    files.extend(news_pages())
    sss()
    contact()
    privacy()
    konya()
    old_redirects()
    # unique
    all_files = []
    for name in ["index.html", "hakkimizda.html", "hizmetler.html"] + [s["slug"] + ".html" for s in SERVICES] + ["referanslar.html", "haberler.html"] + [a["slug"] + ".html" for a in ARTICLES] + ["sss.html", "iletisim.html", "gizlilik.html", "konya-marka-patent.html"]:
        all_files.append(name)
    sitemap(all_files)
    print("pages", len(all_files))


if __name__ == "__main__":
    main()
