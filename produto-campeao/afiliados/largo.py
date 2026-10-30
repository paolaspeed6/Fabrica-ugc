"""Produto largo ou kit comprido: a IA enche o quadro vertical e corta as pontas (motivo nº 1 de desperdício, 27-29/10:
mesa em L, kit 2 poltronas + puff, colchão, cabeceira + recamier, espreguiçadeiras, aparador de cerca). O Tinder mostra o selo
para a dona decidir antes do lote. uso: from largo import largo; largo(nome) -> True/False"""
import re
_R = re.compile(r'\bkit\s*(?:com\s*)?(?:\d+|dois|tr[eê]s|quatro|seis)\b|\bconjunto\b|\bjogo de (?:cadeiras|banquetas|poltronas)\b'
                r'|mesa em l\b|\bcolch[aã]o\b|(?<!mesa de )\bcabeceira\b|\brecamier\b|\bespregui[cç]adeira|\bsof[aá]\b|\bchaise\b'
                r'|\bcama (?:box|casal|queen|king)\b|\bbeliche\b|aparador (?:de )?(?:cerca|grama)|\bcozinha (?:modulada|compacta|completa)\b'
                r'|\bguarda[- ]roupa\b|\bhome theater\b|\brack\b.*\b(?:1[5-9]\d|2\d\d) ?cm', re.I)
def largo(nome): return bool(_R.search(nome or ''))
