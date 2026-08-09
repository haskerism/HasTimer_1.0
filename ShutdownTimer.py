import os
import time
import json
import subprocess
from datetime import datetime, timedelta

STATE_DIR = os.path.join(os.getenv('LOCALAPPDATA') or os.path.expanduser('~'), 'ShutdownTimer')
STATE_FILE = os.path.join(STATE_DIR, 'scheduled.json')


def ensure_state_dir():
    os.makedirs(STATE_DIR, exist_ok=True)


def save_state(scheduled_at, total_seconds):
    ensure_state_dir()
    data = {'scheduled_at': int(scheduled_at), 'total_seconds': int(total_seconds)}
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def load_state():
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        scheduled_at = int(data.get('scheduled_at', 0))
        remaining = scheduled_at - int(time.time())
        if remaining <= 0:
            remove_state()
            return None
        return {'scheduled_at': scheduled_at, 'total_seconds': int(data.get('total_seconds', 0)), 'remaining': remaining}
    except Exception:
        return None


def remove_state():
    try:
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
    except Exception:
        pass


def format_duration(seconds):
    seconds = int(max(0, seconds))
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hrs} saat, {mins} dakika, {secs} saniye"


def schedule_at_clock():
    # Ask user for HH:MM (24-hour) and compute seconds until then
    s = input('Lütfen kapanış zamanını girin (24 saat formatı HH:MM, örn 14:30): ').strip()
    try:
        parts = s.split(':')
        if len(parts) < 2:
            raise ValueError
        hour = int(parts[0])
        minute = int(parts[1])
        now = datetime.now()
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target <= now:
            # schedule next day
            target = target + timedelta(days=1)
        total_seconds = int((target - now).total_seconds())
    except Exception:
        print('Geçersiz zaman formatı. Lütfen HH:MM şeklinde girin.')
        return

    print(f"Kapatma saati: {target.strftime('%Y-%m-%d %H:%M:%S')} (kalan: {format_duration(total_seconds)})")
    confirm = input("Gerçekten kapatma komutu çalıştırılsın mı? (E/h) ").strip().lower()
    if confirm in ("e", "evet", "y", "yes"):
        print("Kapatma komutu gönderiliyor...")
        time.sleep(1)
        os.system(f"shutdown -s -t {total_seconds}")
        save_state(int(time.time()) + total_seconds, total_seconds)
        print('Zamanlayıcı kaydedildi.')
    else:
        print('Demo modu: Kapatma komutu gönderilmeyecek.')
        print(f'Komut olurdu: shutdown -s -t {total_seconds}')


def schedule_shutdown():
    existing = load_state()
    if existing:
        print("Zaten aktif bir zamanlayıcı var:")
        print(f"Kalan süre: {format_duration(existing['remaining'])}")
        over = input("Mevcut zamanlayıcıyı iptal edip yenisini ayarlamak istiyor musunuz? (E/h): ").strip().lower()
        if over not in ('e', 'evet', 'y', 'yes'):
            print('İşlem iptal edildi.')
            return
        else:
            cancel_shutdown(silent=True)

    print("Bilgisayarı kapatmak için zamanlayıcı ayarlayın.")
    try:
        hours = int(input("Kaç saat sonra kapatmak istiyorsunuz? (0 girerek atlayabilirsiniz): "))
    except ValueError:
        hours = 0
    try:
        minutes = int(input("Kaç dakika sonra kapatmak istiyorsunuz?: "))
    except ValueError:
        minutes = 0

    total_seconds = (hours * 3600) + (minutes * 60)

    if total_seconds > 0:
        print(f"Bilgisayar {hours} saat ve {minutes} dakika sonra kapatilacak.")
        print(f"Toplam: {total_seconds} saniye")
        confirm = input("Gerçekten kapatma komutu çalıştırılsın mı? (E/h) ").strip().lower()
        if confirm in ("e", "evet", "y", "yes"):
            print("Kapatma komutu gönderiliyor...")
            time.sleep(1)
            os.system(f"shutdown -s -t {total_seconds}")
            save_state(int(time.time()) + total_seconds, total_seconds)
            print("Zamanlayıcı kaydedildi.")
        else:
            print("Demo modu: Kapatma komutu gönderilmeyecek.")
            print(f"Komut olurdu: shutdown -s -t {total_seconds}")
    else:
        print("Geçersiz süre girdiniz. Lütfen tekrar deneyin.")


def cancel_shutdown(silent=False):
    # Attempt to abort Windows shutdown
    try:
        proc = subprocess.Popen(['shutdown', '-a'], creationflags=subprocess.CREATE_NO_WINDOW)
        proc.wait(timeout=10)
    except Exception as e:
        if not silent:
            print('İptal sırasında hata:', e)
    finally:
        remove_state()
        if not silent:
            print('Kapatma iptal edildi.')


def show_status():
    state = load_state()
    if not state:
        print('Aktif bir zamanlayıcı yok.')
        return
    remaining = state['remaining']
    scheduled_at = state['scheduled_at']
    dt = datetime.fromtimestamp(scheduled_at).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Zamanlayıcı var. Kapatılma zamanı: {dt}")
    print(f"Kalan süre: {format_duration(remaining)}")
    ans = input('Zamanlayıcıyı iptal etmek ister misiniz? (E/h): ').strip().lower()
    if ans in ('e', 'evet', 'y', 'yes'):
        cancel_shutdown()


def main_menu():
    while True:
        print('\n-- Shutdown Timer --')
        print('1) Yeni zamanlayıcı ayarla')
        print('2) Zamanlayıcı durumunu gör')
        print('3) Çıkış')
        choice = input('Seçiminiz: ').strip()
        if choice == '1':
            print('\n1) Süreli (kaç saat / dakika sonra)')
            print('2) Saat bazlı (belirli bir saat HH:MM)')
            sub = input('Seçiminiz (1/2): ').strip()
            if sub == '1':
                schedule_shutdown()
            elif sub == '2':
                schedule_at_clock()
            else:
                print('Geçersiz seçim.')
        elif choice == '2':
            show_status()
        elif choice == '3':
            print('Çıkılıyor...')
            break
        else:
            print('Geçersiz seçim, tekrar deneyin.')


if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print('\nİptal edildi.')
