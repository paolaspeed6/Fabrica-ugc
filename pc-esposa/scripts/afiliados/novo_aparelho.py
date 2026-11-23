"""Espera um aparelho NOVO no USB (serial diferente do tablet), mostra modelo/Android/tela,
ativa adb por Wi-Fi (tcpip 5555) e grava em aparelhos.json como 'celular1' (ou 'celular2').
Não muda nenhuma configuração do aparelho além do modo tcpip do adb."""
import json, os, re, subprocess, sys, time

BASE = r'C:\horst\tablet'
ADB = os.path.join(BASE, 'platform-tools', 'adb.exe')
CFG = os.path.join(BASE, 'aparelhos.json')
TABLET = '<SERIAL_TABLET>'
NW = getattr(subprocess, 'CREATE_NO_WINDOW', 0)


def adb(*a, t=20):
    try:
        r = subprocess.run([ADB, *a], capture_output=True, text=True, timeout=t, creationflags=NW)
        return (r.stdout + r.stderr).strip()
    except Exception as e:
        return f'ERRO {e}'


def conhecidos():
    try:
        d = json.load(open(CFG, encoding='utf-8-sig'))
    except Exception:
        d = {}
    s = {TABLET}
    for v in d.values():
        if isinstance(v, dict):
            s.update(x for x in (v.get('usb'), v.get('wifi')) if x)
    return d, s


fim = time.time() + 3 * 3600
while time.time() < fim:
    d, s = conhecidos()
    lista = [l.split() for l in adb('devices').splitlines()[1:] if l.strip()]
    novo = next((x for x in lista if x[0] not in s and ':' not in x[0]), None)
    if novo:
        serial, estado = novo[0], novo[1]
        if estado == 'unauthorized':
            print(f'{serial}: NÃO AUTORIZADO — aceite "Permitir depuração USB" na tela do celular', flush=True)
            time.sleep(5)
            continue
        if estado != 'device':
            time.sleep(5)
            continue
        info = {k: adb('-s', serial, 'shell', f'getprop {p}') for k, p in
                (('modelo', 'ro.product.model'), ('marca', 'ro.product.brand'),
                 ('android', 'ro.build.version.release'), ('sdk', 'ro.build.version.sdk'))}
        info['tela'] = adb('-s', serial, 'shell', 'wm size')
        info['densidade'] = adb('-s', serial, 'shell', 'wm density')
        info['bateria'] = re.findall(r'(level|AC powered|USB powered): (\S+)', adb('-s', serial, 'shell', 'dumpsys battery'))
        info['shopee'] = 'instalada' if 'com.shopee.br' in adb('-s', serial, 'shell', 'pm list packages com.shopee.br') else 'NÃO instalada'
        m = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', adb('-s', serial, 'shell', 'ip -f inet addr show wlan0'))
        wifi = None
        if m:
            adb('-s', serial, 'tcpip', '5555')
            time.sleep(4)
            adb('connect', f'{m[1]}:5555')
            time.sleep(2)
            if adb('-s', f'{m[1]}:5555', 'get-state').endswith('device'):
                wifi = f'{m[1]}:5555'
        nome = 'celular1' if 'celular1' not in d else 'celular2'
        d[nome] = {'usb': serial, 'wifi': wifi, 'modelo': info['modelo'], 'android': info['android']}
        json.dump(d, open(CFG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(json.dumps({'nome': nome, 'serial': serial, 'wifi': wifi, **info}, ensure_ascii=False), flush=True)
        sys.exit(0)
    time.sleep(10)
print('TIMEOUT: nenhum aparelho novo em 3 h')
sys.exit(2)
