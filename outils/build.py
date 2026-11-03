"""Build the OLY prototype site.

1. Exports the reference artboards (outils/canvas/*.dc.html, from the Claude canvas « Maquettes OLY ») to static pages.
2. Generates every other page of the site map (outils/pages.py) from the content corpus of the current site.

Usage: python3 outils/build.py /path/to/Corpus_contenus_OLY.md
Output is written at the repository root (GitHub Pages serves it as is).
"""
import re, sys, html as H, pathlib
import markdown

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pages import RUBRIQUES, PAGES, PARTNERS, FAQ, LANDINGS, LINKS, BOLD_HEADINGS, LINK_TEXT_FIXES

REPO = pathlib.Path(__file__).parent.parent
SRC = REPO / 'outils/canvas'
STATIC = REPO / 'outils/static'
BLOB = '/_blob/f7b6a400732c3640baab415d48077e2f'

CANVAS_PAGES = [
    ('Accueil', 'accueil.html', 'Accueil'),
    ('Actualites', 'actualites.html', 'Nos Actualités'),
    ('Article', 'article.html', "Prix Espoir d'OLY"),
    ('Page-A', 'page-a.html', 'Le diagnostic et parcours de soin'),
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

SCRIPT = """
<script>
(function () {
  var items = document.querySelectorAll('.nav-item');
  function paint(li, open) {
    var hl = open || li.dataset.current;
    li.style.background = hl ? '#CFE5FA' : li.dataset.bg;
    li.style.boxShadow = hl ? 'inset 0 -5px 0 #1E2B3A' : 'none';
    var s = li.querySelector('.nav-ind'); if (s) s.textContent = open ? '\\u2212' : '+';
  }
  function closeAll(except) {
    items.forEach(function (li) {
      var b = li.querySelector('button.nav-btn');
      if (!b || li === except) return;
      b.setAttribute('aria-expanded', 'false');
      var p = document.getElementById(b.getAttribute('aria-controls'));
      if (p) p.hidden = true;
      paint(li, false);
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
      paint(li, !open);
    });
  });
  var t = document.querySelector('.menu-toggle'), nav = document.getElementById('menu-principal');
  function setMobile(open) {
    nav.classList.toggle('is-open', open);
    t.setAttribute('aria-expanded', open ? 'true' : 'false');
    t.querySelector('.mt-label').textContent = open ? 'Fermer le menu' : 'Menu';
    t.querySelector('.mt-open').hidden = open;
    t.querySelector('.mt-close').hidden = !open;
  }
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var openBtn = document.querySelector('button.nav-btn[aria-expanded="true"]');
    if (openBtn) { closeAll(null); openBtn.focus(); return; }
    // Mobile menu: Escape closes it and gives the focus back to the « Menu » button.
    if (t && nav && nav.classList.contains('is-open') && getComputedStyle(t).display !== 'none') { setMobile(false); t.focus(); }
  });
  var copy = document.getElementById('copy-link'), status = document.getElementById('copy-status');
  if (copy && status) copy.addEventListener('click', function () {
    var done = function () { status.textContent = 'Lien copié'; setTimeout(function () { status.textContent = ''; }, 4000); };
    if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(done, done); else done();
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-item')) closeAll(null);
  });
  if (t && nav) t.addEventListener('click', function () { setMobile(!nav.classList.contains('is-open')); });
})();
</script>
"""

PROTO = ('<nav aria-label="Prototype" class="proto-bar"><span>Maquette de travail, non contractuelle</span>'
         '<a href="index.html">Sommaire des maquettes</a></nav>')
# Styles of the prototype bar: in <head> (RGAA 8.2, <style> is not allowed in <body>).
PROTO_CSS = ("<style>.proto-bar{display:flex;flex-wrap:wrap;gap:4px 20px;justify-content:center;align-items:center;padding:8px 20px;"
         "background:#1E2B3A;color:#FFFFFF;font-family:'Atkinson Hyperlegible',system-ui,sans-serif;font-size:16px;line-height:1.4}"
         '.proto-bar a{color:#FFFFFF;font-weight:700;text-decoration:underline;text-underline-offset:3px;min-height:32px;display:inline-flex;align-items:center}'
         '.proto-bar a:hover{color:#CFE5FA}.proto-bar a:focus-visible{outline:3px solid #FFFFFF;outline-offset:2px}</style>')

# Extra styles for generated pages (cards, partners, FAQ, forms, tables).
EXTRA_CSS = """<style>
.lp-grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.lp-card{display:flex;flex-direction:column;gap:10px;height:100%;padding:26px;border-radius:18px;text-decoration:none;color:#1E2B3A;box-shadow:0 2px 12px rgba(30,43,58,.08)}
.lp-card:hover{color:#1E2B3A;box-shadow:0 6px 20px rgba(30,43,58,.16)}
.lp-card strong{font-size:23px;line-height:1.3}
.lp-go{margin-top:auto;color:#0A5CB0;font-weight:700;text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:2px}
.note-proto{display:flex;gap:12px;align-items:flex-start;margin-top:8px;padding:12px 16px;background:#FFFFFF;border-radius:12px;font-size:16px;max-width:52em}
.pt-grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.pt-card{display:flex;flex-direction:column;gap:10px;height:100%;padding:22px;border-radius:16px;background:#FFFFFF;box-shadow:0 2px 12px rgba(30,43,58,.08)}
.pt-logo{height:96px;border-radius:12px;background:#F1F3F5;border:2px dashed #767676;display:flex;align-items:center;justify-content:center;font-size:16px;text-align:center;padding:8px}
.faq-toc{margin:0 0 32px;padding:20px 24px;background:#FFFFFF;border-radius:16px}
.faq-toc ol{margin:0;padding-left:1.4em}
.faq-toc li{margin:6px 0}
.faq-item{background:#FFFFFF;border-radius:16px;margin-bottom:16px;padding:22px 24px;box-shadow:0 2px 12px rgba(30,43,58,.06)}
.faq-item h2{font-size:22px;line-height:1.35;color:#1E2B3A;margin:0 0 10px}
.faq-item p:last-child{margin-bottom:0}
.fld{display:flex;flex-direction:column;gap:8px;margin-bottom:18px}
.fld label{font-weight:700}
.fld input,.fld textarea,.fld select{border:2px solid #767676;border-radius:12px;padding:12px 16px;font:inherit;color:#1E2B3A;background:#FFFFFF}
.fld input,.fld select{height:56px}
.prose table{border-collapse:collapse;width:100%;margin:0 0 24px;font-size:17px}
.prose th,.prose td{border:1px solid #B8C0CA;padding:10px 12px;text-align:left;vertical-align:top}
.prose th{background:#E3F0FC}
.prose blockquote{margin:24px 0;padding:18px 22px;background:#E3F0FC;border-left:6px solid #006FD6;border-radius:0 12px 12px 0}
.prose img{max-width:100%}
.prose a,.prose p,.prose li,.prose td{overflow-wrap:anywhere}
.table-wrap{overflow-x:auto;margin:0 0 24px;border-radius:8px}
.prose caption{text-align:left;font-weight:700;padding:0 0 8px}
.citation{font-size:22px;font-weight:700}
.citation q{quotes:"« " " »";font-style:italic}
.citation-source{font-weight:400;font-size:18px}
.table-wrap table{margin:0;min-width:560px}
.fld input,.fld textarea,.fld select{width:100%;min-width:0}
.two-col{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr);gap:56px;align-items:start}
@media (max-width:1100px){.lp-grid,.pt-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.two-col{grid-template-columns:minmax(0,1fr);gap:32px}}
@media (max-width:760px){.lp-grid,.pt-grid{grid-template-columns:1fr}}
</style>"""


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
                       '<span class="nav-ind" aria-hidden="true">+</span></button>'
                       f'<ul id="panel-{i}" class="nav-panel" hidden><li><a href="#" class="nav-all">{allx}</a></li>{links}</ul></li>')
        else:
            out.append(f'<li {attrs}><a href="#" class="nav-btn">{label}</a></li>')
    return ''.join(out)


def relink(page, current_file=None):
    def fix(m):
        tag, inner = m.group(1), m.group(2)
        if 'href="#"' not in tag:
            return m.group(0)
        out = _fix(tag, inner)
        # Sub-menu link of the page being displayed: aria-current="page".
        if current_file and f'href="{current_file}"' in out and ('nav-sublink' in tag or 'nav-all' in tag):
            out = out.replace('<a ', '<a aria-current="page" ', 1)
        return out

    def _fix(tag, inner):
        text = H.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', inner))).strip()
        for suffix in (' Lire la page', ' Voir la page'):
            if text.endswith(suffix):
                text = text[:-len(suffix)].strip()
        if 'logo-slot' in tag:
            dest = 'accueil.html'
        elif "Lire l'article" in text:
            dest = 'article.html'
        elif '[Horaire]' in text:
            dest = 'agenda.html'
        elif text in LINKS:
            dest = LINKS[text]
        else:
            dest = next((LINKS[k] for k in sorted(LINKS, key=len, reverse=True) if len(k) > 6 and text.endswith(k)), 'a-venir.html')
        if text == 'Français':
            return '<a' + tag + '>' + inner + '</a>'
        return '<a' + tag.replace('href="#"', f'href="{dest}"') + '>' + inner + '</a>'
    return re.sub(r'<a(\s[^>]*)>(.*?)</a>', fix, page, flags=re.S)


def page_shell(title, body, helmet, extra_head=''):
    return (f'<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<meta name="robots" content="noindex, nofollow">\n'
            f'<title>{H.escape(title)} — Maquette OLY</title>\n<link rel="icon" href="img/favicon.png">\n{helmet}\n{extra_head}\n{PROTO_CSS}\n</head>\n<body>\n{PROTO}\n{body}\n{SCRIPT}</body>\n</html>\n')


def export_canvas(stem):
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
    body = body.replace(BLOB, 'img/logo-oly.png').replace(' class="hide-t"', '')
    left = re.findall(r'\{\{[^}]*\}\}|<sc-', body)
    assert not left, (stem, set(left))
    return helmet, body


# ---------------------------------------------------------------- corpus

class Corpus:
    def __init__(self, path):
        self.lines = pathlib.Path(path).read_text(encoding='utf-8').split('\n')
        # old-site URL -> line where its section starts
        self.urls = {}
        for i, l in enumerate(self.lines, 1):
            m = re.match(r'- \*\*URL :\*\* (\S+)', l)
            if m:
                self.urls[m.group(1).rstrip('/')] = i

    def md(self, a, b):
        out = []
        for l in self.lines[a - 1:b]:
            s = l.strip()
            if re.match(r'- \*\*(URL|Dernière modification|Note de lecture) :\*\*', s) or s.startswith('**Sommaire') or s == '---' or re.match(r'#{1,2} ', s):
                continue
            out.append(l)
        return '\n'.join(out).strip()


BOLD_LINE = re.compile(r'^\*\*([^*].*?)\*\*\s*[:.]?\s*$')
ROMAN = re.compile(r'^[IVX]+\s*-')
ARABIC = re.compile(r'^\d+\s*-')


def bold_to_headings(text, base):
    """Turn standalone bold lines that introduce a block into headings (RGAA 9.1).

    base = level of the heading that owns this part. Roman-numbered lines (« I- … ») sit one level below
    the current real heading, arabic-numbered lines (« 1- … ») one level below the last roman one,
    other bold lines one level below the current heading."""
    lines = text.split('\n')
    current = base          # level of the last real heading
    roman = None            # level of the last roman-numbered heading under it
    out = []
    for i, l in enumerate(lines):
        m = re.match(r'^(#{1,6}) ', l)
        if m:
            current, roman = len(m.group(1)), None
            out.append(l)
            continue
        b = BOLD_LINE.match(l.strip())
        nxt = next((x.strip() for x in lines[i + 1:] if x.strip()), '')
        if b and len(b.group(1)) <= 140 and not re.match(r'^[–-]', b.group(1)) and nxt and not nxt.startswith('#'):
            label = re.sub(r'\s*[:.]\s*$', '', b.group(1).strip())
            if ROMAN.match(label):
                lvl = current + 1
                roman = lvl
            elif ARABIC.match(label):
                lvl = (roman or current) + 1
            else:
                lvl = (roman or current) + 1
            out.append('#' * min(6, lvl) + ' ' + label)
            continue
        out.append(l)
    return '\n'.join(out)


def md_to_html(text, top, bold_headings=False):
    """Convert corpus markdown; the shallowest heading of the part becomes h<top>."""
    levels = [len(m) for m in re.findall(r'^(#{3,6}) ', text, re.M)]
    if levels:
        shift = top - min(levels)
        text = re.sub(r'^(#{3,6}) ', lambda m: '#' * max(1, min(6, len(m.group(1)) + shift)) + ' ', text, flags=re.M)
    if bold_headings:
        text = bold_to_headings(text, top - 1)
    out = markdown.markdown(text, extensions=['tables', 'sane_lists', 'nl2br', 'toc'])
    # Data tables: column headers with scope (RGAA 5.7), caption when the table is known, scrollable container.
    out = re.sub(r'<th(?=[\s>])(?![^>]*scope)', '<th scope="col"', out)

    def wrap(m):
        t = m.group(1)
        cap = '<caption>Cookies utilisés sur le site</caption>' if 'Nom du cookie' in t else ''
        return f'<div class="table-wrap" role="region" aria-label="Tableau, faire défiler horizontalement" tabindex="0"><table>{cap}{t}</table></div>'
    out = re.sub(r'<table>(.*?)</table>', wrap, out, flags=re.S)
    # Quotations written as bold text between « » become <q> (RGAA 9.4).
    out = re.sub(r'<p><strong>«\s*(?:<em>)?(.*?)(?:</em>)?\s*»</strong></p>', r'<p class="citation"><q>\1</q></p>', out)
    return out


def link_corpus(htmltext, url_to_file):
    def fix(m):
        href = m.group(1)
        if 'ouvrirlesyeux.org' in href:
            base = href.split('#')[0].rstrip('/')
            return f'href="{url_to_file.get(base, "a-venir.html")}"'
        return m.group(0)
    return re.sub(r'href="([^"]+)"', fix, htmltext)


def dedupe_ids(htmltext):
    seen = {}
    def fix(m):
        i = m.group(1)
        seen[i] = seen.get(i, 0) + 1
        return f'id="{i}"' if seen[i] == 1 else f'id="{i}-{seen[i]}"'
    return re.sub(r'id="([^"]+)"', fix, htmltext)


def slug(s):
    s = re.sub(r'[^\w\s-]', '', H.unescape(s).lower())
    return re.sub(r'[\s_]+', '-', s).strip('-')[:60]


# ---------------------------------------------------------------- templates

def crumbs(items):
    lis = []
    for i, (label, href) in enumerate(items):
        if i:
            lis.append('<li aria-hidden="true">›</li>')
        if href:
            lis.append(f'<li><a href="{href}">{H.escape(label)}</a></li>')
        else:
            lis.append(f'<li><strong aria-current="page">{H.escape(label)}</strong></li>')
    return f'<nav aria-label="Fil d\'Ariane"><ol class="crumbs">{"".join(lis)}</ol></nav>'


def title_band(title, intro, rub, trail, note=True):
    bg = RUBRIQUES[rub][2]
    proto = ('<p class="note-proto"><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;margin-top:2px"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>'
             '<span>Texte repris du site actuel, à relire et mettre à jour par l\'association.</span></p>') if note else ''
    return (f'<div style="background: {bg}; padding: 28px 0 56px; position: relative; overflow: hidden">'
            '<div class="hero-deco" aria-hidden="true" style="position: absolute; right: 8%; top: 50px; display: flex; gap: 18px; align-items: center">'
            '<span style="width: 130px; height: 130px; border-radius: 50%; border: 14px solid #A9D1F5"></span>'
            '<span style="width: 36px; height: 36px; border-radius: 50%; background: #FFFFFF"></span></div>'
            '<div class="wrap" style="display: flex; flex-direction: column; gap: 28px; position: relative">'
            f'{crumbs(trail)}'
            '<div style="display: flex; flex-direction: column; gap: 14px; max-width: 44em">'
            f'<h1 class="page-title" style="margin: 0; font-size: 48px; line-height: 1.12">{H.escape(title)}</h1>'
            f'<p style="margin: 0; font-size: 21px">{H.escape(intro)}</p>{proto}</div></div></div>')


def toc(htmltext):
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', htmltext, re.S)
    if len(heads) < 3:
        return ''
    items = ''.join(f'<li><a href="#{i}">{re.sub(r"<[^>]+>", "", t)}</a></li>' for i, t in heads)
    return ('<nav aria-labelledby="t-toc" style="background: #FFFFFF; border: 2px solid #CFE5FA; border-radius: 16px; padding: 24px 28px; font-size: 18px; margin-bottom: 8px">'
            f'<h2 id="t-toc" style="margin: 0 0 12px; font-size: 22px; color: #1E2B3A">Dans cette page</h2><ol class="toc">{items}</ol></nav>')


def siblings(rub, current_file, titles):
    land = RUBRIQUES[rub][0]
    files = LANDINGS[land][2] if land in LANDINGS else [p['file'] for p in PAGES if p['rub'] == rub]
    files = [f for f in files if f != current_file][:4]
    if not files:
        return ''
    colors = ['#E3F0FC', '#E2F3EE', '#FFEBDD', '#FFE6E5']
    cards = ''.join(f'<li><a href="{f}" class="rel" style="background: {colors[i % 4]}"><strong style="font-size: 22px; line-height: 1.3">{H.escape(titles[f])}</strong><span class="ulink">Lire la page</span></a></li>'
                    for i, f in enumerate(files))
    return ('<section class="sec" aria-labelledby="t-rel" style="background: #FFFFFF; padding: 72px 0"><div class="wrap" style="display: flex; flex-direction: column; gap: 28px">'
            '<h2 id="t-rel" style="margin: 0; font-size: 32px; line-height: 1.2; color: #006FD6">Dans la même rubrique</h2>'
            f'<ul class="rel-grid" style="list-style: none; margin: 0; padding: 0">{cards}</ul></div></section>')


HELP = ('<section class="sec" aria-labelledby="t-aide" style="padding: 72px 0"><div class="wrap">'
        '<div class="help" style="display: flex; gap: 32px; align-items: center; justify-content: space-between; background: #E2F3EE; border-radius: 24px; padding: 40px 48px">'
        '<div style="display: flex; flex-direction: column; gap: 8px"><h2 id="t-aide" style="margin: 0; font-size: 32px; line-height: 1.2; color: #006FD6">Une question ?</h2>'
        '<p style="margin: 0; font-size: 20px">Notre comité d\'aide aux personnes concernées vous répond.</p></div>'
        '<a href="contact.html" class="btn btn-primary">Nous contacter</a></div></div></section>')


def trail_for(rub, title, self_landing=False):
    t = [('Accueil', 'accueil.html')]
    land, label, _ = RUBRIQUES[rub]
    if not self_landing and rub not in ('infos',):
        t.append((label, land))
    t.append((title, None))
    return t


def cards_grid(files, titles, cardtxt, colors=('#E3F0FC', '#E2F3EE', '#FFEBDD', '#FFE6E5', '#FFFFFF', '#CFE5FA')):
    items = ''.join(f'<li><a class="lp-card" href="{f}" style="background: {colors[i % len(colors)]}"><strong>{H.escape(titles[f])}</strong>'
                    f'<span>{H.escape(cardtxt.get(f, ""))}</span><span class="lp-go">Lire la page</span></a></li>' for i, f in enumerate(files))
    return f'<ul class="lp-grid">{items}</ul>'


# ---------------------------------------------------------------- build

def main(corpus_path):
    corpus = Corpus(corpus_path)
    helmets, bodies = {}, {}
    for stem, name, title in CANVAS_PAGES:
        helmets[name], bodies[name] = export_canvas(stem)
        (REPO / name).write_text(relink(page_shell(title, bodies[name], helmets[name]), name), encoding='utf-8')

    # Shell = Page A (content template): header + footer around a new <main>.
    shell_helmet = helmets['page-a.html']
    pa = bodies['page-a.html']
    head_part = pa[:pa.index('<main id="contenu">')]
    foot_part = pa[pa.index('</main>') + len('</main>'):]

    def shell(current, main_html):
        hp = re.sub(r'(<ul class="navlist">)(.*?)(</ul>\s*</nav>)', lambda m: m.group(1) + nav_html(current) + m.group(3), head_part, count=1, flags=re.S)
        return hp + f'<main id="contenu">{main_html}</main>' + foot_part

    titles = {p['file']: p['title'] for p in PAGES}
    titles.update({f: v[0] for f, v in PARTNERS.items()})
    titles.update({f: v[0] for f, v in FAQ.items()})
    titles.update({'page-a.html': 'Le diagnostic et parcours de soin', 'article.html': "Prix Espoir d'OLY", 'actualites.html': 'Nos Actualités'})
    cardtxt = {p['file']: p['card'] for p in PAGES}
    cardtxt.update({f: v[1] for f, v in PARTNERS.items()})
    cardtxt.update({f: 'Les réponses aux questions les plus fréquentes.' for f in FAQ})

    # old-site URL -> new file, from the corpus ranges used by each page
    url_to_file = {}
    for p in PAGES:
        for _, a, b in p.get('parts', []):
            for u, line in corpus.urls.items():
                if a - 6 <= line <= b:
                    url_to_file.setdefault(u, p['file'])
    url_to_file.setdefault('https://www.ouvrirlesyeux.org/fr/contact', 'contact.html')
    url_to_file.setdefault('https://www.ouvrirlesyeux.org/fr', 'accueil.html')
    url_to_file.setdefault('https://www.ouvrirlesyeux.org/fr/le-soutien/le-don', 'don.html')

    generated = []

    def write(file, title, current, main_html):
        out = page_shell(title, shell(current, main_html), shell_helmet, EXTRA_CSS)
        (REPO / file).write_text(relink(out, file), encoding='utf-8')
        generated.append(file)

    # Content pages
    for p in PAGES:
        if p.get('template'):
            continue
        rub = p['rub']
        current = rub if rub in [n[0] for n in NAV] else ''
        band = title_band(p['title'], p['intro'], rub, trail_for(rub, p['title'], p.get('landing_self')), note=not p.get('placeholder'))
        if p.get('placeholder'):
            body = ('<div class="wrap prose" style="padding-top: 48px; padding-bottom: 72px"><div class="read">'
                    '<div style="background: #FFFFFF; border: 2px dashed #767676; border-radius: 16px; padding: 28px 32px">'
                    '<h2 style="margin-top: 0">Contenu à fournir</h2><p>Présentez ici « La ruche » : ce que c\'est, à qui elle s\'adresse, comment y participer, et une personne à contacter.</p>'
                    '<p style="margin-bottom: 0">À rédiger par Thierry et Maryse (action A5 du 12/10).</p></div></div></div>')
        else:
            chunks = []
            bh = p['file'] in BOLD_HEADINGS
            for heading, a, b in p['parts']:
                md = corpus.md(a, b)
                if heading:
                    chunks.append(f'<h2 id="{slug(heading)}">{H.escape(heading)}</h2>' + md_to_html(md, 3, bh))
                else:
                    chunks.append(md_to_html(md, 2, bh))
            content = dedupe_ids(link_corpus('\n'.join(chunks), url_to_file) + p.get('extra', ''))
            for f_, old, new, href in LINK_TEXT_FIXES:
                if f_ == p['file']:
                    def fixlink(m, new=new, href=href):
                        tag = m.group(1) if href is None else re.sub(r'href="[^"]*"', f'href="{href}"', m.group(1))
                        return f'<a{tag}>{H.escape(new)}</a>'
                    content = re.sub(r'<a(\s[^>]*)>' + re.escape(old) + '</a>', fixlink, content, count=1)
            body = (f'<div class="wrap prose" style="padding-top: 48px; padding-bottom: 72px"><div class="read">{toc(content)}{content}</div></div>')
        write(p['file'], p['title'], current, band + body + siblings(rub, p['file'], titles) + HELP)

    # Partner pages
    for f, (title, intro, ranges, filt) in PARTNERS.items():
        items = []
        for a, b in ranges:
            for l in corpus.lines[a - 1:b]:
                m = re.match(r'- \[([^\]]+)\]\(([^)]+)\)\s*(?:–\s*(.*))?', l.strip())
                m2 = re.match(r'- (.+)', l.strip()) if not m else None
                if m:
                    items.append((m.group(1), m.group(2), m.group(3) or ''))
                elif m2:
                    items.append((m2.group(1), None, ''))
        if filt == 'fondation':
            items = [i for i in items if 'Fondation' in i[0]]
        elif filt == 'notfondation':
            items = [i for i in items if 'Fondation' not in i[0]]
        people = f == 'partenaires-personnalites.html'

        def link_label(n, u):
            if 'wikipedia' in u:
                return f'Page Wikipédia de {n}'
            if 'facebook' in u:
                return f'Page Facebook de {n}'
            return f'Site de {n}'
        cards = ''.join(
            f'<li class="pt-card"><div class="pt-logo">{"Photo" if people else "Logo"} : {H.escape(n)}</div><strong style="font-size: 21px">{H.escape(n)}</strong>'
            + (f'<span>{H.escape(d)}</span>' if d else '')
            + (f'<a href="{H.escape(u)}" style="margin-top: auto">{H.escape(link_label(n, u))}</a>' if u and 'ouvrirlesyeux.org' not in u else '')
            + '</li>' for n, u, d in items)
        lead = ''
        if people:
            bio = md_to_html(corpus.md(694, 698), 3).replace('</q></p>', '</q><span class="citation-source"> — Olivier Gourmet</span></p>')
            lead = ('<div style="max-width: 820px"><h2 id="parrain" style="margin-top: 0">Notre parrain, Olivier Gourmet</h2>' + bio
                    + '</div><h2 id="artistes-sportifs">Artistes et sportifs</h2>')
        body = (f'<div class="wrap prose" style="padding-top: 48px; padding-bottom: 72px">{lead}'
                f'<ul class="pt-grid">{cards}</ul></div>')
        write(f, title, 'partenaires', title_band(title, intro, 'partenaires', trail_for('partenaires', title)) + body + siblings('partenaires', f, titles))

    # FAQ pages
    for f, (title, qas) in FAQ.items():
        qlist = ('<nav class="faq-toc" aria-labelledby="faq-toc-t"><h2 id="faq-toc-t" style="margin: 0 0 8px; font-size: 22px; color: #1E2B3A">Les questions</h2><ol>'
               + ''.join(f'<li><a href="#q{i}">{H.escape(q)}</a></li>' for i, (q, a, h, lt) in enumerate(qas, 1)) + '</ol></nav>')
        dets = qlist + ''.join(f'<section class="faq-item" aria-labelledby="q{i}"><h2 id="q{i}">{H.escape(q)}</h2><p>{H.escape(a)}</p><p><a href="{h}">{H.escape(lt)}</a></p></section>' for i, (q, a, h, lt) in enumerate(qas, 1))
        band = title_band(title, "Les questions les plus fréquentes, et où trouver la réponse détaillée sur le site.", 'faq', trail_for('faq', title), note=False)
        body = ('<div class="wrap" style="padding-top: 48px; padding-bottom: 72px"><div class="read faq" style="max-width: 860px">'
                '<p class="note-proto" style="margin: 0 0 24px">Proposition de réponses rédigée à partir du site actuel, à valider par l\'association et son comité médico-scientifique.</p>'
                f'{dets}</div></div>')
        write(f, title, 'faq', band + body + siblings('faq', f, titles) + HELP)

    # Landing pages of the main rubriques
    for f, (rub, intro, children) in LANDINGS.items():
        title = RUBRIQUES[rub][1]
        band = title_band(title, intro, rub, [('Accueil', 'accueil.html'), (title, None)], note=False)
        body = f'<div class="wrap" style="padding-top: 56px; padding-bottom: 80px">{cards_grid(children, titles, cardtxt)}</div>'
        write(f, title, rub, band + body + HELP)

    # Agenda
    agenda_events = ''.join(
        f'<li><div style="display: flex; gap: 18px; background: #FFFFFF; border-radius: 16px; padding: 20px"><span style="flex-shrink: 0; width: 84px; height: 92px; border-radius: 14px; background: {c}; display: flex; flex-direction: column; align-items: center; justify-content: center; line-height: 1.1"><span style="font-size: 32px; font-weight: 700">JJ</span><span style="font-size: 16px; font-weight: 700">mois</span></span>'
        f'<span style="display: flex; flex-direction: column; gap: 4px"><strong style="font-size: 22px">{n}</strong><span>[Lieu] · [Horaire]</span><span>{d}</span></span></div></li>'
        for n, d, c in [('Repas dans le noir', 'Un repas vécu sans la vue, pour sensibiliser à la cécité.', '#E3F0FC'),
                        ('Ateliers des sens', 'Découvrir le monde par le toucher, l\'ouïe et le goût.', '#FFEBDD'),
                        ('Compétition OLY – Arras Golf Resort', 'Une journée sportive et solidaire.', '#FFE6E5'),
                        ('Assemblée générale', 'Le rendez-vous annuel des adhérents.', '#E2F3EE')])
    agenda = (title_band('Agenda', "Les rendez-vous de l'association : certains sont réservés aux adhérents, d'autres ouverts à tous.", 'actions', [('Accueil', 'accueil.html'), ('Agenda', None)], note=False)
              + '<div class="wrap" style="padding-top: 48px; padding-bottom: 72px"><div class="read prose">'
              + '<h2 id="a-venir">Prochains événements</h2><p class="note-proto">Dates et lieux à compléter. L\'agenda Google actuel sera remplacé par une liste accessible.</p>'
              + f'<ul style="list-style: none; padding: 0; display: flex; flex-direction: column; gap: 16px">{agenda_events}</ul>'
              + '<h2 id="archives">Les animations des années passées</h2>' + link_corpus(md_to_html(corpus.md(2523, 2546), 3), url_to_file)
              + '</div></div>')
    write('agenda.html', 'Agenda', '', agenda + HELP)

    # Contact
    contact = (title_band('Nous contacter', "Une question, un besoin d'aide ? Écrivez-nous ou appelez-nous.", 'infos', [('Accueil', 'accueil.html'), ('Nous contacter', None)], note=False)
               + '<div class="wrap" style="padding-top: 48px; padding-bottom: 80px"><div class="two-col">'
               + '<div style="display: flex; flex-direction: column; gap: 16px"><h2 style="margin: 0; font-size: 30px; color: #006FD6">Coordonnées</h2>'
               + '<address style="font-style: normal; background: #FFFFFF; border-radius: 20px; padding: 28px; font-size: 21px; line-height: 1.6"><strong>Ouvrir Les Yeux</strong><br>Maison des Associations<br>45 rue François Gauthier<br>62300 Lens</address>'
               + '<p style="margin: 0">Téléphone : <a href="tel:+33321054956">03 21 05 49 56</a><br>Répondeur 24 h/24 : <a href="tel:+33366980329">03 66 98 03 29</a></p></div>'
               + '<form style="background: #FFFFFF; border-radius: 20px; padding: 32px" aria-labelledby="t-form"><h2 id="t-form" style="margin: 0 0 20px; font-size: 30px; color: #006FD6">Écrivez-nous</h2>'
               + '<p style="margin: 0 0 20px; font-size: 16px">Les champs obligatoires portent la mention « obligatoire ».</p>'
               + '<div class="fld"><label for="c-nom">Nom (obligatoire)</label><input id="c-nom" type="text" autocomplete="name" required></div>'
               + '<div class="fld"><label for="c-mail">Adresse e-mail (obligatoire)</label><input id="c-mail" type="email" autocomplete="email" required></div>'
               + '<div class="fld"><label for="c-tel">Téléphone (facultatif)</label><input id="c-tel" type="tel" autocomplete="tel"></div>'
               + '<div class="fld"><label for="c-sujet">Sujet (obligatoire)</label><select id="c-sujet" required><option value="">Choisissez un sujet</option><option>Je suis concerné·e par une NOH</option><option>Je suis un proche</option><option>Adhésion, don, bénévolat</option><option>Presse, partenariat</option><option>Autre</option></select></div>'
               + '<div class="fld"><label for="c-msg">Message (obligatoire)</label><textarea id="c-msg" rows="6" required></textarea></div>'
               + '<div style="display: flex; gap: 12px; align-items: flex-start; margin-bottom: 22px"><input id="c-rgpd" type="checkbox" required style="width: 24px; height: 24px; margin-top: 3px; flex-shrink: 0"><label for="c-rgpd">J\'accepte que mes données soient utilisées pour répondre à ma demande (obligatoire). <a href="mentions-legales.html">Politique de confidentialité</a></label></div>'
               + '<button type="button" class="btn btn-primary">Envoyer le message</button></form></div></div>')
    write('contact.html', 'Nous contacter', '', contact)

    # Accessibility statement (skeleton)
    acc = (title_band("Déclaration d'accessibilité", "Ouvrir Les Yeux s'engage à rendre son site accessible à toutes et à tous.", 'infos', [('Accueil', 'accueil.html'), ("Déclaration d'accessibilité", None)], note=False)
           + '<div class="wrap prose" style="padding-top: 48px; padding-bottom: 72px"><div class="read">'
           + '<p class="note-proto">Modèle de déclaration à compléter après l\'audit RGAA (phase D).</p>'
           + '<h2 id="etat">État de conformité</h2><p>Le site est [totalement / partiellement / non] conforme au référentiel général d\'amélioration de l\'accessibilité (RGAA 4.1), en raison des non-conformités listées ci-dessous.</p>'
           + '<h2 id="resultats">Résultats des tests</h2><p>L\'audit réalisé par [prestataire] le [date] révèle que [XX] % des critères du RGAA sont respectés.</p>'
           + '<h2 id="non-accessibles">Contenus non accessibles</h2><p>[Liste des non-conformités, dérogations et contenus non soumis à l\'obligation.]</p>'
           + '<h2 id="technologies">Technologies utilisées</h2><ul><li>HTML</li><li>CSS</li><li>JavaScript</li></ul>'
           + '<h2 id="contact-acc">Retour d\'information et contact</h2><p>Si vous n\'arrivez pas à accéder à un contenu ou à un service, <a href="contact.html">contactez-nous</a> : nous vous orienterons vers une alternative accessible ou vous fournirons le contenu sous une autre forme.</p>'
           + '<h2 id="recours">Voies de recours</h2><p>Si vous nous avez signalé un défaut d\'accessibilité sans obtenir de réponse satisfaisante, vous pouvez saisir le <a href="https://www.defenseurdesdroits.fr/">Défenseur des droits</a>.</p>'
           + '</div></div>')
    write('accessibilite.html', "Déclaration d'accessibilité", '', acc)

    # Site map
    groups = [(RUBRIQUES['noh'][1], ['les-noh.html'] + LANDINGS['les-noh.html'][2]),
              (RUBRIQUES['vie'][1], ['la-vie-handicap-visuel.html'] + LANDINGS['la-vie-handicap-visuel.html'][2]),
              (RUBRIQUES['actions'][1], ['nos-actions.html', 'la-pair-aidance.html', 'recherche-oly.html', 'plaidoyer.html', 'la-ruche.html', 'agenda.html']),
              (RUBRIQUES['actus'][1], ['actualites.html', 'article.html']),
              (RUBRIQUES['partenaires'][1], ['nos-partenaires.html'] + list(PARTNERS)),
              (RUBRIQUES['faq'][1], ['questions-frequentes.html'] + list(FAQ)),
              ("L'association", ['qui-sommes-nous.html', 'notre-histoire.html', 'comite-medico-scientifique.html', 'nos-antennes.html']),
              ('Agir avec nous', ['agir-avec-nous.html', 'don.html', 'adherer.html', 'devenir-benevole.html', 'mecenat.html', 'legs.html', 'taxe-apprentissage.html', 'notre-boutique.html']),
              ('Infos pratiques', ['contact.html', 'mentions-legales.html', 'accessibilite.html'])]
    alltitles = dict(titles)
    alltitles.update({'les-noh.html': 'Les NOH', 'la-vie-handicap-visuel.html': 'La vie en situation de handicap visuel', 'nos-actions.html': 'Nos Actions',
                      'nos-partenaires.html': 'Nos Partenaires', 'questions-frequentes.html': 'Les Questions Fréquentes', 'agenda.html': 'Agenda',
                      'don.html': 'Faire un don', 'contact.html': 'Nous contacter', 'accessibilite.html': "Déclaration d'accessibilité", 'article.html': "Article : prix Espoir d'OLY"})
    sm = ''.join(f'<section><h2 id="{slug(g)}">{H.escape(g)}</h2><ul>' + ''.join(f'<li><a href="{f}">{H.escape(alltitles[f])}</a></li>' for f in fs) + '</ul></section>' for g, fs in groups)
    write('plan-du-site.html', 'Plan du site', '', title_band('Plan du site', 'Toutes les pages du site.', 'infos', [('Accueil', 'accueil.html'), ('Plan du site', None)], note=False)
          + f'<div class="wrap prose" style="padding-top: 48px; padding-bottom: 72px"><div class="lp-grid" style="list-style: none">{sm}</div></div>')

    # Prototype index (summary for reviewers)
    idx = (STATIC / 'index.html').read_text(encoding='utf-8')
    groups_idx = ''.join(f'<h2>{H.escape(g)}</h2><ul class="grid">' + ''.join(f'<li><a class="card" href="{f}"><strong>{H.escape(alltitles[f])}</strong><span class="go">Voir la page</span></a></li>' for f in fs) + '</ul>' for g, fs in groups)
    idx = idx.replace('<!--PAGES-->', groups_idx).replace('<!--COUNT-->', str(len(set(sum((fs for _, fs in groups), [])) | {'accueil.html', 'page-b.html', 'systeme-de-design.html'})))
    (REPO / 'index.html').write_text(idx, encoding='utf-8')
    for f in ('a-venir.html', 'README.md'):
        (REPO / f).write_text((STATIC / f).read_text(encoding='utf-8'), encoding='utf-8')
    print(len(generated), 'pages générées +', len(CANVAS_PAGES), 'pages de référence')


if __name__ == '__main__':
    main(sys.argv[1])
