"""يجزّئ الخطوط الأصلية في fonts/ إلى woff2 ويولّد src/fonts.css بصيغة data: و Base64.

- Noto Naskh Arabic (المتن): نطاقات العربية فقط في unicode-range، فتأخذ الكلمات اللاتينية خطها
  من سلسلة --font-text-theme. size-adjust من رمز Figma ghasaq/arabic-size-adjust.
- Cairo (العناوين والواجهة): العربية واللاتينية معًا.
- كلاهما ملف متغيّر يُقيَّد محوره wght بين 400 و700 (والميل في Cairo يُثبَّت على 0)، فالوزنان حقيقيان.
الناتج المجزّأ يُخزَّن في build/fonts/ (يُعاد توليده عند تغيّر المصدر أو الإعدادات).
"""
from __future__ import annotations

import base64
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tokens_lib import ROOT, Tokens  # noqa: E402

from fontTools import subset as ft_subset  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402
from fontTools.varLib import instancer  # noqa: E402

BUILD = ROOT / "build" / "fonts"
OUT_CSS = ROOT / "src" / "fonts.css"

ARABIC = ("U+0600-06FF, U+0750-077F, U+08A0-08FF, U+200C-200F, U+2066-2069, U+25CC, U+FB50-FDFF, U+FE70-FEFF, U+00AB, U+00BB")
LATIN = ("U+0020-007E, U+00A0-00FF, U+0131, U+0152-0153, U+02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+20AC, U+2122, "
         "U+2190-2193, U+2212, U+2215, U+FEFF, U+FFFD")

FONTS = [
    {"family": "Ghasaq Naskh", "source": "NotoNaskhArabic-VF.ttf", "out": "ghasaq-naskh-arabic.woff2", "axes": {"wght": (400, 700)},
     "unicodes": ARABIC, "range": ARABIC, "size_adjust_token": "ghasaq/arabic-size-adjust"},
    {"family": "Ghasaq Cairo", "source": "Cairo-VF.ttf", "out": "ghasaq-cairo.woff2", "axes": {"wght": (400, 700), "slnt": 0},
     "unicodes": ARABIC + ", " + LATIN, "range": ARABIC + ", " + LATIN, "size_adjust_token": None},
]


def parse_ranges(spec: str) -> list[int]:
    cps = []
    for part in spec.split(","):
        part = part.strip().replace("U+", "")
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-")
            cps.extend(range(int(a, 16), int(b, 16) + 1))
        else:
            cps.append(int(part, 16))
    return cps


def make_subset(spec: dict) -> Path:
    src = ROOT / "fonts" / spec["source"]
    key = hashlib.sha256(src.read_bytes() + json.dumps({k: spec[k] for k in ("axes", "unicodes")}, sort_keys=True).encode()).hexdigest()[:12]
    BUILD.mkdir(parents=True, exist_ok=True)
    out = BUILD / spec["out"]
    stamp = out.with_suffix(".key")
    if out.exists() and stamp.exists() and stamp.read_text() == key:
        return out
    # التجزئة أولًا ثم تقييد المحاور: العكس يكسر جدول gvar الكسول في fontTools.
    font = TTFont(src, lazy=False)
    opts = ft_subset.Options()
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    opts.hinting = False
    sub = ft_subset.Subsetter(opts)
    sub.populate(unicodes=parse_ranges(spec["unicodes"]))
    sub.subset(font)
    font = instancer.instantiateVariableFont(font, spec["axes"])
    font.flavor = "woff2"
    font.save(out)
    stamp.write_text(key)
    return out


def build() -> str:
    t = Tokens()
    blocks = ["/* مولَّد من fonts/ بواسطة scripts/subset_fonts.py. الخطان برخصة SIL OFL 1.1 (fonts/OFL-*.txt). */"]
    for spec in FONTS:
        path = make_subset(spec)
        data = base64.b64encode(path.read_bytes()).decode()
        lo, hi = spec["axes"]["wght"]
        extra = ""
        if spec["size_adjust_token"]:
            pct = t.resolve("Type", spec["size_adjust_token"])
            extra = f"\n  size-adjust: {pct:g}%;"
        blocks.append(
            "@font-face {\n"
            f"  font-family: '{spec['family']}';\n"
            f"  src: url(data:font/woff2;base64,{data}) format('woff2');\n"
            f"  font-weight: {lo} {hi};\n  font-style: normal;\n  font-display: swap;\n"
            f"  unicode-range: {spec['range']};{extra}\n"
            "}")
        print(f"  {spec['family']}: {path.stat().st_size / 1024:.1f}KB woff2 → {len(data) / 1024:.1f}KB base64")
    return "\n".join(blocks) + "\n"


def main() -> int:
    css = build()
    OUT_CSS.write_text(css, encoding="utf-8")
    print(f"fonts.css: {len(css.encode()) / 1024:.1f}KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
