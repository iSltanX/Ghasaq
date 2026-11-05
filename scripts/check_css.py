"""فحوص CSS الآلية لثيم غسق. يُستدعى من build.py، ويمكن تشغيله وحده.

1. لا خصائص فيزيائية (left/right) في src/ خارج مناطق LTR الموثّقة:
      /* ltr-zone: السبب */  ...  /* /ltr-zone */
2. لا !important في theme.css.
3. لا url() يشير إلى http أو //، ولا @import.
4. حجم theme.css ضمن الميزانية.
5. manifest.json صالح، و version بصيغة x.y.z.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
GENERATED = {"tokens.css", "fonts.css"}
BUDGET = 700 * 1024

PHYSICAL = re.compile(
    r"(?<![\w-])("
    r"margin-(?:left|right)|padding-(?:left|right)|"
    r"border-(?:left|right)(?:-(?:width|style|color))?|"
    r"border-(?:top|bottom)-(?:left|right)-radius|"
    r"left|right|"
    r"scroll-(?:margin|padding)-(?:left|right)"
    r")\s*:", re.I)
PHYSICAL_VALUE = re.compile(r"(?<![\w-])(text-align|float|clear)\s*:\s*(left|right)\b", re.I)


def strip_comments_keep_zones(text: str):
    """يعيد قائمة (رقم السطر، السطر، داخل منطقة LTR؟) بعد حذف التعليقات العادية."""
    out, in_zone, in_comment = [], False, False
    for n, line in enumerate(text.splitlines(), 1):
        if "/* ltr-zone:" in line:
            in_zone = True
        if "/* /ltr-zone */" in line:
            in_zone = False
            out.append((n, "", False))
            continue
        clean, i = "", 0
        while i < len(line):
            if in_comment:
                j = line.find("*/", i)
                if j < 0:
                    i = len(line)
                else:
                    in_comment, i = False, j + 2
            else:
                j = line.find("/*", i)
                if j < 0:
                    clean += line[i:]
                    i = len(line)
                else:
                    clean += line[i:j]
                    in_comment, i = True, j + 2
        out.append((n, clean, in_zone))
    return out


def lint_physical() -> list[str]:
    errs = []
    for f in sorted(SRC.glob("*.css")):
        if f.name in GENERATED:
            continue
        text = f.read_text(encoding="utf-8")
        zones_open = text.count("/* ltr-zone:") - text.count("/* /ltr-zone */")
        if zones_open:
            errs.append(f"{f.name}: منطقة ltr-zone غير مغلقة")
        for n, line, zone in strip_comments_keep_zones(text):
            if zone:
                continue
            # تجاهل المحددات: الخصائص فقط تأتي بعد { أو ; أو في أول السطر
            for m in PHYSICAL.finditer(line):
                before = line[:m.start()].rstrip()
                if before and before[-1] not in "{;" and before.strip() != "":
                    continue
                errs.append(f"{f.name}:{n}: خاصية فيزيائية «{m.group(1)}» خارج منطقة LTR")
            for m in PHYSICAL_VALUE.finditer(line):
                errs.append(f"{f.name}:{n}: «{m.group(1)}: {m.group(2)}» خارج منطقة LTR")
    return errs


def lint_theme(css: str) -> list[str]:
    errs = []
    body = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    if "!important" in body:
        errs.append("theme.css: يحوي !important")
    for m in re.finditer(r"url\(\s*['\"]?([^)'\"]+)", body):
        target = m.group(1).strip()
        if re.match(r"(https?:)?//", target, re.I):
            errs.append(f"theme.css: url() خارجي: {target[:60]}")
        elif not target.startswith("data:") and not target.startswith("#"):
            errs.append(f"theme.css: url() لملف غير مضمَّن: {target[:60]}")
    if re.search(r"@import\b", body):
        errs.append("theme.css: يحوي @import")
    size = len(css.encode("utf-8"))
    if size > BUDGET:
        errs.append(f"theme.css: {size / 1024:.0f}KB يتجاوز الميزانية {BUDGET / 1024:.0f}KB")
    return errs


def lint_manifest() -> list[str]:
    errs = []
    try:
        m = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [f"manifest.json غير صالح: {e}"]
    for k in ("name", "version", "minAppVersion", "author"):
        if not isinstance(m.get(k), str) or not m.get(k):
            errs.append(f"manifest.json: الحقل {k} مفقود")
    for k in ("version", "minAppVersion"):
        if isinstance(m.get(k), str) and not re.fullmatch(r"\d+\.\d+\.\d+", m[k]):
            errs.append(f"manifest.json: {k} ليس بصيغة x.y.z: {m[k]}")
    if m.get("name") != "Ghasaq":
        errs.append("manifest.json: name يجب أن يكون Ghasaq")
    return errs


def lint_style_settings(css: str) -> list[str]:
    """كتلة @settings يجب أن تكون YAML صالحًا، وإلا عرض Style Settings خطأً بدل الخيارات."""
    errs = []
    blocks = re.findall(r"/\*\s*@settings(.*?)\*/", css, flags=re.S)
    if not blocks:
        return ["theme.css: لا توجد كتلة @settings"]
    try:
        import yaml  # PyYAML
    except ImportError:
        return []  # الفحص اختياري إن لم تتوفر المكتبة
    for b in blocks:
        try:
            data = yaml.safe_load(b)
        except yaml.YAMLError as e:
            errs.append(f"@settings: YAML غير صالح: {str(e).splitlines()[0]}")
            continue
        for k in ("name", "id", "settings"):
            if k not in data:
                errs.append(f"@settings: الحقل {k} مفقود")
        for item in data.get("settings", []):
            if not {"id", "type"} <= set(item):
                errs.append(f"@settings: عنصر بلا id أو type: {item}")
            if item.get("type") != "heading" and "title" not in item:
                errs.append(f"@settings: {item.get('id')} بلا عنوان")
    return errs


def run(css: str | None = None) -> list[str]:
    if css is None:
        css = (ROOT / "theme.css").read_text(encoding="utf-8")
    return lint_physical() + lint_theme(css) + lint_manifest() + lint_style_settings(css)


if __name__ == "__main__":
    problems = run()
    print("\n".join(problems) if problems else "فحوص CSS: لا مشكلات.")
    sys.exit(1 if problems else 0)
