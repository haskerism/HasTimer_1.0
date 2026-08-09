# HasTimer - Windows Bilgisayar Kapatma Zamanlayıcısı

Siyah temalı PySimpleGUI arayüzü ile Windows bilgisayarını belirli bir süre veya saat bazında kapatmayı planlayan, sistem tray desteğine sahip uygulama.

## 🎯 Özellikler

- **GUI Arayüzü**: PySimpleGUI ile modern, siyah temalı arayüz
- **İki Zamanlama Modu**:
  - Süreli: "2 saat 30 dakika sonra kapat"
  - Saat Bazlı: "14:30'de kapat"
- **Sistem Tray**: Minimized durumda tray'de çalışır, durum gösterir, iptal edebilir
- **Durum Yönetimi**: Zamanlayıcı durumu `%LOCALAPPDATA%\ShutdownTimer\scheduled.json` içinde persiste edilir
- **İptal Fonksiyonu**: `shutdown -a` komutu ile Windows kapatmasını iptal eder
- **Standalone .exe**: PyInstaller ile tek dosya olarak dağıtılır
- **Özel Simge**: Saat tasarımı içine "HAS" yazısı gömülü logo

## 📦 İçindekiler

```
├── ShutdownTimer.py          # Core - durum yönetimi, kapatma mantığı
├── ShutdownTimerGUI.py       # GUI - PySimpleGUI arayüzü (süreli + saat modu)
├── ShutdownTimerTray.py      # Tray - pystray sistem tray menüsü
├── dist/
│   ├── HasTimerGUI.exe       # Kompilenmiş GUI (.onefile --windowed)
│   └── HasTimerTray.exe      # Kompilenmiş Tray (.onefile --windowed)
├── HAS/
│   └── HasTimerIcon.ico      # Özel simge (Masaüstü kısayolu için)
├── RunShutdownTimerGUI.bat   # GUI başlatma (konsol ile)
├── RunShutdownTimerGUI_NoConsole.bat  # GUI başlatma (konsol olmadan)
├── RunShutdownTimerTray.bat  # Tray başlatma
├── CreateHasLogo.py          # Simge üretim scripti (PNG-tarzı)
└── install_shutdown_timer_deps.ps1  # Bağımlılık kurulum (PowerShell)
```

## 🚀 Kurulum

### Seçenek 1: Hazır .exe ile (Önerilen)

1. [Release](../../releases) bölümünden `HasTimerGUI.exe` ve `HasTimerTray.exe` indir
2. Masaüstüne veya `Program Files` içine yerleştir
3. İsteğe bağlı: `HasTimer GUI (No Console).lnk` kısayolunu oluştur

### Seçenek 2: Python Kaynağından

**Gereksinimler:**
- Python 3.10+
- pip

**Adımlar:**
```bash
# 1. Depoyu klonla
git clone https://github.com/yourusername/HasTimer.git
cd HasTimer

# 2. Bağımlılıkları yükle
pip install -r requirements.txt

# 3. GUI'yi çalıştır
python ShutdownTimerGUI.py

# 4. Tray'i çalıştır (opsiyonel)
pythonw ShutdownTimerTray.py
```

## 💻 Kullanım

### GUI Modu

```bash
RunShutdownTimerGUI_NoConsole.bat  # veya HasTimerGUI.exe
```

1. **Süreli Zamanlama**: Radyo düğmesini "Süreli (saat/dakika sonra)" seçin
   - Saat ve dakika girin → "Zamanla" düğmesine basın
   - Kapatma saati ve kalan süre gösterilir

2. **Saat Bazlı Zamanlama**: Radyo düğmesini "Saat bazlı (HH:MM)" seçin
   - Saat (24 saat formatı) ve dakika girin → "Zamanla" düğmesine basın

3. **Durum Kontrol**: "Durum" düğmesine basarak zamanlayıcı bilgisini görüntüle

4. **İptal**: "İptal Et" düğmesine basarak kapatmayı iptal et

### Tray Modu

```bash
RunShutdownTimerTray.bat  # veya HasTimerTray.exe
```

- Tray ikonu sağ tıkla:
  - **Aç**: GUI'yi açar
  - **Durum**: Mevcut kapatma zamanını gösterir
  - **İptal**: Kapatmayı iptal eder
  - **Çık**: Tray'den çıkar (GUI çalışmaya devam edebilir)

## 🔧 Yapılabilecek İyileştirmeler

### Kısa Vadeli

- [ ] **Bildirim Sistemi**: Kapatmaya 5 dakika kala Windows Toast bildirimi gönder
- [ ] **Ses Uyarısı**: Kapatmadan önce sesli uyarı oynat
- [ ] **Sistem Başlangıcında Otomatik Başlama**: Startup klasörüne kısayol
- [ ] **Config Dosyası**: Tema, dil, varsayılan değerleri özelleştir
- [ ] **Birim Testleri**: `pytest` ile `ShutdownTimer.py` ve `load_state()` test et

### Uzun Vadeli

- [ ] **Veritabanı Desteği**: SQLite ile geçmiş zamanlayıcılar, istatistikler
- [ ] **Windows Task Scheduler Entegrasyonu**: `schtasks` ile yinelenen görevler
- [ ] **Multi-language**: TR, EN, DE, FR desteği
- [ ] **Dark/Light Tema**: Dinamik tema değişimi
- [ ] **Zamanlayıcı Hatırlatıcıları**: "Bir gün sonra", "Pazarları 19:00" vb.
- [ ] **REST API**: Uzaktan kontrol için web sunucusu
- [ ] **Tray Dönem Göstergesi**: İkonda kalan zamanı görsel olarak göster (progress bar)
- [ ] **macOS/Linux Desteği**: Cross-platform gelişimi

## 🛠️ Geliştirme

### Build & Release

```bash
# Bağımlılıkları yükle
pip install PySimpleGUI pystray Pillow PyInstaller

# GUI .exe oluştur
pyinstaller --onefile --windowed --name HasTimerGUI ShutdownTimerGUI.py

# Tray .exe oluştur
pyinstaller --onefile --windowed --name HasTimerTray ShutdownTimerTray.py

# .ico oluştur (opsiyonel)
python CreateHasLogo.py

# dist/ klasöründe .exe dosyaları bulunur
```

### Test Etme

```bash
# Kapatmayı iptal et ve durumu kontrol et
python ShutdownTimer.py  # CLI modunda interaktif menü

# GUI testler
python ShutdownTimerGUI.py  # GUI açılıp açılmadığını kontrol et
```

## 📋 State Yapısı

Kapatma durumu şu adreste saklanır:
```
%LOCALAPPDATA%\ShutdownTimer\scheduled.json
```

Örnek içerik:
```json
{
  "scheduled_at": 1723296600,
  "total_seconds": 3600
}
```

- `scheduled_at`: Unix timestamp (kapatılacak zaman)
- `total_seconds`: Toplam saniye cinsinden süre

## 🐛 Bilinen Sorunlar & Çözümler

| Sorun | Çözüm |
|-------|-------|
| GUI penceresinin arkada kalması | `keep_on_top=True` ve `bring_to_front()` kullanılıyor |
| İptal sonrası durum yanlış gösterilmesi | `load_state()` her zaman `remove_state()` ile birlikte çağrılıyor |
| Tray ikonunun çift tıklaması | Pystray varsayılan davranışı (tek tıkla aç) |
| PowerShell yürütme ilkesi | `ExecutionPolicy Bypass` ile script çalıştır |

## 📄 Lisans

MIT License - Serbestçe kullan, değiştir, dağıt.

## 👥 Katkı

Hata raporları ve öneriler için [Issues](../../issues) aç veya pull request gönder.

---

**Geliştirici Notları:**
- Tüm kodlar UTF-8 encoding ile yazılmış (Türkçe dil desteği)
- Windows 10/11 uyumlu
- Python 3.10+ gerekli
- Admin yetkisine gerek yoktur (kapatma komutu yeterli)

