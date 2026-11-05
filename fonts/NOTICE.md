# الخطوط المضمّنة في theme.css · Embedded fonts

هذان الخطّان لا تشملهما رخصة MIT التي تغطي كود الثيم، ويبقى كلٌّ منهما برخصة SIL Open Font License 1.1.
These fonts are not covered by the theme's MIT license; each remains under the SIL Open Font License 1.1.

| الخط · Font | الاستعمال · Use | المصدر · Source | الحقوق · Copyright | نص الرخصة · License text |
|---|---|---|---|---|
| Noto Naskh Arabic (variable, wght 400–700) | المتن، الحروف العربية فقط · Body text, Arabic characters only | https://github.com/notofonts/arabic | Copyright 2022 The Noto Project Authors | [`OFL-NotoNaskhArabic.txt`](OFL-NotoNaskhArabic.txt) |
| Cairo (variable, wght 400–700, slnt 0) | العناوين والواجهة · Headings and interface | https://github.com/Gue3bara/Cairo | Copyright 2009 The Cairo Project Authors | [`OFL-Cairo.txt`](OFL-Cairo.txt) |

الملفان الأصليان هنا (`NotoNaskhArabic-VF.ttf` و`Cairo-VF.ttf`). يجزّئهما `scripts/subset_fonts.py` إلى الحروف التي يحتاجها الثيم، ويقيّد محور الوزن بين 400 و700، ثم يضمّنهما في `theme.css` بصيغة woff2. لا يغيّر شيئًا في رسم الحروف.

The original files live here (`NotoNaskhArabic-VF.ttf` and `Cairo-VF.ttf`). `scripts/subset_fonts.py` subsets them to the characters the theme needs, limits the weight axis to 400–700 and embeds them in `theme.css` as woff2, without changing any glyph outlines.
