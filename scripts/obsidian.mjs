// عميل CDP صغير لنسخة Obsidian المعزولة (scripts/obsidian-test.sh).
// الاستعمال:
//   node scripts/obsidian.mjs eval "<js>"            تنفيذ JS في نافذة Obsidian (await مسموح)
//   node scripts/obsidian.mjs shot out.png [w h dpr scroll]   لقطة للنافذة (بحجم محاكى، وتمرير بالبكسل أو بمحدِّد)
//   node scripts/obsidian.mjs shotel "<sel>" out.png [pad]   لقطة لعنصر
//   node scripts/obsidian.mjs styles "<sel>" "<prop,prop>"   القيم المحسوبة لخصائص عنصر
//   node scripts/obsidian.mjs reload                 إعادة تحميل الثيم بعد البناء
//   node scripts/obsidian.mjs open "<path>"          فتح ملاحظة في التبويب الحالي
//   node scripts/obsidian.mjs mode preview|live|source   وضع العرض
//   node scripts/obsidian.mjs scheme dark|light       الوضع الداكن (غسق) أو الفاتح (أصيل)
//   node scripts/obsidian.mjs scroll top|<px>|"<sel>"  تمرير العرض الحالي
//   node scripts/obsidian.mjs key Escape             ضغط مفتاح
//   node scripts/obsidian.mjs winsize <w> <h>        حجم النافذة الفعلية (مع CDP_TITLE لنافذة أخرى)
const PORT = process.env.CDP_PORT || 9339;
const [cmd, ...args] = process.argv.slice(2);
const targets = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json();
// CDP_TITLE يختار نافذة بجزء من عنوانها (الإعدادات تُفتح في نافذة مستقلة في Obsidian 1.14)
const byTitle = process.env.CDP_TITLE && targets.find(t => t.type === 'page' && (t.title || '').includes(process.env.CDP_TITLE));
const page = byTitle || targets.find(t => t.type === 'page' && /app:\/\/obsidian\.md\/index\.html/.test(t.url)) || targets.find(t => t.type === 'page');
if (!page) { console.error('no page'); process.exit(1); }
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
let id = 0; const pending = new Map();
ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); } };
const send = (method, params = {}) => new Promise(res => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async expr => { const r = await send('Runtime.evaluate', { expression: `(async () => { ${expr.includes('return') ? expr : 'return ' + expr} })()`, awaitPromise: true, returnByValue: true });
  if (r.result?.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails.exception?.description || r.result.exceptionDetails));
  return r.result?.result?.value; };
const fs = await import('node:fs');
const sleep = ms => new Promise(r => setTimeout(r, ms));
try {
  if (cmd === 'eval') {
    const v = await evaluate(args[0]); console.log(typeof v === 'string' ? v : JSON.stringify(v, null, 1));
  } else if (cmd === 'shot') {
    const [out, w, h, dpr = 1, scroll] = args;
    if (w) { await send('Emulation.setDeviceMetricsOverride', { width: +w, height: +h, deviceScaleFactor: +dpr, mobile: false }); await sleep(800); }
    // إبعاد المؤشر عن العناصر كي لا تبقى التلميحات وحالات التحويم في اللقطة
    await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: Math.round((+w || 1200) * 0.06), y: Math.round((+h || 800) * 0.7) });
    await evaluate(`document.querySelectorAll('.tooltip').forEach(e=>e.remove()); return 1`).catch(() => 0);
    if (scroll !== undefined) {
      // التمرير داخل جلسة اللقطة نفسها: تغيير الحجم يعيد رسم العرض ويسترجع موضعه
      if (process.env.CDP_TITLE) {} else await evaluate(`const sc=[...app.workspace.getMostRecentLeaf().view.containerEl.querySelectorAll('.markdown-preview-view, .cm-scroller')].find(e=>e.offsetParent!==null); if(sc){ if(/^\\d+$/.test(${JSON.stringify(scroll)})) sc.scrollTop=+${JSON.stringify(scroll)}; else { const e=sc.querySelector(${JSON.stringify(scroll)}); if(e) e.scrollIntoView({block:'start'}); } } await new Promise(r=>setTimeout(r,700)); return 1`);
    }
    const r = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
    fs.writeFileSync(out, Buffer.from(r.result.data, 'base64')); console.log('saved', out);
  } else if (cmd === 'shotel') {
    const [sel, out, pad = 12] = args;
    const b = await evaluate(`const e=document.querySelector(${JSON.stringify(sel)}); if(!e) return null; e.scrollIntoView({block:'center'}); await new Promise(r=>setTimeout(r,300)); const r=e.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height}`);
    if (!b) { console.error('not found', sel); process.exit(1); }
    const r = await send('Page.captureScreenshot', { format: 'png', clip: { x: Math.max(0, b.x - pad), y: Math.max(0, b.y - pad), width: b.w + 2 * pad, height: b.h + 2 * pad, scale: 2 } });
    fs.writeFileSync(out, Buffer.from(r.result.data, 'base64')); console.log('saved', out);
  } else if (cmd === 'hovershot') {
    // hovershot "<sel>" out.png [pad]  تحويم المؤشر فوق عنصر ثم تصويره (أسهم الطيّ تظهر عند التحويم)
    const [sel, out, pad = 40] = args;
    // المحاكاة تفرض الرسم حتى لو كانت النافذة خلف غيرها (Chromium يؤجّل رسم النوافذ المحجوبة)
    await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 2, mobile: false }); await sleep(900);
    const b = await evaluate(`const e=document.querySelector(${JSON.stringify(sel)}); if(!e) return null; e.scrollIntoView({block:'center'}); await new Promise(r=>setTimeout(r,300)); const r=e.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height}`);
    if (!b) { console.error('not found', sel); process.exit(1); }
    await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: Math.round(b.x + b.w * 0.8), y: Math.round(b.y + b.h / 2) });
    await sleep(500);
    const r = await send('Page.captureScreenshot', { format: 'png', clip: { x: Math.max(0, b.x - +pad), y: Math.max(0, b.y - 10), width: b.w + 2 * +pad, height: b.h + 20, scale: 2 } });
    fs.writeFileSync(out, Buffer.from(r.result.data, 'base64')); console.log('saved', out);
  } else if (cmd === 'styles') {
    const [sel, props] = args;
    const v = await evaluate(`const e=document.querySelector(${JSON.stringify(sel)}); if(!e) return null; const cs=getComputedStyle(e); return Object.fromEntries(${JSON.stringify(props.split(','))}.map(p=>[p,cs.getPropertyValue(p.trim())]))`);
    console.log(JSON.stringify(v, null, 1));
  } else if (cmd === 'reload') {
    // يعيد قراءة theme.css بعد البناء: Obsidian يخزّن نص الثيم في csscache، فنمسحه ثم نطلب التحميل
    const v = await evaluate(`app.customCss.csscache.clear(); app.customCss.requestLoadTheme(); await new Promise(r=>setTimeout(r,1000)); return [app.customCss.theme, app.customCss.styleEl.textContent.length]`);
    console.log(JSON.stringify(v));
  } else if (cmd === 'open') {
    const v = await evaluate(`const f=app.vault.getAbstractFileByPath(${JSON.stringify(args[0])}); if(!f) return 'not found'; await app.workspace.getLeaf(false).openFile(f); await new Promise(r=>setTimeout(r,700)); return f.path`);
    console.log(v);
  } else if (cmd === 'winsize') {
    // winsize <w> <h>  يغيّر حجم النافذة الفعلية (يبقى بعد إغلاق الاتصال)
    const [w, h] = args.map(Number);
    const v = await evaluate(`window.resizeTo(${w}, ${h}); await new Promise(r=>setTimeout(r,600)); return [window.innerWidth, window.innerHeight]`);
    console.log(JSON.stringify(v));
  } else if (cmd === 'key') {
    // key Escape|Enter|...  ضغط مفتاح حقيقي عبر CDP
    const key = args[0];
    const codes = { Escape: 27, Enter: 13, Tab: 9 };
    for (const type of ['keyDown', 'keyUp']) await send('Input.dispatchKeyEvent', { type, key, code: key, windowsVirtualKeyCode: codes[key] || 0 });
    console.log('key', key);
  } else if (cmd === 'mode') {
    // mode preview|live|source
    const m = args[0];
    const v = await evaluate(`const l=app.workspace.getMostRecentLeaf(); const s=l.getViewState(); if(s.type!=='markdown') return s.type; s.state.mode = ${JSON.stringify(m)}==='preview' ? 'preview' : 'source'; s.state.source = ${JSON.stringify(m)}==='source'; await l.setViewState(s); await new Promise(r=>setTimeout(r,600)); return l.getViewState().state`);
    console.log(JSON.stringify(v));
  } else if (cmd === 'scheme') {
    // scheme dark|light
    const v = await evaluate(`app.changeTheme(${JSON.stringify(args[0] === 'light' ? 'moonstone' : 'obsidian')}); await new Promise(r=>setTimeout(r,600)); return document.body.classList.contains('theme-dark') ? 'dark' : 'light'`);
    console.log(v);
  } else if (cmd === 'scroll') {
    // scroll "<css selector of target inside the view>"  أو  scroll top|<pixels>
    const t = args[0];
    const v = await evaluate(`const sc=[...app.workspace.getMostRecentLeaf().view.containerEl.querySelectorAll('.markdown-preview-view, .cm-scroller')].find(e=>e.offsetParent!==null); if(!sc) return 'no scroller'; if(${JSON.stringify(t)}==='top'){sc.scrollTop=0; return 0;} if(/^\\d+$/.test(${JSON.stringify(t)})){sc.scrollTop=+${JSON.stringify(t)}; await new Promise(r=>setTimeout(r,400)); return sc.scrollTop;} const e=sc.querySelector(${JSON.stringify(t)}); if(!e) return 'no target'; e.scrollIntoView({block:'start'}); await new Promise(r=>setTimeout(r,500)); return sc.scrollTop`);
    console.log(v);
  } else { console.error('commands: eval | shot | shotel | styles | reload | open | mode | scheme | scroll'); process.exit(2); }
} finally { ws.close(); }
