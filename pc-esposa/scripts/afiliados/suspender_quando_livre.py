r"""Põe o PC em ESPERA quando TODOS os trabalhos acabarem (pedido do Kevin, 05/11).
Confere a cada 3 min com suspender.pode_suspender() (fila de postagem, render/voz do YouTube, outro
python, download, Drive sincronizando). Não desiste por causa de outro trabalho: espera ele terminar.
Chave para desligar: afiliados\NAO_SUSPENDER. Log: afiliados\suspender_quando_livre.log
"""
import datetime, os, sys, time

PASTA = r'C:\horst\tablet\afiliados'
sys.path.insert(0, PASTA)
import suspender  # noqa: E402

LOG = os.path.join(PASTA, 'suspender_quando_livre.log')


def log(m):
    linha = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {m}'
    print(linha, flush=True)
    open(LOG, 'a', encoding='utf-8').write(linha + '\n')


def main():
    log('esperando todos os trabalhos acabarem para pôr o PC em espera (confere a cada 3 min)')
    ultimo = None
    while True:
        if os.path.exists(suspender.CHAVE):
            log('NAO_SUSPENDER encontrado: não suspendo e saio')
            return
        ok, motivo = suspender.pode_suspender()
        if ok:
            resumo = os.path.join(r'C:\horst\tablet\central', 'resumo_antes_de_suspender.txt')
            open(resumo, 'a', encoding='utf-8').write(
                f'{datetime.datetime.now():%d/%m %H:%M} PC em espera: conferência parada em 100 aprovados; '
                'postagem não rodou (ensaio seco no celular parou na permissão de câmera; ver '
                'central\\calibracao_postagem_celular1.md)\n')
            log('nada rodando: PC em espera agora')
            r = suspender.suspender()
            log(f'PC voltou da espera ({r}); nada é religado sozinho')
            return
        if motivo != ultimo:
            log(f'ainda não: {motivo}')
            ultimo = motivo
        time.sleep(180)


if __name__ == '__main__':
    main()
