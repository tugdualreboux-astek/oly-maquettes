// Flattens a rendered page of the prototype into a compact layout tree for the Figma renderer.
// Usage: node extract.js <baseUrl> <outDir> <width> <page.html> [...]
// Output per page: <outDir>/<page>-<width>.json  { w, h, title, svgs:[...], tree }
// Node format (short keys to fit in one use_figma call):
//   frame: {f:name, x,y,w,h, bg, r, b:[w,color], sh, clip, c:[...]}
//   text : {t:text, x,y,w,h, s:[fs,fw,lh,color,align,italic,underline], runs:[[start,end,fw,color,underline,italic]]}
//   svg  : {v:svgIndex, x,y,w,h}
//   image: {i:'logo', x,y,w,h}
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const [base, outDir, width, ...pages] = process.argv.slice(2);

function extract() {
  const hex = (c) => {
    const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
    if (p.length === 4 && p[3] === 0) return null;
    const h = '#' + p.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
    return p.length === 4 && p[3] < 1 ? h + Math.round(p[3] * 100) : h;
  };
  const R = (v) => Math.round(v);
  const svgs = [], svgIdx = new Map();
  const LAND = new Set(['HEADER', 'NAV', 'MAIN', 'FOOTER', 'SECTION', 'ARTICLE', 'ASIDE', 'FORM', 'UL', 'OL', 'LI', 'FIELDSET', 'TABLE', 'TR']);
  const visible = (el, cs, rc) => cs.display !== 'none' && cs.visibility !== 'hidden' && +cs.opacity > 0 && !(rc.width <= 1 || rc.height <= 1) && rc.right > 0 && rc.left < innerWidth + 2;
  const isInline = (n) => n.nodeType === 3 || (n.nodeType === 1 && n.tagName !== 'svg' && n.tagName !== 'IMG' && getComputedStyle(n).display === 'inline' && [...n.childNodes].every(isInline));
  const textStyle = (cs) => {
    const lh = cs.lineHeight === 'normal' ? +cs.fontSize.replace('px', '') * 1.25 : +cs.lineHeight.replace('px', '');
    return [+cs.fontSize.replace('px', ''), +cs.fontWeight >= 600 ? 700 : 400, R(lh * 10) / 10, hex(cs.color), { left: 'L', start: 'L', center: 'C', right: 'R', end: 'R' }[cs.textAlign] || 'L', cs.fontStyle === 'italic' ? 1 : 0, cs.textDecorationLine.includes('underline') ? 1 : 0];
  };
  const name = (el) => {
    const lab = el.getAttribute('aria-label') || (el.getAttribute('aria-labelledby') && document.getElementById(el.getAttribute('aria-labelledby'))?.textContent.trim());
    const cls = (el.className && typeof el.className === 'string') ? el.className.split(' ')[0] : '';
    return (el.tagName.toLowerCase() + (cls ? '.' + cls : '') + (lab ? ' — ' + lab.slice(0, 40) : '')).slice(0, 60);
  };
  // Collect text of a pure-inline element as one text node with style runs.
  function inlineText(el, ox, oy) {
    let text = ''; const runs = [];
    const base = getComputedStyle(el); const bs = textStyle(base);
    const walk = (n) => {
      if (n.nodeType === 3) {
        let s = n.textContent.replace(/\s+/g, ' ');
        if (text.endsWith(' ') || text.endsWith('\n') || text === '') s = s.replace(/^ /, '');
        if (!s) return;
        const cs = getComputedStyle(n.parentElement); const st = textStyle(cs);
        const start = text.length; text += s;
        if (st[1] !== bs[1] || st[3] !== bs[3] || st[6] !== bs[6] || st[5] !== bs[5] || st[0] !== bs[0]) runs.push([start, text.length, st[1], st[3], st[6], st[5], st[0]]);
      } else if (n.nodeType === 1) {
        if (n.tagName === 'BR') { text = text.replace(/ $/, '') + '\n'; return; }
        if (getComputedStyle(n).display === 'none') return;
        n.childNodes.forEach(walk);
      }
    };
    el.childNodes.forEach(walk);
    text = text.replace(/ $/, '');
    if (!text.trim()) return null;
    const rg = document.createRange(); rg.selectNodeContents(el); const rc = rg.getBoundingClientRect();
    const node = { t: text, x: R(rc.left - ox), y: R(rc.top - oy), w: R(rc.width) + 2, h: R(rc.height), s: bs };
    if (runs.length) node.runs = runs;
    return node;
  }
  function walk(el, ox, oy) {
    const out = [];
    for (const ch of el.childNodes) {
      if (ch.nodeType === 3) {
        const s = ch.textContent.replace(/\s+/g, ' ').trim(); if (!s) continue;
        const rg = document.createRange(); rg.selectNodeContents(ch); const rc = rg.getBoundingClientRect();
        if (rc.width < 1) continue;
        out.push({ t: s, x: R(rc.left - ox), y: R(rc.top - oy), w: R(rc.width) + 2, h: R(rc.height), s: textStyle(getComputedStyle(el)) });
        continue;
      }
      if (ch.nodeType !== 1) continue;
      if (ch.matches('script,style,template,.proto-bar,.skip,[hidden]')) continue;
      const cs = getComputedStyle(ch), rc = ch.getBoundingClientRect();
      if (!visible(ch, cs, rc)) continue;
      const x = R(rc.left - ox), y = R(rc.top - oy), w = R(rc.width), h = R(rc.height);
      if (ch.tagName === 'svg') {
        const c = ch.cloneNode(true); const col = hex(cs.color) || '#1E2B3A';
        c.setAttribute('width', w); c.setAttribute('height', h); c.removeAttribute('style'); c.removeAttribute('aria-hidden'); c.removeAttribute('class');
        let s = c.outerHTML.replace(/currentColor/g, col.slice(0, 7));
        if (!/fill=/.test(s.slice(0, s.indexOf('>')))) s = s.replace('<svg', '<svg fill="none"');
        if (!svgIdx.has(s)) { svgIdx.set(s, svgs.length); svgs.push(s); }
        out.push({ v: svgIdx.get(s), x, y, w, h }); continue;
      }
      if (ch.tagName === 'IMG') { out.push({ i: 'logo', x, y, w, h }); continue; }
      if (ch.tagName === 'INPUT' || ch.tagName === 'SELECT' || ch.tagName === 'TEXTAREA') {
        const f = { f: ch.tagName.toLowerCase() + (ch.id ? '#' + ch.id : ''), x, y, w, h, bg: hex(cs.backgroundColor) };
        const bw = +cs.borderTopWidth.replace('px', ''); if (bw) f.b = [bw, hex(cs.borderTopColor)];
        const r = +cs.borderTopLeftRadius.replace('px', ''); if (r) f.r = r;
        const val = ch.tagName === 'SELECT' ? ch.options[ch.selectedIndex]?.text : (ch.value || ch.placeholder);
        if (val) { const st = textStyle(cs); if (!ch.value && ch.placeholder) st[3] = '#5B6470'; f.c = [{ t: val, x: +cs.paddingLeft.replace('px', '') + bw, y: R((h - st[2]) / 2), w: w - 60, h: st[2], s: st }]; }
        if (ch.type === 'checkbox') { f.r = 4; delete f.c; }
        out.push(f); continue;
      }
      const bg = hex(cs.backgroundColor);
      const bws = ['Top', 'Right', 'Bottom', 'Left'].map(sd => +cs['border' + sd + 'Width'].replace('px', ''));
      const bcs = ['Top', 'Right', 'Bottom', 'Left'].map(sd => hex(cs['border' + sd + 'Color']));
      const hasB = bws.some(v => v > 0) && bcs.some(Boolean);
      const sh = cs.boxShadow !== 'none' ? cs.boxShadow : null;
      const paints = bg || hasB || sh;
      const pureInline = [...ch.childNodes].length && [...ch.childNodes].every(isInline) && ch.textContent.trim();
      if (!paints && !LAND.has(ch.tagName) && cs.display === 'inline' && pureInline) continue; // handled by parent inline text
      if (paints || LAND.has(ch.tagName) || cs.position === 'absolute') {
        const f = { f: name(ch), x, y, w, h };
        if (bg) f.bg = bg;
        if (hasB) {
          const same = bws.every(v => v === bws[0]) && bcs.every(c => c === bcs[0]);
          f.b = same ? [bws[0], bcs[0]] : [bws, bcs];
        }
        const rad = ['TopLeft', 'TopRight', 'BottomRight', 'BottomLeft'].map(k => +cs['border' + k + 'Radius'].replace('px', '').split(' ')[0] || 0).map(v => Math.min(v, R(Math.min(w, h) / 2)));
        if (rad.some(Boolean)) f.r = rad.every(v => v === rad[0]) ? rad[0] : rad;
        if (sh) { const m = sh.match(/rgba?\([^)]+\)\s+(-?\d+)px\s+(-?\d+)px\s+(\d+)px/); if (m) f.sh = [hex(sh.match(/rgba?\([^)]+\)/)[0]), +m[1], +m[2], +m[3]]; }
        if (cs.overflow === 'hidden' && rad.some(Boolean)) f.clip = 1;
        if (pureInline) { const tn = inlineText(ch, rc.left, rc.top); f.c = tn ? [tn] : []; }
        else f.c = walk(ch, rc.left, rc.top);
        if (!paints && !f.c.length) continue;
        out.push(f);
      } else if (pureInline) {
        const tn = inlineText(ch, ox, oy); if (tn) out.push(tn);
      } else {
        out.push(...walk(ch, ox, oy));
      }
    }
    return out;
  }
  const root = document.body;
  const pageBg = hex(getComputedStyle(document.querySelector('body > div') || root).backgroundColor) || '#FAF8F7';
  return { w: innerWidth, h: R(document.documentElement.scrollHeight), title: document.title, bg: pageBg, svgs, tree: walk(root, 0, 0) };
}

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROME || undefined });
  const page = await browser.newPage({ viewport: { width: +width, height: 900 } });
  for (const p of pages) {
    const [file, state] = p.split('#');
    await page.goto(base + file);
    await page.addStyleTag({ content: '.proto-bar{display:none !important}' });
    if (state === 'menu') await page.click('button.nav-btn[aria-controls="panel-noh"]');
    if (state === 'mobilemenu') { await page.click('.menu-toggle'); }
    await page.evaluate(() => document.fonts.ready);
    const data = await page.evaluate(extract);
    const out = path.join(outDir, `${file.replace('.html', '')}${state ? '-' + state : ''}-${width}.json`);
    fs.writeFileSync(out, JSON.stringify(data));
    console.log(out, JSON.stringify(data).length, 'chars', data.h, 'px high', data.svgs.length, 'svgs');
  }
  await browser.close();
})();
