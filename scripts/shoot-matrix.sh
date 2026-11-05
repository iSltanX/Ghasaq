#!/usr/bin/env bash
# مصفوفة اللقطات: الوضع (غسق/أصيل) × العرض (تحرير/قراءة) لواجهة واحدة، ثم لقطات الواجهة.
# يُشغَّل والنسخة المعزولة تعمل (scripts/obsidian-test.sh) وبعد scripts/build.py.
# الاستعمال:  scripts/shoot-matrix.sh ar|en
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UI="${1:-ar}"
OUT="$ROOT/screenshots/matrix"; UIO="$ROOT/screenshots/ui"
mkdir -p "$OUT" "$UIO"
N="/opt/homebrew/bin/node"; O="$ROOT/scripts/obsidian.mjs"
W=1440; H=900

$N "$O" reload >/dev/null
for scheme in dark light; do
  name=$([ "$scheme" = dark ] && echo ghasaq || echo asil)
  $N "$O" scheme "$scheme" >/dev/null
  $N "$O" open "يوميات/نثر مشكول.md" >/dev/null
  $N "$O" mode live >/dev/null;    $N "$O" shot "$OUT/$UI-$name-live.png" $W $H 1 0 >/dev/null
  $N "$O" mode preview >/dev/null; $N "$O" shot "$OUT/$UI-$name-read.png" $W $H 1 0 >/dev/null
  $N "$O" open "ملاحظة مختلطة الاتجاه.md" >/dev/null
  $N "$O" mode preview >/dev/null; $N "$O" shot "$OUT/$UI-$name-mixed-read.png" $W $H 1 0 >/dev/null
  $N "$O" open "قصائد/الخيل والليل.md" >/dev/null
  $N "$O" mode live >/dev/null;    $N "$O" shot "$OUT/$UI-$name-qasida-live.png" $W $H 1 0 >/dev/null
  $N "$O" mode preview >/dev/null; $N "$O" shot "$OUT/$UI-$name-qasida-read.png" $W $H 1 0 >/dev/null
  $N "$O" open "English/On dusk.md" >/dev/null
  $N "$O" mode preview >/dev/null; $N "$O" shot "$OUT/$UI-$name-english-read.png" $W $H 1 0 >/dev/null
  $N "$O" open "كل العناصر.md" >/dev/null
  $N "$O" mode preview >/dev/null; $N "$O" shot "$OUT/$UI-$name-callouts-read.png" $W $H 1 1500 >/dev/null
  # الواجهة
  $N "$O" open "لوحة الغسق.canvas" >/dev/null; sleep 1
  $N "$O" eval "const v=app.workspace.getMostRecentLeaf().view; if(v.canvas) v.canvas.zoomToFit(); await new Promise(r=>setTimeout(r,600)); return 1" >/dev/null
  $N "$O" shot "$UIO/$UI-$name-canvas.png" $W $H 1 >/dev/null
  $N "$O" eval "app.commands.executeCommandById('graph:open'); await new Promise(r=>setTimeout(r,2500)); return 1" >/dev/null
  $N "$O" shot "$UIO/$UI-$name-graph.png" $W $H 1 >/dev/null
  $N "$O" open "ملاحظات الغسق.base" >/dev/null; sleep 1.2
  $N "$O" shot "$UIO/$UI-$name-bases.png" $W $H 1 >/dev/null
  $N "$O" open "يوميات/نثر مشكول.md" >/dev/null
  $N "$O" eval "app.commands.executeCommandById('command-palette:open'); await new Promise(r=>setTimeout(r,500)); const i=document.querySelector('.prompt-input'); i.value='$([ "$UI" = ar ] && echo 'فتح' || echo 'open')'; i.dispatchEvent(new Event('input',{bubbles:true})); await new Promise(r=>setTimeout(r,500)); return 1" >/dev/null
  $N "$O" shot "$UIO/$UI-$name-command-palette.png" $W $H 1 >/dev/null
  $N "$O" key Escape >/dev/null
  $N "$O" eval "app.setting.open(); app.setting.openTabById('appearance'); await new Promise(r=>setTimeout(r,900)); return 1" >/dev/null
  T=$(curl -s http://127.0.0.1:9339/json | /usr/bin/python3 -c "import json,sys; ts=[t['title'] for t in json.load(sys.stdin) if t['type']=='page' and t['url']=='about:blank']; print(ts[0].split(' - ')[0] if ts else '')")
  if [ -n "$T" ]; then
    CDP_TITLE="$T" $N "$O" winsize 1100 760 >/dev/null
    CDP_TITLE="$T" $N "$O" shot "$UIO/$UI-$name-settings.png" >/dev/null
    $N "$O" eval "app.setting.openTabById('obsidian-style-settings'); await new Promise(r=>setTimeout(r,900)); return 1" >/dev/null
    CDP_TITLE="$T" $N "$O" eval "for (const h of document.querySelectorAll('.style-settings-heading.is-collapsed')) h.click(); await new Promise(r=>setTimeout(r,500)); return 1" >/dev/null
    CDP_TITLE="$T" $N "$O" shot "$UIO/$UI-$name-style-settings.png" >/dev/null
  fi
  $N "$O" eval "app.setting.close(); return 1" >/dev/null
done
$N "$O" scheme dark >/dev/null
echo "اللقطات في screenshots/matrix وscreenshots/ui"
