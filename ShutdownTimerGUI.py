try:
    import PySimpleGUI as sg
except Exception:
    print('PySimpleGUI yüklü değil. GUI için: pip install PySimpleGUI')
    raise

import ctypes
import os
import time
import subprocess
from datetime import datetime, timedelta

from ShutdownTimer import save_state, cancel_shutdown, load_state, remove_state, format_duration

sg.theme('DarkBlack')
sg.set_options(
    background_color='#0b0b0b',
    text_color='white',
    input_text_color='white',
    button_color=('white', '#2b2b2b'),
    element_background_color='#121212',
    element_text_color='white'
)

layout = [
    [sg.Text('HasTimer', font=('Helvetica', 16, 'bold'), justification='center', text_color='white')],
    [sg.Radio('Süreli (saat/dakika sonra)', 'MODE', key='-REL-', default=True, background_color='#0b0b0b', text_color='white'), sg.Radio('Saat bazlı (HH:MM)', 'MODE', key='-ABS-', background_color='#0b0b0b', text_color='white')],
    [sg.Text('Saat:', size=(8,1), background_color='#0b0b0b', text_color='white'), sg.Input(key='-HOURS-', size=(8,1), background_color='#1c1c1c', text_color='white'), sg.Text('Dakika:', size=(8,1), background_color='#0b0b0b', text_color='white'), sg.Input(key='-MINUTES-', size=(8,1), background_color='#1c1c1c', text_color='white')],
    [sg.Button('Zamanla', key='-SCHEDULE-', button_color=('white', '#333333')), sg.Button('Durum', key='-STATUS-', button_color=('white', '#333333')), sg.Button('İptal Et', key='-CANCEL-', button_color=('white', '#333333')), sg.Button('Çıkış', button_color=('white', '#333333'))],
    [sg.Text('', key='-MSG-', size=(60,2), background_color='#141414', text_color='lightgrey')],
    [sg.Text('', key='-INFO-', size=(60,1), background_color='#141414', text_color='lightgrey')]
]

window = sg.Window('HasTimer', layout, keep_on_top=True, background_color='#0b0b0b', finalize=True)
window['-INFO-'].update(f'Çalıştırılan dosya: {os.path.basename(__file__)}')

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Çıkış'):
        break
    if event == '-SCHEDULE-':
        if values['-REL-']:
            # relative: HOURS -> hours, MINUTES -> minutes
            try:
                hrs = int(values['-HOURS-'] or 0)
                mins = int(values['-MINUTES-'] or 0)
            except ValueError:
                window['-MSG-'].update('Geçersiz sayı girdiniz.')
                continue
            total_seconds = hrs*3600 + mins*60
            if total_seconds <= 0:
                window['-MSG-'].update('Lütfen geçerli bir süre girin.')
                continue
            subprocess.Popen(['shutdown', '-s', '-t', str(total_seconds)], creationflags=subprocess.CREATE_NO_WINDOW)
            save_state(int(time.time())+total_seconds, total_seconds)
            window['-MSG-'].update('Zamanlayıcı aktif. Durum için Durum butonuna basın.')
        else:
            # absolute
            try:
                h = int(values['-HOURS-'] or 0)
                m = int(values['-MINUTES-'] or 0)
                if h < 0 or h > 23 or m < 0 or m > 59:
                    raise ValueError
                now = datetime.now()
                target = now.replace(hour=h, minute=m, second=0, microsecond=0)
                if target <= now:
                    target = target + timedelta(days=1)
                total_seconds = int((target-now).total_seconds())
            except Exception:
                window['-MSG-'].update('Lütfen saat ve dakika değerlerini doğru girin (örn 14 ve 30).')
                continue
            if values['-HOURS-'] == '' or values['-MINUTES-'] == '':
                window['-MSG-'].update('Tam saat ve dakika girin, örn 14 ve 30.')
                continue
            if len(values['-HOURS-']) > 2 or len(values['-MINUTES-']) > 2:
                window['-MSG-'].update('Saat ve dakika iki rakamdan uzun olamaz.')
                continue
            if values['-HOURS-'].startswith('0') and len(values['-HOURS-']) > 1:
                window['-MSG-'].update('Saat için 0 ön eki kullanmayın.')
                continue
            if values['-MINUTES-'].startswith('0') and len(values['-MINUTES-']) > 1:
                window['-MSG-'].update('Dakika için 0 ön eki kullanmayın.')
                continue
            subprocess.Popen(['shutdown', '-s', '-t', str(total_seconds)], creationflags=subprocess.CREATE_NO_WINDOW)
            save_state(int(time.time())+total_seconds, total_seconds)
            window['-MSG-'].update('Zamanlayıcı aktif.')
    if event == '-STATUS-':
        st = load_state()
        if not st:
            window['-MSG-'].update('Aktif bir zamanlayıcı yok.')
        else:
            dt = datetime.fromtimestamp(st['scheduled_at']).strftime('%Y-%m-%d %H:%M:%S')
            window['-MSG-'].update(f"Kapatılma zamanı: {dt} -- Kalan: {format_duration(st['remaining'])}")
    if event == '-CANCEL-':
        cancel_shutdown()
        remove_state()
        st = load_state()
        if st:
            window['-MSG-'].update('Zamanlayıcı hala var, lütfen konsolu kontrol edin.')
        else:
            window['-MSG-'].update('Zamanlayıcı iptal edildi. Artık aktif bir zamanlayıcı yok.')
            window['-INFO-'].update(f'Çalıştırılan dosya: {os.path.basename(__file__)}')

window.close()
