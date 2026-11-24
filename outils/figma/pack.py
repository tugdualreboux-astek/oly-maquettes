"""Packs extracted pages + renderer into use_figma scripts (≤ 50 000 characters each)."""
import json, re, sys, pathlib
FIG = pathlib.Path(sys.argv[1]); OUT = FIG / 'calls'
R = (pathlib.Path(__file__).parent / 'renderer.js').read_text()
R = '\n'.join(l.strip() for l in R.splitlines() if l.strip() and not l.strip().startswith('//'))
D, M = 'Ordinateur — 1440', 'Mobile — 390'
CALLS = [
 ('D1', True, D, [('accueil', 'Accueil'), ('contact', 'Nous contacter')]),
 ('D2', False, D, [('accueil-menu', 'Accueil — sous-menu ouvert'), ('les-noh', 'Page de rubrique — Les NOH')]),
 ('D3', False, D, [('page-a', 'Page de contenu — étapes et téléchargements'), ('don', 'Faire un don')]),
 ('D4', False, D, [('actualites', 'Nos Actualités — liste'), ('faq-aidant', 'Questions fréquentes')]),
 ('D5', False, D, [('article', 'Article'), ('partenaires-entreprises', 'Partenaires')]),
 ('D6', False, D, [('page-b', 'Page de contenu — colonne latérale'), ('agenda', 'Agenda')]),
 ('M1', False, M, [('accueil', 'Accueil'), ('les-noh', 'Page de rubrique — Les NOH'), ('contact', 'Nous contacter')]),
 ('M2', False, M, [('accueil-mobilemenu', 'Accueil — menu ouvert'), ('don', 'Faire un don')]),
 ('M3', False, M, [('page-a', 'Page de contenu'), ('actualites', 'Nos Actualités — liste')]),
 ('M4', False, M, [('article', 'Article'), ('faq-aidant', 'Questions fréquentes')]),
]
for cid, setup, page, items in CALLS:
    w = '1440' if page == D else '390'
    data = [{'n': f'{label} — {"Ordinateur" if w == "1440" else "Mobile"}', 'd': json.load(open(FIG / f'{f}-{w}.json'))} for f, label in items]
    code = f'const SETUP={str(setup).lower()};const PAGE={json.dumps(page, ensure_ascii=False)};const DATA={json.dumps(data, ensure_ascii=False, separators=(",", ":"))};\n' + R
    (OUT / f'{cid}.js').write_text(code)
    print(cid, len(code), 'chars', len(code.encode()), 'bytes')
