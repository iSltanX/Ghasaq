// تصدير متغيرات Figma لثيم غسق.
// يُشغَّل داخل ملف Figma عبر أداة use_figma في Figma MCP (واجهة REST للمتغيرات خاصة بخطة Enterprise).
// الناتج JSON مضغوط يُحفظ كما هو في tokens/figma.json، ومنه يولّد scripts/build_tokens.py الملف src/tokens.css.
//
// الصيغة:
// { "file": "<key>", "exportedAt": "<iso>", "collections": [
//     { "name": "Theme", "modes": ["غسق","أصيل"], "vars": [
//         [name, type, valuesByMode[], description, webCodeSyntax], ... ] } ] }
// القيمة إما لون "#RRGGBB" أو "#RRGGBBAA"، أو رقم، أو نص، أو مرجع "@Collection:name".

const hex = c => {
  const h = x => Math.round(x * 255).toString(16).padStart(2, '0').toUpperCase();
  return '#' + h(c.r) + h(c.g) + h(c.b) + (c.a !== undefined && c.a < 1 ? h(c.a) : '');
};
const cols = await figma.variables.getLocalVariableCollectionsAsync();
const vars = await figma.variables.getLocalVariablesAsync();
const byId = Object.fromEntries(vars.map(v => [v.id, v]));
const colName = Object.fromEntries(cols.map(c => [c.id, c.name]));
const round = x => (typeof x === 'number' ? +x.toFixed(4) : x);
const out = { file: figma.fileKey || 'w39BycohJtGzAGt0ycPoDT', exportedAt: new Date().toISOString(), collections: [] };
for (const c of cols) {
  const entry = { name: c.name, modes: c.modes.map(m => m.name), vars: [] };
  for (const id of c.variableIds) {
    const v = byId[id];
    const values = c.modes.map(m => {
      const val = v.valuesByMode[m.modeId];
      if (val && typeof val === 'object' && val.type === 'VARIABLE_ALIAS') { const t = byId[val.id]; return '@' + colName[t.variableCollectionId] + ':' + t.name; }
      if (v.resolvedType === 'COLOR') return hex(val);
      return round(val);
    });
    entry.vars.push([v.name, v.resolvedType, values, v.description || '', (v.codeSyntax && v.codeSyntax.WEB) || '']);
  }
  out.collections.push(entry);
}
// أنماط النص: العائلة والوزن والحجم وارتفاع السطر (نسبة مئوية) وتباعد الحروف
out.textStyles = (await figma.getLocalTextStylesAsync()).map(s => [s.name, s.fontName.family, s.fontName.style, round(s.fontSize),
  s.lineHeight.unit === 'PERCENT' ? round(s.lineHeight.value) : s.lineHeight.unit === 'PIXELS' ? round(s.lineHeight.value / s.fontSize * 100) : null,
  s.letterSpacing.value]);
return out;
