"""Packs extracted pages into use_figma scripts (≤ 50 000 characters each).
Header and footer become shared components (built once in the first call); pages reference them with {k: name}.
Usage: python3 pack.py <dir with <page>-<width>.json> <out dir>"""
import json, sys, pathlib
SRC, OUT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
R = (pathlib.Path(__file__).parent / 'renderer.js').read_text()
R = '\n'.join(l.strip() for l in R.splitlines() if l.strip() and not l.strip().startswith('//'))
D, M = 'Ordinateur — 1440', 'Mobile — 390'
LBL = {'1440': 'Ordinateur', '390': 'Mobile'}

def load(name, w):
    d = json.load(open(SRC / f'{name}-{w}.json'))
    kids = d['tree'][0]['c'] if len(d['tree']) == 1 and d['tree'][0].get('w') == d['w'] else d['tree']
    return d, kids

def subset(nodes, svgs):
    """Re-index the SVGs used by these nodes."""
    used, out = {}, []
    def walk(n):
        if 'v' in n:
            if n['v'] not in used: used[n['v']] = len(out); out.append(svgs[n['v']])
            n['v'] = used[n['v']]
        for c in n.get('c', []): walk(c)
    for n in nodes: walk(n)
    return out

def page(name, w, label, only_header=None):
    d, kids = load(name, w)
    tree = []
    for k in kids:
        tag = k.get('f', '').split('.')[0].split(' ')[0]
        if tag == 'header': tree.append({'k': only_header or f'En-tête — {LBL[w]}', 'x': k['x'], 'y': k['y']})
        elif tag == 'footer': tree.append({'k': f'Pied de page — {LBL[w]}', 'x': k['x'], 'y': k['y']})
        else: tree.append(k)
    h = d['h']
    if only_header:  # menu-open views: header instance only, cropped below the open menu
        tree = [t for t in tree if t.get('k') == only_header]
        h = 900 if w == '1440' else 1100
    return {'n': f'{label} — {LBL[w]}', 'd': {'w': d['w'], 'h': h, 'bg': d['bg'], 'svgs': subset(tree, d['svgs']), 'tree': tree}}

def comp(name, w, tag, label):
    d, kids = load(name, w)
    node = next(k for k in kids if k.get('f', '').startswith(tag))
    node = json.loads(json.dumps(node)); node['x'] = 0; node['y'] = 0
    return {'n': label, 'd': {'w': d['w'], 'h': node['h'], 'svgs': subset([node], d['svgs']), 'tree': [node]}}

COMPS = [comp('accueil', '1440', 'header', 'En-tête — Ordinateur'), comp('accueil', '1440', 'footer', 'Pied de page — Ordinateur'),
         comp('accueil-menu', '1440', 'header', 'En-tête — sous-menu ouvert — Ordinateur'),
         comp('accueil', '390', 'header', 'En-tête — Mobile'), comp('accueil', '390', 'footer', 'Pied de page — Mobile'),
         comp('accueil-mobilemenu', '390', 'header', 'En-tête — menu ouvert — Mobile')]
CALLS = [
 ('C1', True, D, COMPS, [('Navigation et pages d\'entrée', [('accueil-menu', 'Menu — sous-menu ouvert', 'En-tête — sous-menu ouvert — Ordinateur'), ('les-noh', 'Page de rubrique (Les NOH)', None), ('contact', 'Nous contacter', None)]),
                               ('Agenda et page à colonne', [('page-b', 'Page de contenu avec colonne latérale', None), ('agenda', 'Agenda', None)])]),
 ('C2', False, D, [], [('Accueil, contenu et don', [('accueil', 'Accueil', None), ('page-a', 'Page de contenu (étapes, téléchargements)', None), ('don', 'Faire un don', None)])]),
 ('C3', False, D, [], [('Actualités, FAQ et partenaires', [('actualites', 'Nos Actualités (liste)', None), ('article', 'Article', None), ('faq-aidant', 'Questions fréquentes', None), ('partenaires-entreprises', 'Partenaires', None)])]),
 ('C5', False, M, [], [('Accueil, navigation et pages d\'entrée', [('accueil', 'Accueil', None), ('accueil-mobilemenu', 'Menu ouvert', 'En-tête — menu ouvert — Mobile'), ('les-noh', 'Page de rubrique (Les NOH)', None), ('contact', 'Nous contacter', None), ('don', 'Faire un don', None)])]),
 ('C6', False, M, [], [('Contenu, actualités, FAQ et partenaires', [('page-a', 'Page de contenu (étapes, téléchargements)', None), ('actualites', 'Nos Actualités (liste)', None), ('faq-aidant', 'Questions fréquentes', None), ('partenaires-entreprises', 'Partenaires', None)])]),
 ('C7', False, M, [], [('Article, agenda et page à colonne', [('article', 'Article', None), ('agenda', 'Agenda', None), ('page-b', 'Page de contenu avec colonne latérale', None)])]),
]
def encode(tree, ST):
    """Positional arrays + shared text-style table, decoded by renderer.js (dec)."""
    def st(sv):
        k = json.dumps(sv)
        if k not in ST: ST[k] = len(ST)
        return ST[k]
    def e(n):
        if 'k' in n: return [4, n['k'], n['x'], n['y']]
        if 'i' in n: return [3, n['x'], n['y'], n['w'], n['h']]
        if 'v' in n: return [2, n['v'], n['x'], n['y'], n['w'], n['h']]
        if 't' in n:
            a = [1, n['t'], n['x'], n['y'], n['w'], round(n['h']), st(n['s'])]
            if n.get('runs'): a.append(n['runs'])
            return a
        return [0, n['f'], n['x'], n['y'], n['w'], n['h'], n.get('bg') or 0, n.get('r', 0), n.get('b', 0), n.get('sh', 0), n.get('clip', 0), [e(c) for c in n.get('c', [])]]
    return [e(n) for n in tree]

OUT.mkdir(exist_ok=True)
for cid, setup, pg, comps, secs in CALLS:
    w = '1440' if pg == D else '390'
    ST = {}
    data = [{'sec': s, 'items': [page(n, w, l, oh) for n, l, oh in items]} for s, items in secs]
    for blk in [c['d'] for c in comps] + [it['d'] for sec in data for it in sec['items']]:
        blk['tree'] = encode(blk['tree'], ST)
    j = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
    st_list = [json.loads(k) for k in sorted(ST, key=ST.get)]
    code = f'const SETUP={str(setup).lower()};const PAGE={j(pg)};const ST={j(st_list)};const COMPS={j(comps)};const SECS={j(data)};\n' + R
    (OUT / f'{cid}.js').write_text(code)
    print(cid, len(code))
