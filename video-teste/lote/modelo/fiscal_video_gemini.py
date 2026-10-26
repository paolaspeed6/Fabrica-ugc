"""Fiscal de vídeo (trava 3) pelo Gemini, grátis, no lugar do subagente (a dona, 26/10: economizar o uso do Claude).
Manda a imagem de partida + o clipe (mp4) e pede o trecho limpo. Saída no formato do aprovar.py: pNN-cenas/fiscal_video.json
{"A": {"veredito": "usar 0.0-3.0s", "inicio": 0.0, "fim": 3.0, "defeitos": [...]}} (mescla). Depois: python3 -I aprovar.py pNN ...
uso: python3 -I fiscal_video_gemini.py p01A,p01B,...   (MODELO=... troca o modelo; padrão o mesmo do fiscal_gemini.py)"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fiscal_gemini as G
from fiscal_gemini import B, b64, chamar

PEDIDO = """Você é a FISCAL DE VÍDEO de uma fábrica de vídeos de produtos da Shopee. A 1ª mídia é a IMAGEM DE PARTIDA (aprovada), a 2ª é
o CLIPE de 5 s gerado a partir dela. Assista o clipe inteiro e diga de qual segundo a qual segundo ele está LIMPO. Fica sujo a partir do momento em que:
o produto escorrega, gira, derrete, muda de forma, ganha ou perde peça, muda de cor; letras do produto mudam ou entortam; tela/painel acende;
surge objeto novo (garrafa, copo, vaso, pessoa, mão, bebê, animal); o produto é cortado pela borda; corte de cena ou transição; câmera treme feio.
Câmera parada demais também é defeito leve (anote). Um trecho limpo de 2 s já serve.
Responda SÓ um JSON: {"inicio": número em segundos (normalmente 0), "fim": número em segundos (fim do trecho limpo; 0 se nada presta),
"defeitos": ["o que acontece e em que segundo, em português, curto"], "nota": "nota de 0 a 10 para a beleza e o movimento"}"""

if __name__ == '__main__':
    for pk in sys.argv[1].split(','):
        p, k = pk[:3], pk[3:]; d = B / f'{p}-cenas'
        mp4 = d / f'{k}_fixa.mp4' if (d / f'{k}_fixa.mp4').exists() else d / f'{k}.mp4'
        if not mp4.exists() or not (d / f'{k}.jpg').exists(): print(pk, 'SEM CLIPE'); continue
        try: v = chamar([{'text': PEDIDO}, {'inline_data': {'mime_type': 'image/jpeg', 'data': b64(d / f'{k}.jpg')}},
                    {'inline_data': {'mime_type': 'video/mp4', 'data': b64(mp4)}}])
        except Exception as e: print(pk, 'FALHOU', e, flush=True); continue
        ini, fim = float(v.get('inicio') or 0), min(float(v.get('fim') or 0), 5.0)
        v.update(inicio=ini, fim=fim, veredito=f'usar {ini:.1f}-{fim:.1f}s' if fim - ini >= 1.5 else 'REPROVADO', fiscal=f'gemini ({G.MOD})')
        fj = d / 'fiscal_video.json'; dd = json.loads(fj.read_text()) if fj.exists() else {}
        dd[k] = v; fj.write_text(json.dumps(dd, ensure_ascii=False, indent=1))
        print(pk, v['veredito'], '|', '; '.join(v.get('defeitos') or [])[:150], flush=True)
