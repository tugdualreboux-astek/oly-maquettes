// Figma Plugin API renderer (runs inside use_figma). Prepended with:
//   const SETUP = true|false; const PAGE = 'Ordinateur — 1440'; const SRC = 'https://…/figma/B1-1440.json';
// SRC holds [{sec: 'Les NOH', items: [{n: 'Frame name', d: {w, h, bg, svgs, tree}}]}] produced by extract.js.
const PALETTE = [
  ['Texte/Encre', '#1E2B3A'], ['Texte/Bleu OLY (titres ≥ 24 px)', '#006FD6'], ['Texte/Bleu lien', '#0A5CB0'], ['Texte/Bleu lien survol', '#08498C'],
  ['Texte/Gris désactivé', '#5B6470'], ['Action/Corail bouton', '#D93A39'], ['Action/Corail survol', '#B92F2E'], ['Accent/Canard', '#015C73'],
  ['Fond/Bleu pastel', '#E3F0FC'], ['Fond/Bleu moyen', '#CFE5FA'], ['Fond/Bleu ciel', '#A9D1F5'], ['Fond/Rose', '#FFE6E5'], ['Fond/Menthe', '#E2F3EE'],
  ['Fond/Pêche', '#FFEBDD'], ['Fond/Page', '#FAF8F7'], ['Fond/Blanc', '#FFFFFF'], ['Bordure/Champ', '#767676'], ['Bordure/Tableau', '#B8C0CA'],
  ['Bordure/Filet', '#D9DEE5'], ['Bordure/Filet de liste', '#E6E9ED'], ['Décor/Rose', '#FFB3B2'], ['Décor/Corail charte', '#FF4948']];
const t0 = Date.now();
const errors = [];
let SECS;
try { SECS = await (await fetch(SRC)).json(); }
catch (e) { return { fetchError: String(e).slice(0, 300) }; }
const hex2rgb = (h) => ({ r: parseInt(h.slice(1, 3), 16) / 255, g: parseInt(h.slice(3, 5), 16) / 255, b: parseInt(h.slice(5, 7), 16) / 255 });

// --- pages, variables, logo
let logoComp = figma.currentPage.findOne(n => n.type === 'COMPONENT' && n.name === 'Logo OLY');
if (!logoComp && SETUP) {
  await figma.loadFontAsync({ family: 'Inter', style: 'Bold' });
  logoComp = figma.createComponent();
  logoComp.name = 'Logo OLY'; logoComp.resize(560, 198); logoComp.x = 0; logoComp.y = 0;
  logoComp.fills = [{ type: 'SOLID', color: { r: 0.89, g: 0.94, b: 0.99 } }];
  logoComp.description = "Coller ici l'image img/logo-oly.png (remplissage image, mode Ajuster) puis supprimer le texte : le logo se met à jour sur tous les écrans.";
  const lt = figma.createText(); logoComp.appendChild(lt);
  lt.fontName = { family: 'Inter', style: 'Bold' }; lt.characters = 'LOGO OLY'; lt.fontSize = 64;
  lt.x = (560 - lt.width) / 2; lt.y = (198 - lt.height) / 2; lt.constraints = { horizontal: 'SCALE', vertical: 'SCALE' };
}
if (SETUP) figma.root.children[0].name = 'Ressources';
let coll = (await figma.variables.getLocalVariableCollectionsAsync()).find(c => c.name === 'OLY — Couleurs');
const vmap = {};
if (!coll && SETUP) {
  coll = figma.variables.createVariableCollection('OLY — Couleurs');
  for (const [n, h] of PALETTE) {
    const v = figma.variables.createVariable(n, coll, 'COLOR');
    v.setValueForMode(coll.modes[0].modeId, hex2rgb(h));
    v.scopes = ['ALL_FILLS', 'STROKE_COLOR', 'EFFECT_COLOR'];
    v.description = h;
    vmap[h] = v;
  }
} else if (coll) {
  for (const id of coll.variableIds) { const v = await figma.variables.getVariableByIdAsync(id); if (v && v.description) vmap[v.description] = v; }
}
let page = figma.root.children.find(p => p.name === PAGE);
if (!page) { page = figma.createPage(); page.name = PAGE; }
await figma.setCurrentPageAsync(page);

// --- fonts
let fam = 'Atkinson Hyperlegible';
const styles = ['Regular', 'Bold', 'Italic', 'Bold Italic'];
try { for (const s of styles) await figma.loadFontAsync({ family: fam, style: s }); }
catch (e) { fam = 'Inter'; for (const s of styles) await figma.loadFontAsync({ family: fam, style: s }); }
const font = (w, i) => ({ family: fam, style: w >= 700 ? (i ? 'Bold Italic' : 'Bold') : (i ? 'Italic' : 'Regular') });

function paint(h) {
  if (!h) return null;
  let p = { type: 'SOLID', color: hex2rgb(h) };
  if (h.length > 7) p.opacity = Math.min(1, parseInt(h.slice(7), 10) / 100);
  const v = vmap[h.slice(0, 7)];
  if (v && h.length === 7) p = figma.variables.setBoundVariableForPaint(p, 'color', v);
  return p;
}

function build(n, parent, svgs) {
  try {
    if ('t' in n) {
      const [fs, fw, lh, col, al, it, ul] = n.s;
      const t = figma.createText();
      parent.appendChild(t);
      t.fontName = font(fw, it);
      t.characters = n.t;
      t.fontSize = fs;
      t.lineHeight = { unit: 'PIXELS', value: lh };
      t.fills = [paint(col || '#1E2B3A')];
      t.textAlignHorizontal = { L: 'LEFT', C: 'CENTER', R: 'RIGHT' }[al];
      if (ul) t.textDecoration = 'UNDERLINE';
      for (const [a, b, w, c, u, i, s] of (n.runs || [])) {
        t.setRangeFontName(a, b, font(w, i));
        if (c) t.setRangeFills(a, b, [paint(c)]);
        t.setRangeTextDecoration(a, b, u ? 'UNDERLINE' : 'NONE');
        if (s) t.setRangeFontSize(a, b, s);
      }
      if (n.h > lh * 1.5) { t.textAutoResize = 'HEIGHT'; t.resize(Math.max(n.w, 4), n.h); t.textAutoResize = 'HEIGHT'; }
      else t.textAutoResize = 'WIDTH_AND_HEIGHT';
      t.x = n.x; t.y = n.y;
      if (n.h <= lh * 1.5 && al === 'C') t.x = n.x + (n.w - t.width) / 2;
      if (n.h <= lh * 1.5 && al === 'R') t.x = n.x + n.w - t.width;
      t.name = n.t.slice(0, 40);
      return;
    }
    if ('v' in n) {
      const s = figma.createNodeFromSvg(svgs[n.v]);
      parent.appendChild(s);
      s.resize(Math.max(n.w, 1), Math.max(n.h, 1));
      s.x = n.x; s.y = n.y; s.name = 'Icône';
      return;
    }
    if ('i' in n) {
      const r = logoComp ? logoComp.createInstance() : figma.createRectangle();
      parent.appendChild(r);
      r.resize(n.w, n.h); r.x = n.x; r.y = n.y; r.name = 'Logo OLY';
      if (!logoComp) r.fills = [paint('#CFE5FA')];
      return;
    }
    const f = figma.createFrame();
    parent.appendChild(f);
    f.name = n.f; f.resize(Math.max(n.w, 1), Math.max(n.h, 1)); f.x = n.x; f.y = n.y;
    f.fills = n.bg ? [paint(n.bg)] : [];
    f.clipsContent = !!n.clip;
    if (n.r !== undefined) {
      if (Array.isArray(n.r)) { [f.topLeftRadius, f.topRightRadius, f.bottomRightRadius, f.bottomLeftRadius] = n.r; }
      else f.cornerRadius = n.r;
    }
    if (n.b) {
      if (Array.isArray(n.b[0])) {
        const [ws, cs] = n.b; const c = cs.find(Boolean);
        f.strokes = [paint(c)]; f.strokeAlign = 'INSIDE';
        f.strokeTopWeight = cs[0] ? ws[0] : 0; f.strokeRightWeight = cs[1] ? ws[1] : 0;
        f.strokeBottomWeight = cs[2] ? ws[2] : 0; f.strokeLeftWeight = cs[3] ? ws[3] : 0;
      } else { f.strokes = [paint(n.b[1])]; f.strokeWeight = n.b[0]; f.strokeAlign = 'INSIDE'; }
    }
    if (n.sh) {
      const c = hex2rgb(n.sh[0]); const a = n.sh[0].length > 7 ? parseInt(n.sh[0].slice(7), 10) / 100 : 1;
      f.effects = [{ type: 'DROP_SHADOW', color: { ...c, a }, offset: { x: n.sh[1], y: n.sh[2] }, radius: n.sh[3], spread: 0, visible: true, blendMode: 'NORMAL' }];
    }
    for (const c of (n.c || [])) build(c, f, svgs);
  } catch (e) { errors.push(String(e).slice(0, 120) + ' @ ' + (n.f || n.t || n.v)); }
}

let y = 0;
for (const c of page.children) y = Math.max(y, c.y + c.height + 400);
const created = [];
for (const { sec, items } of SECS) {
  const section = figma.createSection();
  section.name = sec; section.x = 0; section.y = y;
  let x = 120, maxH = 0;
  for (const { n, d } of items) {
    const root = figma.createFrame();
    section.appendChild(root);
    root.name = n; root.resize(d.w, d.h); root.x = x; root.y = 160;
    root.fills = [paint(d.bg || '#FAF8F7')]; root.clipsContent = true;
    for (const c of d.tree) build(c, root, d.svgs);
    const only = root.children.length === 1 && root.children[0].type === 'FRAME' && root.children[0].width === d.w ? root.children[0] : null;
    if (only) { for (const k of [...only.children]) { root.appendChild(k); k.y += only.y; k.x += only.x; } only.remove(); }
    created.push({ id: root.id, name: n, nodes: root.findAll(() => true).length });
    x += d.w + 160; maxH = Math.max(maxH, d.h);
  }
  section.resizeWithoutConstraints(x - 40, maxH + 280);
  y += maxH + 280 + 400;
}
return { page: page.id, font: fam, logo: !!logoComp, variables: Object.keys(vmap).length, ms: Date.now() - t0, frames: created.length, nodes: created.reduce((a, c) => a + c.nodes, 0), created: created.map(c => c.id + ' ' + c.name), errors: errors.slice(0, 12), errorCount: errors.length };
