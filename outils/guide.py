"""Developer guide of the OLY prototype: tokens, layout rules, every reusable component, behaviours.

Generates:
- guide-integration.html (through build.py's shell, so the live examples use the real site CSS),
- tokens/oly-tokens.json (W3C Design Tokens format, for Figma / Tokens Studio),
- tokens/oly-tokens.css (CSS custom properties).
Single source of truth for the values: TOKENS below.
"""
import json, html as H

# ---------------------------------------------------------------- tokens

COLORS = [
    # (token, hex, name, usage, group)
    ('ink', '#1E2B3A', 'Encre', 'Tout le texte, y compris sur les fonds pastel. Icônes.', 'Texte et marque'),
    ('oly-blue', '#006FD6', 'Bleu OLY', 'Titres de 24 px et plus uniquement (h2 de section).', 'Texte et marque'),
    ('link', '#0A5CB0', 'Bleu lien', 'Liens, bouton secondaire, onglet actif, contour de focus.', 'Texte et marque'),
    ('link-hover', '#08498C', 'Bleu lien survol', 'Survol des liens et du bouton secondaire.', 'Texte et marque'),
    ('coral', '#D93A39', 'Corail bouton', 'Fond du bouton principal (texte blanc). Un seul par écran si possible.', 'Texte et marque'),
    ('coral-hover', '#B92F2E', 'Corail survol', 'Survol du bouton principal.', 'Texte et marque'),
    ('teal', '#015C73', 'Canard', 'Accent de texte ponctuel.', 'Texte et marque'),
    ('muted', '#5B6470', 'Gris texte', 'Texte d\'un élément désactivé (pagination).', 'Texte et marque'),
    ('bg-blue', '#E3F0FC', 'Bleu pastel', 'Fonds de section, pied de page, en-têtes de tableau, survol des sous-menus.', 'Fonds pastel'),
    ('bg-blue-mid', '#CFE5FA', 'Bleu moyen', 'Entrée de menu ouverte ou active, bouton doux, badge « Interne », zone photo.', 'Fonds pastel'),
    ('bg-sky', '#A9D1F5', 'Bleu ciel', 'Décor (cercles), survol du bouton doux.', 'Fonds pastel'),
    ('bg-coral', '#FFE6E5', 'Rose', 'Bandeau « Agir avec nous », rubrique Nos Actions.', 'Fonds pastel'),
    ('bg-mint', '#E2F3EE', 'Menthe', 'Agenda, encadré « À retenir », bloc « Une question ? ».', 'Fonds pastel'),
    ('bg-peach', '#FFEBDD', 'Pêche', 'Newsletter, rubrique Nos Actualités.', 'Fonds pastel'),
    ('page', '#FAF8F7', 'Fond de page', 'Fond général du site.', 'Surfaces'),
    ('card', '#FFFFFF', 'Blanc', 'Cartes, en-tête, panneaux de menu, champs.', 'Surfaces'),
    ('border-field', '#767676', 'Bordure de champ', 'Bordure 2 px des champs, séparateurs du menu (3:1 minimum).', 'Bordures'),
    ('border-table', '#B8C0CA', 'Bordure de tableau', 'Cellules de tableau, pagination désactivée. Jamais pour un composant interactif.', 'Bordures'),
    ('border-soft', '#D9DEE5', 'Filet', 'Filets de l\'en-tête autour du menu. Décoratif.', 'Bordures'),
    ('border-list', '#E6E9ED', 'Filet de liste', 'Séparation des liens d\'un sous-menu. Décoratif.', 'Bordures'),
    ('deco-pink', '#FFB3B2', 'Rose décor', 'Pastilles décoratives (aria-hidden). Jamais sous du texte.', 'Décor'),
    ('deco-coral', '#FF4948', 'Corail charte', 'Couleur d\'origine de la charte : décor uniquement, jamais sous un texte blanc (3,3:1).', 'Décor'),
]
RUB_COLORS = [('Les NOH', 'bg-blue'), ('La vie en situation de handicap visuel', 'bg-mint'), ('Nos Actions', 'bg-coral'),
              ('Nos Actualités', 'bg-peach'), ('Nos Partenaires', 'bg-blue'), ('Les Questions Fréquentes', 'bg-mint'),
              ('Notre boutique', 'bg-coral'), ('L\'association, Infos pratiques', 'bg-blue'), ('Agir avec nous', 'bg-coral')]

FONT_SIZES = [
    # token, px desktop, px mobile (<760), line-height, weight, usage
    ('display', 52, 38, 1.12, 700, 'Titre h1 de l\'accueil (.hero-title).'),
    ('h1', 48, 34, 1.12, 700, 'Titre h1 des autres pages (.page-title, bandeau de titre).'),
    ('h2-section', 36, 28, 1.2, 700, 'Titre h2 d\'une section pleine largeur (Agenda, Nos actualités, À lire aussi…). La maquette va de 32 à 40 px : s\'aligner sur 36 px.'),
    ('h2-content', 32, 28, 1.25, 700, 'Titre h2 dans un texte de lecture (.prose h2), « Dans la même rubrique », « Une question ? ».'),
    ('h3', 26, 23, 1.3, 700, 'Titre h3 de carte « engagement ». Dans .prose : 23 px.'),
    ('h4', 22, 22, 1.3, 700, 'Titre de carte, question de FAQ, « À retenir », titre de sommaire.'),
    ('lead', 21, 19, 1.5, 400, 'Chapeau sous le h1 du bandeau de titre.'),
    ('article', 20, 19, 1.7, 400, 'Texte de lecture longue (.prose) et chapeaux de section.'),
    ('body', 18, 18, 1.6, 400, 'Texte courant, menu, boutons. Minimum pour un paragraphe.'),
    ('meta', 16, 16, 1.5, 400, 'Dates, badges, mentions sous un formulaire. Minimum absolu, jamais un paragraphe de contenu.'),
]
RADII = [('sm', 8, 'Conteneur de tableau défilant.'), ('field', 12, 'Champs, numéros de pagination, notes.'), ('md', 14, 'Lien de téléchargement, pastille de date.'),
         ('card', 16, 'Cartes, encadrés, questions de FAQ, sommaire.'), ('lg', 18, 'Cartes de rubrique (.lp-card).'), ('xl', 20, 'Carte photo de l\'accueil, bloc HelloAsso.'),
         ('xxl', 24, 'Grands encarts : engagements, agenda, « Une question ? ».'), ('pill', 999, 'Boutons, badges, onglets.')]
SPACES = [4, 8, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64, 72, 80, 96]
SHADOWS = [('rest', '0 2px 12px rgba(30,43,58,.08)', 'Carte au repos.'), ('hover', '0 6px 20px rgba(30,43,58,.16)', 'Carte cliquable au survol.'),
           ('raised', '0 6px 24px rgba(30,43,58,.10)', 'Carte photo de l\'accueil.'), ('panel', '0 14px 32px rgba(30,43,58,.18)', 'Sous-menu ouvert.')]
BREAKPOINTS = [('Ordinateur', '> 1100 px', 'Menu horizontal à 7 entrées, grilles à 3 ou 4 colonnes, colonne latérale.'),
               ('Tablette', '≤ 1100 px', 'Bouton « Menu », menu en liste verticale, grilles à 2 colonnes, plus de colonne latérale.'),
               ('Mobile', '≤ 760 px', 'Marges de 20 px, une seule colonne, titres réduits, décor masqué, bouton « Faire un don » pleine largeur.'),
               ('Petit mobile', '≤ 600 px', 'Rembourrages réduits (agenda, système de design). Aucun défilement horizontal à 320 px.')]


def hex_rgb(h):
    h = h.lstrip('#')
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def contrast(a, b):
    def lum(c):
        c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in hex_rgb(c)]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def fr(x, d=1):
    return f'{x:.{d}f}'.replace('.', ',')


def tokens_json():
    t = {'color': {k: {'$type': 'color', '$value': v, '$description': f'{n}. {u}'} for k, v, n, u, _ in COLORS},
         'font': {'family': {'$type': 'fontFamily', '$value': ['Atkinson Hyperlegible', 'system-ui', 'sans-serif'],
                             '$description': 'Police du texte. Charte : Luciole pour les titres.'},
                  'size': {k: {'$type': 'dimension', '$value': f'{d}px', '$description': u} for k, d, m, lh, w, u in FONT_SIZES},
                  'size-mobile': {k: {'$type': 'dimension', '$value': f'{m}px'} for k, d, m, lh, w, u in FONT_SIZES},
                  'line-height': {k: {'$type': 'number', '$value': lh} for k, d, m, lh, w, u in FONT_SIZES},
                  'weight': {'regular': {'$type': 'fontWeight', '$value': 400}, 'bold': {'$type': 'fontWeight', '$value': 700}}},
         'radius': {k: {'$type': 'dimension', '$value': f'{v}px', '$description': u} for k, v, u in RADII},
         'space': {str(v): {'$type': 'dimension', '$value': f'{v}px'} for v in SPACES},
         'shadow': {k: {'$type': 'string', '$value': v, '$description': u} for k, v, u in SHADOWS},
         'focus': {'$type': 'string', '$value': '3px solid #0A5CB0, offset 2px', '$description': 'Contour de focus clavier, sur tout élément interactif.'},
         'layout': {'container': {'$type': 'dimension', '$value': '1344px'}, 'gutter': {'$type': 'dimension', '$value': '48px'},
                    'gutter-mobile': {'$type': 'dimension', '$value': '20px'}, 'reading-width': {'$type': 'dimension', '$value': '820px'},
                    'bp-tablet': {'$type': 'dimension', '$value': '1100px'}, 'bp-mobile': {'$type': 'dimension', '$value': '760px'},
                    'bp-small': {'$type': 'dimension', '$value': '600px'}, 'target-min': {'$type': 'dimension', '$value': '44px'}}}
    return json.dumps(t, ensure_ascii=False, indent=2) + '\n'


def tokens_css():
    L = ['/* Ouvrir Les Yeux — design tokens (généré par outils/guide.py) */', ':root {']
    L += [f'  --color-{k}: {v}; /* {n} */' for k, v, n, u, _ in COLORS]
    L += ["  --font-family: 'Atkinson Hyperlegible', system-ui, sans-serif;"]
    L += [f'  --fs-{k}: {d}px; --lh-{k}: {lh};' for k, d, m, lh, w, u in FONT_SIZES]
    L += [f'  --radius-{k}: {v}px;' for k, v, u in RADII]
    L += [f'  --space-{v}: {v}px;' for v in SPACES]
    L += [f'  --shadow-{k}: {v};' for k, v, u in SHADOWS]
    L += ['  --focus-ring: 3px solid #0A5CB0;', '  --container: 1344px;', '  --gutter: 48px;', '  --reading-width: 820px;', '}',
          '@media (max-width: 760px) {', '  :root {', '    --gutter: 20px;']
    L += [f'    --fs-{k}: {m}px;' for k, d, m, lh, w, u in FONT_SIZES if m != d]
    L += ['  }', '}', ':focus-visible { outline: var(--focus-ring); outline-offset: 2px; }']
    return '\n'.join(L) + '\n'


# ---------------------------------------------------------------- page

GUIDE_CSS = """<style>
.g-layout{display:grid;grid-template-columns:260px minmax(0,1fr);gap:56px;align-items:start}
.g-side{position:sticky;top:16px;max-height:calc(100vh - 32px);overflow:auto;background:#FFFFFF;border-radius:16px;padding:20px 22px;font-size:16px}
.g-side ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:4px}
.g-side ol ol{padding-left:14px;margin:4px 0 8px}
.g-main{min-width:0}
.g-main>section{margin-bottom:72px}
.g-main h2{margin:0 0 16px;font-size:36px;line-height:1.2;color:#006FD6;scroll-margin-top:16px}
.g-main h3{margin:0 0 8px;font-size:26px;line-height:1.3;scroll-margin-top:16px}
.g-lead{font-size:20px;max-width:46em;margin:0 0 24px}
.g-comp{background:#FFFFFF;border-radius:20px;padding:28px;margin:0 0 32px;box-shadow:0 2px 12px rgba(30,43,58,.06)}
.g-use{margin:0 0 20px;max-width:52em}
.g-demo{background:#FAF8F7;border:2px dashed #B8C0CA;border-radius:16px;padding:28px;margin:0 0 20px}
.g-demo-label{margin:0 0 12px;font-size:16px;font-weight:700}
.g-cols{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px}
.g-table{border-collapse:collapse;width:100%;font-size:16px;margin:0 0 20px}
.g-table caption{text-align:left;font-weight:700;font-size:18px;padding:0 0 8px}
.g-table th,.g-table td{border:1px solid #B8C0CA;padding:8px 12px;text-align:left;vertical-align:top}
.g-table th{background:#E3F0FC}
.g-table td code,.g-comp code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:15px;background:#F1F3F5;border-radius:6px;padding:1px 6px;overflow-wrap:anywhere}
.g-wrap{overflow-x:auto;margin:0 0 20px}
.g-wrap .g-table{margin:0;min-width:620px}
.g-wrap-s .g-table{min-width:0}
.g-code code{background:none;color:inherit;padding:0;font-size:inherit;border-radius:0}
.g-sw{display:inline-block;width:40px;height:40px;border-radius:10px;border:1px solid #767676;vertical-align:middle}
.g-code{margin:0;background:#1E2B3A;color:#FFFFFF;border-radius:12px;padding:16px 18px;overflow:auto;max-height:340px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:14px;line-height:1.5;white-space:pre}
.g-code:focus-visible{outline:3px solid #0A5CB0;outline-offset:2px}
.g-code-t{margin:0 0 8px;font-size:16px;font-weight:700}
.g-list{margin:0 0 16px;padding-left:24px}
.g-list li{margin-bottom:6px}
.g-main p,.g-main li,.g-main td{overflow-wrap:anywhere}
.g-table td code{white-space:nowrap;overflow-wrap:normal}
.g-dl{display:flex;flex-wrap:wrap;gap:12px;margin:0 0 8px}
.g-specs{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px}
.g-specs h4{margin:0 0 8px;font-size:20px}
/* Components whose CSS lives in the reference templates (accueil, actualités, article, don) */
.btn-soft{background:#CFE5FA;color:#1E2B3A}
.btn-soft:hover{background:#A9D1F5;color:#1E2B3A}
.badge{padding:2px 12px;border-radius:999px;font-size:16px;font-weight:700}
.card-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px}
.card{display:flex;flex-direction:column;height:100%;background:#FFFFFF;border-radius:16px;overflow:hidden;text-decoration:none;color:#1E2B3A;box-shadow:0 2px 12px rgba(30,43,58,0.08)}
.card:hover{color:#1E2B3A;box-shadow:0 6px 20px rgba(30,43,58,0.16)}
.card-img{aspect-ratio:16/10;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;font-size:16px}
.card-body{padding:22px;display:flex;flex-direction:column;gap:10px;flex-grow:1}
.tabs{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:12px}
.tab{display:inline-flex;align-items:center;gap:8px;min-height:48px;padding:8px 22px;border-radius:999px;border:2px solid #0A5CB0;background:#FFFFFF;color:#0A5CB0;font-weight:700;text-decoration:none}
.tab:hover{background:#E3F0FC}
.tab-on{background:#0A5CB0;color:#FFFFFF}
.tab-on:hover{background:#08498C;color:#FFFFFF}
.pager{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:center}
.pg{display:inline-flex;align-items:center;justify-content:center;min-width:48px;min-height:48px;padding:0 12px;border-radius:12px;color:#0A5CB0;font-weight:700}
.share{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:12px}
.nl-row{display:flex;gap:12px;align-items:stretch}
@media (max-width:1100px){.g-layout{grid-template-columns:minmax(0,1fr)}.g-side{position:static;max-height:none}.card-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:760px){.g-cols,.g-specs,.card-grid{grid-template-columns:minmax(0,1fr)}.g-comp{padding:18px}.g-demo{padding:16px}.g-main h2{font-size:28px}.g-main h3{font-size:23px}.nl-row{flex-direction:column}}
</style>"""

ICON = {
    'image': '<svg aria-hidden="true" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#1E2B3A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.1-3.1a2 2 0 0 0-2.8 0L6 21"/></svg>',
    'pin': '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
    'clock': '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    'dl': '<svg aria-hidden="true" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>',
    'bulb': '<svg aria-hidden="true" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#1E2B3A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0; margin-top: 4px"><path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1V17h6v-.2c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2Z"/></svg>',
    'check': '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
    'mega': '<svg width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="#1E2B3A" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/></svg>',
    'link': '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/></svg>',
}

# Each component: id, name, usage, demo (live HTML, headings at h4 to keep the guide's outline),
# code (real markup, at the real heading level), specs [(property, value)], a11y [rules], used [(label, file)], gutenberg
COMPONENTS = [
 dict(id='c-boutons', name='Boutons', group='Actions',
      usage="Action principale (corail, une seule par zone), action secondaire (contour bleu), action discrète (bleu doux : partage). Un lien qui change de page reste un <a> stylé en bouton ; un <button> ne sert qu'aux actions sur place.",
      demo='<div style="display: flex; flex-wrap: wrap; gap: 16px"><a href="don.html" class="btn btn-primary">Faire un don</a><a href="nos-actions.html" class="btn btn-secondary">Voir toutes nos actions</a><a href="agenda.html" class="btn btn-soft">Voir l\'agenda</a></div>',
      code='<a href="/don" class="btn btn-primary">Faire un don</a>\n<a href="/nos-actions" class="btn btn-secondary">Voir toutes nos actions</a>\n<button type="button" class="btn btn-soft">Copier le lien</button>',
      specs=[('Classes', '.btn + .btn-primary | .btn-secondary | .btn-soft'), ('Gabarit', 'pilule (rayon 999), hauteur min. 52 px, padding 12 × 28 px, gras 18 px, gap icône 10 px'),
             ('Principal', 'fond #D93A39, texte #FFFFFF (4,55:1) ; survol #B92F2E'), ('Secondaire', 'fond #FFFFFF, bordure 2 px et texte #0A5CB0 ; survol fond #E3F0FC, texte #08498C'),
             ('Doux', 'fond #CFE5FA, texte #1E2B3A ; survol #A9D1F5'), ('Mobile', 'les boutons des bandeaux passent en pleine largeur (grilles .agir-btns, .utils)')],
      a11y=['Aucune flèche, aucun chevron, aucun soulignement (réservé aux liens).', 'Libellé explicite hors contexte : « Je fais un don sur HelloAsso », pas « Cliquez ici ».', 'Focus : contour 3 px #0A5CB0 décalé de 2 px (global :focus-visible).', 'Désactivé : à éviter ; si nécessaire, aria-disabled="true" et texte #5B6470 sur bordure #B8C0CA.'],
      used=[('Accueil', 'accueil.html'), ('Faire un don', 'don.html'), ('Article', 'article.html')], gutenberg='core/button avec 3 variations de style (is-style-primary, -secondary, -soft)'),
 dict(id='c-liens', name='Liens texte', group='Actions',
      usage="Lien dans un paragraphe, ou lien d'appel sous une carte (« Lire la page »).",
      demo='<p style="margin: 0 0 12px">Consultez <a href="les-demarches.html">les démarches pour obtenir une aide humaine</a> sur notre page dédiée.</p><p style="margin: 0"><span class="ulink">Lire la page</span> (dans une carte cliquable)</p>',
      code='<a href="/les-demarches">les démarches pour obtenir une aide humaine</a>\n<span class="ulink">Lire la page</span>  <!-- dans une carte dont le <a> englobe tout -->',
      specs=[('Couleur', '#0A5CB0 (6,3:1 sur le fond) ; survol #08498C'), ('Soulignement', 'toujours visible, épaisseur 2 px, décalage 3 px'), ('.ulink', 'même rendu en gras, pour le faux lien visible dans une carte entièrement cliquable')],
      a11y=['Jamais « cliquez ici », « en savoir plus » ou « ici » seuls.', 'Lien externe : le dire dans l\'intitulé ou le texte qui suit (ex. « (site mdph.fr) »).', 'Un seul lien par carte : le <a> englobe la carte, .ulink n\'est qu\'un repère visuel.'],
      used=[('Les démarches', 'les-demarches.html'), ('Nos Actions', 'nos-actions.html')], gutenberg='styles globaux de theme.json (elements.link)'),
 dict(id='c-entete', name='En-tête et accès rapides', group='Navigation',
      usage="En haut de toutes les pages : logo (lien vers l'accueil), lien d'évitement, recherche, langues, bouton « Faire un don », puis menu principal.",
      demo=None,
      code='<header>\n  <div class="wrap topbar-in">\n    <a href="/" class="logo-slot"><img src="logo-oly.png" alt="Ouvrir Les Yeux, pour voir demain : accueil"></a>\n    <nav aria-label="Accès rapides" class="utils">\n      <a href="#contenu" class="skip">Aller au contenu</a>\n      <a href="/recherche"><svg aria-hidden="true">…</svg>Rechercher</a>\n      <span>\n        <a href="/" lang="fr" aria-current="true">Français</a> <span aria-hidden="true">·</span>\n        <a href="/en/" lang="en" hreflang="en">English</a> <span aria-hidden="true">·</span>\n        <a href="/es/" lang="es" hreflang="es">Español</a>\n      </span>\n      <a href="/don" class="btn btn-primary">Faire un don</a>\n    </nav>\n    <button type="button" class="menu-toggle" aria-expanded="false" aria-controls="menu-principal">\n      <svg class="mt-open" aria-hidden="true">…</svg><svg class="mt-close" hidden aria-hidden="true">…</svg>\n      <span class="mt-label">Menu</span>\n    </button>\n  </div>\n  <nav id="menu-principal" aria-label="Menu principal" class="mainnav">…</nav>\n</header>',
      specs=[('Hauteur', 'barre 96 px min. ; logo 64 px de haut (48 px sur mobile)'), ('Fond', '#FFFFFF ; filets #D9DEE5 au-dessus et au-dessous du menu'), ('Langues', 'nom complet dans sa langue, langue active en gras couleur encre, séparateur « · » masqué'), ('≤ 1100 px', 'bouton « Menu » visible ; le lien d\'évitement est masqué hors focus'), ('≤ 760 px', 'accès rapides sur toute la largeur, sous le logo ; « Faire un don » pleine largeur')],
      a11y=['Le lien d\'évitement est le premier élément focusable du vrai site (la barre de maquette n\'existe pas en production).', 'lang et hreflang sur chaque langue ; pas de drapeau, pas d\'abréviation.', 'Alternative du logo : « Ouvrir Les Yeux, pour voir demain : accueil ».'],
      used=[('Toutes les pages', 'accueil.html')], gutenberg='partie de modèle header.html (template part) + bloc de navigation sur mesure'),
 dict(id='c-menu', name='Menu principal à sous-menus', group='Navigation',
      usage="7 rubriques sur 2 lignes chacune, chacune avec sa couleur pastel et un sous-menu qui s'ouvre au clic (pas au survol).",
      demo=None,
      code='<ul class="navlist">\n  <li class="nav-item" data-bg="#E3F0FC" style="background:#E3F0FC">\n    <button type="button" class="nav-btn" aria-expanded="false" aria-controls="panel-noh">\n      <span><span class="nl">Les</span> <span class="nl">NOH</span></span>\n      <span class="nav-ind" aria-hidden="true">+</span>\n    </button>\n    <ul id="panel-noh" class="nav-panel" hidden>\n      <li><a class="nav-all" href="/les-noh">Tout savoir sur les NOH</a></li>\n      <li><a class="nav-sublink" href="/les-traitements" aria-current="page">Les traitements</a></li>\n      …\n    </ul>\n  </li>\n  …\n</ul>',
      specs=[('Grille', '7 colonnes égales ; séparateur vertical 2 px #767676 entre entrées'), ('Entrée', 'hauteur 104 px, gras 18 px, centré ; fond = couleur de la rubrique ; ouverte ou active : fond #CFE5FA + trait bas 5 px #1E2B3A'), ('Sous-menu', 'blanc, largeur 300 à 380 px, rayon bas 16 px, ombre « panel » ; liens 18 px, filet #E6E9ED ; survol fond #E3F0FC + soulignement ; les 2 derniers s\'alignent à droite'), ('≤ 1100 px', 'liste verticale ; entrée 60 px de haut, texte à gauche, indicateur « + » / « − » à droite ; sous-menu en place, retrait 44 px')],
      a11y=['Bouton avec aria-expanded et aria-controls ; un seul sous-menu ouvert à la fois.', 'Échap ferme le sous-menu et rend le focus à son bouton ; sur mobile, Échap ferme le menu et rend le focus à « Menu ».', 'Clic en dehors : ferme tout.', 'aria-current="page" sur le lien de la page en cours.', 'Rubriques séparées par une bordure ET une couleur, jamais la couleur seule.'],
      used=[('Toutes les pages', 'accueil.html')], gutenberg='bloc de navigation sur mesure (le bloc core/navigation ne gère ni les couleurs par rubrique ni ce comportement)'),
 dict(id='c-ariane', name="Fil d'Ariane", group='Navigation',
      usage="Sur toutes les pages sauf l'accueil, en haut du bandeau de titre.",
      demo='<nav aria-label="Fil d\'Ariane (exemple)"><ol class="crumbs"><li><a href="accueil.html">Accueil</a></li><li aria-hidden="true">›</li><li><a href="les-noh.html">Les NOH</a></li><li aria-hidden="true">›</li><li><strong aria-current="page">Les traitements</strong></li></ol></nav>',
      code='<nav aria-label="Fil d\'Ariane">\n  <ol class="crumbs">\n    <li><a href="/">Accueil</a></li>\n    <li aria-hidden="true">›</li>\n    <li><a href="/les-noh">Les NOH</a></li>\n    <li aria-hidden="true">›</li>\n    <li><strong aria-current="page">Les traitements</strong></li>\n  </ol>\n</nav>',
      specs=[('Disposition', 'flex, retour à la ligne, gap 8 px'), ('Dernier élément', 'gras, encre, non cliquable'), ('Séparateur', '« › » masqué aux lecteurs d\'écran')],
      a11y=['aria-current="page" sur le dernier élément.'], used=[('Les traitements', 'les-traitements.html')], gutenberg='bloc d\'un plugin de fil d\'Ariane (Yoast, Rank Math) restylé, ou bloc sur mesure'),
 dict(id='c-bandeau', name='Bandeau de titre', group='Structure de page',
      usage="Haut de chaque page intérieure : fil d'Ariane, h1, chapeau. Fond = couleur pastel de la rubrique.",
      demo='<div style="background: #FFE6E5; padding: 28px 28px 40px; position: relative; overflow: hidden; border-radius: 12px"><div class="hero-deco" aria-hidden="true" style="position: absolute; right: 6%; top: 30px; display: flex; gap: 18px; align-items: center"><span style="width: 100px; height: 100px; border-radius: 50%; border: 12px solid #A9D1F5"></span><span style="width: 30px; height: 30px; border-radius: 50%; background: #FFFFFF"></span></div><div style="position: relative; display: flex; flex-direction: column; gap: 14px; max-width: 34em"><p style="margin: 0; font-size: 40px; line-height: 1.12; font-weight: 700">Nos Actions</p><p style="margin: 0; font-size: 21px">Chapeau de la page, une ou deux phrases.</p></div></div>',
      code='<div class="title-band" style="background: var(--rubrique-bg)">\n  <div class="hero-deco" aria-hidden="true">…cercles décoratifs…</div>\n  <div class="wrap">\n    <nav aria-label="Fil d\'Ariane">…</nav>\n    <h1 class="page-title">Nos Actions</h1>\n    <p class="lead">Chapeau de la page.</p>\n  </div>\n</div>',
      specs=[('Espacement', '28 px en haut, 56 px en bas ; gap 28 px fil d\'Ariane / titre ; texte limité à 44 em'), ('Titre', 'h1 48 px / 1,12 (34 px sur mobile), encre'), ('Chapeau', '21 px'), ('Décor', 'cercle 130 px bordure 14 px #A9D1F5 + pastille 36 px blanche, à droite ; masqué ≤ 760 px'), ('Couleurs de rubrique', 'voir le tableau des couleurs de rubrique')],
      a11y=['Un seul h1 par page.', 'Le décor est aria-hidden et ne passe jamais sous du texte.'], used=[('Nos Actions', 'nos-actions.html'), ('Prévention', 'prevention.html')], gutenberg='compo (pattern) « Bandeau de titre » : core/group + core/post-title + core/post-excerpt'),
 dict(id='c-sommaire', name='Sommaire « Dans cette page »', group='Structure de page',
      usage="Affiché automatiquement en tête d'une page de lecture qui compte 3 titres h2 ou plus.",
      demo='<nav aria-labelledby="g-toc-t" style="background: #FFFFFF; border: 2px solid #CFE5FA; border-radius: 16px; padding: 24px 28px; font-size: 18px"><h4 id="g-toc-t" style="margin: 0 0 12px; font-size: 22px">Dans cette page</h4><ol class="toc"><li><a href="#c-sommaire">Le porteur sain</a></li><li><a href="#c-sommaire">Le déclenchement</a></li><li><a href="#c-sommaire">La transmission des NOH</a></li></ol></nav>',
      code='<nav aria-labelledby="t-toc" class="page-toc">\n  <h2 id="t-toc">Dans cette page</h2>\n  <ol class="toc">\n    <li><a href="#le-porteur-sain">Le porteur sain</a></li>\n    …\n  </ol>\n</nav>',
      specs=[('Fond', '#FFFFFF, bordure 2 px #CFE5FA, rayon 16 px, padding 24 × 28 px'), ('Titre', '22 px gras, encre'), ('Liens', '18 px, gap 8 px, zone cliquable 4 px au-dessus et au-dessous'), ('Règle', 'généré si la page a 3 h2 ou plus ; ancres = id des h2')],
      a11y=['Les h2 ont un scroll-margin-top de 24 px pour ne pas coller au bord.'], used=[('Prévention', 'prevention.html'), ('Que sont ces maladies ?', 'que-sont-ces-maladies.html')], gutenberg='bloc « table des matières » (plugin) ou bloc sur mesure lisant les h2'),
 dict(id='c-prose', name='Texte de lecture', group='Contenu',
      usage="Toute page de contenu éditorial. Les titres s'emboîtent sans sauter de niveau (h2 → h3 → h4).",
      demo='<div class="prose" style="max-width: 720px"><p style="margin: 0 0 6px; font-size: 32px; line-height: 1.25; color: #006FD6; font-weight: 700">Titre h2 de contenu</p><p>Texte courant à 20 px, interligne 1,7, sur une colonne de 820 px maximum, soit environ 70 caractères par ligne.</p><p style="margin: 0 0 10px; font-size: 23px; line-height: 1.3; font-weight: 700">Titre h3</p><ul><li>Élément de liste, retrait 28 px</li><li>Espacement de 10 px entre éléments</li></ul><blockquote style="margin: 0"><p style="margin: 0">Encadré de citation longue : fond #E3F0FC, filet gauche 6 px #006FD6.</p></blockquote></div>',
      code='<div class="wrap prose">\n  <div class="read">\n    <h2 id="…">Titre h2 de contenu</h2>\n    <p>…</p>\n    <h3>Titre h3</h3>\n    <ul><li>…</li></ul>\n    <blockquote><p>…</p></blockquote>\n  </div>\n</div>',
      specs=[('Conteneur', '.read : 820 px max, centré'), ('Texte', '20 px / 1,7 (19 px sur mobile), paragraphes espacés de 20 px'), ('h2', '32 px / 1,25, #006FD6, marge haute 64 px (40 px mobile, 28 px)'), ('h3', '23 px / 1,3, encre, marge haute 28 px'), ('Listes', 'retrait 28 px, 10 px entre éléments'), ('Bloc de citation', 'fond #E3F0FC, filet gauche 6 px #006FD6, rayon 0 12 12 0'), ('Coupure', 'overflow-wrap:anywhere sur les paragraphes, liens et cellules (URL longues)')],
      a11y=['Un texte en gras seul sur sa ligne qui annonce une partie est un titre (h2 à h6), pas un <strong>.', 'Pas d\'italique long, pas de capitales sur plusieurs mots.'], used=[('Que sont ces maladies ?', 'que-sont-ces-maladies.html'), ('Les démarches', 'les-demarches.html')], gutenberg='styles par défaut des blocs core/paragraph, core/heading, core/list, core/quote dans theme.json'),
 dict(id='c-tableau', name='Tableau de données', group='Contenu',
      usage="Données à deux dimensions (cookies, tarifs). Jamais pour de la mise en page.",
      demo='<div class="prose" style="font-size: 18px"><div class="table-wrap" role="region" aria-label="Tableau d\'exemple, faire défiler horizontalement" tabindex="0"><table><caption>Cookies utilisés sur le site</caption><thead><tr><th scope="col">Nom du cookie</th><th scope="col">Finalité</th><th scope="col">Durée</th></tr></thead><tbody><tr><td>_pk_id</td><td>Mesure d\'audience (Matomo)</td><td>13 mois</td></tr></tbody></table></div></div>',
      code='<div class="table-wrap" role="region" aria-label="Tableau, faire défiler horizontalement" tabindex="0">\n  <table>\n    <caption>Cookies utilisés sur le site</caption>\n    <thead><tr><th scope="col">Nom du cookie</th><th scope="col">Finalité</th><th scope="col">Durée</th></tr></thead>\n    <tbody><tr><td>…</td><td>…</td><td>…</td></tr></tbody>\n  </table>\n</div>',
      specs=[('Texte', '17 px'), ('Cellules', 'bordure 1 px #B8C0CA, padding 10 × 12 px, alignées en haut à gauche'), ('En-têtes', 'fond #E3F0FC'), ('Petit écran', 'conteneur défilant ; tableau large de 560 px minimum')],
      a11y=['<caption> obligatoire ; scope="col" (ou "row") sur chaque <th>.', 'Le conteneur défilant est focusable (tabindex="0") et nommé.'], used=[('Mentions légales', 'mentions-legales.html')], gutenberg='core/table (cocher « en-tête », renseigner la légende) ; ajouter scope par filtre PHP'),
 dict(id='c-citation', name='Citation courte', group='Contenu',
      usage="Parole rapportée d'une personne, mise en valeur.",
      demo='<p class="citation" style="margin: 0"><q>Ensemble, rendons le monde accessible.</q><span class="citation-source"> — Prénom Nom</span></p>',
      code='<p class="citation"><q>Texte de la citation</q><span class="citation-source"> — Prénom Nom</span></p>',
      specs=[('Texte', '22 px gras, italique'), ('Guillemets', '« » générés par CSS (quotes), pas tapés dans le texte'), ('Source', '18 px normal, précédée d\'un tiret cadratin')],
      a11y=['Utiliser <q> (ou <blockquote> si plusieurs phrases), pas un <strong>.'], used=[('Personnalités', 'partenaires-personnalites.html')], gutenberg='core/pullquote ou core/quote avec style « citation »'),
 dict(id='c-retenir', name='Encadré « À retenir »', group='Contenu',
      usage="Une information essentielle à ne pas manquer dans un article (date limite, condition).",
      demo='<aside aria-labelledby="g-retenir" style="padding: 24px 28px; background: #E2F3EE; border-radius: 16px; display: flex; gap: 18px; align-items: flex-start">' + ICON['bulb'] + '<div><h4 id="g-retenir" style="margin: 0 0 6px; font-size: 22px">À retenir</h4><p style="margin: 0">Le dossier complet est envoyé en un seul fichier PDF avant la date limite.</p></div></aside>',
      code='<aside aria-labelledby="t-retenir" class="callout">\n  <svg aria-hidden="true">…ampoule…</svg>\n  <div>\n    <h3 id="t-retenir">À retenir</h3>\n    <p>…</p>\n  </div>\n</aside>',
      specs=[('Fond', '#E2F3EE (menthe), rayon 16 px, padding 24 × 28 px, marge 32 px'), ('Icône', '32 px au trait, encre'), ('Titre', '22 px gras')], a11y=['Le titre porte le sens, l\'icône est aria-hidden.'],
      used=[('Article', 'article.html')], gutenberg='compo « Encadré » : core/group (fond menthe) + core/heading + core/paragraph'),
 dict(id='c-etapes', name='Étapes numérotées', group='Contenu',
      usage="Un parcours dans l'ordre (diagnostic, démarche).",
      demo='<ol class="steps" style="margin: 0"><li class="step"><span class="step-num" aria-hidden="true">1</span><div><h4 style="margin: 0 0 4px">Consulter un centre expert</h4><p style="margin: 0">Prenez rendez-vous dans le centre de votre région.</p></div></li><li class="step"><span class="step-num" aria-hidden="true" style="background: #E2F3EE">2</span><div><h4 style="margin: 0 0 4px">Confirmer le diagnostic</h4><p style="margin: 0">Une prise de sang permet le diagnostic moléculaire.</p></div></li></ol>',
      code='<ol class="steps">\n  <li class="step">\n    <span class="step-num" aria-hidden="true">1</span>\n    <div><h3>Consulter un centre expert</h3><p>…</p></div>\n  </li>\n  …\n</ol>',
      specs=[('Étape', 'fond blanc, rayon 16 px, padding 22 × 24 px, gap 20 px ; 16 px entre étapes'), ('Numéro', 'disque 52 px, 24 px gras ; couleurs tournantes #CFE5FA, #E2F3EE, #FFEBDD, #FFE6E5'), ('Mobile', 'numéro au-dessus du texte')],
      a11y=['<ol> porte l\'ordre ; le numéro visuel est aria-hidden pour éviter la double lecture.'], used=[('Le diagnostic et parcours de soin', 'page-a.html')], gutenberg='compo « Étapes » sur core/list ordonnée, ou bloc sur mesure'),
 dict(id='c-telechargement', name='Lien de téléchargement', group='Contenu',
      usage="Document à télécharger (PDF), avec son poids et sa source.",
      demo='<a href="a-venir.html" class="dl" style="margin: 0">' + ICON['dl'] + '<span><span class="ulink">Synthèse pour le médecin traitant</span><br><span style="font-size: 16px">PDF · 420 Ko · site de la HAS</span></span></a>',
      code='<a href="/docs/synthese.pdf" class="dl">\n  <svg aria-hidden="true">…téléchargement…</svg>\n  <span><span class="ulink">Synthèse pour le médecin traitant</span><br>\n  <span class="meta">PDF · 420 Ko · site de la HAS</span></span>\n</a>',
      specs=[('Bloc', 'fond blanc, bordure 2 px #0A5CB0, rayon 14 px, padding 16 × 20 px ; survol fond #E3F0FC'), ('Méta', 'format, poids, source en 16 px')],
      a11y=['Format et poids dans l\'intitulé du lien (RGAA 6.1).', 'Document lui-même accessible (PDF balisé) ou alternative HTML.'], used=[('Le diagnostic et parcours de soin', 'page-a.html')], gutenberg='core/file restylé (afficher format et poids)'),
 dict(id='c-carte-rubrique', name='Carte de rubrique', group='Cartes',
      usage="Pages d'entrée de rubrique (Les NOH, Nos Actions…) : une carte par sous-page.",
      demo='<ul class="lp-grid"><li><a class="lp-card" href="prevention.html" style="background: #E3F0FC"><strong>Prévention</strong><span>Porteur sain, déclenchement, transmission.</span><span class="lp-go">Lire la page</span></a></li><li><a class="lp-card" href="les-traitements.html" style="background: #E2F3EE"><strong>Les traitements</strong><span>Idébénone, thérapie génique, essais.</span><span class="lp-go">Lire la page</span></a></li><li><a class="lp-card" href="la-recherche.html" style="background: #FFEBDD"><strong>La recherche</strong><span>Les équipes et projets soutenus.</span><span class="lp-go">Lire la page</span></a></li></ul>',
      code='<ul class="lp-grid">\n  <li><a class="lp-card" href="/prevention" style="background:#E3F0FC">\n    <strong>Prévention</strong>\n    <span>Résumé en une ligne.</span>\n    <span class="lp-go">Lire la page</span>\n  </a></li>\n</ul>',
      specs=[('Grille', '3 colonnes, gap 20 px (2 ≤ 1100 px, 1 ≤ 760 px)'), ('Carte', 'rayon 18 px, padding 26 px, ombre « rest », survol « hover » ; hauteur égale par ligne'), ('Fonds', 'cycle #E3F0FC, #E2F3EE, #FFEBDD, #FFE6E5, #FFFFFF, #CFE5FA'), ('Titre', '23 px gras'), ('Appel', '« Lire la page » en .lp-go collé en bas')],
      a11y=['Toute la carte est un seul lien ; l\'intitulé lu = titre + résumé + « Lire la page ».'], used=[('Les NOH', 'les-noh.html'), ('Nos Actions', 'nos-actions.html')], gutenberg='compo « Grille de cartes » (core/columns ou bloc sur mesure) ; liste des pages enfants'),
 dict(id='c-carte-meme-rubrique', name='Cartes « Dans la même rubrique »', group='Cartes',
      usage="Bas de page de contenu : jusqu'à 4 autres pages de la même rubrique.",
      demo='<ul class="rel-grid" style="list-style: none; margin: 0; padding: 0"><li><a href="prevention.html" class="rel" style="background: #E3F0FC"><strong style="font-size: 22px; line-height: 1.3">Prévention</strong><span class="ulink">Lire la page</span></a></li><li><a href="les-traitements.html" class="rel" style="background: #E2F3EE"><strong style="font-size: 22px; line-height: 1.3">Les traitements</strong><span class="ulink">Lire la page</span></a></li></ul>',
      code='<section aria-labelledby="t-rel">\n  <h2 id="t-rel">Dans la même rubrique</h2>\n  <ul class="rel-grid">\n    <li><a href="/prevention" class="rel"><strong>Prévention</strong><span class="ulink">Lire la page</span></a></li>\n  </ul>\n</section>',
      specs=[('Grille', '4 colonnes, gap 20 px (2 ≤ 1100 px, 1 ≤ 760 px)'), ('Carte', 'hauteur min. 140 px, padding 24 px, rayon 16 px, ombre « rest » / « hover »'), ('Fonds', 'cycle #E3F0FC, #E2F3EE, #FFEBDD, #FFE6E5'), ('Section', 'fond blanc, padding 72 px (56 px mobile)')],
      a11y=['La page en cours est exclue de la liste.'], used=[('Prévention', 'prevention.html')], gutenberg='bloc « pages sœurs » sur mesure ou core/query filtré par parent'),
 dict(id='c-carte-actu', name="Carte d'actualité et badge", group='Cartes',
      usage="Liste des actualités, accueil, « À lire aussi ». Même gabarit pour article et actualité.",
      demo='<ul class="card-grid" style="list-style: none; margin: 0; padding: 0; max-width: 380px; grid-template-columns: minmax(0,1fr)"><li><a href="article.html" class="card"><span class="card-img" style="background: #CFE5FA">' + ICON['image'] + 'Photo de l\'article</span><span class="card-body"><span style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap"><span class="badge" style="background: #CFE5FA">Interne</span><span style="font-size: 16px">12 mars 2026</span></span><strong style="font-size: 21px; line-height: 1.3">Prix Espoir d\'OLY : appel à candidatures</strong><span>Un prix pour les jeunes chercheurs qui travaillent sur les NOH.</span><span class="ulink" style="margin-top: auto">Lire l\'article</span></span></a></li></ul>',
      code='<ul class="card-grid">\n  <li><a href="/actualites/prix-espoir" class="card">\n    <img class="card-img" src="…" alt="">\n    <span class="card-body">\n      <span><span class="badge">Interne</span> <time datetime="2026-03-12">12 mars 2026</time></span>\n      <strong>Prix Espoir d\'OLY : appel à candidatures</strong>\n      <span>Extrait en une ou deux phrases.</span>\n      <span class="ulink">Lire l\'article</span>\n    </span>\n  </a></li>\n</ul>',
      specs=[('Grille', '3 colonnes, gap 28 px (2 ≤ 1100 px, 1 ≤ 760 px)'), ('Carte', 'blanc, rayon 16 px, ombre « rest » / « hover », image 16:10 en haut'), ('Corps', 'padding 22 px, gap 10 px ; titre 21 px gras'), ('Badge', 'pilule, padding 2 × 12 px, 16 px gras, encre sur pastel : Interne #CFE5FA, Externe #FFEBDD, Événement #E2F3EE')],
      a11y=['Aucun texte posé sur l\'image ; image décorative (alt="") puisque le titre suit.', 'Le libellé du badge porte l\'information, pas sa couleur.', 'Date dans un <time datetime>.'], used=[('Nos Actualités', 'actualites.html'), ('Accueil', 'accueil.html')], gutenberg='core/query + core/post-template (image, catégorie, date, titre, extrait)'),
 dict(id='c-agenda', name="Événement d'agenda", group='Cartes',
      usage="Accueil (encart Agenda) et page Agenda.",
      demo='<ul style="list-style: none; margin: 0; padding: 0; max-width: 480px"><li><a href="agenda.html" style="display: flex; gap: 18px; background: #FFFFFF; border-radius: 16px; padding: 18px; text-decoration: none; color: #1E2B3A"><span style="flex-shrink: 0; width: 76px; height: 84px; border-radius: 14px; background: #E3F0FC; display: flex; flex-direction: column; align-items: center; justify-content: center; line-height: 1.1"><span style="font-size: 30px; font-weight: 700">14</span><span style="font-size: 16px; font-weight: 700">mars</span></span><span style="display: flex; flex-direction: column; gap: 4px"><strong style="font-size: 20px; line-height: 1.3">Repas dans le noir</strong><span style="display: flex; gap: 8px; align-items: center; font-size: 16px">' + ICON['pin'] + 'Lens</span><span style="display: flex; gap: 8px; align-items: center; font-size: 16px">' + ICON['clock'] + '19 h 30</span></span></a></li></ul>',
      code='<li><a href="/agenda/repas-dans-le-noir" class="event">\n  <span class="event-date"><span>14</span><span>mars</span></span>\n  <span class="event-body">\n    <strong>Repas dans le noir</strong>\n    <span><svg aria-hidden="true">…lieu…</svg>Lens</span>\n    <span><svg aria-hidden="true">…horloge…</svg>19 h 30</span>\n  </span>\n</a></li>',
      specs=[('Encart', 'fond #E2F3EE, rayon 24 px, padding 32 px (20 px ≤ 600 px)'), ('Événement', 'blanc, rayon 16 px, padding 18 px, gap 18 px ; 16 px entre événements'), ('Pastille', '76 × 84 px, rayon 14 px, fond pastel ; jour 30 px gras, mois 16 px gras'), ('Méta', 'icône 18 px + texte 16 px')],
      a11y=['Lieu et horaire : toujours icône + texte.', 'Prévoir un texte complet pour les lecteurs d\'écran si le mois est abrégé.', 'Pas d\'agenda Google intégré : liste HTML.'], used=[('Accueil', 'accueil.html'), ('Agenda', 'agenda.html')], gutenberg='plugin d\'événements (The Events Calendar) avec gabarit de liste sur mesure'),
 dict(id='c-engagement', name="Carte d'engagement", group='Cartes',
      usage="Accueil, section « Nos engagements » : 4 cartes non cliquables.",
      demo='<ul style="list-style: none; margin: 0; padding: 0; max-width: 320px"><li style="position: relative; overflow: hidden; background: #FFEBDD; border-radius: 24px; padding: 32px; display: flex; flex-direction: column; gap: 16px"><span aria-hidden="true" style="position: absolute; top: 24px; right: 28px; width: 20px; height: 20px; border-radius: 50%; background: #FFB3B2"></span><div aria-hidden="true" style="width: 96px; height: 96px; border-radius: 50%; background: #FFFFFF; display: flex; align-items: center; justify-content: center">' + ICON['mega'] + '</div><h4 style="margin: 0; font-size: 26px; line-height: 1.3">Informer</h4><p style="margin: 0">Des informations claires et accessibles sur les NOH.</p></li></ul>',
      code='<ul class="eng-grid">\n  <li class="eng-card">\n    <span class="deco" aria-hidden="true"></span>\n    <div class="eng-icon" aria-hidden="true"><svg>…</svg></div>\n    <h3>Informer</h3>\n    <p>…</p>\n  </li>\n</ul>',
      specs=[('Grille', '4 colonnes, gap 24 px (2 ≤ 1100 px, 1 ≤ 760 px)'), ('Carte', 'rayon 24 px, padding 32 px, gap 16 px, fond pastel'), ('Icône', 'disque blanc 96 px, icône au trait 54 px, trait 1,7'), ('Décor', 'pastilles 20 et 10 px (#FFB3B2, #A9D1F5) en haut à droite')],
      a11y=['Non cliquable ; le lien « Voir toutes nos actions » est placé sous la grille.'], used=[('Accueil', 'accueil.html')], gutenberg='compo « Engagements » : core/columns de core/group'),
 dict(id='c-partenaire', name='Carte partenaire', group='Cartes',
      usage="Pages partenaires : logo ou photo, nom, description, lien externe.",
      demo='<ul class="pt-grid" style="max-width: 340px; grid-template-columns: minmax(0,1fr)"><li class="pt-card"><div class="pt-logo">Logo : Nom du partenaire</div><strong style="font-size: 21px">Nom du partenaire</strong><span>Une ligne de présentation.</span><a href="a-venir.html" style="margin-top: auto">Site de Nom du partenaire</a></li></ul>',
      code='<ul class="pt-grid">\n  <li class="pt-card">\n    <img src="logo.png" alt="">\n    <strong>Nom du partenaire</strong>\n    <span>Une ligne de présentation.</span>\n    <a href="https://…">Site de Nom du partenaire</a>\n  </li>\n</ul>',
      specs=[('Grille', '3 colonnes, gap 20 px (2, puis 1)'), ('Carte', 'blanc, rayon 16 px, padding 22 px, ombre « rest »'), ('Logo', 'zone 96 px de haut, fond #F1F3F5 en maquette')],
      a11y=['Logo décoratif (alt="") car le nom suit ; lien « Site de … » explicite.'], used=[('Entreprises', 'partenaires-entreprises.html'), ('Personnalités', 'partenaires-personnalites.html')], gutenberg='type de contenu « Partenaire » + core/query'),
 dict(id='c-faq', name='Questions fréquentes', group='Contenu',
      usage="Pages FAQ : liste des questions en liens, puis chaque question affichée en clair avec sa réponse. Pas d'accordéon.",
      demo='<nav class="faq-toc" aria-labelledby="g-faq-t" style="margin-bottom: 16px"><h4 id="g-faq-t" style="margin: 0 0 8px; font-size: 22px">Les questions</h4><ol><li><a href="#g-q1">Quelles aides humaines existent ?</a></li></ol></nav><section class="faq-item" aria-labelledby="g-q1" style="margin: 0"><h4 id="g-q1" style="font-size: 22px; line-height: 1.35; margin: 0 0 10px">Quelles aides humaines existent ?</h4><p>Selon la situation, la MDPH peut financer une aide humaine.</p><p><a href="les-aidants.html">Les aidants</a></p></section>',
      code='<nav class="faq-toc" aria-labelledby="faq-toc-t">\n  <h2 id="faq-toc-t">Les questions</h2>\n  <ol><li><a href="#q1">Quelles aides humaines existent ?</a></li></ol>\n</nav>\n<section class="faq-item" aria-labelledby="q1">\n  <h2 id="q1">Quelles aides humaines existent ?</h2>\n  <p>Réponse.</p>\n  <p><a href="/les-aidants">Les aidants</a></p>\n</section>',
      specs=[('Liste', 'fond blanc, rayon 16 px, padding 20 × 24 px, marge basse 32 px'), ('Question', 'carte blanche, rayon 16 px, padding 22 × 24 px, ombre légère ; titre 22 px gras encre')],
      a11y=['Pas de <details> ni d\'accordéon dans le contenu : tout est lisible sans action.'], used=[('Je suis aidant', 'faq-aidant.html')], gutenberg='compo « Question » : core/group + core/heading + core/paragraph (pas core/details)'),
 dict(id='c-champs', name='Champs de formulaire', group='Formulaires',
      usage="Contact, newsletter, adhésion.",
      demo='<form onsubmit="return false" style="max-width: 420px"><div class="fld"><label for="g-nom">Nom (obligatoire)</label><input id="g-nom" type="text" autocomplete="name" required></div><div class="fld" style="margin: 0"><label for="g-sujet">Sujet (obligatoire)</label><select id="g-sujet" required><option value="">Choisissez un sujet</option><option>Adhésion, don, bénévolat</option></select></div></form>',
      code='<div class="fld">\n  <label for="c-nom">Nom (obligatoire)</label>\n  <input id="c-nom" type="text" autocomplete="name" required>\n</div>\n<div class="fld">\n  <label for="c-mail">Adresse e-mail (obligatoire)</label>\n  <input id="c-mail" type="email" autocomplete="email" required\n         aria-describedby="c-mail-err" aria-invalid="true">\n  <p id="c-mail-err" class="fld-error"><svg aria-hidden="true">…</svg>Saisissez une adresse complète, par exemple nom@exemple.fr</p>\n</div>',
      specs=[('Libellé', 'toujours visible au-dessus, gras ; gap 8 px'), ('Champ', 'bordure 2 px #767676 (4,5:1), rayon 12 px, padding 12 × 16 px, hauteur 56 px, largeur 100 %'), ('Focus', 'bordure + contour 3 px #0A5CB0'), ('Espacement', '18 px entre champs')],
      a11y=['« (obligatoire) » dans chaque libellé concerné, et une phrase d\'explication en tête de formulaire.', 'autocomplete sur les données personnelles (name, email, tel).', 'Erreur : icône + texte relié par aria-describedby, jamais la couleur seule ; focus sur le premier champ en erreur.', 'Le placeholder ne remplace jamais le libellé.'], used=[('Nous contacter', 'contact.html')], gutenberg='plugin de formulaires accessible (Gravity Forms en mode accessible, ou formulaire sur mesure)'),
 dict(id='c-newsletter', name='Inscription à la newsletter', group='Formulaires',
      usage="Accueil et Nos Actualités, sur fond pêche.",
      demo='<form onsubmit="return false" style="display: flex; flex-direction: column; gap: 10px; max-width: 560px"><label for="g-nl" style="font-weight: 700">Votre adresse e-mail</label><div class="nl-row"><input id="g-nl" type="email" autocomplete="email" placeholder="nom@exemple.fr" style="flex-grow: 1; min-width: 0; height: 56px; border: 2px solid #767676; border-radius: 12px; padding: 0 16px; font: inherit; color: #1E2B3A; background: #FFFFFF"><button type="submit" class="btn btn-primary" style="min-height: 56px">Je m\'inscris</button></div><p style="margin: 0; font-size: 16px">Votre adresse sert uniquement à l\'envoi de la lettre. <a href="mentions-legales.html">Politique de confidentialité</a></p></form>',
      code='<form>\n  <label for="nl-email">Votre adresse e-mail</label>\n  <div class="nl-row">\n    <input id="nl-email" type="email" autocomplete="email">\n    <button type="submit" class="btn btn-primary">Je m\'inscris</button>\n  </div>\n  <p class="meta">Votre adresse sert uniquement à l\'envoi de la lettre. <a href="/confidentialite">Politique de confidentialité</a></p>\n</form>',
      specs=[('Section', 'fond #FFEBDD, padding 80 px ; 2 colonnes (texte / formulaire), 1 sur mobile'), ('Ligne', 'champ + bouton côte à côte, hauteur 56 px ; empilés ≤ 760 px'), ('Branchement', 'Brevo (formulaire intégré ou API)')],
      a11y=['Message de confirmation ou d\'erreur annoncé (role="status" ou focus sur le message).'], used=[('Accueil', 'accueil.html'), ('Nos Actualités', 'actualites.html')], gutenberg='bloc du plugin Brevo restylé'),
 dict(id='c-onglets', name='Filtres en onglets', group='Navigation',
      usage="Filtrer une liste (actualités : Toutes, Internes, Externes). Ce sont des liens, pas des onglets ARIA.",
      demo='<nav aria-label="Filtrer les actualités (exemple)"><ul class="tabs"><li><a href="actualites.html" class="tab tab-on" aria-current="page">' + ICON['check'] + 'Toutes</a></li><li><a href="actualites.html" class="tab">Internes</a></li><li><a href="actualites.html" class="tab">Externes</a></li></ul></nav>',
      code='<nav aria-label="Filtrer les actualités">\n  <ul class="tabs">\n    <li><a href="/actualites" class="tab tab-on" aria-current="page"><svg aria-hidden="true">…coche…</svg>Toutes</a></li>\n    <li><a href="/actualites/internes" class="tab">Internes</a></li>\n  </ul>\n</nav>\n<p class="meta">9 actualités affichées · page 1 sur 3</p>',
      specs=[('Onglet', 'pilule, hauteur 48 px, padding 8 × 22 px, bordure 2 px #0A5CB0, texte bleu gras ; survol fond #E3F0FC'), ('Actif', 'fond #0A5CB0, texte blanc, coche ; survol #08498C')],
      a11y=['L\'état actif est porté par aria-current et une coche, pas seulement la couleur.', 'Annoncer le nombre de résultats sous les filtres.'], used=[('Nos Actualités', 'actualites.html')], gutenberg='liens de catégories (core/categories restylé) ou bloc sur mesure'),
 dict(id='c-pagination', name='Pagination', group='Navigation',
      usage="Listes longues (actualités).",
      demo='<nav aria-label="Pagination (exemple)"><ul class="pager"><li><span class="pg" aria-disabled="true" style="color: #5B6470; border: 2px solid #B8C0CA; border-radius: 999px; padding: 0 20px">Page précédente</span></li><li><a href="actualites.html" class="pg" aria-current="page" style="background: #0A5CB0; color: #FFFFFF; text-decoration: none">1</a></li><li><a href="actualites.html" class="pg">2</a></li><li><a href="actualites.html" class="btn btn-secondary">Page suivante</a></li></ul></nav>',
      code='<nav aria-label="Pagination">\n  <ul class="pager">\n    <li><span class="pg pg-disabled" aria-disabled="true">Page précédente</span></li>\n    <li class="pg-num"><a href="?page=1" class="pg" aria-current="page">1</a></li>\n    <li class="pg-num"><a href="?page=2" class="pg">2</a></li>\n    <li><a href="?page=2" class="btn btn-secondary">Page suivante</a></li>\n  </ul>\n</nav>',
      specs=[('Numéro', 'cible 48 × 48 px, rayon 12 px, bleu gras ; page en cours fond #0A5CB0, texte blanc'), ('Désactivé', 'texte #5B6470, bordure #B8C0CA, non cliquable'), ('≤ 760 px', 'numéros masqués (.pg-num), seuls « précédente / suivante » restent')],
      a11y=['aria-current="page" sur la page en cours ; « Page précédente / suivante » en toutes lettres.'], used=[('Nos Actualités', 'actualites.html')], gutenberg='core/query-pagination restylé'),
 dict(id='c-partage', name='Partage et copie du lien', group='Actions',
      usage="Fin d'article.",
      demo='<ul class="share"><li><a href="a-venir.html" class="btn btn-soft">Facebook</a></li><li><a href="a-venir.html" class="btn btn-soft">LinkedIn</a></li><li><button type="button" class="btn btn-soft" onclick="var s=document.getElementById(\'g-copy-status\');s.textContent=\'Lien copié\';setTimeout(function(){s.textContent=\'\'},4000)">' + ICON['link'] + 'Copier le lien</button></li></ul><p id="g-copy-status" role="status" style="margin: 8px 0 0; font-size: 16px; font-weight: 700; min-height: 1.6em"></p>',
      code='<h2>Partager cet article</h2>\n<ul class="share">\n  <li><a href="https://www.facebook.com/sharer/…" class="btn btn-soft">Facebook</a></li>\n  <li><button type="button" id="copy-link" class="btn btn-soft"><svg aria-hidden="true">…</svg>Copier le lien</button></li>\n</ul>\n<p id="copy-status" role="status"></p>\n<!-- JS : copie dans le presse-papiers puis écrit « Lien copié » dans #copy-status, vidé après 4 s -->',
      specs=[('Boutons', '.btn .btn-soft, gap 12 px, retour à la ligne'), ('Statut', '16 px gras, hauteur réservée 1,6 em pour éviter un saut de mise en page')],
      a11y=['role="status" : « Lien copié » est annoncé sans déplacer le focus.', 'Nom du réseau en texte, pas seulement son logo.'], used=[('Article', 'article.html')], gutenberg='bloc de partage sur mesure (éviter les scripts tiers des réseaux)'),
 dict(id='c-aide', name='Bloc « Une question ? »', group='Bandeaux',
      usage="Bas des pages de contenu : renvoi vers le contact.",
      demo='<div class="help" style="display: flex; gap: 32px; align-items: center; justify-content: space-between; background: #E2F3EE; border-radius: 24px; padding: 32px 36px; flex-wrap: wrap"><div style="display: flex; flex-direction: column; gap: 8px"><p style="margin: 0; font-size: 32px; line-height: 1.2; color: #006FD6; font-weight: 700">Une question ?</p><p style="margin: 0; font-size: 20px">Notre comité d\'aide aux personnes concernées vous répond.</p></div><a href="contact.html" class="btn btn-primary">Nous contacter</a></div>',
      code='<section aria-labelledby="t-aide">\n  <div class="wrap"><div class="help">\n    <div><h2 id="t-aide">Une question ?</h2><p>…</p></div>\n    <a href="/contact" class="btn btn-primary">Nous contacter</a>\n  </div></div>\n</section>',
      specs=[('Bloc', 'fond #E2F3EE, rayon 24 px, padding 40 × 48 px ; texte à gauche, bouton à droite ; empilés ≤ 760 px'), ('Titre', 'h2 32 px #006FD6')], a11y=['Un seul bouton principal dans le bloc.'],
      used=[('Les démarches', 'les-demarches.html')], gutenberg='compo synchronisé (bloc réutilisable) « Une question ? »'),
 dict(id='c-agir', name='Bandeau « Agir avec nous »', group='Bandeaux',
      usage="Accueil et article : les 4 façons de soutenir l'association.",
      demo='<div style="background: #FFE6E5; border-radius: 16px; padding: 28px; display: flex; flex-direction: column; gap: 20px"><p style="margin: 0; font-size: 36px; line-height: 1.2; color: #006FD6; font-weight: 700">Agir avec nous</p><div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px"><a href="don.html" class="btn btn-primary">Faire un don</a><a href="adherer.html" class="btn btn-secondary">Adhérer</a><a href="devenir-benevole.html" class="btn btn-secondary">Devenir bénévole</a><a href="notre-boutique.html" class="btn btn-secondary">Notre boutique</a></div></div>',
      code='<section aria-labelledby="t-agir" class="band-agir">\n  <div class="wrap">\n    <h2 id="t-agir">Agir avec nous</h2>\n    <p>Chaque geste compte…</p>\n    <p class="info"><svg aria-hidden="true">…i…</svg>Don déductible à 66 % de vos impôts</p>\n    <div class="agir-btns">\n      <a href="/don" class="btn btn-primary">Faire un don</a>\n      <a href="/adherer" class="btn btn-secondary">Adhérer</a>\n      …\n    </div>\n  </div>\n</section>',
      specs=[('Section', 'fond #FFE6E5, padding 88 px'), ('Boutons', 'grille de 4 colonnes égales, gap 16 px (2 ≤ 1100 px, 1 ≤ 760 px) ; un seul principal (don)')],
      a11y=['L\'information fiscale est en texte, l\'icône est aria-hidden.'], used=[('Accueil', 'accueil.html'), ('Article', 'article.html')], gutenberg='compo synchronisé « Agir avec nous »'),
 dict(id='c-don', name='Bloc de don HelloAsso', group='Bandeaux',
      usage="Page Faire un don : on explique les 3 étapes, puis un bouton envoie vers HelloAsso. Aucun paiement sur le site.",
      demo='<div style="background: #FFFFFF; border: 2px solid #CFE5FA; border-radius: 20px; padding: 28px; display: flex; flex-direction: column; gap: 18px; max-width: 560px"><p style="margin: 0; font-size: 22px; font-weight: 700">Votre don en 3 étapes</p><ol style="margin: 0; padding-left: 26px; display: flex; flex-direction: column; gap: 10px"><li>Cliquez sur « Je fais un don sur HelloAsso ».</li><li>Choisissez votre montant sur le formulaire sécurisé.</li><li>Vous recevez la confirmation par e-mail.</li></ol><a href="don.html" class="btn btn-primary" style="align-self: flex-start">Je fais un don sur HelloAsso</a><p style="margin: 0; font-size: 16px">Vous quittez le site pour la plateforme de paiement sécurisée HelloAsso.</p></div>',
      code='<div class="embed">\n  <h3>Votre don en 3 étapes</h3>\n  <ol>…</ol>\n  <a href="https://www.helloasso.com/associations/ouvrir-les-yeux/formulaires/1" class="btn btn-primary">Je fais un don sur HelloAsso</a>\n  <p class="meta">Vous quittez le site d\'Ouvrir Les Yeux pour la plateforme de paiement sécurisée HelloAsso.</p>\n</div>',
      specs=[('Bloc', 'blanc, bordure 2 px #CFE5FA, rayon 20 px, padding 36 px (24 px mobile), gap 22 px'), ('Mise en page', 'texte à gauche, bloc à droite (colonnes 1 / 1,15), empilés ≤ 1100 px')],
      a11y=['Prévenir du changement de site avant le clic.', 'Pas d\'iframe HelloAsso : son formulaire n\'est pas maîtrisé côté accessibilité.'], used=[('Faire un don', 'don.html')], gutenberg='compo « Don HelloAsso » : core/group + core/list + core/button'),
 dict(id='c-pied', name='Pied de page', group='Structure de page',
      usage="Bas de toutes les pages : présentation, adresse, 3 colonnes de liens, liens légaux, réseaux.",
      demo=None,
      code='<footer>\n  <div class="wrap">\n    <div class="foot-grid">\n      <div><img src="logo-oly.png" alt="Ouvrir Les Yeux, pour voir demain"><p>…</p><p class="meta">Adresse</p></div>\n      <nav aria-labelledby="f-noh"><h2 id="f-noh">Les NOH</h2><ul class="foot-list">…</ul></nav>\n      …\n    </div>\n    …liens légaux, « Accessibilité : partiellement conforme », réseaux sociaux…\n  </div>\n</footer>',
      specs=[('Fond', '#E3F0FC, padding 72 px en haut, 32 px en bas'), ('Grille', '1,4 fr + 4 colonnes, gap 40 px ; 2 colonnes ≤ 1100 px, la présentation passe sur toute la largeur ≤ 760 px'), ('Liens', 'encre, soulignés ; survol #0A5CB0 ; titres de colonne h2 20 px')],
      a11y=['Mention « Accessibilité : partiellement conforme » (ou le niveau réel) avec lien vers la déclaration, obligatoire.', 'Réseaux sociaux nommés en texte.'], used=[('Toutes les pages', 'accueil.html')], gutenberg='partie de modèle footer.html'),
]

GROUPS = ['Actions', 'Navigation', 'Structure de page', 'Contenu', 'Cartes', 'Formulaires', 'Bandeaux']


def _table(caption, head, rows, wide=True):
    th = ''.join(f'<th scope="col">{h}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    t = f'<table class="g-table"><caption>{caption}</caption><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
    cls = 'g-wrap' if wide else 'g-wrap g-wrap-s'
    return f'<div class="{cls}" role="region" aria-label="{H.escape(caption)}, tableau défilant" tabindex="0">{t}</div>'


def _code(code, label):
    return f'<p class="g-code-t">{label}</p><pre class="g-code" tabindex="0" aria-label="{H.escape(label)}"><code>{H.escape(code)}</code></pre>'


def guide_main(title_band):
    page_bg = '#FAF8F7'
    by_tok = {k: v for k, v, *_ in COLORS}
    # --- colours
    rows = []
    for k, v, n, u, g in COLORS:
        c1, c2 = contrast(v, page_bg), contrast(v, '#FFFFFF')
        best = f'{fr(c1)}:1 sur le fond · {fr(c2)}:1 sur blanc'
        if g == 'Fonds pastel' or g == 'Surfaces':
            best = f'encre dessus : {fr(contrast("#1E2B3A", v))}:1'
        if k == 'coral':
            best = f'texte blanc dessus : {fr(contrast("#FFFFFF", v), 2)}:1'
        rows.append([f'<span class="g-sw" style="background: {v}" aria-hidden="true"></span>', f'<strong>{H.escape(n)}</strong><br><code>--color-{k}</code>', f'<code>{v}</code>', H.escape(g), H.escape(u), best])
    colours = _table('Couleurs : jeton, valeur, usage et contraste', ['Aperçu', 'Nom et jeton', 'Valeur', 'Famille', 'Usage', 'Contraste'], rows)
    rub = _table('Couleur de fond par rubrique (menu et bandeau de titre)', ['Rubrique', 'Fond', 'Valeur'],
                 [[H.escape(r), f'<span class="g-sw" style="background: {by_tok[t]}; width: 28px; height: 28px" aria-hidden="true"></span> <code>--color-{t}</code>', f'<code>{by_tok[t]}</code>'] for r, t in RUB_COLORS], wide=False)
    forbid = ('<ul class="g-list"><li>Texte blanc sur un fond pastel.</li><li>Bleu #006FD6 pour un texte de moins de 24 px (4,27:1 sur pastel).</li>'
              '<li>Corail d\'origine #FF4948 sous un texte blanc (3,3:1) : décor uniquement.</li><li>Couleur seule pour porter une information (badge, état actif, erreur) : toujours un texte ou une icône en plus.</li></ul>')
    # --- type
    trows = [[f'<code>--fs-{k}</code>', f'{d} px', f'{m} px', fr(lh, 2).rstrip('0').rstrip(','), 'gras' if w == 700 else 'normal',
              f'<span style="font-size: {min(d, 36)}px; line-height: 1.2; font-weight: {w}">Aa</span>', H.escape(u)] for k, d, m, lh, w, u in FONT_SIZES]
    typo = _table('Échelle typographique', ['Jeton', 'Ordinateur', 'Mobile ≤ 760 px', 'Interligne', 'Graisse', 'Aperçu', 'Usage'], trows)
    # --- spacing / radius / shadow
    sp = '<div style="display: flex; flex-wrap: wrap; gap: 16px; align-items: flex-end; margin: 0 0 20px">' + ''.join(
        f'<div style="display: flex; flex-direction: column; align-items: center; gap: 6px; font-size: 16px"><span aria-hidden="true" style="display: block; width: {v}px; height: {v}px; background: #A9D1F5; border-radius: 4px"></span><code>{v}</code></div>' for v in SPACES) + '</div>'
    rad = _table('Rayons d\'arrondi', ['Jeton', 'Valeur', 'Aperçu', 'Usage'],
                 [[f'<code>--radius-{k}</code>', f'{v} px', f'<span aria-hidden="true" style="display: inline-block; width: 56px; height: 40px; background: #CFE5FA; border-radius: {min(v, 20)}px"></span>', H.escape(u)] for k, v, u in RADII], wide=False)
    sha = _table('Ombres', ['Jeton', 'Valeur CSS', 'Aperçu', 'Usage'],
                 [[f'<code>--shadow-{k}</code>', f'<code>{v}</code>', f'<span aria-hidden="true" style="display: inline-block; width: 64px; height: 40px; background: #FFFFFF; border-radius: 10px; box-shadow: {v}"></span>', H.escape(u)] for k, v, u in SHADOWS])
    bp = _table('Points de rupture', ['Écran', 'Largeur', 'Ce qui change'], [[a, b, c] for a, b, c in BREAKPOINTS], wide=False)
    grids = _table('Grilles réutilisables', ['Classe', 'Ordinateur', '≤ 1100 px', '≤ 760 px', 'Gap'], [
        ['<code>.lp-grid</code>, <code>.pt-grid</code>', '3', '2', '1', '20 px'], ['<code>.rel-grid</code>', '4', '2', '1', '20 px'],
        ['<code>.card-grid</code>', '3', '2', '1', '28 px'], ['<code>.eng-grid</code>', '4', '2', '1', '24 px'], ['<code>.act-grid</code> (accueil)', '3', '3', '1', '24 px'],
        ['<code>.agir-btns</code>', '4', '2', '1', '16 px'], ['<code>.two-col</code> (contact)', '1 fr / 1,3 fr', '1', '1', '56 px puis 32 px'],
        ['<code>.layout-b</code> (contenu + colonne)', '1 fr / 380 px', '1', '1', '64 px puis 40 px'], ['<code>.foot-grid</code>', '1,4 fr + 4', '2', '2', '40 px']])

    # --- components
    comps = []
    for g in GROUPS:
        items = [c for c in COMPONENTS if c['group'] == g]
        blocks = []
        for c in items:
            demo = (f'<div class="g-demo"><p class="g-demo-label">Exemple</p>{c["demo"]}</div>' if c['demo']
                    else f'<p class="g-demo-label" style="margin: 0 0 20px">Composant global : voir n\'importe quelle page, par exemple <a href="{c["used"][0][1]}">{H.escape(c["used"][0][0])}</a>.</p>')
            specs = '<ul class="g-list">' + ''.join(f'<li><strong>{H.escape(a)} :</strong> {H.escape(b)}</li>' for a, b in c['specs']) + '</ul>'
            a11y = '<ul class="g-list">' + ''.join(f'<li>{H.escape(x)}</li>' for x in c['a11y']) + '</ul>'
            used = ', '.join(f'<a href="{f}">{H.escape(l)}</a>' for l, f in c['used'])
            blocks.append(f'<article class="g-comp" aria-labelledby="{c["id"]}"><h3 id="{c["id"]}">{H.escape(c["name"])}</h3>'
                          f'<p class="g-use">{H.escape(c["usage"])}</p>{demo}'
                          f'<div class="g-specs"><div><h4>Spécifications</h4>{specs}</div><div><h4>Accessibilité</h4>{a11y}</div></div>'
                          f'<p style="margin: 0 0 8px"><strong>Utilisé dans :</strong> {used}</p>'
                          f'<p style="margin: 0 0 16px"><strong>Intégration WordPress suggérée :</strong> {H.escape(c["gutenberg"])}</p>'
                          + _code(c['code'], f'Structure HTML : {c["name"]}') + '</article>')
        comps.append((g, blocks))

    behaviours = ('<ul class="g-list">'
                  '<li><strong>Sous-menus :</strong> ouverture au clic sur le bouton (aria-expanded passe à true, le panneau perd hidden) ; un seul ouvert ; clic en dehors ou Échap pour fermer, Échap rend le focus au bouton ; l\'entrée ouverte prend le fond #CFE5FA et le trait bas, l\'indicateur passe de « + » à « − » (mobile).</li>'
                  '<li><strong>Menu mobile (≤ 1100 px) :</strong> le bouton « Menu » bascule la classe is-open du menu, aria-expanded, son libellé (« Menu » / « Fermer le menu ») et son icône ; Échap le ferme et rend le focus au bouton.</li>'
                  '<li><strong>Copier le lien :</strong> navigator.clipboard.writeText(location.href), puis « Lien copié » dans la zone role="status", vidée après 4 s.</li>'
                  '<li><strong>Mouvement :</strong> aucun carrousel automatique ; toute animation est coupée avec prefers-reduced-motion: reduce.</li>'
                  '<li><strong>Script de référence :</strong> le code complet (environ 60 lignes, sans dépendance) est en bas de chaque page de la maquette.</li></ul>')
    rules = ('<ul class="g-list"><li><strong>Contraste :</strong> 4,5:1 pour le texte courant, 3:1 pour les titres de 24 px et plus et pour les bordures de composants.</li>'
             '<li><strong>Focus :</strong> contour 3 px #0A5CB0 décalé de 2 px sur tout élément interactif, jamais supprimé (outline: none interdit).</li>'
             '<li><strong>Cibles :</strong> 44 × 44 px minimum pour tout ce qui se clique ou se touche.</li>'
             '<li><strong>Titres :</strong> un seul h1 par page, pas de saut de niveau.</li>'
             '<li><strong>Repères :</strong> header, nav nommées (aria-label), main id="contenu", footer ; lien d\'évitement en premier.</li>'
             '<li><strong>Icônes :</strong> au trait (24 × 24, trait 2 à 2,2 en interface, 1,6 à 1,8 en illustration), aria-hidden="true", toujours accompagnées d\'un texte. Pas d\'émoji.</li>'
             '<li><strong>Images :</strong> jamais de texte dans une image ; alt vide si décorative, sinon alternative courte.</li>'
             '<li><strong>Zoom :</strong> rien ne déborde à 320 px de large ni à 200 % de zoom texte.</li>'
             '<li><strong>Langue :</strong> lang sur &lt;html&gt; et sur chaque passage dans une autre langue.</li></ul>')

    nav_items = [('t-demarrer', 'Démarrer'), ('t-couleurs', 'Couleurs'), ('t-typo', 'Typographie'), ('t-espaces', 'Espacements, rayons, ombres'),
                 ('t-grilles', 'Mise en page et grilles')] + [(f'g-{i}', g) for i, (g, _) in enumerate(comps)] + [('t-comportements', 'Comportements'), ('t-regles', 'Règles d\'accessibilité')]
    side = []
    for a, l in nav_items:
        sub = ''
        if a.startswith('g-'):
            g = l
            sub = '<ol>' + ''.join(f'<li><a href="#{c["id"]}">{H.escape(c["name"])}</a></li>' for c in COMPONENTS if c['group'] == g) + '</ol>'
        side.append(f'<li><a href="#{a}">{H.escape(l)}</a>{sub}</li>')
    sidebar = f'<nav class="g-side" aria-label="Sommaire du guide"><ol>{"".join(side)}</ol></nav>'

    start = ('<section aria-labelledby="t-demarrer"><h2 id="t-demarrer">Démarrer</h2>'
             '<p class="g-lead">Ce guide décrit chaque élément réutilisable de la maquette : couleurs, typographie, espacements, composants, comportements. '
             'Chaque composant montre un exemple réel, ses mesures, ses règles d\'accessibilité, sa structure HTML et une piste d\'intégration dans le thème enfant Gutenberg.</p>'
             '<div class="g-dl"><a class="btn btn-secondary" href="tokens/oly-tokens.json" download>Jetons (JSON, format W3C)</a>'
             '<a class="btn btn-secondary" href="tokens/oly-tokens.css" download>Jetons (variables CSS)</a>'
             '<a class="btn btn-soft" href="systeme-de-design.html">Système de design visuel</a></div>'
             '<ul class="g-list"><li><strong>Police :</strong> Atkinson Hyperlegible 400 et 700 (WOFF2, hébergée sur le site, font-display: swap). La charte prévoit Luciole pour les titres ; cette maquette utilise Atkinson Hyperlegible partout.</li>'
             '<li><strong>Base :</strong> fond #FAF8F7, texte #1E2B3A, 18 px, interligne 1,6, box-sizing: border-box partout.</li>'
             '<li><strong>Conteneur :</strong> .wrap = 1344 px max, marges latérales 48 px (20 px ≤ 760 px). Colonne de lecture .read = 820 px.</li>'
             '<li><strong>Unités :</strong> la maquette est en px ; à l\'intégration, convertir tailles de texte et espacements en rem (base 16 px) pour respecter le zoom navigateur.</li>'
             '<li><strong>Figma :</strong> le fichier JSON suit le format W3C Design Tokens, lisible par le plugin Tokens Studio pour créer les variables et styles ; les pages en ligne peuvent être importées en calques avec un plugin d\'import de page web (par exemple html.to.design).</li></ul></section>')
    body = (start
            + f'<section aria-labelledby="t-couleurs"><h2 id="t-couleurs">Couleurs</h2><p class="g-lead">Une palette pastel, sans bleu nuit. Le texte est toujours en encre, y compris sur les fonds colorés. Contrastes calculés selon WCAG 2.1.</p>{colours}{rub}<h3>Interdits</h3>{forbid}</section>'
            + f'<section aria-labelledby="t-typo"><h2 id="t-typo">Typographie</h2><p class="g-lead">Tailles mesurées sur la maquette. Les titres de section de l\'accueil varient de 32 à 40 px : à l\'intégration, les ramener au jeton h2-section.</p>{typo}</section>'
            + f'<section aria-labelledby="t-espaces"><h2 id="t-espaces">Espacements, rayons, ombres</h2><h3>Échelle d\'espacement</h3><p>Toutes les marges et tous les écarts de la maquette sont pris dans cette échelle. Sections : 72 à 96 px en haut et en bas sur ordinateur, 56 px sur mobile.</p>{sp}{rad}{sha}</section>'
            + f'<section aria-labelledby="t-grilles"><h2 id="t-grilles">Mise en page et grilles</h2>{bp}{grids}<p>Les colonnes sont toujours en <code>minmax(0, 1fr)</code> pour qu\'un mot long ou un champ ne fasse pas déborder la grille.</p></section>'
            + ''.join(f'<section aria-labelledby="g-{i}"><h2 id="g-{i}">Composants : {H.escape(g)}</h2>{"".join(b)}</section>' for i, (g, b) in enumerate(comps))
            + f'<section aria-labelledby="t-comportements"><h2 id="t-comportements">Comportements</h2>{behaviours}</section>'
            + f'<section aria-labelledby="t-regles"><h2 id="t-regles">Règles d\'accessibilité communes</h2>{rules}</section>')
    band = title_band
    return band + f'<div class="wrap" style="padding-top: 48px; padding-bottom: 72px"><div class="g-layout">{sidebar}<div class="g-main">{body}</div></div></div>'
