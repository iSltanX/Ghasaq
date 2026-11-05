"""فحص التباين (WCAG 2) من tokens/figma.json مباشرة. يخرج برمز 1 إن نزل أي لون عن حدّه.

الحدود (من المهمة):
- النص الأساسي ≥ 11:1 (القيمة المعتمدة في اللوحة الابتدائية)
- النص الثانوي، والتمييز، والوسوم، والدافئ، والتوكيد ≥ 4.5:1
- النص الخافت (للزخرفي وغير الجوهري فقط) ≥ 3:1
تُفحص على الخلفيات الثلاث: المحرر، والأشرطة الجانبية، والخلفية البديلة، في الوضعين، ولخيارات التمييز الثلاثة.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tokens_lib import ACCENT_MODES, THEME_MODES, Tokens, blend, contrast, parse_hex  # noqa: E402

BGS = {"المحرر": "background/primary", "الشريط": "background/secondary", "البديلة": "background/primary-alt"}

# (الرمز، الحد، الخلفيات) — None = الخلفيات الثلاث
ON_SURFACES = [
    ("text/normal", 11.0), ("text/muted", 4.5), ("text/faint", 3.0),
    ("text/accent", 4.5), ("link/color", 4.5), ("tag/color", 4.5), ("color/red", 4.5), ("text/error", 4.5),
    ("italic-color", 4.5), ("text/success", 4.5), ("text/warning", 4.5),
    ("ghasaq/high-contrast/text-muted", 7.0), ("ghasaq/high-contrast/text-faint", 4.5),
]
CODE = ["code/normal", "code/comment", "code/function", "code/keyword", "code/operator", "code/property",
        "code/punctuation", "code/string", "code/tag", "code/value", "code/important"]
CALLOUTS = ["callout/default", "callout/info", "callout/todo", "callout/summary", "callout/tip", "callout/important", "callout/success",
            "callout/question", "callout/warning", "callout/fail", "callout/error", "callout/bug", "callout/example", "callout/quote"]
CALLOUT_WASH = 0.10  # غلالة الـ callout في الثيم


def main() -> int:
    t = Tokens()
    failures, rows = [], 0

    def col(name, ctx):
        return parse_hex(t.resolve("Theme", name, ctx))

    def check(label, fg, bg, minimum):
        nonlocal rows
        rows += 1
        r = contrast(fg, bg)
        if r + 1e-9 < minimum:
            failures.append(f"✗ {label}: {r:.2f} < {minimum}")
        return r

    for mode in THEME_MODES:
        for accent in ACCENT_MODES:
            ctx = {"Theme": mode, "Accent": accent}
            surf = {k: col(v, ctx) for k, v in BGS.items()}
            tag = f"{mode}/{accent}"
            for name, minimum in ON_SURFACES:
                if accent != "كهرماني" and "accent" not in name and name != "link/color":
                    continue  # ما لا يتغيّر بالتمييز يُفحص مرة واحدة
                for bname, bg in surf.items():
                    check(f"{tag} {name} على {bname}", blend(col(name, ctx), bg), bg, minimum)
            # النص فوق لون التمييز (الأزرار)
            acc = col("interactive/accent", ctx)
            check(f"{tag} text/on-accent على interactive/accent", col("text/on-accent", ctx), acc, 4.5)
            # النص فوق التحديد والتظليل
            for overlay in ("text/selection", "text/highlight-bg"):
                bg = blend(col(overlay, ctx), surf["المحرر"])
                check(f"{tag} text/normal على {overlay}", col("text/normal", ctx), bg, 4.5)
            # عنصر محدد في المستكشف
            sel = blend(col("nav-item/background-selected", ctx), surf["الشريط"])
            check(f"{tag} nav-item/color-active على العنصر المحدد", col("nav-item/color-active", ctx), sel, 4.5)
            if accent != "كهرماني":
                continue
            code_bg = col("code/background", ctx)
            for name in CODE:
                check(f"{tag} {name} على code/background", col(name, ctx), code_bg, 4.5)
            for name in CALLOUTS:
                c = col(name, ctx)
                wash = blend((c[0], c[1], c[2], CALLOUT_WASH), surf["المحرر"])
                check(f"{tag} عنوان {name} على غلالته", c, wash, 4.5)
                check(f"{tag} text/normal داخل {name}", col("text/normal", ctx), wash, 7.0)
            tip_bg = col("ghasaq/tooltip-background", ctx)
            check(f"{tag} ghasaq/tooltip-text على التلميح", col("ghasaq/tooltip-text", ctx), tip_bg, 4.5)
            for i in range(1, 7):
                check(f"{tag} canvas/color/{i} على canvas", col(f"canvas/color/{i}", ctx), col("canvas/background", ctx), 3.0)
            for g in ("graph/node", "graph/node-focused", "graph/node-tag", "graph/node-attachment"):
                check(f"{tag} {g} على الخلفية", col(g, ctx), surf["المحرر"], 3.0)

    if failures:
        print(f"فحص التباين: فشل {len(failures)} من {rows}")
        print("\n".join(failures))
        return 1
    print(f"فحص التباين: {rows} فحصًا، كلها ضمن حدودها.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
