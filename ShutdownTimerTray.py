import os
import sys
import threading
import subprocess
import shutil
from datetime import datetime

try:
    import pystray
    from PIL import Image, ImageDraw
except Exception:
    print('Eksik paketler: lütfen `pip install pystray pillow` çalıştırın.')
    raise

# Import functions from the main script
from ShutdownTimer import load_state, cancel_shutdown, format_duration

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
GUI_SCRIPT_PATH = os.path.join(BASE_DIR, 'ShutdownTimerGUI.py')
GUI_EXE_PATH = os.path.join(BASE_DIR, 'HasTimerGUI.exe')


def create_image():
    # 64x64 dark blue background with white power-circle
    img = Image.new('RGB', (64, 64), color='#101A2A')
    d = ImageDraw.Draw(img)
    # outer ring
    d.ellipse((8, 8, 56, 56), outline='white', width=4)
    # power line
    d.rectangle((30, 9, 34, 28), fill='white')
    # inner glow accent
    d.ellipse((22, 22, 42, 42), outline='#4DB8FF', width=2)
    return img


def show_message(title, msg):
    # Use Windows MessageBox for simplicity
    try:
        import ctypes
        MB_OK = 0x00000000
        MB_ICONINFORMATION = 0x00000040
        MB_SETFOREGROUND = 0x00010000
        MB_TOPMOST = 0x00040000
        MB_TASKMODAL = 0x00002000
        ctypes.windll.user32.MessageBoxW(0, msg, title, MB_OK | MB_ICONINFORMATION | MB_SETFOREGROUND | MB_TOPMOST | MB_TASKMODAL)
    except Exception:
        # fallback to printing
        print(title)
        print(msg)


def open_gui(icon=None, item=None):
    # Launch the GUI in a separate process
    def _start():
        if os.path.exists(GUI_EXE_PATH):
            subprocess.Popen([GUI_EXE_PATH], shell=False)
            return
        if os.path.exists(GUI_SCRIPT_PATH):
            python_path = shutil.which('py') or shutil.which('python') or sys.executable
            subprocess.Popen([python_path, GUI_SCRIPT_PATH], shell=False)
            return
        show_message('Hata', f'GUI dosyası bulunamadı:\n{GUI_EXE_PATH}\n{GUI_SCRIPT_PATH}')

    threading.Thread(target=_start, daemon=True).start()


def show_status(icon=None, item=None):
    st = load_state()
    if not st:
        show_message('HasTimer', 'Aktif bir zamanlayıcı yok.')
        return
    dt = datetime.fromtimestamp(st['scheduled_at']).strftime('%Y-%m-%d %H:%M:%S')
    msg = f'Kapatılma zamanı: {dt}\nKalan: {format_duration(st["remaining"])}'
    show_message('HasTimer - Durum', msg)


def cancel(icon=None, item=None):
    cancel_shutdown()
    show_message('HasTimer', 'Varsa zamanlayıcı iptal edildi.')


def quit_app(icon, item):
    icon.stop()


def main():
    icon = pystray.Icon('HasTimer')
    icon.icon = create_image()
    icon.title = 'HasTimer'
    icon.menu = pystray.Menu(
        pystray.MenuItem('Aç (GUI)', open_gui, default=True),
        pystray.MenuItem('Durum göster', show_status),
        pystray.MenuItem('Zamanlayıcıyı iptal et', cancel),
        pystray.MenuItem('Çıkış', quit_app),
    )
    icon.run()


if __name__ == '__main__':
    main()
