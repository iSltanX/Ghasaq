<div dir="rtl">

<p align="center">
  <img src="screenshots/readme-header.png" alt="غَسَق: ثيم Obsidian للكتابة والقراءة بالعربية" width="100%">
</p>

<h1 align="center">غَسَق · Ghasaq</h1>

<p align="center">ثيم Obsidian للكتابة والقراءة بالعربية: حبرٌ ليلي، وورقٌ دافئ، وآخرُ الضوء.</p>

<p align="center" dir="ltr"><b>An Arabic-first Obsidian theme for long-form writing and reading:</b> violet night ink, warm paper and an amber last light. Careful right-to-left layout, embedded Noto Naskh Arabic and Cairo, a qasida mode for classical verse, dark and light modes, and 9 Style Settings options. <a href="README.en.md">Full English documentation →</a></p>

<p align="center">
  <a href="https://github.com/iSltanX/Ghasaq/releases/latest"><img src="https://img.shields.io/github/v/release/iSltanX/Ghasaq?label=release&color=AB632B" alt="الإصدار"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-5F459A" alt="الرخصة"></a>
  <img src="https://img.shields.io/badge/Obsidian-1.14.4%2B-1E1B29" alt="Obsidian 1.14.4+">
</p>

<p align="center">
  <a href="https://community.obsidian.md/themes/ghasaq">دليل الثيمات</a> ·
  <a href="#المعاينة">المعاينة</a> ·
  <a href="#التثبيت">التثبيت</a> ·
  <a href="#الإعدادات">الإعدادات</a> ·
  <a href="#القصيدة-العمودية">القصيدة العمودية</a> ·
  <a href="#التطوير">التطوير</a> ·
  <a href="README.en.md">English</a>
</p>

## عن غسق

الغَسَق ظلمة أول الليل، حين يغيب الشفق ويبقى أثر ضوئه. يقوم الثيم على ثلاثة عناصر:

- **حبر:** خلفيات ليلية مائلة إلى البنفسجي.
- **ورق:** نصٌّ دافئ لا أبيض ناصع.
- **آخر الضوء:** لون تمييز كهرماني يُستعمل قليلًا، في الروابط والمؤشر والأزرار.

الوضع الداكن «**غَسَق**» هو الأصل، والوضع الفاتح «**أصيل**» آخر النهار قبل الغروب. صُمّمت الهوية كاملة في Figma أولًا، ثم اشتُقّت ألوان الثيم ومقاساته منها آليًا.

المعيار: ملاحظة عربية طويلة مشكولة، فيها سطر إنجليزي وكتلة شيفرة وجدول وقصيدة عمودية. ينبغي أن يظهر ذلك كله في موضعه الصحيح، ومريحًا للعين، في الوضعين، وتحت الواجهة العربية والإنجليزية.

## المعاينة

لقطات حقيقية من Obsidian 1.15.0 بواجهة عربية.

| غَسَق · قراءة | أصيل · قراءة |
|---|---|
| ![نثر مشكول في وضع القراءة، الوضع الداكن](screenshots/matrix/ar-ghasaq-read.png) | ![نثر مشكول في وضع القراءة، الوضع الفاتح](screenshots/matrix/ar-asil-read.png) |
| **غَسَق · Live Preview** | **أصيل · قصيدة عمودية** |
| ![نثر مشكول في Live Preview](screenshots/matrix/ar-ghasaq-live.png) | ![قصيدة المتنبي بوضع القصيدة](screenshots/matrix/ar-asil-qasida-read.png) |
| **ملاحظة مختلطة الاتجاه** | **لوحة الأوامر** |
| ![ملاحظة فيها إنجليزي وأرقام وشيفرة](screenshots/matrix/ar-ghasaq-mixed-read.png) | ![لوحة الأوامر](screenshots/ui/ar-ghasaq-command-palette.png) |

بقية اللقطات في [`screenshots/`](screenshots/). وفيها مصفوفة كاملة: الوضعان، والواجهتان العربية والإنجليزية، والتحرير والقراءة، وCanvas، والرسم البياني، وBases، والإعدادات.

## المزايا

**الطباعة العربية**
- المتن بخط **Noto Naskh Arabic** مضمَّنًا، بوزنين حقيقيين 400 و700، وارتفاع سطر 1.9 حتى لا يتصادم التشكيل.
- العناوين والواجهة بخط **Cairo** مضمَّنًا، فتتّحد الواجهة على كل الأنظمة.
- الخط العربي مقصور على الحروف العربية (`unicode-range`)، فتأخذ الكلمات اللاتينية خطًّا لاتينيًا من النظام، بمائل حقيقي.
- **لا ميل اصطناعي للعربية:** التوكيد بلون خفيف بدل الميل.
- **لا تباعد حروف:** صفر في كل نص قد يكون عربيًا.
- **لا قصّ للتشكيل:** في التبويبات والمستكشف والمخطط والعناوين.
- الحجم البصري بين العربي واللاتيني موزون بـ `size-adjust`، دون المساس بحجم الخط الذي تختاره.

**الاتجاه والنص المختلط**
- يبني على دعم Obsidian الأصلي لـ RTL ولا يحاربه، ويكمل ما ينقصه:
  - كتل الشيفرة والرياضيات وMermaid LTR دائمًا.
  - الشيفرة المضمّنة معزولة داخل السطر العربي.
  - اختصارات المفاتيح لا تنقلب.
  - سهم الـ callout المطويّ يشير إلى جهة نهاية السطر.
- حدّ الاقتباس، وأيقونة الـ callout، والنقاط، والمهام، والأرقام، والجداول، والحواشي، وأسهم الطيّ، وأرقام الأسطر، ولوحة الخصائص: كلها في جهتها في الاتجاهين.

**الألوان**
- سلّم `--color-base` كامل لكل وضع، وألوان الشيفرة والـ callouts وCanvas والرسم البياني من عائلة واحدة.
- التباين مفحوص آليًا وفق WCAG في كل بناء: النص الأساسي 11:1 فأكثر، والثانوي والتمييز والوسوم 4.5:1 فأكثر.
- إن اخترت لون تمييز من إعدادات Obsidian فاختيارك يتقدّم، والكهرماني افتراضي فقط.

## التثبيت

### من متجر الثيمات

غسق مدرج في [دليل ثيمات Obsidian](https://community.obsidian.md/themes/ghasaq)، فاضغط «Add to Obsidian» من صفحته، أو من داخل التطبيق:

1. افتح **الإعدادات ← المظهر ← السمات ← إدارة**.
2. ابحث عن **Ghasaq**.
3. اضغط **تثبيت واستخدام**.

### يدويًا

1. نزّل `manifest.json` و`theme.css` من [آخر إصدار](https://github.com/iSltanX/Ghasaq/releases/latest).
2. ضعهما في `.obsidian/themes/Ghasaq/` داخل خزينتك.
3. اختر Ghasaq من الإعدادات ← المظهر.

يحتاج Obsidian **1.14.4** فأحدث. اختُبر على 1.14.4 و1.15.0 على macOS.

## الإعدادات

الثيم يعمل كاملًا بدون إضافة [Style Settings](https://github.com/obsidian-community/obsidian-style-settings). إن ثبّتّها ظهرت الخيارات التالية بعناوين عربية:

| الخيار | ما يفعله |
|---|---|
| خط المتن | اتركه فارغًا للخط المضمَّن، أو اكتب اسم خط مثبّت على جهازك (مثل Amiri) |
| ارتفاع السطر | من 1.6 إلى 2.2 (الافتراضي 1.9) |
| عرض سطر القراءة | من 560 إلى 960 بكسل (الافتراضي 720) |
| محاذاة المتن | بداية السطر (افتراضي) أو ضبط. Chromium لا يدعم الكشيدة، فالضبط يوسّع الفراغات |
| لون التمييز | كهرماني (افتراضي)، أو نحاسي، أو بنفسجي غسقي |
| لون العناوين | بلون النص (افتراضي) أو بلون التمييز |
| تباين أعلى | يرفع تباين النص الثانوي والخافت والحدود |
| فاصل `---` مزخرف | معيّن صغير بلون آخر الضوء بين خطين |
| ضبط الشطر في القصيدة | يمدّ كل شطر على عرض عموده بدل توسيطه |

## القصيدة العمودية

أضف الصنف `qasida` إلى خصائص الملاحظة، واكتب الأبيات جدولًا من عمودين: الصدر في العمود الأول، والعجز في الثاني. اترك صف الترويسة فارغًا، فهو صف يفرضه Markdown والثيم يخفيه.

```markdown
---
cssclasses:
  - qasida
---

| | |
| --- | --- |
| الخَيْلُ وَاللَّيْلُ وَالبَيْدَاءُ تَعْرِفُنِي | وَالسَّيْفُ وَالرُّمْحُ وَالقِرْطَاسُ وَالقَلَمُ |
| أَنَا الَّذِي نَظَرَ الأَعْمَى إِلَى أَدَبِي | وَأَسْمَعَتْ كَلِمَاتِي مَنْ بِهِ صَمَمُ |
```

**النتيجة:**
- الصدر في جهة البداية والعجز بعده، بعرضين متساويين، وبينهما فراغ واضح.
- بلا حدود ولا ترويسة.
- يعمل في وضع القراءة وفي Live Preview، ويتحمّل التشكيل التام، ويبقى RTL حتى تحت واجهة إنجليزية.

الملاحظة تبقى Markdown عاديًا. إن غيّرت الثيم يومًا ظهرت الأبيات جدولًا مقروءًا.

## الخطوط

| الخط | الاستعمال | الرخصة |
|---|---|---|
| [Noto Naskh Arabic](https://github.com/notofonts/arabic) | المتن (الحروف العربية) | SIL OFL 1.1: [`fonts/OFL-NotoNaskhArabic.txt`](fonts/OFL-NotoNaskhArabic.txt) |
| [Cairo](https://github.com/Gue3bara/Cairo) | العناوين والواجهة | SIL OFL 1.1: [`fonts/OFL-Cairo.txt`](fonts/OFL-Cairo.txt) |

الخطّان مضمَّنان في `theme.css` بصيغة woff2 مجزّأة، فلا طلبات شبكة. الكلمات اللاتينية في المتن تأخذ خط النظام (Iowan Old Style ← Charter ← Georgia)، والشيفرة خط mono النظام.

## قيود معروفة

- **حقل التاريخ في الخصائص:** يعرض حروف «يوم/شهر/سنة» معكوسة تحت الواجهة العربية. هذا عيب في Obsidian/Chromium يظهر في الثيم الافتراضي أيضًا.
- **الصورة المنفردة في سطرها:** تأخذ اتجاه LTR، لأن السطر بلا حرف قوي فيأخذ `dir=auto` اتجاه LTR، وهذا سلوك Obsidian.
- **الجوال وWindows وLinux:** لم تُختبر على أجهزة حقيقية بعد.

## المشكلات والاقتراحات

- **وجدت خللًا؟** افتح [بلاغًا](https://github.com/iSltanX/Ghasaq/issues/new) وأرفق لقطة شاشة، واذكر نسخة Obsidian والجهاز ولغة الواجهة.
- **عندك فكرة؟** افتح [اقتراحًا](https://github.com/iSltanX/Ghasaq/issues/new) وصِف ما تريد.

## التطوير

- **الهوية في Figma هي مصدر الحقيقة:** الألوان والمقاسات والطباعة تُعدَّل هناك. ثم يُشغَّل `scripts/figma/export-variables.js` عبر Figma MCP، ويُحفظ ناتجه في `tokens/figma.json`.
- **أمر البناء الواحد:**

  ```
  python3 scripts/build.py
  ```

  يولّد `src/tokens.css` و`src/fonts.css`، ويجمع `src/` في `theme.css`. ويُفشل البناء إن نزل التباين، أو ظهرت خاصية فيزيائية خارج مناطق LTR الموثّقة، أو `!important`، أو رابط خارجي، أو تجاوز الحجم 700KB، أو فسد `manifest.json` أو كتلة Style Settings.
- **سكربتات الاختبار:**
  - `scripts/obsidian-test.sh`: يشغّل نسخة Obsidian معزولة على `test-vault/`. إضافة Style Settings لا تُرفع مع المستودع؛ ثبّتها في الخزينة من المتجر، أو انسخها إلى `test-vault/.obsidian/plugins/obsidian-style-settings/`.
  - `scripts/cli-check.sh`: يتحقق عبر Obsidian CLI.
  - `scripts/shoot-matrix.sh`: يلتقط مصفوفة اللقطات.
- **الإصدار:** ارفع `version` في `manifest.json`، وأضف سطرًا إلى [CHANGELOG.md](CHANGELOG.md)، ثم ادفع وسمًا بالرقم نفسه، فينشئ GitHub Actions مسودّة الإصدار.

## شكر

- [Noto Naskh Arabic](https://github.com/notofonts/arabic) من مؤلفي مشروع Noto.
- [Cairo](https://github.com/Gue3bara/Cairo) من مؤلفي مشروع Cairo.
- إضافة [Style Settings](https://github.com/obsidian-community/obsidian-style-settings) التي جعلت الإعدادات ممكنة.
- فريق [Obsidian](https://obsidian.md) على دعم الواجهة من اليمين إلى اليسار.

## الرخصة

كود الثيم برخصة [MIT](LICENSE). الخطوط المضمَّنة برخصة SIL Open Font License 1.1، وحقوقها ونصّ رخصتها في [`fonts/NOTICE.md`](fonts/NOTICE.md).

---

<p align="center"><sub>
  تصميم وتطوير: سلطان العنزي — Sultan Al-Anazi · <a href="https://bysltan.com">bysltan.com</a>
</sub></p>

</div>
