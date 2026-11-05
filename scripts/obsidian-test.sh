#!/usr/bin/env bash
# يشغّل نسخة Obsidian معزولة على خزينة الاختبار فقط:
#   - ملف تعريف مستقل في .cache/obsidian-profile (لا يمسّ إعدادات Obsidian العامة ولا يفتح خزائن أخرى)
#   - منفذ CDP على 9339 لأداة scripts/obsidian.mjs (لقطات، eval، فحص المحددات)
# الاستعمال:  scripts/obsidian-test.sh [start|stop|restart]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROFILE="$ROOT/.cache/obsidian-profile"
VAULT="$ROOT/test-vault"
PORT="${CDP_PORT:-9339}"
APP="/Applications/Obsidian.app/Contents/MacOS/Obsidian"

stop() {
  pkill -f -- "--user-data-dir=$PROFILE" 2>/dev/null || true
  for _ in $(seq 1 20); do pgrep -f -- "--user-data-dir=$PROFILE" >/dev/null || return 0; sleep 0.5; done
}

start() {
  mkdir -p "$PROFILE"
  /usr/bin/python3 - "$PROFILE/obsidian.json" "$VAULT" <<'PY'
import json, sys, time, os
path, vault = sys.argv[1], sys.argv[2]
data = json.load(open(path)) if os.path.exists(path) else {}
data["vaults"] = {"a7c3d9e1f2b4c6d8": {"path": vault, "ts": int(time.time() * 1000), "open": True}}
data.setdefault("frame", "hidden")
json.dump(data, open(path, "w"))
PY
  nohup "$APP" --user-data-dir="$PROFILE" --remote-debugging-port="$PORT" >"$ROOT/.cache/obsidian.log" 2>&1 &
  for _ in $(seq 1 60); do
    curl -fs "http://127.0.0.1:$PORT/json" | grep -q 'app://obsidian.md/index.html' && { echo "Obsidian (معزول) جاهز على المنفذ $PORT"; return 0; }
    sleep 0.5
  done
  echo "لم يستجب Obsidian على المنفذ $PORT" >&2; return 1
}

case "${1:-start}" in
  start) start ;;
  stop) stop ;;
  restart) stop; start ;;
esac
