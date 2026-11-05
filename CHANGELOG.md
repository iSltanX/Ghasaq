# سجل التغييرات · Changelog

صيغة الإصدارات `x.y.z`، ويطابق وسم كل إصدار على GitHub رقم `version` في `manifest.json`.

## 1.0.0 · 2026-11-05

الإصدار الأول.

- **الوضعان:** «غَسَق» الداكن و«أصيل» الفاتح، بسلّم `--color-base` كامل لكلٍّ منهما، وألوان الشيفرة والـ callouts وCanvas والرسم البياني من عائلة واحدة.
- **الخطوط المضمَّنة:** Noto Naskh Arabic للمتن، وCairo للعناوين والواجهة، بوزنين حقيقيين 400 و700.
- **الطباعة العربية:**
  - لا تباعد حروف، ولا ميل اصطناعي.
  - ارتفاع سطر 1.9، وموازنة العربي باللاتيني بـ `size-adjust`.
  - حماية التشكيل من القصّ في العناصر أحادية السطر.
- **الاتجاه:**
  - كتل الشيفرة والرياضيات وMermaid LTR دائمًا، والشيفرة المضمّنة واختصارات المفاتيح معزولة.
  - إصلاح سهم الـ callout المطويّ في RTL.
  - إصلاح موضع سهم الطيّ في إضافة Style Settings تحت RTL.
- **وضع القصيدة:** `cssclasses: [qasida]` في القراءة وLive Preview.
- **Style Settings:** تسعة خيارات بعناوين عربية.
- **التباين:** مفحوص آليًا في كل بناء، ويحترم الثيم لون التمييز الذي يختاره المستخدم في Obsidian.

### English

First release: dark «Ghasaq» and light «Asil» modes, embedded Noto Naskh Arabic and Cairo, Arabic-first typography, mixed-direction fixes, qasida mode, nine Style Settings options, and automated WCAG contrast checks.
