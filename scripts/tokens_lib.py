"""مكتبة مشتركة لقراءة tokens/figma.json وحلّ مراجعه وحساب الألوان.

الملف مصدَّر من Figma بالسكربت scripts/figma/export-variables.js، ولا يُحرَّر يدويًا.
"""
from __future__ import annotations

import colorsys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS = ROOT / "tokens" / "figma.json"

THEME_MODES = {"غسق": ".theme-dark", "أصيل": ".theme-light"}
ACCENT_MODES = {"كهرماني": "amber", "نحاسي": "copper", "بنفسجي غسقي": "dusk"}
DEFAULT_ACCENT = "كهرماني"


class Tokens:
    def __init__(self, path: Path = TOKENS):
        self.data = json.loads(path.read_text(encoding="utf-8"))
        self.collections = {c["name"]: c for c in self.data["collections"]}
        self.vars: dict[tuple[str, str], dict] = {}
        for c in self.data["collections"]:
            for name, typ, values, desc, code in c["vars"]:
                self.vars[(c["name"], name)] = {
                    "collection": c["name"], "name": name, "type": typ, "values": values,
                    "desc": desc, "code": code, "modes": c["modes"],
                }

    # ---------- access ----------
    def entries(self, collection: str):
        return [v for (c, _), v in self.vars.items() if c == collection]

    def get(self, collection: str, name: str) -> dict:
        try:
            return self.vars[(collection, name)]
        except KeyError as e:
            raise KeyError(f"token not found: {collection}:{name}") from e

    def raw(self, entry: dict, ctx: dict):
        """القيمة الخام للمتغير في سياق الأوضاع (قد تكون مرجعًا '@Col:name')."""
        modes = entry["modes"]
        mode = ctx.get(entry["collection"], modes[0])
        if mode not in modes:
            mode = modes[0]
        return entry["values"][modes.index(mode)]

    def resolve(self, collection: str, name: str, ctx: dict | None = None, depth: int = 0):
        ctx = ctx or {}
        if depth > 20:
            raise RecursionError(f"alias loop at {collection}:{name}")
        val = self.raw(self.get(collection, name), ctx)
        if isinstance(val, str) and val.startswith("@"):
            col, nm = val[1:].split(":", 1)
            return self.resolve(col, nm, ctx, depth + 1)
        return val

    def alias_target(self, entry: dict, ctx: dict):
        val = self.raw(entry, ctx)
        if isinstance(val, str) and val.startswith("@"):
            col, nm = val[1:].split(":", 1)
            return col, nm
        return None

    @staticmethod
    def css_name(entry: dict) -> str:
        code = entry["code"]
        if code.startswith("var(") and code.endswith(")"):
            return code[4:-1]
        return "--" + entry["name"].replace("/", "-")

    @staticmethod
    def unit(entry: dict) -> str:
        d = entry.get("desc") or ""
        return d[5:] if d.startswith("unit:") else ""


# ---------- colour maths ----------
def parse_hex(h: str):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
    return r, g, b, a


def to_hex(rgba) -> str:
    r, g, b, a = rgba
    s = "#" + "".join(f"{round(x * 255):02X}" for x in (r, g, b))
    return s + (f"{round(a * 255):02X}" if a < 0.999 else "")


def blend(fg, bg):
    """يركّب لونًا شفافًا فوق خلفية معتمة."""
    r, g, b, a = fg
    br, bgc, bb, _ = bg
    return (r * a + br * (1 - a), g * a + bgc * (1 - a), b * a + bb * (1 - a), 1.0)


def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgba) -> float:
    r, g, b, _ = rgba
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a, b) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def to_hsl(rgba):
    r, g, b, _ = rgba
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s * 100, l * 100
