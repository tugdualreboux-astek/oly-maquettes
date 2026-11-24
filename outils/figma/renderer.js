// Figma Plugin API renderer (runs inside use_figma). Prepended with:
//   const SETUP = true|false; const PAGE = 'Ordinateur — 1440';
//   const COMPS = [{n: 'En-tête — Ordinateur', d: {w, h, svgs, tree}}]   (shared header/footer, built once as components)
//   const SECS = [{sec: 'Section name', items: [{n: 'Frame name', d: {w, h, bg, svgs, tree}}]}]
// In trees, {k: 'Component name', x, y} places an instance of a shared component (built by pack.py).
const PALETTE = [
  ['Texte/Encre', '#1E2B3A'], ['Texte/Bleu OLY (titres ≥ 24 px)', '#006FD6'], ['Texte/Bleu lien', '#0A5CB0'], ['Texte/Bleu lien survol', '#08498C'],
  ['Texte/Gris désactivé', '#5B6470'], ['Action/Corail bouton', '#D93A39'], ['Action/Corail survol', '#B92F2E'], ['Accent/Canard', '#015C73'],
  ['Fond/Bleu pastel', '#E3F0FC'], ['Fond/Bleu moyen', '#CFE5FA'], ['Fond/Bleu ciel', '#A9D1F5'], ['Fond/Rose', '#FFE6E5'], ['Fond/Menthe', '#E2F3EE'],
  ['Fond/Pêche', '#FFEBDD'], ['Fond/Page', '#FAF8F7'], ['Fond/Blanc', '#FFFFFF'], ['Bordure/Champ', '#767676'], ['Bordure/Tableau', '#B8C0CA'],
  ['Bordure/Filet', '#D9DEE5'], ['Bordure/Filet de liste', '#E6E9ED'], ['Décor/Rose', '#FFB3B2'], ['Décor/Corail charte', '#FF4948']];
const t0 = Date.now();
// Decode the compact positional format produced by pack.py.
function dec(a) {
  switch (a[0]) {
    case 0: return { f: a[1], x: a[2], y: a[3], w: a[4], h: a[5], bg: a[6] || null, r: a[7] || undefined, b: a[8] || null, sh: a[9] || null, clip: a[10], c: a[11].map(dec) };
    case 1: return { t: a[1], x: a[2], y: a[3], w: a[4], h: a[5], s: ST[a[6]], runs: a[7] };
    case 2: return { v: a[1], x: a[2], y: a[3], w: a[4], h: a[5] };
    case 3: return { i: 1, x: a[1], y: a[2], w: a[3], h: a[4] };
    default: return { k: a[1], x: a[2], y: a[3] };
  }
}
for (const blk of [...COMPS.map(c => c.d), ...SECS.flatMap(s => s.items.map(i => i.d))]) blk.tree = blk.tree.map(dec);
const errors = [];
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
  lt.fontName = { family: 'Inter', style: 'Bold' }; lt.characters = 'LOGO OLY'; lt.fontSize = 20;
  lt.x = (560 - lt.width) / 2; lt.y = (198 - lt.height) / 2; lt.constraints = { horizontal: 'SCALE', vertical: 'SCALE' };
}
if (SETUP) figma.root.children[0].name = 'Ressources';
// Placeholder text of the logo must stay readable once the instances are scaled down.
const lt0 = logoComp && logoComp.findOne(n => n.type === 'TEXT');
if (lt0 && lt0.fontSize > 20) { await figma.loadFontAsync(lt0.fontName); lt0.fontSize = 20; lt0.x = (560 - lt0.width) / 2; lt0.y = (198 - lt0.height) / 2; }
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
const compByName = {};
for (const c of figma.currentPage.findAllWithCriteria({ types: ['COMPONENT'] })) compByName[c.name] = c;
let page = figma.root.children.find(p => p.name === PAGE);

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
    if ('k' in n) {
const inst = compByName[n.k].createInstance();
parent.appendChild(inst); inst.x = n.x; inst.y = n.y;
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

// Shared components on the first page (Ressources), in a row under the logo.
let cx = 0;
for (const c of figma.currentPage.children) if (c.y >= 300) cx = Math.max(cx, c.x + c.width + 120);
for (const { n, d } of COMPS) {
  const holder = figma.createFrame(); holder.resize(d.w, d.h); holder.fills = [];
  for (const c of d.tree) build(c, holder, d.svgs);
  const node = holder.children[0];
  figma.currentPage.appendChild(node); holder.remove();
  const comp = figma.createComponentFromNode(node);
  comp.name = n; comp.x = cx; comp.y = 300; cx += comp.width + 120;
  compByName[n] = comp;
}
if (!page) { page = figma.createPage(); page.name = PAGE; }
await figma.setCurrentPageAsync(page);
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
    created.push({ id: root.id, name: n });
    x += d.w + 160; maxH = Math.max(maxH, d.h);
  }
  section.resizeWithoutConstraints(x - 40, maxH + 280);
  y += maxH + 280 + 400;
}
const shot = await figma.getNodeByIdAsync(created[created.length > 1 ? 1 : 0].id);
await shot.screenshot({ scale: 0.25 });
return { page: page.id, font: fam, comps: Object.keys(compByName), variables: Object.keys(vmap).length, ms: Date.now() - t0, created, errors: errors.slice(0, 12), errorCount: errors.length };
