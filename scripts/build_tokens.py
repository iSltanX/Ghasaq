"""يولّد src/tokens.css من tokens/figma.json. لا يُحرَّر الناتج يدويًا: أي تعديل يتم في Figma ثم يُعاد التصدير.

قواعد التحويل:
- Sizes وType: على body، والوحدة من وصف المتغير (unit:px|em|rem|unitless|%).
- Theme: تحت .theme-dark (وضع غسق) و.theme-light (وضع أصيل)، ومعهما .is-mobile لأن Obsidian
  يعيد تعريف بعض درجات الأساس على الجوال بمحدِّد أعلى.
- المرجع إلى متغير Theme آخر يصير var(--x)، والمرجع إلى Primitives يصير قيمة اللون نفسها.
- لون التمييز يُكتب --accent-h/s/l، ودرجتاه 1 و2 تُشتقّان بـ calc من القيم المصدَّرة،
  والألوان الشفافة المشتقة منه تصير color-mix مع var(--color-accent). بذلك يتقدّم لون المستخدم
  (يكتبه Obsidian في style على body) على كل ذلك.
- أوضاع Accent الأخرى (نحاسي، بنفسجي غسقي) تصير أصنافًا يفعّلها Style Settings.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tokens_lib import ACCENT_MODES, DEFAULT_ACCENT, ROOT, THEME_MODES, Tokens, parse_hex, to_hex, to_hsl  # noqa: E402

OUT = ROOT / "src" / "tokens.css"

# لا تُكتب: مقاسات مرجعية أو أسماء خطوط يستعملها البناء، أو بدائل Figma.
SKIP_UNITS = {"figma-only", "family", "%"}
SKIP_NAMES = {"font/text-size-reference"}
UNIT = {"px": "px", "em": "em", "rem": "rem", "unitless": "", "": ""}
ACCENT_VAR = "color/accent"
ACCENT_STEPS = {"color/accent-1": "-1", "color/accent-2": "-2"}


def fmt_num(x) -> str:
    s = f"{float(x):.4f}".rstrip("0").rstrip(".")
    return s or "0"


def static_block(t: Tokens) -> list[str]:
    lines = []
    for col in ("Sizes", "Type"):
        for e in t.entries(col):
            unit = t.unit(e)
            if e["name"] in SKIP_NAMES or unit in SKIP_UNITS:
                continue
            val = t.raw(e, {})
            if e["type"] == "STRING":
                if e["name"] == "font/text-theme":
                    # خطاف Style Settings: «خط المتن» يستبدل الخط المضمَّن باسم خط مثبّت.
                    val = val.replace("'Ghasaq Naskh'", "var(--ghasaq-text-font, 'Ghasaq Naskh')")
                lines.append(f"  {t.css_name(e)}: {val};")
            else:
                lines.append(f"  {t.css_name(e)}: {fmt_num(val)}{UNIT.get(unit, unit)};")
    return lines


# ارتفاعات أسطر مأخوذة من أنماط النص في Figma (لا من المتغيرات)
TEXT_STYLE_LINE_HEIGHTS = {
    "واجهة/صغير": "--ghasaq-ui-line-height",
    "شيفرة/عادي": "--ghasaq-code-line-height",
    "قصيدة/شطر": "--ghasaq-qasida-line-height",
    "حاشية": "--ghasaq-footnote-line-height",
}


def text_style_block(t: Tokens) -> list[str]:
    styles = {s[0]: s for s in t.data.get("textStyles", [])}
    lines = []
    for style, var in TEXT_STYLE_LINE_HEIGHTS.items():
        s = styles.get(style)
        if s and s[4]:
            lines.append(f"  {var}: {fmt_num(s[4] / 100)}; /* نمط النص «{style}» */")
    return lines


def hsl_parts(hex_color: str):
    h, s, l = to_hsl(parse_hex(hex_color))
    return h, s, l


def accent_decls(t: Tokens, theme_mode: str, accent_mode: str) -> list[str]:
    ctx = {"Theme": theme_mode, "Accent": accent_mode}
    base = t.resolve("Theme", ACCENT_VAR, ctx)
    h, s, l = hsl_parts(base)
    out = [f"  --accent-h: {fmt_num(round(h, 2))};", f"  --accent-s: {fmt_num(round(s, 2))}%;", f"  --accent-l: {fmt_num(round(l, 2))}%;",
           "  --color-accent: hsl(var(--accent-h), var(--accent-s), var(--accent-l));"]
    for name, suffix in ACCENT_STEPS.items():
        h2, s2, l2 = hsl_parts(t.resolve("Theme", name, ctx))
        dh = round(h2 - h, 2)
        ks = round(s2 / s, 4) if s else 1
        kl = round(l2 / l, 4) if l else 1
        sign = "+" if dh >= 0 else "-"
        out.append(f"  --color-accent{suffix}: hsl(calc(var(--accent-h) {sign} {fmt_num(abs(dh))}), calc(var(--accent-s) * {fmt_num(ks)}), calc(var(--accent-l) * {fmt_num(kl)}));"
                   f" /* {t.resolve('Theme', name, ctx)} */")
    return out


def theme_value(t: Tokens, e: dict, theme_mode: str) -> str | None:
    ctx = {"Theme": theme_mode, "Accent": DEFAULT_ACCENT}
    tgt = t.alias_target(e, ctx)
    if tgt is None:
        return to_hex(parse_hex(t.raw(e, ctx)))
    col, nm = tgt
    if col == "Theme":
        return f"var({t.css_name(t.get('Theme', nm))})"
    if col == "Accent":
        # درجات التمييز الشفافة: نفس لون التمييز بنسبة شفافية ثابتة
        val = t.resolve("Accent", nm, ctx)
        a = parse_hex(val)[3]
        if a < 0.999:
            return f"color-mix(in srgb, var(--color-accent) {fmt_num(round(a * 100, 1))}%, transparent)"
        return None  # color/accent و-1 و-2 تُكتب في accent_decls
    return to_hex(parse_hex(t.resolve(col, nm, ctx)))


def theme_block(t: Tokens, theme_mode: str) -> list[str]:
    lines = accent_decls(t, theme_mode, DEFAULT_ACCENT)
    for e in t.entries("Theme"):
        if e["name"] == ACCENT_VAR or e["name"] in ACCENT_STEPS:
            continue
        v = theme_value(t, e, theme_mode)
        if v is not None:
            lines.append(f"  {t.css_name(e)}: {v};")
    return lines


def build() -> str:
    t = Tokens()
    out = ["/* مولَّد من tokens/figma.json بواسطة scripts/build_tokens.py. لا تحرّره يدويًا: عدّل Figma ثم أعد التصدير. */",
           f"/* Figma: {t.data['file']} · exported {t.data['exportedAt']} */", "", "body {", *static_block(t), *text_style_block(t), "}", ""]
    for mode, sel in THEME_MODES.items():
        out += [f"{sel},", f"{sel}.is-mobile {{", *theme_block(t, mode), "}", ""]
    for amode, cls in ACCENT_MODES.items():
        if amode == DEFAULT_ACCENT:
            continue
        for mode, sel in THEME_MODES.items():
            out += [f"{sel}.ghasaq-accent-{cls} {{", *accent_decls(t, mode, amode), "}", ""]
    return "\n".join(out)


def main() -> int:
    css = build()
    OUT.write_text(css, encoding="utf-8")
    print(f"tokens.css: {OUT.relative_to(ROOT)} ({len(css.encode())} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
