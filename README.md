# 🕒 Digital Clock Widget

Masaüstünüzde duran, **çerçevesiz ve şeffaf** arka planlı, 7 parçalı (seven-segment) tarzında bir dijital saat widget'ı. Tamamen Python + Tkinter ile yazılmıştır; her rakam, hücrelere bölünerek tek tek çizilir.

Saatin **konumu, rengi ve boyutu** doğrudan widget üzerinden düzenlenebilir ve ayarlar kalıcı olarak saklanır — bilgisayarı her açtığınızda saat en son bıraktığınız hâliyle gelir.

---

## ✨ Özellikler

- 🪟 **Çerçevesiz & şeffaf** — masaüstüne yapışık, başlık çubuğu olmayan sade bir görünüm.
- 🎨 **Renk değiştirme** — tek tıkla renk paletinde gezin.
- ✋ **Sürükle-bırak konum** — saati istediğin yere taşı.
- 🔍 **Köşeden boyutlandırma** — istediğin köşeden tutup büyüt/küçült.
- 💾 **Kalıcı ayarlar** — konum, renk ve boyut `%APPDATA%\DigitalClock\config.json` içine kaydedilir.
- 🚀 **Tek dosya .exe** — Python kurulu olmayan makinelerde de çalışır.

---

## 🎮 Kullanım (Düzenleme Modu)

Tüm düzenleme, **Ctrl tuşu basılıyken** yapılır. Ctrl'ü basılı tutup fareyi saatin üzerinde gezdirdiğinde pencere kararır ve **4 köşede yeşil noktalar** belirir — bu, düzenleme modunda olduğunu gösterir.

| İşlem | Nasıl |
|---|---|
| 🎨 Rengi değiştir | Ctrl + saate **tek tık** (her tık sıradaki renk) |
| ✋ Konumu taşı | Ctrl + saatin gövdesine **basılı tutup sürükle** |
| 🔍 Boyutlandır | Ctrl + bir **köşe noktasını tutup sürükle** (karşı köşe sabit kalır) |
| 💾 Kaydet | **Ctrl + S** (ekranda "KAYDEDILDI" yazısı çıkar) |
| ❌ Düzenlemeden çık | **Ctrl'ü bırak** |

> Renk paleti: `lightsteelblue → red → orange → yellow → lime green → cyan → white → magenta`
> Boyut aralığı: **0.4x – 4.0x**

---

## 🖥️ Kaynaktan Çalıştırma

Gereksinim: **Python 3** (Tkinter standart kütüphanede gelir, ekstra paket gerekmez).

```bash
python main.py
```

---

## 📦 Tek Dosya .exe Oluşturma

[PyInstaller](https://pyinstaller.org/) ile tek tıklanabilir bir `.exe` üretebilirsin:

```bash
pip install pyinstaller
python -m PyInstaller --onefile --noconsole --clean --name DigitalClock --icon clock.ico main.py
```

Çıktı: `dist/DigitalClock.exe`

> Konsol penceresi açılmaması için `--noconsole`, ikon için `--icon clock.ico` kullanılır. Ayarlar exe'nin içine gömülmez; çalışırken `%APPDATA%\DigitalClock\` altında oluşturulur.

---

## 🔁 Windows'ta Açılışta Otomatik Başlatma

1. `Win + R` → `shell:startup` yaz, Enter.
2. Açılan klasöre **`DigitalClock.exe`'nin kısayolunu** koy (exe'nin kendisini değil, kısayolunu koyman önerilir).

Ayar dosyası `%APPDATA%` altında tutulduğu için Startup klasöründe gereksiz dosya birikmez.

---

## 🗂️ Proje Yapısı

```
.
├── main.py        # Ana uygulama: pencere, saat döngüsü, düzenleme modu (taşı/renk/boyut/kaydet)
├── gui.py         # Ekran ve rakam geometrisi (Screen / Digits / hücre koordinatları)
├── utils.py       # Yardımcılar: saat alma, basamak/hücre ayrıştırma, çizim
├── clock.ico      # Uygulama ikonu
└── README.md
```

### Nasıl çalışıyor?

- Ekran **25 × 9 hücrelik** bir ızgara olarak tanımlanır; her rakam 5 hücre genişliğindedir.
- Her saniye saat okunur, basamaklara (`divide_digits`) ve hücrelere (`divide_cells`) bölünür; yalnızca **değişen hücreler** yeniden çizilir.
- Saat ve dakika arasındaki **iki nokta (`:`)**, ayrılmış orta sütuna iki kare olarak çizilir.
- Tüm geometri pencere boyutundan türetildiği için **tek bir ölçek (scale)** değeri her şeyi orantılı büyütür/küçültür.

---

## 📄 Lisans

Kişisel/eğitim amaçlı kullanım için serbesttir. Dilediğin gibi değiştirip geliştirebilirsin.
