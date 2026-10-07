"""Export the canvas .dc.html artboards to a static, self-contained prototype site."""
import re, shutil, pathlib, html as H

ROOT = pathlib.Path(__file__).parent.parent
SRC = ROOT / 'oly-canvas/project'
OUT = ROOT / 'site'
FONTS = ROOT / 'tools/node_modules/@fontsource/atkinson-hyperlegible/files'
LOGO = ROOT / 'logo/logo-oly-principal.png'
BLOB = '/_blob/f7b6a400732c3640baab415d48077e2f'

PAGES = [
    ('Accueil', 'accueil.html', 'Accueil'),
    ('Actualites', 'actualites.html', 'Nos Actualités'),
    ('Article', 'article.html', 'Article'),
    ('Page-A', 'page-a.html', 'Le diagnostic et parcours de soin (variante A)'),
    ('Page-B', 'page-b.html', 'Le diagnostic et parcours de soin (variante B)'),
    ('Don', 'don.html', 'Faire un don'),
    ('Main', 'systeme-de-design.html', 'Système de design'),
]

NAV = [
    ('noh', 'Les', 'NOH', '#E3F0FC', 'Tout savoir sur les NOH', ['Que sont ces maladies', 'Prévention', 'Le diagnostic et parcours de soin', 'Les traitements', 'La recherche']),
    ('vie', 'La vie en situation', 'de handicap visuel', '#E2F3EE', 'Toute la rubrique', ['Les démarches', 'Adapter son environnement', 'Les aidants', 'Les loisirs']),
    ('actions', 'Nos', 'Actions', '#FFE6E5', 'Toutes nos actions', ['La pair-aidance', 'Recherche', 'Plaidoyer', 'La ruche']),
    ('actus', 'Nos', 'Actualités', '#FFEBDD', 'Toutes les actualités', ['Internes', 'Externes']),
    ('partenaires', 'Nos', 'Partenaires', '#E3F0FC', 'Tous nos partenaires', ['Institutionnels', 'Entreprises', 'Associations', 'Fondations', 'Personnalités']),
    ('faq', 'Les Questions', 'Fréquentes', '#E2F3EE', 'Toutes les questions', ['Je suis malade', 'Je suis aidant', 'Je suis médecin']),
    ('boutique', 'Notre', 'boutique', '#FFE6E5', '', []),
]

# Link text -> destination. Anything else that points to "#" goes to a-venir.html.
LINKS = {
    'Faire un don': 'don.html', 'Accueil': 'accueil.html',
    'Nos Actualités': 'actualites.html', 'Toutes les actualités': 'actualites.html',
    'Internes': 'actualites.html', 'Externes': 'actualites.html', 'Toutes': 'actualites.html',
    'Le diagnostic et parcours de soin': 'page-a.html',
    'Français': '#', 'Page suivante': 'actualites.html', '2': 'actualites.html', '3': 'actualites.html', '1': 'actualites.html',
}

SCRIPT = """
<script>
(function () {
  var items = document.querySelectorAll('.nav-item');
  function closeAll(except) {
    items.forEach(function (li) {
      var b = li.querySelector('button.nav-btn');
      if (!b || li === except) return;
      b.setAttribute('aria-expanded', 'false');
      var p = document.getElementById(b.getAttribute('aria-controls'));
      if (p) p.hidden = true;
      li.style.background = li.dataset.bg;
      li.style.boxShadow = li.dataset.current ? 'inset 0 -5px 0 #1E2B3A' : 'none';
      if (li.dataset.current) li.style.background = '#CFE5FA';
      var s = b.querySelector('svg'); if (s) s.style.transform = 'none';
    });
  }
  items.forEach(function (li) {
    var b = li.querySelector('button.nav-btn');
    if (!b) return;
    b.addEventListener('click', function () {
      var open = b.getAttribute('aria-expanded') === 'true';
      closeAll(li);
      b.setAttribute('aria-expanded', open ? 'false' : 'true');
      var p = document.getElementById(b.getAttribute('aria-controls'));
      if (p) p.hidden = open;
      li.style.background = open && !li.dataset.current ? li.dataset.bg : '#CFE5FA';
      li.style.boxShadow = (!open || li.dataset.current) ? 'inset 0 -5px 0 #1E2B3A' : 'none';
      var s = b.querySelector('svg'); if (s) s.style.transform = open ? 'none' : 'rotate(180deg)';
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var openBtn = document.querySelector('button.nav-btn[aria-expanded="true"]');
    closeAll(null);
    if (openBtn) openBtn.focus();
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-item')) closeAll(null);
  });
  var t = document.querySelector('.menu-toggle'), nav = document.getElementById('menu-principal');
  if (t && nav) t.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    t.setAttribute('aria-expanded', open ? 'true' : 'false');
    t.querySelector('.mt-label').textContent = open ? 'Fermer le menu' : 'Menu';
    t.querySelector('.mt-open').hidden = open;
    t.querySelector('.mt-close').hidden = !open;
  });
})();
</script>
"""

PROTO = ('<nav aria-label="Prototype"><a href="index.html" class="proto-pill">Sommaire des maquettes</a></nav>'
         '<style>.proto-pill{position:fixed;left:16px;bottom:16px;z-index:50;display:inline-flex;align-items:center;'
         'min-height:44px;padding:8px 18px;border-radius:999px;background:#1E2B3A;color:#FFFFFF !important;font-weight:700;'
         'font-size:16px;text-decoration:none;box-shadow:0 4px 14px rgba(0,0,0,.25)}'
         '.proto-pill:hover{background:#0A5CB0}</style>')


def nav_html(current):
    out = []
    for i, l1, l2, bg, allx, subs in NAV:
        cur = current == i
        bgnow = '#CFE5FA' if cur else bg
        sh = 'inset 0 -5px 0 #1E2B3A' if cur else 'none'
        label = f'<span><span class="nl">{l1}</span> <span class="nl">{l2}</span></span>'
        attrs = f'class="nav-item" data-bg="{bg}"' + (' data-current="1"' if cur else '') + f' style="background: {bgnow}; box-shadow: {sh}"'
        if subs:
            links = ''.join(f'<li><a href="#" class="nav-sublink">{s}</a></li>' for s in subs)
            out.append(f'<li {attrs}><button type="button" class="nav-btn" aria-expanded="false" aria-controls="panel-{i}">{label}'
                       '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0"><path d="m6 9 6 6 6-6"/></svg></button>'
                       f'<ul id="panel-{i}" class="nav-panel" hidden><li><a href="#" class="nav-all">{allx}</a></li>{links}</ul></li>')
        else:
            out.append(f'<li {attrs}><a href="#" class="nav-btn">{label}</a></li>')
    return ''.join(out)


def relink(page):
    def fix(m):
        tag, inner = m.group(1), m.group(2)
        if 'href="#"' not in tag:
            return m.group(0)
        text = re.sub(r'<[^>]+>', ' ', inner)
        text = H.unescape(re.sub(r'\s+', ' ', text)).strip()
        if 'logo-slot' in tag:
            dest = 'accueil.html'
        elif "Lire l'article" in text:
            dest = 'article.html'
        elif text in LINKS:
            dest = LINKS[text]
        else:
            dest = 'a-venir.html'
        return '<a' + tag.replace('href="#"', f'href="{dest}"') + '>' + inner + '</a>'
    return re.sub(r'<a(\s[^>]*)>(.*?)</a>', fix, page, flags=re.S)


def export(stem, out_name, title):
    src = (SRC / f'{stem}.dc.html').read_text(encoding='utf-8')
    cur = re.search(r"var CURRENT = '(\w*)'", src)
    current = cur.group(1) if cur else ''
    helmet = re.search(r'<helmet>(.*?)</helmet>', src, re.S).group(1)
    helmet = re.sub(r'<link[^>]*fonts\.g[^>]*>\s*', '', helmet)
    face = ''.join(f"@font-face{{font-family:'Atkinson Hyperlegible';font-weight:{w};font-display:swap;src:url('fonts/atkinson-{w}.woff2') format('woff2')}}" for w in (400, 700))
    face += "[hidden]{display:none !important}"
    helmet = helmet.replace('<style>', '<style>' + face, 1)
    body = re.search(r'<x-dc>.*?</helmet>(.*)</x-dc>', src, re.S).group(1)
    body = re.sub(r'<sc-for list="\{\{items\}\}".*?</sc-for>\s*(?=</ul>\s*</nav>)', lambda m: nav_html(current), body, flags=re.S)
    body = re.sub(r'<sc-if value="\{\{mobileClosed\}\}"[^>]*>(.*?)</sc-if>', lambda m: m.group(1).replace('<svg', '<svg class="mt-open"', 1), body, flags=re.S)
    body = re.sub(r'<sc-if value="\{\{mobileOpen\}\}"[^>]*>(.*?)</sc-if>', lambda m: m.group(1).replace('<svg', '<svg class="mt-close" hidden', 1), body, flags=re.S)
    body = body.replace('{{menuLabel}}', '<span class="mt-label">Menu</span>')
    body = body.replace('{{menuExpanded}}', 'false').replace(' {{navOpenClass}}', '')
    body = re.sub(r'\s*onClick="\{\{[^}]*\}\}"', '', body)
    body = body.replace(BLOB, 'img/logo-oly.png')
    body = body.replace(' class="hide-t"', '')
    left = re.findall(r'\{\{[^}]*\}\}|<sc-', body)
    assert not left, (stem, set(left))
    if stem != 'Main':
        body = relink(body)
        script = SCRIPT
    else:
        script = ''
    page = (f'<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<meta name="robots" content="noindex, nofollow">\n'
            f'<title>{title} — Maquette OLY</title>\n<link rel="icon" href="img/favicon.png">\n{helmet}\n</head>\n<body>\n{body}\n{PROTO}\n{script}</body>\n</html>\n')
    (OUT / out_name).write_text(page, encoding='utf-8')


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / 'fonts').mkdir(parents=True)
    (OUT / 'img').mkdir()
    for w in (400, 700):
        shutil.copy(FONTS / f'atkinson-hyperlegible-latin-{w}-normal.woff2', OUT / f'fonts/atkinson-{w}.woff2')
    shutil.copy(LOGO, OUT / 'img/logo-oly.png')
    from PIL import Image
    logo = Image.open(LOGO)
    w, h = logo.size
    icon = logo.crop((0, 0, int(h * 0.98), h))
    side = max(icon.size)
    sq = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    sq.paste(icon, ((side - icon.size[0]) // 2, (side - icon.size[1]) // 2))
    sq.resize((64, 64), Image.LANCZOS).save(OUT / 'img/favicon.png')
    for stem, name, title in PAGES:
        export(stem, name, title)
    for f in (ROOT / 'tools/static').iterdir():
        shutil.copy(f, OUT / f.name)
    (OUT / '.nojekyll').write_text('')
    print('exported', sorted(p.name for p in OUT.iterdir()))


if __name__ == '__main__':
    main()
