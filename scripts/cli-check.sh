#!/usr/bin/env bash
# فحص آلي عبر Obsidian CLI (1.12.7 فأحدث، مع تفعيل «Command line interface»):
# يفعّل الثيم في test-vault، ويفتح ملاحظات الاختبار، ويتحقق من القيم المحسوبة لأهم القواعد في الوضعين.
# يُشغَّل والنسخة المعزولة تعمل (scripts/obsidian-test.sh). يخرج برمز 1 إن فشل تحقق.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLI="/Applications/Obsidian.app/Contents/MacOS/obsidian-cli"
V="vault=test-vault"
fail=0

"$CLI" $V theme:set name=Ghasaq >/dev/null

check() { # الوصف، الشيفرة (تُعيد true/false أو قيمة)، القيمة المتوقعة
  local desc="$1" code="$2" want="$3" got
  got=$("$CLI" $V eval code="$code" 2>&1 | sed 's/^=> //' | tail -1)
  if [ "$got" = "$want" ]; then echo "✓ $desc"; else echo "✗ $desc: «$got» بدل «$want»"; fail=1; fi
}

# يفتح الملاحظة ويفرض رسمها كاملة (عرض القراءة يرسم الأقسام الظاهرة فقط، والنافذة قد تكون محجوبة)
open_note() { "$CLI" $V eval code="(async()=>{const f=app.vault.getAbstractFileByPath('$1');await app.workspace.getLeaf(false).openFile(f);const l=app.workspace.getMostRecentLeaf();const s=l.getViewState();s.state.mode='$2';s.state.source=false;await l.setViewState(s);const pm=l.view.previewMode;if(pm&&pm.renderer){pm.renderer.showAll=true;pm.rerender(true);}await new Promise(r=>setTimeout(r,1200));return 'ok'})()" >/dev/null
  # إن كانت النافذة خلف غيرها لا يرسم Chromium شيئًا؛ لقطة بمحاكاة الحجم عبر CDP تفرض الرسم
  /opt/homebrew/bin/node "$ROOT/scripts/obsidian.mjs" shot "$ROOT/.cache/render.png" 1440 900 1 >/dev/null 2>&1 || true; }
Q="app.workspace.getMostRecentLeaf().view.containerEl" 

for scheme in obsidian moonstone; do
  "$CLI" $V eval code="app.changeTheme('$scheme')" >/dev/null; sleep 0.6
  echo "── $([ $scheme = obsidian ] && echo غسق || echo أصيل)"
  open_note "كل العناصر.md" preview
  check "الثيم مفعّل" "app.customCss.theme" "Ghasaq"
  check "خط المتن يبدأ بـ Ghasaq Naskh" "getComputedStyle($Q.querySelector('.markdown-preview-view')).fontFamily.includes('Ghasaq Naskh')" "true"
  check "العناوين بخط Cairo" "getComputedStyle($Q.querySelector('.markdown-preview-view h1')).fontFamily.includes('Ghasaq Cairo')" "true"
  check "تباعد حروف العناوين صفر" "[...$Q.querySelectorAll('.markdown-preview-view h1, .markdown-preview-view h2, .inline-title')].every(e=>['0px','normal'].includes(getComputedStyle(e).letterSpacing))" "true"
  check "ارتفاع سطر المتن 1.9" "(()=>{const p=$Q.querySelector('.markdown-preview-view p');const cs=getComputedStyle(p);return (parseFloat(cs.lineHeight)/parseFloat(cs.fontSize)).toFixed(2)})()" "1.90"
  check "لا ميل اصطناعي للتوكيد" "getComputedStyle($Q.querySelector('.markdown-preview-view em')).fontSynthesisStyle" "none"
  check "كتل الشيفرة LTR" "[...$Q.querySelectorAll('.markdown-preview-view pre')].every(p=>getComputedStyle(p).direction==='ltr')" "true"
  check "الشيفرة المضمّنة معزولة" "getComputedStyle($Q.querySelector('.markdown-preview-view p code')).unicodeBidi" "plaintext"
  check "الواجهة RTL" "document.body.classList.contains('mod-rtl')" "true"
  check "حدّ الاقتباس في جهة البداية (يمين)" "(()=>{const b=$Q.querySelector('.markdown-preview-view blockquote');const cs=getComputedStyle(b);return cs.borderRightWidth!=='0px' && cs.borderLeftWidth==='0px'})()" "true"
  check "لون التمييز من --accent-h/s/l" "getComputedStyle(document.body).getPropertyValue('--color-accent').trim().startsWith('hsl(')" "true"
  open_note "قصائد/الخيل والليل.md" preview
  check "القصيدة: الجدول RTL" "getComputedStyle($Q.querySelector('.markdown-preview-view.qasida table')).direction" "rtl"
  check "القصيدة: الترويسة مخفية" "getComputedStyle($Q.querySelector('.markdown-preview-view.qasida table thead')).display" "none"
  check "القصيدة: الصدر في اليمين" "(()=>{const r=$Q.querySelector('.markdown-preview-view.qasida table tbody tr');return r.children[0].getBoundingClientRect().left > r.children[1].getBoundingClientRect().left})()" "true"
  check "القصيدة: عرضان متساويان" "(()=>{const r=$Q.querySelector('.markdown-preview-view.qasida table tbody tr');return Math.abs(r.children[0].offsetWidth-r.children[1].offsetWidth)<=1})()" "true"
done

"$CLI" $V eval code="app.changeTheme('obsidian')" >/dev/null
"$CLI" $V dev:screenshot path="$ROOT/screenshots/cli-ghasaq.png" >/dev/null && echo "✓ dev:screenshot ← screenshots/cli-ghasaq.png"
exit $fail
