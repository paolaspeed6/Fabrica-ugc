"""Espera o tablet no cabo USB (até 2 h), confere bateria, ativa adb por Wi-Fi e grava aparelhos.json."""
import json, os, re, subprocess, sys, time

BASE = r'C:\horst\tablet'
ADB = os.path.join(BASE, 'platform-tools', 'adb.exe')
USB = '<SERIAL_TABLET>'
CFG = os.path.join(BASE, 'aparelhos.json')
NW = getattr(subprocess, 'CREATE_NO_WINDOW', 0)


def adb(*a, t=20):
    r = subprocess.run([ADB, *a], capture_output=True, text=True, timeout=t, creationflags=NW)
    return (r.stdout + r.stderr).strip()


fim = time.time() + 120 * 60
while time.time() < fim:
    if adb('-s', USB, 'get-state').endswith('device'):
        break
    time.sleep(10)
else:
    print('TIMEOUT: tablet não apareceu no USB em 2 h')
    sys.exit(2)
bat = re.search(r'level: (\d+)', adb('-s', USB, 'shell', 'dumpsys battery'))
nivel = int(bat[1]) if bat else -1
print('bateria', nivel)
if 0 <= nivel < 20:
    print('BATERIA_BAIXA')
    sys.exit(3)
ipinfo = adb('-s', USB, 'shell', 'ip -f inet addr show wlan0')
m = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', ipinfo)
if not m:
    print('SEM_WIFI: wlan0 sem IP —', ipinfo[:200])
    sys.exit(4)
ip = m[1]
print(adb('-s', USB, 'tcpip', '5555'))
time.sleep(4)
print(adb('connect', f'{ip}:5555'))
time.sleep(2)
ok = adb('-s', f'{ip}:5555', 'get-state').endswith('device')
print('wifi ok' if ok else 'wifi FALHOU', ip)
# fica acordado enquanto estiver na tomada (sem depender do scrcpy -w): se dormir, o adb Wi-Fi cai
print('stayon:', adb('-s', USB, 'shell', 'svc power stayon ac') or 'ok')
try:
    d = json.load(open(CFG, encoding='utf-8-sig'))
except Exception:
    d = {}
d.setdefault('tablet', {})
d['tablet'].update({'usb': USB, 'wifi': f'{ip}:5555'})
json.dump(d, open(CFG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('aparelhos.json:', json.dumps(d))
sys.exit(0 if ok else 5)

