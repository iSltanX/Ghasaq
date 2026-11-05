"""أمر البناء الواحد لثيم غسق:  python3 scripts/build.py

1. يولّد src/tokens.css من tokens/figma.json.
2. يجزّئ الخطوط ويولّد src/fonts.css.
3. يجمع src/ بالترتيب في theme.css.
4. يشغّل الفحوص الآلية (التباين، الخصائص الفيزيائية، !important، الروابط الخارجية، الحجم، manifest)،
   ويفشل البناء (رمز خروج 1) إن فشل أيٌّ منها.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_tokens  # noqa: E402
import check_contrast  # noqa: E402
import check_css  # noqa: E402
import subset_fonts  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ORDER = ["fonts.css", "tokens.css", "typography.css", "rtl.css", "editor.css", "ui.css", "components.css", "qasida.css", "settings.css"]


def main() -> int:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    print("١. الرموز"); build_tokens.main()
    print("٢. الخطوط"); subset_fonts.main()
    print("٣. التجميع")
    parts = [f"/* {manifest['name']} (غَسَق) {manifest['version']} · {manifest['author']} · MIT\n"
             "   ثيم Obsidian صُمّم للكتابة والقراءة بالعربية. هذا الملف ناتج البناء: لا تحرّره، وعدّل src/ ثم شغّل scripts/build.py.\n"
             "   الخطوط المضمَّنة: Noto Naskh Arabic وCairo برخصة SIL OFL 1.1. */\n"]
    missing = []
    for name in ORDER:
        f = ROOT / "src" / name
        if not f.exists():
            missing.append(name)
            continue
        parts.append(f"/* ───── {name} ───── */\n" + f.read_text(encoding="utf-8").strip() + "\n")
    css = "\n".join(parts)
    (ROOT / "theme.css").write_text(css, encoding="utf-8")
    print(f"   theme.css: {len(css.encode()) / 1024:.1f}KB" + (f" (ملفات غير موجودة بعد: {', '.join(missing)})" if missing else ""))
    print("٤. الفحوص")
    failed = 0
    if check_contrast.main():
        failed += 1
    problems = check_css.run(css)
    if problems:
        failed += 1
        print("\n".join(problems))
    else:
        print("فحوص CSS: لا مشكلات.")
    if failed:
        print("✗ فشل البناء.")
        return 1
    print("✓ البناء سليم.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
