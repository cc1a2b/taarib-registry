# taarib-registry

<div align="center">

[![License](https://img.shields.io/badge/license-CC0--1.0-blue.svg)](LICENSE)
[![Manifest](https://img.shields.io/badge/manifest-sequence%202-B7410E)](bayan.json)
[![Patches](https://img.shields.io/badge/patches-1-lightgrey)](isdar)
[![Index](https://img.shields.io/badge/index-267%20translations-2b6cb0)](fahras/tarjamat.json)
[![Client](https://img.shields.io/badge/client-Taarib-orange?style=flat&logo=rust)](https://github.com/cc1a2b/Taarib)

**سجلّ الرقع العام الذي يقرؤه عميل تعريب، وفهرسٌ لكل تعريب مجتمعي لألعاب الحاسوب أمكن التحقق منه في مصدره.**

*ملفات JSON ساكنة، وحزم مختومة، ولا خادم.*

[English](README.md)

</div>

> هذه نسخة عربية كاملة من التوثيق، لا ملخّص له. النسخة الإنجليزية في
> [`README.md`](README.md)، وعقد التخطيط التقني في `docs/mustawda.md` داخل
> مستودع العميل بالإنجليزية.

## نبذة

**taarib-registry** هو البيانات التي وراء زرّ «ثبّت الرقعة العربية» في
[تعريب](https://github.com/cc1a2b/Taarib). مستودع Git من ملفات ساكنة لا غير:
بيان، و256 شريحة فهرس، وقائمة سحب موقّعة، وحزم `.ruqaa` المختومة التي تشير
إليها الشرائح. يحلّ العميل التخطيط نفسه من GitHub، أو من مرآة CDN لهذا
المستودع، أو من مجلد على القرص، ولا يُؤتمَن أحدها أكثر من غيره، لأن كل بايت
يتصرّف العميل بناءً عليه يُفحص بتجزئة أو بتوقيع قبل أن يُقرأ.

ويحمل المستودع شيئًا لا يقرؤه العميل بعد: `fahras/`، فهرس مقروء آليًا
لتعريبات ألعاب الحاسوب التي صنعتها فرق وأفراد خارج تعريب، مع رابط موطن كل
تعريب والحقائق التي تصرّح بها صفحته. لا يستضيف السجلّ شيئًا منها. هو خريطة، لا
مرآة.

الكاتب والقائم على الصيانة [cc1a2b](https://github.com/cc1a2b).

---

## المحتويات

- [نبذة](#نبذة)
- [ما في الشجرة](#ما-في-الشجرة)
- [كيف يقرؤه العميل](#كيف-يقرؤه-العميل)
- [الختم والسحب](#الختم-والسحب)
- [مفتاح التطوير، بلا مواربة](#مفتاح-التطوير-بلا-مواربة)
- [الحزم المقدَّمة](#الحزم-المقدَّمة)
- [فهرس التعريبات المجتمعية](#فهرس-التعريبات-المجتمعية)
- [استعمال السجلّ](#استعمال-السجلّ)
- [بداية سريعة](#بداية-سريعة)
- [أمثلة الاستعمال](#أمثلة-الاستعمال)
- [مرجع الأوامر](#مرجع-الأوامر)
- [استعمال متقدّم](#استعمال-متقدّم)
- [المساهمة](#المساهمة)
- [الرخصة](#الرخصة)
- [الدعم](#الدعم)

---

## ما في الشجرة

```
bayan.json                       البيان: المخطط، والتسلسل، وتجزئة BLAKE3 واحدة لكل شريحة
sharaih/00.json … ff.json        256 شريحة؛ كلها دائمًا، والفارغة منها أيضًا
sahb/qaima.json                  قائمة السحب، موقّعة بـ Ed25519 بمفتاح المالك
isdar/<lineage>/<slug>-r<n>.ruqaa الحزم المختومة؛ البايتات نفسها مرفقة في إصدار GitHub
fahras/tarjamat.json             فهرس التعريبات المجتمعية (مُحقَّق يدويًا، لا مسبوك)
fahras/mukhattat.json            مخطط JSON Schema له (مسودة 2020-12)
fahras/jadwal.py                 يتحقق من الفهرس ويولّد الجداول أدناه
LICENSE                          CC0 1.0 مع إشعار الناشر
```

في المستودع نوعان من الملفات يُصنعان بطريقتين مختلفتين.

**الملفات المسبوكة** (`bayan.json` و`sharaih/` و`sahb/` و`isdar/`) يكتبها
`crates/taarib-mustawda/src/bin/sabk.rs` في مستودع العميل. لا يُكتب فيها حرف
باليد: كل حقل في القائمة يُقرأ من البيانات الوصفية المختومة داخل الحزمة نفسها،
وكل شريحة تُجزَّأ وهي تُكتب، وما البيان إلا قائمة تلك التجزئات. غيّر بايتًا
واحدًا في شريحة يرفض العميل الشريحة كلها، فالسبيل الوحيد لتغييرها هو إعادة
تشغيل السابك مع زيادة رقم التسلسل. عقد التخطيط في `docs/mustawda.md` داخل
مستودع العميل.

**الملفات المُحرَّرة** (`fahras/` وهذا الملف و`LICENSE`) يكتبها إنسان. يفحص
`fahras/jadwal.py` الفهرس على مخططه، لكن محتواه ما قرأه أحدٌ في صفحة ودوّنه،
ويقول ذلك في كل مدخل.

### الأرقام، بحسب آخر سبك

| ما | القيمة |
| --- | --- |
| مخطط البيان / التسلسل | 1 / 2، سُبك في 2026-09-04T22:27:58Z |
| الشرائح | 256؛ 255 منها الشريحة الفارغة ذات 23 بايتًا `{"ruqaa":{},"aswat":{}}`، والشريحة `67` تحمل قائمة واحدة |
| حجم البيان | 20 810 بايتًا، تجزئة BLAKE3 من 64 خانة ست‌عشرية لكل شريحة |
| قائمة السحب | التسلسل 2، 323 بايتًا، 0 مدخلات، صالحة حتى 2027-09-04 |
| الحزم | سلالة واحدة، المراجعة 2، 44 976 بايتًا |
| مفتاح التوقيع | مفتاح التطوير المُلتزَم `e4260a5f…4cea` (انظر أدناه) |
| الفهرس | 267 تعريبًا، 21 فريقًا، فُحص في 2026-09-11 |

---

## كيف يقرؤه العميل

كل ما يلي هو ما يفعله `crates/taarib-mustawda`؛ الجمل وصفٌ لشيفرة لا لسياسة.

### المصادر، بترتيب تجربتها

تسمّي إعدادات العميل (`IdadatMasadir`) ثلاثة أنواع من المصادر، وتحوّلها
`silsilat_masadir` في الاستوديو إلى سلسلة واحدة:

1. **المجلدات المحلية أولًا** (`mahalliya`): أي مجلد ضبطه المستخدم يحمل نسخة من
   هذه الشجرة، سواء أكان `git clone` على القرص أم مشاركة شبكية مركّبة. لا تكلّف
   شيئًا، وتعمل بلا اتصال، ومن ضبط واحدًا منها أراد أن يُسأل قبل المصدر
   الرئيسي. لا شيء منها مضبوط افتراضيًا.
2. **المصدر الرئيسي** (`rasmi`)، وافتراضيّه `https://github.com/cc1a2b/taarib-registry`.
3. **المرايا** (`maraya`)، وافتراضيّها
   `https://cdn.jsdelivr.net/gh/cc1a2b/taarib-registry@main`.

يُلحق مسار المستودع مثل `bayan.json` أو `sharaih/67.json` بكل جذر ويُجلب عبر
`https` فقط؛ جذرُ `http` يُرفض قبل فتح المقبس، والتحويلات محدودة بثلاث ولا يجوز
أن تنزل إلى `http`، والجسم الذي يتجاوز 8 ميبيبايت يُقطع وهو يصل، والمصدر الذي
يجيب بغير 2xx يخسر دوره للمصدر التالي.

نتيجة واحدة تستحق التصريح لأنها لا تُستشفّ من شاشة الإعدادات. الـ `rasmi`
الافتراضي هو *صفحة ويب* المستودع، وGitHub يجيب على
`https://github.com/cc1a2b/taarib-registry/bayan.json` بـ 404. فينتقل العميل،
وبالإعدادات الافتراضية **تخدم مرآة jsDelivr كل بيان وكل شريحة**؛ ولا يخدم مدخل
المصدر الرئيسي شيئًا إلا إن غُيّر إلى جذر المحتوى الخام
`https://raw.githubusercontent.com/cc1a2b/taarib-registry/main`. تحقّقنا من ذلك
بقارئ العميل نفسه في 2026-09-11: الـ `rasmi` الافتراضي وحده يفشل بـ «answered
404»، والثنائي الافتراضي ينجح من المرآة، والجذر الخام ينجح من المصدر الرئيسي.
والكتالوج واحد من أيّها جاء، لأن الموثوق به سلسلة تجزئات البيان لا المضيف.

### البيان وحارس التراجع

يُحلَّل `bayan.json` بـ `deny_unknown_fields`؛ الحقل الذي لا تعرفه هذه البنية
بيانٌ تالف لا امتدادٌ متوافق مستقبلًا. و`tasalsul` لا يزيد إلا صعودًا. يمرّر
العميل آخر تسلسل قبله إلى المحلّل، والبيان الأدنى منه يُرفض بوصفه تراجعًا
(`TasalsulLilkhalf`). من رأى عميله التسلسل 2 سيرفض التسلسل 1 إلى الأبد، ولهذا
يجب أن يزيد التسلسل مع كل نشر، حتى النشر الذي لا يبدّل إلا ملف إصدار.

### أيّ الشرائح، ولماذا توجد 256 كلها

شريحة اللعبة هي البايت الأول من تجزئة BLAKE3 لهويتها، والهوية UUIDv5 على
`steam:<appid>` والعنوان المطبَّع (`LubaId::min_masdar`). R.E.P.O. (Steam
3241660) تُجزَّأ إلى `9034a136-69b8-5ca2-a603-8b000f600abd`، وأول بايت من
تجزئتها `0x67`، فقائمتها في `sharaih/67.json` لا في غيره. يجلب العميل البيان
وشريحةً واحدة لكل دلوٍ مختلف تقع فيه مكتبته هو، ستًّا في الأكثر معًا، ولا يجلب
الكتالوج كله أبدًا.

الشريحة التي لا تُحلّ تُعامَل فشلًا لجلب الفهرس كله لا جوابًا فارغًا، لأن
الشريحة التي تعذّر الوصول إليها والشريحة الغائبة تبدوان سواء على السلك. ولهذا
تُنشر الشرائح الـ 256 كلها حتى وإن كانت 255 منها فارغة: كتالوج فتيّ لا ينشر
إلا شرائحه غير الفارغة سيُري لا شيء البتة لكل مستخدم تقع ألعابه في الدلاء
الأخرى.

### التجزئة قبل التحليل والمخبأ

لا تصير بايتات الشريحة `ShareehaMuwaththaqa` إلا عبر منشئ واحد يجزّئها ويقارن
التجزئة بمدخل البيان قبل أن يحلّل سجلًا واحدًا. ولا سبيل آخر إلى الحصول عليها،
فمحتوى الفهرس غير المُتحقَّق منه لا يمكن تمثيله في العميل، فضلًا عن قراءته.
تُخبَّأ الشرائح المُتحقَّق منها تحت مجلد بيانات العميل في
`makhbaa/mustawda/sharaih/`؛ وفي التحديث التالي تُقرأ الشريحة المخبّأة التي ما
زالت تجزئتها تطابق البيان من القرص ولا تُطلب أبدًا، فالكتالوج الذي لم يتغير
يكلّف جلبَ بيانٍ واحد وصفر شريحة. يعمل التحديث في الخلفية كل 180 دقيقة
افتراضيًا، و`wadaa_ghayr_muttasil` يطفئ الشبكة كلّيًا لمن يريد ذلك الضمان،
تاركًا المجلدات المحلية مصادر وحيدة.

### ملفات الإصدار

تحمل القائمة عنوانَي `https` مطلقَين، `rabt` و`rabt_mira`، وحجم الحزمة، وتجزئة
BLAKE3 لملف الحزمة. يرفض المنزّل أي عنوان ليس `https` أو يتجاوز 2048 بايتًا أو
يحمل حرف تحكّم قبل أن يفتح مقبسًا؛ ويستأنف النقل المقطوع بـ
`Range: bytes=<n>-` ويبدأ من الصفر إن تجاهل الخادم المدى؛ وينتقل إلى المرآة
من الإزاحة نفسها؛ ويجزّئ البايتات وهي تصل، فالحزمة التي لا تطابق قائمتها تُطرح
قبل أن تُفتح أصلًا. للحزمة الوحيدة هنا المصدرُ الأول ملف إصدار على GitHub
(`nashr-2`) والمرآةُ الملف نفسه داخل هذه الشجرة تخدمه jsDelivr على الوسم
`nashr-2`.

### التثبيت

تسلك الحزمة المنزَّلة الطريق نفسه الذي يسلكه ملفٌ مستورَد أو نسخة من مشاركة
شبكية: الحجر، ثم بوابة ما قبل التثبيت في `taarib-aman` (التوقيع تحت مرساة
البنية، وقائمة السحب، وأدلة مكافحة الغش واللعب الجماعي، والسلامة)، التي تسكّ
الإذن الذي يشترطه `taarib-tathbeet`. والاستعادة بايتًا ببايت؛ مشوار التحقق في
`docs/mustawda.md` أعاد 208 ملفات و1 492 605 039 بايتًا مطابقةً للنسخة
البِكر.

---

## الختم والسحب

كل `.ruqaa` موقَّعة بـ Ed25519 على تجزئة محتواها، والمفتاح العام للموقّع مكتوب
في كتلة توقيع الحزمة نفسها. حقل `musahim` في القائمة هو ذلك المفتاح لا اسمًا
كتبه من نشر، فلا تستطيع قائمة أن تدّعي هوية لا يسندها ختمها. يستعمل التحقق
`verify_strict` الذي يرفض المفاتيح ذات الرتبة الصغيرة وغير القانونية التي كان
فحصٌ متساهل سيقبلها.

توجد مرساتا ثقة وهما بنيتان مختلفتان بنيويًا. تُصرَّف بنية الإصدار من العميل مع
`TAARIB_MIFTAH_ISDAR` مضبوطًا على المفتاح العام لإصدار المالك؛ وتُصرَّف بنية
التطوير من دونه وترسو على مفتاح التطوير المُلتزَم. كل بنية تثق بمرساتها لا
بغيرها، وبنية الإصدار ترفض مفتاح التطوير **بالاسم**
(`SababTawqee::TawqeeTatwir`) لا بوصفه مجرد مفتاح مجهول.

`sahb/qaima.json` هي مفتاح الإيقاف. تستطيع سحب مفتاح توقيع، أو سلالة رقعة، أو
تجزئة محتوى واحدة، لكلٍّ سببٌ وختمٌ زمني؛ وهي موقّعة بمفتاح المالك على صيغة
بايتات قانونية (`taarib.qaimat-sahb.v1\0` تتلوها حقول مسبوقة بأطوالها بترتيب
`BTreeMap`)، وتحمل تسلسلها الخاص بقاعدة التراجع نفسها التي للبيان، وتنقضي بعد
سنة من السبك حتى يُبلغ السجلُّ الذي لم يعد أحد توقيعه في سنة عن نفسه بذلك
تحديدًا. يجلبها العميل من سلسلة المصادر نفسها، ويتحقق منها قبل أن يعيدها،
ويسجّل نتيجة كل تحديث بجانب المخبأ، فلا تُقرأ القائمة الفارغة «لا شيء مسحوب»
حين تعني «لم يسأل أحد». في 2026-09-11 تحقّقت القائمة الحية تحت مفتاح التطوير،
وساوى تسلسلها تسلسل البيان، ولم يكن مفتاح النشر فيها، ورُفض قلبُ بايت واحد من
التوقيع، ورُفضت البايتات نفسها تحت مفتاح مالك مختلف.

---

## مفتاح التطوير، بلا مواربة

**كل ما هنا مختوم بمفتاح تطوير تعريب.** نصفه العام
`e4260a5f02029a64b6a41a31a5db53e0af74d6110122d9a352a721a2438b4cea`، وهو
مُلتزَم في مستودع العميل باسم `MIFTAH_TATWIR`، ونصفه الخاص في سلسلة مفاتيح
مطوّر لا تحمي شيئًا. وقائمة السحب موقّعة بالمفتاح نفسه، وهذا المعنى الوحيد
الذي يكون به أيّ شيء هنا «موقَّعًا من المالك» اليوم.

ما يعنيه ذلك لك:

- **بنية الإصدار المنزَّلة من تعريب ترفض كل حزمة في هذا السجلّ، عمدًا.** تسمّي
  المفتاح وتقول ذلك؛ هذا السلوك المقصود لا عيبٌ يُلتفّ عليه.
- **البنية المصرَّفة من دون `TAARIB_MIFTAH_ISDAR` تقبلها.** تلك بنية التطوير،
  وشاشة المكتبة ترسم طوال الوقت الشريط «نسخة تطوير — تثق بمفتاح التطوير المعلن
  لا بمفتاح الإصدار».

لم يُسكّ مفتاح توقيع الإصدار. يصف `docs/mustawda.md` §7.1 في مستودع العميل
الأداة التي تسكّه، على جهاز المالك، في سلسلة مفاتيح المنصة، كاتبةً النصف العام
وحده في ملف. وحين يحدث ذلك، ستُعاد ختمُ كل حزمة وقائمة السحب هنا ونشرُها تحت
تسلسل جديد، وستصير القديمة غير قابلة للتثبيت على بنى الإصدار، وهذه الخاصية هي
ما يجعل المرساة تساوي شيئًا. لن يحوي هذا المستودع مفتاحًا خاصًا أبدًا، ولا يوجد
مسار توقيع ثانٍ ولا يجوز أن يُضاف.

---

## الحزم المقدَّمة

سلالة واحدة، `01a06d42-dc5d-74b2-b27d-5c4441a03a3f`، للعبة **R.E.P.O.** (Steam
3241660، البناء `23363152`، Unity 2022، Mono)، مدرجة باسم «REPO — Arabic».

| المراجعة | البايتات | BLAKE3 | الطريقة المصرَّح بها | الحالة |
| --- | --- | --- | --- | --- |
| r1 | 45 472 | `fac7dfa2…2f0a` | `bashariya_kamila` — «ترجمة بشرية كاملة» | **مسحوبة** 2026-09-04 (الإيداع `c543ae1`)، والإصدار محذوف |
| r2 | 44 976 | `75ee52cc…4003` | `aaliya_faqat` — «ترجمة آلية دون مراجعة» | مقدَّمة: ملف `nashr-2` و`isdar/…/r-e-p-o-r2.ruqaa` |

الصدق في وصف هذه الرقعة أن يُقال إنها وُجدت لإثبات النقل لا لتُلعب. نصوصها
التسعون مسودات آلية لم يعتمدها مراجع (`musawwada: 90, muakkada: 0`)، ولم
تسجّل جلسة التقاط افتتاحَ اللعبة قط فلم تُقَس تغطية الساعة الأولى أصلًا،
وبوابة التغطية فيها تقول `qabila_lil_nashr: false`. ومع ذلك صرّحت r1 بـ
`tareeqa: bashariya_kamila` تحت اسم مساهم «haqiqi walk»، وهو اسم لا يظهر في
مصدر ولا في مثبّت اختبار ولا في سجل. وذلك التصريح يقع داخل البيانات الوصفية
المختومة، فتصحيحه معناه إعادة ختم لا تحرير: r2 تصرّح بـ `aaliya_faqat`، وتسمّي
مفتاح التطوير مساهمًا، وتقصّ أطلس المحارف من 4096×4096 إلى 4096×128 (المحارف
الـ 315 نفسها، وأقل بـ 16 ميبيبايت في التخصيص). أُزيلت r1 من الشجرة وسُحب
إصدارها في النشر نفسه. ولم يُعدَّل أيٌّ من الملفين المختومين منذ ذلك؛ لا تُحرَّر
الحزمة في مكانها أبدًا، وإنما تُستبدَل بلاحقة.

`rukhsa` القائمة CC0، و`aila: unity`، و`khalfiya: mono`، و`tabaqa: kamil`
(الطبقة الساكنة الكاملة)، وارتباطها معرّفُ بناء المشغّل
`steam-3241660-build-23363152` وبصمةُ محتوى واحدة، وهما ما تطابق به `mutabaqa`
النسخة المثبّتة.

الملفات التي **ليست** هنا عمدًا: مثبّتات الاختبار التي تنتجها مشاوير العميل
نفسه (`khayal-saif` و`mithal` و`mutanakkir` ومجلدات `taarib_fath_*` وقصاصات
الـ 624 بايتًا التي يختمها حامل استعادة بمفتاح مؤقت)، والنسخة العاملة غير
المضغوطة التي يضعها المثبّت بجانب اللعبة. ليس منها ما هو ترجمة لأي شيء.

## تجاوزات النشر

يرفض السابك الحزمة التي حكمُ تغطيتها `false` إلا إن كتب المشغّل جملة تشرح لماذا
تُنشر رغم ذلك، وتُكتب تلك الجملة في `bayan.json` مدخلًا في `tajawuzat` يسمّي
السلالة والمراجعة بعينها وأسبابَ البوابة الحاجبة بنصّها. يحمل البيان حاليًا
مدخلًا واحدًا كهذا، لـ r2، سببه: «لم تسجّل جلسة التقاط افتتاح اللعبة، فلم تُقَس
تغطية الساعة الأولى البتة». لا تعرضه واجهة في العميل بعد؛ الحقل سجلٌّ عام
باقٍ لا أكثر.

---

## فهرس التعريبات المجتمعية

يجيب `fahras/tarjamat.json` عن سؤال غير سؤال الشرائح: لا «ما الذي يستطيع تعريب
تثبيته» بل «ما التعريبات العربية لألعاب الحاسوب الموجودة أصلًا، وأين». رقع
تعريب مختلفة بنيويًا (مشكَّلة عبر HarfRust بلا أشكال عرض، مختومة، مراجَعة قبل
النشر، قابلة للسحب)؛ وأكثر ما يدرجه الفهرس عملُ استبدال ملفات من فرق هواة،
بعضه ممتاز وبعضه مخرجات آلية، والفهرس لا يقيّمه. يسجّل ما تقوله كل صفحة.

### ما ليس هو

- لا يستضيف شيئًا ولا يعيد توزيع شيء. كل مدخل رابطٌ إلى موطن التعريب نفسه
  والحقائقُ المصرَّح بها هناك.
- لا يكفل قانونية ولا جودة ولا أمانًا. حقل `rukhsa` هو الرخصة **كما يصرّح بها
  أصحابها**؛ وحيث لا تصرّح الصفحة بشيء يقول المدخل `ghayr_musarraha` ولا
  يُستنتَج شيء. وأكثر الصفحات لا تصرّح بشيء.
- ليس حصرًا شاملًا ولا لوحة تصنيف. الاتساع والدقة هما الغاية لا الكمّ.

### قاعدة الإدراج

لم يُضَف مدخل إلا إن جُلب `rabt` وقُرئ في التاريخ المذكور في `tahaqquq.waqt`
بإحدى الوسائل المسجَّلة:

| `tahaqquq.tareeqa` | ما الذي قُرئ |
| --- | --- |
| `safha` | الصفحة نفسها عبر HTTPS |
| `api_nexus` | يجيب Nexus Mods طلبات غير المتصفحات بـ 403، فقُرئت قوائمه عبر واجهة GraphQL v2 الخاصة به بنطاق اللعبة ومعرّف المود (`legacyModsByDomain`)؛ وكتلة الأذونات غير مكشوفة هناك، فلا يدّعي أي مدخل من Nexus رخصة |
| `api_github` | واجهة GitHub REST: بيانات المستودع وملف الرخصة والإصدارات وREADME |
| `api_gamebanana` | سجل الملف الشخصي `apiv11` في GameBanana، وهو يحمل حقل الرخصة فعلًا |
| `api_thunderstore` | قائمة حزم المجتمع، مع صفحة الحزمة |

استُبعدت الألعاب التي لا تعمل على الحاسوب إلا بالمحاكاة (عناوين نينتندو في
قوائم عدة فرق). واستُبعدت تعريبات *المودات* لا الألعاب، ومودات الخطوط وحدها،
وقوائم Nexus التي حالتها `removed` أو `hidden` أو `wastebinned`. واستُبعد
العمل الذي لا يوزَّع إلا عبر Discord أو أوصاف YouTube أو روابط المنتديات
المختصرة أو مواقع التجميع (Metro Exodus وJedi: Fallen Order من AR Team،
ومشروع Civilization VI، وتعريبات Skyrim المتداولة في المنتديات، ورقع Hades
وThe Sims 4 على مواقع الاستضافة) لأن لا صفحة مؤلَّفة أمكن جلبها لتسجيل حقائق
منها؛ واستُعملت مواقع التجميع muarrab.com وta3reb.com وmahfda.com
وfree-wargamer.com للعثور على صفحات الأصحاب وليست هي نفسها مفهرسة.

مُلئ `arabiya_rasmiya` من واجهة متجر Steam (اللغات المدعومة في `appdetails`)
يوم الفحص، لكل مدخل له معرّف تطبيق Steam أكّده بحثٌ في المتجر بمطابقة الاسم
تمامًا. يخفي تعريب واجهة التعريب الخاصة به عن اللعبة التي تشحن عربية رسمية
(`istibdal_lugha_rasmiya`)، ولهذا وُجد الحقل؛ و«نعم» بجانب رقعة هواة لا يجعل
الرقعة بلا قيمة، بل يعني أن اللعبة نالت العربية بعدها أو معها.

### الفهرس

مولَّد من `fahras/tarjamat.json` بـ `python3 fahras/jadwal.py`. التواريخ آخر ما
تصرّح به الصفحة؛ والأعداد تنزيلات أو مشتركو الورشة كما ظهرت ذلك اليوم.

<!-- fahras:start -->
**267** تعريبًا لـ **231** لعبة من **21** فريقًا وعددٍ من الأفراد. 216 منها مجاني، و51 مدفوع أو باشتراك. 54 تصرّح صفحته بترجمة بشرية أو تسمّي مترجميها، و10 تصرّح بترجمة آلية كليًا أو جزئيًا، والباقي لا يقول. 34 فقط تذكر رخصة أو شرط استعمال؛ الباقي لا يذكر شيئًا. 7 منها للعبة صار لها عربية رسمية بعد ذلك بحسب Steam.

<details>
<summary><strong>[الحلم المتجدد للتعريب](https://etrdream.com/)</strong> — 81</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Afterimage](https://etrdream.com/game/afterimage/) | 1701520 | لا | Eternal Dream Arabization; translation: Allen Wouka • Zojaj  | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-04-04 | 2026-09-11 |
| [AI LIMIT](https://etrdream.com/game/ai-limit/) | 2407270 | لا | Eternal Dream Arabization; translation: Allen Wouka (كلها) | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-01-04 | 2026-09-11 |
| [AM2R (Metroid 2 fan remake)](https://etrdream.com/game/am2r-metroid-2-fan-remake/) | — | ؟ | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2021-07-20 | 2026-09-11 |
| [Amnesia: The Bunker](https://etrdream.com/game/amnesia-the-bunker/) | 1944430 | لا | Eternal Dream Arabization; translation: فهد العتيبي | موقع الفريق | كاملة | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-10-23 | 2026-09-11 |
| [Armored Core VI: Fires of Rubicon](https://etrdream.com/game/armored-core-vi-fires-of-rubicon/) | 1888160 | لا | Eternal Dream Arabization; translation: ‏Allen Wouka • منصور | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-08-25 | 2026-09-11 |
| [Bad North](https://etrdream.com/game/bad-north/) | 688420 | لا | Eternal Dream Arabization; translation: مسدار | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-03-22 | 2026-09-11 |
| [Balatro](https://etrdream.com/game/balatro/) | 2379780 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-06-03 | 2026-09-11 |
| [Blue Archive: Love is War](https://etrdream.com/game/blue-archive-love-is-war/) | — | ؟ | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-07-21 | 2026-09-11 |
| [Bokutachi wa Benkyou ga Dekinai (visual novel)](https://etrdream.com/game/bokutachi-wa-benkyou-ga-dekinai-visual-novel/) | — | ؟ | Eternal Dream Arabization; translation: Flkrin / فلكرين • SH | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-06-12 | 2026-09-11 |
| [Bright Memory](https://etrdream.com/game/bright-memory/) | 955050 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-04-11 | 2026-09-11 |
| [Bright Memory: Infinite](https://etrdream.com/game/bright-memory-infinite/) | 1178830 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-04-12 | 2026-09-11 |
| [Buckshot Roulette](https://etrdream.com/game/buckshot-roulette/) | 2835570 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-03-28 | 2026-09-11 |
| [Call of the Sea](https://etrdream.com/game/call-of-the-sea/) | 1042490 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2022-09-26 | 2026-09-11 |
| [Celeste](https://etrdream.com/game/celeste/) | 504230 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2020-09-06 | 2026-09-11 |
| [Clair Obscur: Expedition 33](https://etrdream.com/game/clair-obscur-expedition-33/) | 1903340 | نعم | Eternal Dream Arabization; translation: Allen Wouka • KevRan | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-02-14 | 2026-09-11 |
| [Code Vein](https://etrdream.com/game/code-vein/) | 678960 | لا | Eternal Dream Arabization; translation: Allen Wouka • عبد ال | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-01-13 | 2026-09-11 |
| [Code Vein II](https://etrdream.com/game/code-vein-ii/) | 2362060 | لا | Eternal Dream Arabization; translation: Allen Wouka (كل النص | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-03-26 | 2026-09-11 |
| [CRYMACHINA](https://etrdream.com/game/crymachina/) | 2258500 | لا | Eternal Dream Arabization; translation: Allen Wouka (كلها، أ | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-05-29 | 2026-09-11 |
| [Cuphead](https://etrdream.com/game/cuphead/) | 268910 | لا | Eternal Dream Arabization; translation: Allen Wouka | موقع الفريق | كاملة | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-06-04 | 2026-09-11 |
| [Dark Souls II](https://etrdream.com/game/dark-souls-ii/) | 335300 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-08-06 | 2026-09-11 |
| [Dark Souls III](https://etrdream.com/game/dark-souls-iii/) | 374320 | لا | Eternal Dream Arabization | موقع الفريق | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-08-07 | 2026-09-11 |
| [Dark Souls: Remastered](https://etrdream.com/game/dark-souls-remastered/) | 570940 | لا | Eternal Dream Arabization; translation: منصور • جين • The So | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2022-10-03 | 2026-09-11 |
| [DARQ: Complete Edition](https://etrdream.com/game/darq-complete-edition/) | 433550 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2019-09-05 | 2026-09-11 |
| [Death's Door](https://etrdream.com/game/deaths-door/) | 894020 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-03-22 | 2026-09-11 |
| [Deltarune (Chapter 1)](https://etrdream.com/game/deltarune/) | 1671210 | لا | Eternal Dream Arabization; translation: السير مروان (المعرب  | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-12-24 | 2026-09-11 |
| [Doki Doki Literature Club](https://etrdream.com/game/doki-doki-litterature-club/) | 698780 | لا | Eternal Dream Arabization; translation: Allen Wouka • MAZ •  | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-02-03 | 2026-09-11 |
| [Dolls Nest](https://etrdream.com/game/dolls-nest/) | 1839430 | لا | Eternal Dream Arabization; translation: Tetetetetoris | موقع الفريق | كاملة | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-10-16 | 2026-09-11 |
| [Elden Ring](https://etrdream.com/game/elden-ring/) | 1245620 | نعم | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | مثبّت, استبدال ملفات | غير مذكورة | مجاني | منشورة | 2026-02-06 | 2026-09-11 |
| [Fate/stay night [Réalta Nua]](https://etrdream.com/game/fate-stay-night-realta-nua/) | — | ؟ | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-11-23 | 2026-09-11 |
| [FEZ](https://etrdream.com/game/fez/) | 224760 | لا | Eternal Dream Arabization; translation: مسدار • Allen Wouka | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-01-01 | 2026-09-11 |
| [Getting Over It with Bennett Foddy](https://etrdream.com/game/getting-over-it/) | 240720 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2020-08-26 | 2026-09-11 |
| [Guacamelee!](https://etrdream.com/game/guacamelee/) | 275390 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2021-12-23 | 2026-09-11 |
| [Half-Life](https://etrdream.com/game/half-life/) | 70 | لا | Eternal Dream Arabization; translation: Allen Wouka | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-03-23 | 2026-09-11 |
| [Half-Life 2](https://etrdream.com/game/half-life-2/) | 220 | لا | Eternal Dream Arabization | موقع الفريق | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-07-15 | 2026-09-11 |
| [Hollow Knight](https://etrdream.com/game/hollow-knight/) | 367520 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-07-27 | 2026-09-11 |
| [Hue](https://etrdream.com/game/hue/) | 383270 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-02-07 | 2026-09-11 |
| [Hydra Castle Labyrinth](https://etrdream.com/game/hydra-castle-labyrinth/) | — | ؟ | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-03-27 | 2026-09-11 |
| [Junji Ito Maniac: An Infinite Gaol](https://etrdream.com/game/junji-ito-maniac-an-infinite-gaol/) | 3633250 | لا | Eternal Dream Arabization; translation: KevRan | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-12-08 | 2026-09-11 |
| [Katana ZERO](https://etrdream.com/game/katana-zero/) | 460950 | لا | Eternal Dream Arabization; translation: آسغور • الضوء • ‏All | موقع الفريق | كاملة | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-04-19 | 2026-09-11 |
| [Kena: Bridge of Spirits](https://etrdream.com/game/kena-bridge-of-spirits/) | 1954200 | لا | Eternal Dream Arabization; translation: AdamSaeed، و Striver | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2021-12-23 | 2026-09-11 |
| [Lethal Company](https://etrdream.com/game/lethal-company/) | 1966720 | لا | Eternal Dream Arabization; translation: Allen Wouka | موقع الفريق | غير مصرّح بها | بشرية | BepInEx, خط | غير مذكورة | مجاني | منشورة | 2025-04-04 | 2026-09-11 |
| [Little Witch Nobeta](https://etrdream.com/game/little-witch-nobeta/) | 1049890 | لا | Eternal Dream Arabization; translation: ‏Allen Wouka • ‏Zoja | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-07-08 | 2026-09-11 |
| [Mark of the Ninja: Remastered](https://etrdream.com/game/mark-of-the-ninja-remastered/) | 860950 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-06-17 | 2026-09-11 |
| [MOTORSLICE](https://etrdream.com/game/motorslice/) | 2830030 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-05-31 | 2026-09-11 |
| [Mouthwashing](https://etrdream.com/game/mouthwashing/) | 2475490 | لا | Eternal Dream Arabization; translation: KevRan • Stryker24hz | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-03-25 | 2026-09-11 |
| [NieR Replicant ver.1.22474487139...](https://etrdream.com/game/nier-replicant-ver-1-22474487139/) | 1113560 | لا | Eternal Dream Arabization; translation: Allen Wouka • منصور | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-04-28 | 2026-09-11 |
| [NieR: Automata](https://etrdream.com/game/nier-automata/) | 524220 | لا | Eternal Dream Arabization; translation: ‏Allen Wouka (كلها ب | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-07-12 | 2026-09-11 |
| [Ori and the Blind Forest](https://etrdream.com/game/ori-and-the-blind-forest/) | 387290 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2019-09-09 | 2026-09-11 |
| [Pause Ahead](https://etrdream.com/game/pause-ahead/) | — | ؟ | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2019-01-01 | 2026-09-11 |
| [PEAK](https://etrdream.com/game/peak/) | 3527290 | لا | Eternal Dream Arabization; translation: AdamSaeed • GinJehad | موقع الفريق | غير مصرّح بها | بشرية | BepInEx, خط | غير مذكورة | مجاني | منشورة | 2026-03-25 | 2026-09-11 |
| [Pizza Tower](https://etrdream.com/game/pizza-tower/) | 2231450 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-11-23 | 2026-09-11 |
| [R.E.P.O.](https://etrdream.com/game/r-e-p-o/) | 3241660 | لا | Eternal Dream Arabization; translation: GINJEHAD • AdamSaeed | موقع الفريق | كاملة | بشرية | BepInEx, خط | غير مذكورة | مجاني | منشورة | 2025-06-22 | 2026-09-11 |
| [R.E.P.O.](https://thunderstore.io/c/repo/p/Eternal_Dream_Arabization/REPO_Arabic/) | 3241660 | لا | Eternal_Dream_Arabization | Thunderstore | غير مصرّح بها | بشرية | BepInEx, XUnity AutoTranslator | غير مذكورة | مجاني | منشورة | 2025-04-06 | 2026-09-11 |
| [Rise & Shine](https://etrdream.com/game/rise-and-shine/) | 347290 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2021-08-15 | 2026-09-11 |
| [RoboCop: Rogue City](https://etrdream.com/game/robocop-rogue-city/) | 1681430 | لا | Eternal Dream Arabization; translation: منصور، Allen Wouka،  | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-05-04 | 2026-09-11 |
| [ROKKO CHAN](https://etrdream.com/game/rokko-chan/) | — | ؟ | Eternal Dream Arabization | موقع الفريق | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2019-12-31 | 2026-09-11 |
| [Silent Hill 2 (2001, PC)](https://etrdream.com/game/silent-hill-2/) | 2124490 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-06-09 | 2026-09-11 |
| [Silent Hill 2 (2024)](https://etrdream.com/game/silent-hill-2-2024/) | 2124490 | لا | Eternal Dream Arabization; translation: AdamSaeed | موقع الفريق | غير مصرّح بها | بشرية | pak, خط | غير مذكورة | مجاني | منشورة | 2025-02-03 | 2026-09-11 |
| [Silent Hill 3](https://etrdream.com/game/silent-hill-3/) | — | ؟ | Eternal Dream Arabization; translation: AdamSaeed • منصور •  | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-12-28 | 2026-09-11 |
| [Silent Hill 4: The Room](https://etrdream.com/game/silent-hill-4/) | — | ؟ | Eternal Dream Arabization; translation: AdamSaeed • منصور | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-08-16 | 2026-09-11 |
| [Silent Hill f](https://etrdream.com/game/silent-hill-f/) | 2947440 | لا | Eternal Dream Arabization; translation: Allen Wouka | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-11-23 | 2026-09-11 |
| [SMT: Synchrocity](https://etrdream.com/game/smt-synchrocity/) | — | ؟ | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2020-08-13 | 2026-09-11 |
| [Snake Pass](https://etrdream.com/game/snake-pass/) | 544330 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2021-09-17 | 2026-09-11 |
| [Snowbreak: Containment Zone](https://etrdream.com/game/snowbreak-containment-zone/) | 2668080 | لا | Eternal Dream Arabization; translation: Allen Wouka • Desert | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-02-01 | 2026-09-11 |
| [Sonic Omens](https://etrdream.com/game/sonic-omens/) | — | ؟ | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-08-28 | 2026-09-11 |
| [Soulstice](https://etrdream.com/game/soulstice/) | 1602080 | لا | Eternal Dream Arabization; translation: Allen Wouka | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-12-20 | 2026-09-11 |
| [Stellar Blade](https://etrdream.com/game/stellar-blade/) | 3489700 | نعم | Eternal Dream Arabization; translation: Allen Wouka | موقع الفريق | كاملة | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-02-28 | 2026-09-11 |
| [Stray](https://etrdream.com/game/stray/) | 1332010 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2022-08-03 | 2026-09-11 |
| [The First Berserker: Khazan](https://etrdream.com/game/the-first-berserker-khazan/) | 2680010 | لا | Eternal Dream Arabization; translation: KOBY | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-10-09 | 2026-09-11 |
| [The Last Faith](https://etrdream.com/game/the-last-faith/) | 1274600 | لا | Eternal Dream Arabization; translation: KOBY • منصور • Majd  | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-02-25 | 2026-09-11 |
| [The Legend of Zelda: Twilight Princess (PC port)](https://etrdream.com/game/the-legend-of-zelda-twilight-princess/) | — | ؟ | Eternal Dream Arabization; translation: Allen Wouka (كامل ال | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-09-02 | 2026-09-11 |
| [Titan Souls](https://etrdream.com/game/titan-souls/) | 297130 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2021-12-23 | 2026-09-11 |
| [Touhou Luna Nights](https://etrdream.com/game/touhou-luna-nights/) | 851100 | لا | Eternal Dream Arabization; translation: Mega Hero | موقع الفريق | كاملة | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-08-21 | 2026-09-11 |
| [Ultra Age](https://etrdream.com/game/ultra-age/) | 1683100 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-03-29 | 2026-09-11 |
| [Wing of Darkness](https://etrdream.com/game/wing-of-darkness/) | 1179060 | لا | Eternal Dream Arabization | موقع الفريق | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-07-11 | 2026-09-11 |
| [Wuchang: Fallen Feathers](https://etrdream.com/game/wuchang-fallen-feathers/) | 2277560 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-08-24 | 2026-09-11 |
| [Wuthering Waves](https://etrdream.com/game/wuthering-waves/) | 3513350 | لا | Eternal Dream Arabization | موقع الفريق | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-07-02 | 2026-09-11 |
| [Yoku's Island Express](https://etrdream.com/game/yokus-island-express/) | 334940 | لا | Eternal Dream Arabization; translation: AdamSaeed، منصور | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-04-27 | 2026-09-11 |
| [Yume Nikki](https://etrdream.com/game/yume-nikki/) | 650700 | لا | Eternal Dream Arabization; translation: MAZ | موقع الفريق | غير مصرّح بها | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2024-06-11 | 2026-09-11 |
| [YUMENIKKI -DREAM DIARY-](https://etrdream.com/game/yumenikki-dream-diary/) | 774811 | لا | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2025-10-02 | 2026-09-11 |
| [Zelda: The Seeds of Darkness (fan game)](https://etrdream.com/game/zelda-the-seeds-of-darkness/) | — | ؟ | Eternal Dream Arabization | موقع الفريق | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2019-12-21 | 2026-09-11 |

</details>

<details>
<summary><strong>[العب بالعربي](https://www.playinarabic.com/fan)</strong> — 36</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [007 First Light](https://www.playinarabic.com/translations/007-first-light) | 3768760 | لا | Play in Arabic | موقع الفريق | كاملة | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2026-05-28 | 2026-09-11 |
| [Astroneer](https://www.playinarabic.com/translations/astroneer) | 361420 | لا | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2021-01-01 | 2026-09-11 |
| [Batman: Arkham Knight](https://www.playinarabic.com/translations/batman-arkham-knight) | 208650 | لا | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2024-01-01 | 2026-09-11 |
| [Bendy and the Ink Machine](https://www.playinarabic.com/translations/bendy-and-the-ink-machine) | 622650 | لا | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2025-05-30 | 2026-09-11 |
| [Crimson Desert](https://www.playinarabic.com/translations/crimson-desert) | 3321460 | نعم | Play in Arabic | موقع الفريق | كاملة | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | — | 2026-09-11 |
| [Ender Magnolia](https://www.playinarabic.com/translations/ender-magnolia) | — | ؟ | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2025-03-31 | 2026-09-11 |
| [FAMILY SECRETS 1 EMPTY PLATE](https://www.playinarabic.com/translations/family-secrets-1-empty-plate) | — | ؟ | Play in Arabic | موقع الفريق | كاملة | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2026-08-06 | 2026-09-11 |
| [Fears To Fathom Carson](https://www.playinarabic.com/translations/fears-to-fathom-carson) | — | ؟ | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2025-05-30 | 2026-09-11 |
| [Fears to Fathom Ironbark](https://www.playinarabic.com/translations/fears-to-fathom-ironbark) | 1965810 | ؟ | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2025-05-30 | 2026-09-11 |
| [Fears To Fathom Norwood](https://www.playinarabic.com/translations/fears-to-fathom-norwood) | 1965810 | ؟ | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2025-04-28 | 2026-09-11 |
| [Fears to Fathom Scratch Creek](https://www.playinarabic.com/translations/fears-to-fathom-scratch-creek) | 4121170 | لا | Play in Arabic | موقع الفريق | كاملة | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2026-06-20 | 2026-09-11 |
| [Fears to Fathom Woodbury](https://www.playinarabic.com/translations/fears-to-fathom-woodbury) | 1965810 | ؟ | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2025-05-30 | 2026-09-11 |
| [GYLT](https://www.playinarabic.com/translations/gylt) | 2206210 | لا | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2023-01-01 | 2026-09-11 |
| [Heavy Rain](https://www.playinarabic.com/translations/heavy-rain) | 960910 | لا | Play in Arabic | موقع الفريق | كاملة | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2026-05-04 | 2026-09-11 |
| [Hollow knight silksong](https://www.playinarabic.com/translations/hollow-knight-silksong) | 1030300 | لا | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | أولية | 2025-09-20 | 2026-09-11 |
| [Hollow knight silksong (GAME PASS)](https://www.playinarabic.com/translations/hollow-knight-silksong-game-pass) | 1030300 | لا | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | أولية | 2025-09-20 | 2026-09-11 |
| [Karma The Dark World](https://www.playinarabic.com/translations/karma-the-dark-world) | 1376200 | لا | Play in Arabic | موقع الفريق | كاملة | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2025-08-18 | 2026-09-11 |
| [Life Is Strange Double Exposure](https://www.playinarabic.com/translations/life-is-strange-double-exposure) | 3122800 | ؟ | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2025-10-21 | 2026-09-11 |
| [Mafia The Old Country](https://www.playinarabic.com/translations/mafia-the-old-country) | 1941540 | لا | Play in Arabic | موقع الفريق | كاملة | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2025-08-15 | 2026-09-11 |
| [Mafia: The Old Country DLC](https://www.playinarabic.com/translations/mafia-the-old-country-dlc) | 4492700 | لا | Play in Arabic | موقع الفريق | كاملة | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | — | 2026-09-11 |
| [Red Dead Redemption](https://www.playinarabic.com/translations/red-dead-redemption) | 1174180 | لا | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2024-01-01 | 2026-09-11 |
| [Remember Me](https://www.playinarabic.com/translations/remember-me) | 228300 | لا | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2023-01-01 | 2026-09-11 |
| [Silent Hill F](https://www.playinarabic.com/translations/silent-hill-f) | 2947440 | لا | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2025-09-23 | 2026-09-11 |
| [Someday You WIll Return](https://www.playinarabic.com/translations/someday-you-will-return) | — | ؟ | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2025-10-17 | 2026-09-11 |
| [Split Fiction](https://www.playinarabic.com/translations/split-fiction) | 2001120 | لا | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2025-03-06 | 2026-09-11 |
| [Stardew Valley](https://www.playinarabic.com/translations/stardew-valley) | 413150 | لا | Play in Arabic | موقع الفريق | كاملة | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2026-01-21 | 2026-09-11 |
| [supraland](https://www.playinarabic.com/translations/supraland) | 813630 | لا | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2023-01-01 | 2026-09-11 |
| [Tales Beyond The Tomb - No Witnesses](https://www.playinarabic.com/translations/tales-beyond-the-tomb-no-witnesses) | 4483120 | لا | Play in Arabic | موقع الفريق | كاملة | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2026-08-06 | 2026-09-11 |
| [Tales Beyond The Tomb - The Farm's Secret](https://www.playinarabic.com/translations/the-farms-secret) | 3374720 | لا | Play in Arabic | موقع الفريق | كاملة | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2026-04-15 | 2026-09-11 |
| [Tales Beyond The Tomb : The Last Vigil](https://www.playinarabic.com/translations/tales-beyond-the-tomb-the-last-vigil) | 3416690 | لا | Play in Arabic | موقع الفريق | كاملة | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2026-06-23 | 2026-09-11 |
| [The Blood of Dawnwalker](https://www.playinarabic.com/translations/the-blood-of-dawnwalker) | 3751260 | لا | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | أولية | — | 2026-09-11 |
| [the cave](https://www.playinarabic.com/translations/the-cave) | 221810 | لا | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2022-01-01 | 2026-09-11 |
| [The First Berserker Khazan](https://www.playinarabic.com/translations/the-first-berserker-khazan) | 2676630 | ؟ | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2025-04-24 | 2026-09-11 |
| [The Last of Us 2](https://www.playinarabic.com/translations/the-last-of-us-2) | 2531310 | لا | Play in Arabic | موقع الفريق | الحوار | غير مصرّح بها | غير مصرّح به | غير مذكورة | مدفوع | منشورة | 2025-08-06 | 2026-09-11 |
| [the room](https://www.playinarabic.com/translations/the-room) | 288160 | لا | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2021-01-01 | 2026-09-11 |
| [Valfaris](https://www.playinarabic.com/translations/valfaris) | 600130 | لا | Play in Arabic | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2022-01-01 | 2026-09-11 |

</details>

<details>
<summary><strong>[فلتة](https://www.fltah-translator.com/)</strong> — 24</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Alice: Madness Returns](https://www.fltah-translator.com/games/alice-madness-returns) | 19680 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Bravely Default: Flying Fairy HD Remaster](https://www.fltah-translator.com/games/bravely-default-flying-fairy-hd-remaster) | 2833580 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Cities: Skylines](https://www.fltah-translator.com/games/cities-skylines) | 255710 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Creature Kitchen](https://www.fltah-translator.com/games/creature-kitchen) | 3097300 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Dishonored](https://www.fltah-translator.com/games/dishonored) | 205100 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Fairy Tail 2](https://www.fltah-translator.com/games/fairy-tail-2) | 3002850 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Fields of Mistria](https://www.fltah-translator.com/games/fields-of-mistria) | 2142790 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Final Fantasy XII: The Zodiac Age](https://www.fltah-translator.com/games/final-fantasy-xii-the-zodiac-age) | 595520 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Folklands](https://www.fltah-translator.com/games/folklands) | 2282890 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Highway Police Simulator](https://www.fltah-translator.com/games/highway-police-simulator) | 2789130 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Honeycomb: The World Beyond](https://www.fltah-translator.com/games/honeycomb-the-world-beyond) | 1510440 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [L.A. Noire](https://www.fltah-translator.com/games/la-noire) | 110800 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Life is Strange](https://www.fltah-translator.com/games/life-is-strange) | — | ؟ | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Mad Max](https://www.fltah-translator.com/games/mad-max) | 234140 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [No Rest for the Wicked](https://www.fltah-translator.com/games/no-rest-for-the-wicked) | 1371980 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Shantae: Half-Genie Hero](https://www.fltah-translator.com/games/shantae-half-genie-hero) | 253840 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Sniper Elite 5](https://www.fltah-translator.com/games/sniper-elite-5) | 1029690 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Star Wars Outlaws](https://www.fltah-translator.com/games/star-wars-outlaws) | 2842040 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Stardew Valley](https://www.fltah-translator.com/games/stardew-valley) | 413150 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [The Crust](https://www.fltah-translator.com/games/the-crust) | 1465470 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Visions of Mana](https://www.fltah-translator.com/games/visions-of-mana) | 2490990 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Wanderburg](https://www.fltah-translator.com/games/wanderburg) | 3624140 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Welcome to Elderfield](https://www.fltah-translator.com/games/welcome-to-elderfield) | 3195440 | لا | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |
| [Yes, Your Grace: Snowfall](https://www.fltah-translator.com/games/yes-your-grace-snowfall) | — | ؟ | FLTAH | موقع الفريق | غير مصرّح بها | غير مصرّح بها | تطبيق خاص | غير مذكورة | اشتراك | منشورة | — | 2026-09-11 |

</details>

<details>
<summary><strong>[تعريبات هشام](https://arabichesham.com/)</strong> — 20</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [007 First Light](https://www.nexusmods.com/007firstlight/mods/11) | 3768760 | لا | HeshamLocalization | Nexus Mods | كاملة | غير مصرّح بها | مثبّت, خط | غير مذكورة | مجاني | منشورة | 2026-06-15 | 2026-09-11 |
| [Absolum](https://www.nexusmods.com/absolum/mods/12) | 1904480 | لا | HeshamLocalization | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-08-17 | 2026-09-11 |
| [Blasphemous 2](https://www.nexusmods.com/blasphemous2/mods/22) | 2114740 | لا | HeshamLocalization | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-08-17 | 2026-09-11 |
| [Dishonored 2](https://github.com/7akeem0/Arabic_Hesham-Downloads/releases) | 403640 | لا | Hesham | GitHub | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2026-09-06 | 2026-09-11 |
| [Final Fantasy VII](https://github.com/7akeem0/Arabic_Hesham-Downloads/releases) | 39140 | لا | Hesham | GitHub | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2026-09-06 | 2026-09-11 |
| [Forza Horizon 6](https://www.nexusmods.com/forzahorizon6/mods/65) | 2483190 | لا | HeshamLocalization | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-07-30 | 2026-09-11 |
| [Hades II](https://www.nexusmods.com/hades2/mods/121) | 1145350 | لا | HeshamLocalization | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-06-04 | 2026-09-11 |
| [Halo: Campaign Evolved](https://www.nexusmods.com/halocampaignevolved/mods/27) | 2806050 | لا | HeshamLocalization | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-07-27 | 2026-09-11 |
| [Hollow Knight: Silksong](https://www.nexusmods.com/hollowknightsilksong/mods/1105) | 1030300 | لا | HeshamLocalization | Nexus Mods | كاملة | غير مصرّح بها | BepInEx, خط, تشكيل/اتجاه | غير مذكورة | مجاني | منشورة | 2026-09-02 | 2026-09-11 |
| [Inscryption](https://www.nexusmods.com/inscryption/mods/5) | 1092790 | لا | X7akeem (uploaded by HeshamLocalization) | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-07-27 | 2026-09-11 |
| [Kingdom Come: Deliverance](https://www.nexusmods.com/kingdomcomedeliverance/mods/2339) | 379430 | لا | HeshamLocalization | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-08-24 | 2026-09-11 |
| [Kingdom Come: Deliverance II](https://www.nexusmods.com/kingdomcomedeliverance2/mods/3542) | 1771300 | لا | HeshamLocalization | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-08-24 | 2026-09-11 |
| [Metaphor: ReFantazio](https://www.nexusmods.com/metaphorrefantazio/mods/86) | 2679460 | لا | HeshamLocalization | Nexus Mods | كاملة | غير مصرّح بها | مثبّت, خط | غير مذكورة | مجاني | منشورة | 2026-06-28 | 2026-09-11 |
| [Mina the Hollower](https://www.nexusmods.com/minathehollower/mods/7) | 1875580 | لا | HeshamLocalization | Nexus Mods | كاملة | غير مصرّح بها | مثبّت, خط | غير مذكورة | مجاني | منشورة | 2026-07-09 | 2026-09-11 |
| [MOUSE: P.I. For Hire](https://www.nexusmods.com/mousepiforhire/mods/20) | 2416450 | لا | X7akeem (uploaded by HeshamLocalization) | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-08-03 | 2026-09-11 |
| [Outer Wilds (with Echoes of the Eye)](https://outerwildsmods.com/mods/outerwildsarabictranslation/) | 753640 | لا | Hesham (7akeem0) | outerwildsmods.com | كاملة | آلية راجعها إنسان | OWML, خط | MIT | مجاني | منشورة | — | 2026-09-11 |
| [Slay the Spire 2](https://www.nexusmods.com/slaythespire2/mods/759) | 2868840 | لا | X7akeem (uploaded by HeshamLocalization) | Nexus Mods | كاملة | غير مصرّح بها | مثبّت, خط | غير مذكورة | مجاني | منشورة | 2026-05-03 | 2026-09-11 |
| [Tears of Metal](https://www.nexusmods.com/tearsofmetal/mods/2) | 1913120 | لا | HeshamLocalization | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-08-02 | 2026-09-11 |
| [The Outer Worlds 2](https://www.nexusmods.com/theouterworlds2/mods/102) | 1449110 | لا | X7akeem (uploaded by HeshamLocalization) | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-05-03 | 2026-09-11 |
| [Undertale](https://www.nexusmods.com/undertale/mods/39) | 391540 | لا | HeshamLocalization | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | أولية | 2026-05-15 | 2026-09-11 |

</details>

<details>
<summary><strong>[أوكي شوب](https://okshopsa.net/games)</strong> — 19</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Baldur's Gate 3](https://okshopsa.net/games/baldurs-gate-3-okshop) | 1086940 | لا | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط | مذكورة | مجاني | منشورة | 2026-08-27 | 2026-09-11 |
| [Crimson Desert](https://okshopsa.net/games/crimson-desert-okshop) | — | ؟ | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط, خانة لغة أخرى | مذكورة | مجاني | منشورة | 2026-08-05 | 2026-09-11 |
| [Fallout 4](https://okshopsa.net/games/fallout-4-okshop) | 377160 | لا | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط | مذكورة | مجاني | منشورة | 2026-08-05 | 2026-09-11 |
| [Fallout: New Vegas — Ultimate Edition](https://okshopsa.net/games/fallout-new-vegas-okshop) | — | ؟ | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط | مذكورة | مجاني | منشورة | 2026-08-22 | 2026-09-11 |
| [Kingdom Come: Deliverance](https://okshopsa.net/games/kingdom-come-deliverance-okshop) | 379430 | لا | OK SHOP | موقع الفريق | كاملة | آلية راجعها إنسان | مثبّت, خط, خانة لغة أخرى | مذكورة | مجاني | منشورة | 2026-08-27 | 2026-09-11 |
| [Kingdom Come: Deliverance II](https://okshopsa.net/games/kingdom-come-deliverance-2-okshop) | 1771300 | لا | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط, خانة لغة أخرى | مذكورة | مجاني | منشورة | 2026-08-23 | 2026-09-11 |
| [Lords of the Fallen](https://okshopsa.net/games/lords-of-the-fallen-okshop) | 1501750 | لا | OK SHOP | موقع الفريق | كاملة | آلية راجعها إنسان | مثبّت, خط | مذكورة | مجاني | منشورة | 2026-08-23 | 2026-09-11 |
| [Mass Effect Legendary Edition](https://okshopsa.net/games/mass-effect-legendary-edition-okshop) | 1328670 | لا | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط | مذكورة | مجاني | منشورة | 2026-08-25 | 2026-09-11 |
| [Mortal Shell II](https://okshopsa.net/games/mortal-shell-ii-okshop) | 2584270 | لا | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط, خانة لغة أخرى | مذكورة | مجاني | منشورة | 2026-08-26 | 2026-09-11 |
| [Palworld](https://okshopsa.net/games/palworld-okshop) | 1623730 | لا | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط | مذكورة | مجاني | منشورة | 2026-08-05 | 2026-09-11 |
| [Sekiro: Shadows Die Twice](https://okshopsa.net/games/sekiro-okshop) | — | ؟ | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط | مذكورة | مجاني | منشورة | 2026-08-05 | 2026-09-11 |
| [Stardew Valley](https://okshopsa.net/games/stardew-valley-okshop) | 413150 | لا | OK SHOP | موقع الفريق | كاملة | آلية راجعها إنسان | مثبّت, خط, خانة لغة أخرى | مذكورة | مجاني | منشورة | 2026-08-22 | 2026-09-11 |
| [Starfield](https://okshopsa.net/games/starfield-okshop) | 1716740 | لا | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط, خانة لغة أخرى | مذكورة | مجاني | منشورة | 2026-08-11 | 2026-09-11 |
| [State of Decay 2](https://okshopsa.net/games/state-of-decay-2-okshop) | — | ؟ | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط | مذكورة | مجاني | منشورة | 2026-08-25 | 2026-09-11 |
| [The Blood of Dawnwalker](https://okshopsa.net/games/the-blood-of-dawnwalker-okshop) | 3751260 | لا | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط, خانة لغة أخرى | مذكورة | مجاني | منشورة | 2026-09-09 | 2026-09-11 |
| [The Elder Scrolls IV: Oblivion Remastered](https://okshopsa.net/games/oblivion-remastered-okshop) | 2623190 | لا | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط, خانة لغة أخرى | مذكورة | مجاني | منشورة | 2026-08-05 | 2026-09-11 |
| [The Elder Scrolls V: Skyrim Special Edition](https://okshopsa.net/games/skyrim-special-edition-okshop) | 489830 | لا | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط, خانة لغة أخرى | مذكورة | مجاني | منشورة | 2026-08-05 | 2026-09-11 |
| [Warhammer 40,000: Space Marine 2](https://okshopsa.net/games/space-marine-2-okshop) | 2183900 | لا | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط | مذكورة | مجاني | منشورة | 2026-08-05 | 2026-09-11 |
| [Wo Long: Fallen Dynasty](https://okshopsa.net/games/wo-long-fallen-dynasty-okshop) | 1448440 | لا | OK SHOP | موقع الفريق | كاملة | غير مصرّح بها | مثبّت, خط | مذكورة | مجاني | منشورة | 2026-08-26 | 2026-09-11 |

</details>

<details>
<summary><strong>[عمرو شاهين](https://arb-sub.blogspot.com/)</strong> — 9</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [A Plague Tale: Innocence](https://arb-sub.blogspot.com/2023/07/plague-tale-innocence.html) | 752590 | لا | Amr Shaheen | مدونة | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2023-07-01 | 2026-09-11 |
| [Call of Duty: Black Ops](https://arb-sub.blogspot.com/2025/08/call-of-duty-black-ops.html) | 42700 | لا | Amr Shaheen | مدونة | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2025-08-01 | 2026-09-11 |
| [Far Cry 3](https://arb-sub.blogspot.com/2023/07/far-cry-3.html) | 220240 | لا | Amr Shaheen | مدونة | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2023-07-01 | 2026-09-11 |
| [Mafia II: Definitive Edition](https://arb-sub.blogspot.com/2023/04/mafia-2-definitive-edition.html) | 1030830 | لا | Amr Shaheen | مدونة | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2023-04-01 | 2026-09-11 |
| [Mafia: Definitive Edition](https://arb-sub.blogspot.com/2023/08/mafia-definitive-edition.html) | 1030840 | لا | Amr Shaheen | مدونة | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2023-08-01 | 2026-09-11 |
| [Prince of Persia: The Forgotten Sands](https://arb-sub.blogspot.com/2023/07/prince-of-persia-forgotten-sands.html) | 33320 | لا | Amr Shaheen | مدونة | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2023-07-01 | 2026-09-11 |
| [Shady Part of Me](https://arb-sub.blogspot.com/2023/12/shady-part-of-me.html) | 1116580 | لا | Amr Shaheen | مدونة | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2023-12-01 | 2026-09-11 |
| [Sifu](https://arb-sub.blogspot.com/2023/07/sifu.html) | 2138710 | لا | Amr Shaheen | مدونة | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2023-07-01 | 2026-09-11 |
| [Total Overdose](https://arb-sub.blogspot.com/2023/12/total-overdose.html) | — | ؟ | Amr Shaheen | مدونة | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2023-12-01 | 2026-09-11 |

</details>

<details>
<summary><strong>[ترس](https://github.com/DiNaSoR/Tersreleases/releases)</strong> — 6</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Diablo](https://github.com/DiNaSoR/Tersreleases/releases/tag/diablo1) | — | ؟ | Ters | GitHub | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, دبلجة | غير مذكورة | مجاني | منشورة | 2026-09-09 | 2026-09-11 |
| [Diablo II](https://github.com/DiNaSoR/Tersreleases/releases/tag/diablo2) | — | ؟ | Ters | GitHub | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, دبلجة | غير مذكورة | مجاني | منشورة | 2026-09-11 | 2026-09-11 |
| [DragonSword Awakening](https://github.com/DiNaSoR/Tersreleases/releases/tag/DragonSwordAwakening) | 4570720 | لا | Ters | GitHub | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2026-08-01 | 2026-09-11 |
| [Graveyard Keeper](https://github.com/DiNaSoR/Tersreleases/releases/tag/graveyardkeeper) | 599140 | لا | Ters | GitHub | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2026-08-03 | 2026-09-11 |
| [Ninja Gaiden 4](https://github.com/DiNaSoR/Tersreleases/releases/tag/NinjaGaiden4) | 2627260 | لا | Ters | GitHub | غير مصرّح بها | غير مصرّح بها | استبدال ملفات, دبلجة | غير مذكورة | مجاني | منشورة | 2026-09-08 | 2026-09-11 |
| [The Blood of Dawnwalker](https://github.com/DiNaSoR/Tersreleases/releases/tag/TheBloodofDawnwalker) | 3751260 | لا | Ters | GitHub | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2026-09-03 | 2026-09-11 |

</details>

<details>
<summary><strong>[تركي المطيري](https://gamebanana.com/mods/601841)</strong> — 4</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Half-Life](https://gamebanana.com/wips/87752) | 70 | لا | saudi305 | GameBanana | الواجهة | غير مصرّح بها | استبدال ملفات | CC-BY-NC-ND-4.0 | مجاني | قيد العمل | 2024-09-12 | 2026-09-11 |
| [Half-Life 2](https://gamebanana.com/mods/601841) | 220 | لا | saudi305 (Turki Al Mutairi) | GameBanana | جزئية | بشرية | استبدال ملفات, مثبّت | CC-BY-NC-ND-4.0 | مجاني | منشورة | 2025-06-20 | 2026-09-11 |
| [Half-Life 2: Lost Coast](https://gamebanana.com/mods/477069) | 340 | لا | saudi305 and Osamaisgood | GameBanana | كاملة | بشرية | استبدال ملفات | CC-BY-NC-ND-4.0 | مجاني | منشورة | 2024-04-10 | 2026-09-11 |
| [Papers, Please](https://gamebanana.com/mods/682074) | 239030 | لا | saudi305, Hjbiki, Nasrallah Issa (Papers Please Arabic team) | GameBanana | كاملة | بشرية | استبدال ملفات, خط | CC-BY-NC-ND-4.0 | مجاني | أولية | 2026-06-01 | 2026-09-11 |

</details>

<details>
<summary><strong>[الألعاب بالعربي](https://www.nexusmods.com/sekiro/mods/431)</strong> — 4</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Resident Evil 2 (2019)](https://www.nexusmods.com/residentevil22019/mods/540) | 883710 | نعم | Games in Arabic (uploaded by GamesinArabic) | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات | غير مذكورة | مجاني | منشورة | 2020-08-27 | 2026-09-11 |
| [Resident Evil 3 (2020)](https://www.nexusmods.com/residentevil32020/mods/145) | 952060 | نعم | Games in Arabic (uploaded by GamesinArabic) | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات | غير مذكورة | مجاني | منشورة | 2020-10-02 | 2026-09-11 |
| [Sekiro: Shadows Die Twice](https://www.nexusmods.com/sekiro/mods/431) | 814380 | لا | Games in Arabic (uploaded by GamesinArabic) | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات | غير مذكورة | مجاني | منشورة | 2020-12-17 | 2026-09-11 |
| [The Medium](https://www.nexusmods.com/themedium/mods/5) | 1293160 | لا | Games in Arabic (uploaded by GamesinArabic) | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات | غير مذكورة | مجاني | منشورة | 2022-03-09 | 2026-09-11 |

</details>

<details>
<summary><strong>[عزام](https://steamcommunity.com/sharedfiles/filedetails/?id=3641916210)</strong> — 3</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Don't Starve](https://steamcommunity.com/sharedfiles/filedetails/?id=3704921982) | 219740 | لا | Azaam | ورشة Steam | كاملة | بشرية | الورشة | غير مذكورة | مجاني | منشورة | 2026-04-11 | 2026-09-11 |
| [Don't Starve Together](https://steamcommunity.com/sharedfiles/filedetails/?id=3641916210) | 322330 | لا | Azaam | ورشة Steam | الواجهة | بشرية | الورشة | مذكورة | مجاني | منشورة | 2026-01-08 | 2026-09-11 |
| [Mortal Shell II](https://www.nexusmods.com/mortalshell2/mods/210) | 2584270 | لا | Azaam1 | Nexus Mods | كاملة | بشرية | pak, خط | غير مذكورة | مجاني | منشورة | 2026-09-05 | 2026-09-11 |

</details>

<details>
<summary><strong>[آفاق التعريب](https://www.arhorizons.com/Projects)</strong> — 2</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Lies of P: Overture](https://www.arhorizons.com/Projects/lies-of-p-overture) | 1627720 | لا | Arabization Horizons | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | — | 2026-09-11 |
| [Portal](https://www.nexusmods.com/portal/mods/47) | 400 | لا | Arabization Horizons | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات, مثبّت | مذكورة | مجاني | منشورة | 2025-04-13 | 2026-09-11 |

</details>

<details>
<summary><strong>[بيسّوف](https://besofh.wordpress.com/)</strong> — 2</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Metal Gear Solid (1998)](https://besofh.wordpress.com/2025/12/21/%d8%a7%d9%84%d8%b9%d8%aa%d8%a7%d8%af-%d8%a7%d9%84%d9%85%d8%b9%d8%af%d9%86%d9%8a-%d8%a7%d9%84%d8%b5%d9%84%d8%a8/) | — | ؟ | Besofh | مدونة | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2025-12-21 | 2026-09-11 |
| [Resident Evil 3: Nemesis (1999)](https://besofh.wordpress.com/2026/09/10/%d8%a7%d9%84%d8%b4%d8%b1-%d8%a7%d9%84%d9%85%d9%82%d9%8a%d9%85-3-%d9%86%d9%85%d8%b3%d9%8a%d8%b3-1999-resident-evil-3-nemisis/) | 4249120 | لا | Besofh | مدونة | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2026-09-10 | 2026-09-11 |

</details>

<details>
<summary><strong>[فريق رحلة](https://steamcommunity.com/sharedfiles/filedetails/?id=3300660739)</strong> — 2</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Mount & Blade II: Bannerlord](https://www.nexusmods.com/mountandblade2bannerlord/mods/7137) | 261550 | لا | rihla team (uploaded by lub131) | Nexus Mods | كاملة | آلية راجعها إنسان | استبدال ملفات | غير مذكورة | مجاني | منشورة | 2026-01-10 | 2026-09-11 |
| [Mount & Blade II: Bannerlord](https://steamcommunity.com/sharedfiles/filedetails/?id=3300660739) | 261550 | لا | Rihla team with translator Abu Dahim | ورشة Steam | كاملة | آلية راجعها إنسان | الورشة | غير مذكورة | مجاني | منشورة | 2024-07-31 | 2026-09-11 |

</details>

<details>
<summary><strong>[الدبران](https://aldebaran.moe/)</strong> — 1</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Steins;Gate](https://aldebaran.moe/) | 412830 | لا | Aldebaran (translator Salman, programming Abu Uqba, founder  | موقع الفريق | كاملة | بشرية | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-09-11 | 2026-09-11 |

</details>

<details>
<summary><strong>[الوكر](https://arraqim.github.io/alwakr/)</strong> — 1</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Yakuza 0](https://arraqim.github.io/alwakr/zero) | 638970 | لا | Al-Wakr | موقع الفريق | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | — | 2026-09-11 |

</details>

<details>
<summary><strong>[ArabVikings](https://thunderstore.io/c/valheim/p/ArabVikings/Arab_Viking/)</strong> — 1</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Valheim](https://thunderstore.io/c/valheim/p/ArabVikings/Arab_Viking/) | 892970 | لا | ArabVikings | Thunderstore | الواجهة | غير مصرّح بها | BepInEx, Jötunn | غير مذكورة | مجاني | منشورة | 2025-08-07 | 2026-09-11 |

</details>

<details>
<summary><strong>[فوتبول مانيجر العربي](https://arabfm.net/)</strong> — 1</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Football Manager (2018 to 2026 language files)](https://arabfm.net/) | — | ؟ | AFM community | موقع الفريق | الواجهة | غير مصرّح بها | استبدال ملفات | غير مذكورة | مجاني | منشورة | 2025-11-17 | 2026-09-11 |

</details>

<details>
<summary><strong>[مكتبة أسمر](https://asmar-ar.com/)</strong> — 1</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Subnautica 2](https://asmar-ar.com/) | 1962700 | لا | Asmar | موقع الفريق | غير مصرّح بها | غير مصرّح بها | مثبّت | غير مذكورة | مجاني | منشورة | — | 2026-09-11 |

</details>

<details>
<summary><strong>[Better Rimworlds](https://github.com/BetterRimworlds/Rimworld-Arabic)</strong> — 1</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [RimWorld](https://steamcommunity.com/sharedfiles/filedetails/?id=3687785648) | 294100 | لا | Better Rimworlds (Autonomo AI) | ورشة Steam | كاملة | آلية | استبدال ملفات | MIT | مجاني | منشورة | 2026-03-19 | 2026-09-11 |

</details>

<details>
<summary><strong>[قلعة الخوف](https://castle-of-fear.itch.io/misaoarabic)</strong> — 1</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Misao](https://castle-of-fear.itch.io/misaoarabic) | 1043270 | ؟ | Castle of Fear | itch.io | كاملة | بشرية | استبدال ملفات | مذكورة | مجاني | منشورة | 2024-02-12 | 2026-09-11 |

</details>

<details>
<summary><strong>[فريق ريدمبشن وعماد عادل](https://emadadeldev.github.io/rtea/)</strong> — 1</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Red Dead Redemption 2](https://github.com/emadadeldev/rtea/releases) | 1174180 | لا | Emad Adel (Redemption Team) | GitHub | غير مصرّح بها | غير مصرّح بها | مثبّت | غير مذكورة | مجاني | منشورة | 2026-09-11 | 2026-09-11 |

</details>

<details>
<summary><strong>أفراد وفرق بلا صفحة فريق</strong> — 47</summary>

| اللعبة | Steam | عربية رسمية | المؤلّف | المضيف | التغطية | الطريقة | الشكل التقني | الرخصة | التوزيع | الحالة | آخر تاريخ | فُحص |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Balatro](https://github.com/BloodyARZ/BALATRO-ARABIC) | 2379780 | لا | BloodyARZ | GitHub | جزئية | غير مصرّح بها | استبدال ملفات | CC0-1.0 | مجاني | أولية | 2026-01-27 | 2026-09-11 |
| [Baldur's Gate 3](https://www.nexusmods.com/baldursgate3/mods/5732) | 1086940 | لا | ahmadmot (uploaded by ahmadmotx) | Nexus Mods | غير مصرّح بها | غير مصرّح بها | pak | غير مذكورة | مجاني | منشورة | 2024-01-07 | 2026-09-11 |
| [Bears In Space](https://github.com/M7MD-Zz/Bears-In-Space-Arabic) | 1309620 | لا | M7MD-XD | GitHub | كاملة | غير مصرّح بها | غير مصرّح به | مذكورة | مجاني | منشورة | 2026-09-07 | 2026-09-11 |
| [Black Mesa](https://steamcommunity.com/sharedfiles/filedetails/?id=2893890254) | 362890 | لا | Workshop author (unnamed on the page) | ورشة Steam | الحوار | غير مصرّح بها | الورشة | غير مذكورة | مجاني | أولية | 2022-11-26 | 2026-09-11 |
| [Black Myth: Wukong](https://www.nexusmods.com/blackmythwukong/mods/69) | 2358720 | لا | AG GROUP (uploaded by Salehalmsmary209) | Nexus Mods | غير مصرّح بها | غير مصرّح بها | pak | غير مذكورة | مجاني | منشورة | 2024-08-23 | 2026-09-11 |
| [Bum Simulator](https://github.com/M7MD-Zz/Bum-Simulator-Arabic) | 855740 | لا | M7MD-XD | GitHub | كاملة | غير مصرّح بها | غير مصرّح به | مذكورة | مجاني | منشورة | 2026-09-07 | 2026-09-11 |
| [Car Mechanic Simulator 2018](https://steamcommunity.com/sharedfiles/filedetails/?id=1381898351) | 645630 | لا | Saud Arishi (سعود عريشي) | ورشة Steam | الواجهة | بشرية | الورشة | غير مذكورة | مجاني | منشورة | 2018-05-09 | 2026-09-11 |
| [Cities: Skylines II](https://www.nexusmods.com/citiesskylines2/mods/195) | 949230 | لا | algammal | Nexus Mods | غير مصرّح بها | غير مصرّح بها | استبدال ملفات | غير مذكورة | مجاني | منشورة | 2026-06-29 | 2026-09-11 |
| [Cities: Skylines II](https://www.nexusmods.com/citiesskylines2/mods/94) | 949230 | لا | Feras (uploaded by Fras1z) | Nexus Mods | غير مصرّح بها | آلية | استبدال ملفات | غير مذكورة | مجاني | أولية | 2023-12-23 | 2026-09-11 |
| [Clair Obscur: Expedition 33](https://www.nexusmods.com/clairobscurexpedition33/mods/258) | 1903340 | نعم | Majood7 aka Sharky (uploaded by majood7) | Nexus Mods | الحوار | غير مصرّح بها | pak, خط | غير مذكورة | مجاني | منشورة | 2025-06-23 | 2026-09-11 |
| [Command & Conquer: Red Alert 2 - Yuri's Revenge](https://gamebanana.com/mods/609752) | — | ؟ | ATAA SY | GameBanana | كاملة | غير مصرّح بها | استبدال ملفات, خط | CC-BY-NC-ND-4.0 | مجاني | منشورة | 2025-07-27 | 2026-09-11 |
| [Crimson Moon](https://github.com/faisalkindi/CrimsonMoon-Arabic) | 4317690 | لا | Faisal Al-Kindi (faisalkindi / kindiboy) | GitHub | كاملة | غير مصرّح بها | pak, خط, مثبّت | غير مذكورة | مجاني | منشورة | 2026-09-02 | 2026-09-11 |
| [Crusader Kings III](https://steamcommunity.com/sharedfiles/filedetails/?id=2235954743) | 1158310 | لا | Volunteers (unnamed on the page) | ورشة Steam | جزئية | غير مصرّح بها | الورشة | غير مذكورة | مجاني | منشورة | 2020-09-22 | 2026-09-11 |
| [Crusader Kings III](https://steamcommunity.com/sharedfiles/filedetails/?id=2556621728) | 1158310 | لا | x7amtoGamer and xRover | ورشة Steam | جزئية | غير مصرّح بها | الورشة | غير مذكورة | مجاني | منشورة | 2021-07-24 | 2026-09-11 |
| [Dark Souls III](https://www.nexusmods.com/darksouls3/mods/929) | 374320 | لا | Arabic Bonfire (uploaded by mido23dz) | Nexus Mods | كاملة | غير مصرّح بها | ModEngine2, استبدال ملفات | غير مذكورة | مجاني | منشورة | 2025-10-17 | 2026-09-11 |
| [Dawn of Man](https://steamcommunity.com/sharedfiles/filedetails/?id=1672618199) | 858810 | لا | Workshop author (unnamed on the page) | ورشة Steam | جزئية | بشرية | الورشة | غير مذكورة | مجاني | منشورة | 2019-03-03 | 2026-09-11 |
| [Endzone 2](https://www.nexusmods.com/endzone2/mods/1) | 2144640 | لا | Shinigami3361 | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات | غير مذكورة | مجاني | منشورة | 2025-02-10 | 2026-09-11 |
| [Factorio](https://github.com/mosa8899/-factorio) | 427520 | لا | mosa8899 | GitHub | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2025-07-05 | 2026-09-11 |
| [Fallout 4](https://www.nexusmods.com/fallout4/mods/74914) | 377160 | لا | ar (uploaded by JXnQ8) | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات | غير مذكورة | مجاني | منشورة | 2023-09-22 | 2026-09-11 |
| [Friday Night Funkin'](https://gamebanana.com/mods/374192) | — | ؟ | Abdragon Z | GameBanana | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | CC-BY-NC-ND-4.0 | مجاني | منشورة | 2022-04-28 | 2026-09-11 |
| [Grand Theft Auto V](https://arabictrilogy.blogspot.com/2023/02/grand-theft-auto-v.html) | 271590 | لا | Hamza Al-Hamoud (ArabicTrilogy) | مدونة | كاملة | بشرية | استبدال ملفات | غير مذكورة | مجاني | منشورة | 2024-01-29 | 2026-09-11 |
| [Grand Theft Auto V Enhanced](https://www.nexusmods.com/gta5enhanced/mods/1136) | 3240220 | لا | Nasser262 (uploaded by n262n) | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات, خط | غير مذكورة | مجاني | منشورة | 2026-07-21 | 2026-09-11 |
| [Hearts of Iron IV](https://steamcommunity.com/sharedfiles/filedetails/?id=3402098254) | 394360 | لا | Workshop author (unnamed on the page) | ورشة Steam | كاملة | آلية | الورشة | غير مذكورة | مجاني | متوقفة | 2025-01-06 | 2026-09-11 |
| [Hearts of Iron IV](https://steamcommunity.com/sharedfiles/filedetails/?id=3599864223) | 394360 | لا | Gamer Arabic - Hamid Bouide | ورشة Steam | كاملة | غير مصرّح بها | الورشة | غير مذكورة | مجاني | منشورة | 2025-11-04 | 2026-09-11 |
| [Kingdom Come: Deliverance II](https://www.nexusmods.com/kingdomcomedeliverance2/mods/133) | 1771300 | لا | ARAB translation (uploaded by AliMeftah) | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات | غير مذكورة | مجاني | منشورة | 2025-02-06 | 2026-09-11 |
| [Kingdom Come: Deliverance II](https://www.nexusmods.com/kingdomcomedeliverance2/mods/3432) | 1771300 | لا | yazeed5112 | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات | غير مذكورة | مجاني | أولية | 2026-08-01 | 2026-09-11 |
| [Lethal Company](https://thunderstore.io/c/lethal-company/p/KaTaKuri/ArabicTranslationBykatakuri98/) | 1966720 | لا | KaTaKuri | Thunderstore | الواجهة | غير مصرّح بها | BepInEx | غير مذكورة | مجاني | منشورة | — | 2026-09-11 |
| [Lethal Company](https://thunderstore.io/c/lethal-company/p/OmarElBanna/ArabicLanguageSupportPlus/) | 1966720 | لا | OmarElBanna | Thunderstore | غير مصرّح بها | غير مصرّح بها | BepInEx | غير مذكورة | مجاني | منشورة | — | 2026-09-11 |
| [Manor Lords](https://www.nexusmods.com/manorlords/mods/190) | 1363080 | لا | Shinigami3361 | Nexus Mods | غير مصرّح بها | غير مصرّح بها | pak | غير مذكورة | مجاني | منشورة | 2025-02-11 | 2026-09-11 |
| [Metal Gear Solid V: The Phantom Pain](https://www.nexusmods.com/metalgearsolidvtpp/mods/2224) | 287700 | لا | VHussain and Yazed0071 (uploaded by yazed0071) | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات | غير مذكورة | مجاني | منشورة | 2026-05-07 | 2026-09-11 |
| [Mount & Blade II: Bannerlord](https://www.nexusmods.com/mountandblade2bannerlord/mods/7906) | 261550 | لا | abuda7mx | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات, خط, دبلجة | غير مذكورة | مجاني | منشورة | 2025-04-25 | 2026-09-11 |
| [My Hero Ultra Rumble](https://www.nexusmods.com/myheroultrarumble/mods/303) | 1607250 | لا | 1MHR | Nexus Mods | كاملة | غير مصرّح بها | pak, خط | غير مذكورة | مجاني | منشورة | 2026-04-17 | 2026-09-11 |
| [OMORI](https://omar-ibn-al-khattab-plus.itch.io/omori) | 1150690 | لا | Omar ibn al-Khattab plus | itch.io | غير مصرّح بها | غير مصرّح بها | استبدال ملفات | غير مذكورة | مجاني | قيد العمل | — | 2026-09-11 |
| [OneShot](https://github.com/MO1-O1/oneshot-ar) | 420530 | لا | MO1-O1 | GitHub | جزئية | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | قيد العمل | 2026-08-21 | 2026-09-11 |
| [Palworld](https://www.nexusmods.com/palworld/mods/4369) | 1623730 | لا | iqcp1 | Nexus Mods | كاملة | غير مصرّح بها | pak, خط | غير مذكورة | مجاني | منشورة | 2026-07-30 | 2026-09-11 |
| [Persona 3 Reload](https://github.com/AboSami1s/P3R_AR/releases) | 2161700 | لا | AboSami1s | GitHub | غير مصرّح بها | غير مصرّح بها | pak | غير مذكورة | مجاني | منشورة | 2026-08-28 | 2026-09-11 |
| [Pizza Tower](https://gamebanana.com/wips/90033) | 2231450 | لا | Fares_127 and Karrartheuhh (continuation of the KayMaw / Man | GameBanana | كاملة | غير مصرّح بها | استبدال ملفات | CC-BY-NC-ND-4.0 | مجاني | منشورة | 2025-10-08 | 2026-09-11 |
| [Project Zomboid](https://steamcommunity.com/sharedfiles/filedetails/?id=3751112547) | 108600 | لا | SA7 | ورشة Steam | كاملة | غير مصرّح بها | الورشة | غير مذكورة | مجاني | منشورة | 2026-06-24 | 2026-09-11 |
| [RimWorld (with DLC)](https://github.com/mosa8899/-RimWorld-DLC) | 294100 | لا | mosa8899 | GitHub | غير مصرّح بها | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2024-12-07 | 2026-09-11 |
| [Startup Company](https://steamcommunity.com/sharedfiles/filedetails/?id=2181994709) | 606800 | لا | Workshop author (unnamed on the page) | ورشة Steam | غير مصرّح بها | غير مصرّح بها | الورشة | غير مذكورة | مجاني | منشورة | 2020-07-29 | 2026-09-11 |
| [Terraria](https://steamcommunity.com/sharedfiles/filedetails/?id=3427983380) | 105600 | لا | Workshop author (unnamed on the page) | ورشة Steam | غير مصرّح بها | غير مصرّح بها | الورشة | غير مذكورة | مجاني | منشورة | 2025-02-15 | 2026-09-11 |
| [The Adventures of Elliot: The Millennium Tales](https://www.nexusmods.com/theadventuresofelliotthemilleniumtales/mods/1) | 3483510 | لا | kindiboy | Nexus Mods | كاملة | بشرية | مثبّت, خط | غير مذكورة | مجاني | منشورة | 2026-06-23 | 2026-09-11 |
| [The First Berserker: Khazan](https://www.nexusmods.com/thefirstberserkerkhazan/mods/16) | 2680010 | لا | MSH (uploaded by mshfm) | Nexus Mods | كاملة | غير مصرّح بها | pak | غير مذكورة | مجاني | منشورة | 2026-07-26 | 2026-09-11 |
| [The Invincible](https://www.nexusmods.com/theinvincible/mods/5) | 731040 | لا | MSH (uploaded by mshfm) | Nexus Mods | كاملة | غير مصرّح بها | استبدال ملفات | غير مذكورة | مجاني | أولية | 2025-04-04 | 2026-09-11 |
| [The Planet Crafter](https://github.com/ishak10123/The-Planet-Crafter-arabic-translation) | 1284190 | لا | ishak10123 | GitHub | كاملة | آلية | BepInEx, خط, تشكيل/اتجاه | غير مذكورة | مجاني | منشورة | 2026-06-21 | 2026-09-11 |
| [Victoria 3](https://steamcommunity.com/sharedfiles/filedetails/?id=2880200030) | 529340 | لا | Workshop author (unnamed on the page) | ورشة Steam | جزئية | غير مصرّح بها | الورشة | غير مذكورة | مجاني | أولية | 2022-10-26 | 2026-09-11 |
| [Vintage Story](https://github.com/mosa8899/-Vintage-Story) | — | ؟ | mosa8899 | GitHub | جزئية | غير مصرّح بها | غير مصرّح به | غير مذكورة | مجاني | منشورة | 2025-05-19 | 2026-09-11 |

</details>

<!-- fahras:end -->

### مواضع ذات صلة غير مفهرسة

- **muarrab.com** و**ta3reb.com** يفهرسان رقعًا عربية (رسمية ومن الهواة) وكانا
  أفضل دليل إلى صفحات الأصحاب؛ ta3reb يستضيف ملفات بلا نسبة متسقة.
- **taaribat.blogspot.com** أرشيف لتاريخ التعريب في الألعاب، الرسمي والرمادي،
  من عصر الأقراص فصاعدًا.
- **Miqbas** (`github.com/aboali-hub/Miqbas`) أداة ترجمة آلية لألعاب RPG Maker
  وRen'Py وUnity وUnreal تشغّل نموذجًا على بطاقة اللاعب نفسه؛ تنتج تعريبات ولا
  تُعدّ تعريبًا.
- **t3reeb.games** يغطي رقع الكونسول فقط.

---

## استعمال السجلّ

### مع تعريب

لا شيء يُثبَّت: العميل الجديد يشير إلى هنا أصلًا. تحمل الإعدادات ← المصادر
القوائم الثلاث الموصوفة أعلاه؛ اضبط المصدر الرئيسي على جذر المحتوى الخام إن
أردت أن يخدم GitHub نفسه الفهرس بدل المرآة، وأضف مجلدًا تحت *المصادر
المحلية* لقراءة نسخة أو مشاركة شبكية، وفعّل وضع عدم الاتصال لئلا تُلمس الشبكة
أبدًا.

### مرآةً أو نسخةً بلا اتصال

```bash
git clone https://github.com/cc1a2b/taarib-registry.git
```

النسخة سجلّ كامل. وجّه تعريب إلى المجلد فتُحلّ من القرص البيان والشرائح وقائمة
السحب والحزم نفسها؛ وانسخه إلى مشاركة فيقرأ كل جهاز يركّبها الشيء نفسه. لا
شيء في الشجرة خاصٌّ بمضيف إلا عنوانا الملف المطلقان في القائمة، والحزمة التي
يسمّيانها موجودة داخل النسخة أيضًا في `isdar/`.

### المتطلبات

- أي مضيف ملفات ساكنة يخدم الشجرة كما هي ويجيب طلبات `Range` للحزم (شبكة
  إصدارات GitHub وjsDelivr كلاهما يفعل).
- لأدوات هذا الملف: `git` و`python3` (3.10 فأعلى) واختياريًا حزمة
  `jsonschema`؛ وللساابك سلسلةُ أدوات Rust المثبّتة في مستودع العميل.

---

## بداية سريعة

```bash
# البيان: المخطط والتسلسل وتجزئة لكل شريحة
curl -s https://cdn.jsdelivr.net/gh/cc1a2b/taarib-registry@main/bayan.json | jq '{isdar, tasalsul, waqt, shards: (.sharaih|length)}'

# الشريحة غير الفارغة الوحيدة، واللعبة التي تُفهرَس عليها
curl -s https://cdn.jsdelivr.net/gh/cc1a2b/taarib-registry@main/sharaih/67.json | jq '.ruqaa | keys'

# افحص شريحة على البيان بنفسك (b3sum من مشروع blake3)
curl -s https://cdn.jsdelivr.net/gh/cc1a2b/taarib-registry@main/sharaih/67.json | b3sum
curl -s https://cdn.jsdelivr.net/gh/cc1a2b/taarib-registry@main/bayan.json | jq -r '.sharaih["103"]'
```

يجب أن تتطابق التجزئتان؛ و`103` هي `0x67` عشريًّا، رقم الشريحة الذي يفهرس عليه
البيان.

---

## أمثلة الاستعمال

```bash
# اقرأ الفهرس: كل تعريب مجاني منشور له معرّف تطبيق Steam
jq -r '.tarjamat[] | select(.tawzee=="majjani" and .hala=="nashita" and .steam_appid) | "\(.steam_appid)\t\(.luba.ism)\t\(.rabt)"' fahras/tarjamat.json

# أيّ الألعاب المفهرسة تشحن اليوم عربية رسمية على Steam
jq -r '.tarjamat[] | select(.arabiya_rasmiya.hala=="naam") | .luba.ism' fahras/tarjamat.json | sort -u

# المدخلات التي تصرّح برخصة، وما هي
jq -r '.tarjamat[] | select(.rukhsa.naw!="ghayr_musarraha") | "\(.luba.ism): \(.rukhsa.muarrif // .rukhsa.nass)"' fahras/tarjamat.json

# تحقّق من الفهرس وأعد توليد جداول README
python3 fahras/jadwal.py

# تحقّق من ملف الحزمة على قائمته
b3sum isdar/01a06d42-dc5d-74b2-b27d-5c4441a03a3f/r-e-p-o-r2.ruqaa
jq -r '.ruqaa[][0].basmat_muhtawa' sharaih/67.json
```

---

## مرجع الأوامر

الساابك، يُشغَّل من مستودع العميل ومفتاحُ المالك (اليوم: مفتاح التطوير) في سلسلة
مفاتيح الجهاز:

```
سبك — cast the registry from sealed packages

  sabk --jidhr <repo> --tasalsul <n> --asas <https://base/>
       [--mira <https://mirror/>] [--ism-miftah <keychain account>]
       [--huzma <file.ruqaa> --luba <game-uuid> --ism <title> [--tajawuz <why>]]...
       [--mulgha <64-hex key> --sabab <why>]...

  --jidhr       شجرة العمل التي يُكتب فيها المستودع (مطلوب)
  --tasalsul    رقم تسلسل البيان؛ يزيد في كل مرة
  --asas        أساس ملفات الإصدار: {ism} لمنطقة إصدارات مسطّحة، {masar}
                لمسار المستودع، ولا شيء منهما فيُلحق المسار
  --mira        عنوان ثانٍ اختياري للملفات نفسها
  --ism-miftah  حساب سلسلة المفاتيح الحامل لمفتاح التوقيع
  --huzma       حزمة مختومة تُنشر، يتلوها --luba و--ism
  --tajawuz     انشر فوق بوابة تغطية الحزمة نفسها مع ذكر السبب
  --mulgha      مفتاح توقيع يُسحب، يتلوه --sabab
```

أدوات الفهرس، تُشغَّل من نسخة من هذا المستودع:

```
python3 fahras/jadwal.py            تحقّق من fahras/tarjamat.json وأعد كتابة جدولي README
python3 fahras/jadwal.py --check    تحقّق فقط؛ الخروج 1 عند أي مشكلة
```

---

## استعمال متقدّم

### خدمة نسختك

يصلح أي خادم مجلدات جذرَ مرآة لأن الشجرة لا تحتاج إعادة كتابة: يُلحق القارئ
`bayan.json` و`sharaih/<xx>.json` ومسارَ السحب النسبيَّ في البيان بأي جذر
يُعطاه. وملفات الإصدار استثناء: تحمل القوائم عناوين مطلقة، فالمرآة التي تريد
خدمة الحزم أيضًا إما تُبقي مجلد `isdar/` في مكانه (كما تفعل jsDelivr) أو تعيد
السبك بـ `--asas` مشيرًا إليها.

### تفريع الكتالوج

الفرع `git clone` ومفتاح. أعد السبك بمفتاح توقيعك، ووجّه مصادر عميلٍ إلى جذرك،
فيثق عميلك بكتالوجك ويرفض هذا، تمامًا كما ترفض بنية الإصدار مفتاح التطوير.
لا سجلّ مركزيًا يُسجَّل لديه.

### التحقق من الشجرة بقارئ العميل نفسه

الفحوص المنقولة في هذا الملف شغّلها حاملٌ صغير يربط صناديق العميل ويستدعي
الدوال نفسها التي يستدعيها المنتج: البيان وحارس التراجع، والشرائح الـ 256
كلها عبر منشئ التجزئة قبل التحليل، وقائمة السحب عبر منشئها المتحقِّق (ومعه قلب
بايت ومفتاح مالك خطأ)، والحزمة عبر فحص التوقيع قبل التثبيت تحت المرساتين،
واشتقاق هوية اللعبة، ومسار الجلب كاملًا (`jalb_fahras` و`jalb_qaimat_sahb`
وإصابة المخبأ) عبر مجلد محلي ومشاركة شبكية وجذر المصدر الخام والمرآة وسلسلة
المنتج الافتراضية بنصّها، مع تجزئة عنواني ملف الإصدار على القائمة. مصدره ليس
جزءًا من هذا المستودع لأنه يعتمد بالمسار على صناديق العميل؛ والأرقام التي
أنتجها في رسالة الإيداع الذي أضاف الفهرس.

---

## المساهمة

**الرقع.** لا تصل رقعة إلى هذا السجلّ إلا بتوقيع المالك. ابنِها واختمها في
تعريب، ثم قدّمها للمراجعة؛ يستعمل مسار التقديم في الاستوديو تفويضَ أجهزة
GitHub وهو تسليمٌ محلي حتى يوفّر المشغّل معرّفَ عميل OAuth وإصدارَ التجهيز
(`docs/mustawda.md` §7.2). وإلى ذلك الحين افتح مسألة في هذا المستودع مرفقًا
الحزمة ومصرِّحًا بهوية `luba`؛ يراجعها القائم على الصيانة ويشغّل الساابك وينشر
تحت تسلسل جديد. لا شيء يُنشر تلقائيًا، ولا شيء يُنشر بمفتاح غير مفتاح المالك.

**مدخلات الفهرس.** افتح طلب دمج يعدّل `fahras/tarjamat.json` وشغّل
`python3 fahras/jadwal.py` لينجح فحص المخطط وتُعاد الجداول. يحتاج المدخل
الصفحةَ التي جاء منها في `rabt`، وتاريخ قراءتك لها في `tahaqquq.waqt`، ولا
شيء لا تصرّح به الصفحة؛ واترك `rukhsa` على `ghayr_musarraha` بدل التخمين.
وتصحيحات أصحاب التعريبات المفهرسة تُؤخذ كما هي.

**بلاغات العلل** في القارئ أو الساابك أو التخطيط مكانها
[مستودع العميل](https://github.com/cc1a2b/Taarib/issues).

---

## الرخصة

بيانات الكتالوج والفهرس وهذا التوثيق مطروحة تحت **CC0 1.0 Universal**؛ النص
الكامل مع إشعار الإهداء في [LICENSE](LICENSE).

```
taarib-registry — public domain under CC0 1.0 Universal
Author and maintainer: cc1a2b
```

كل حزمة `.ruqaa` تصرّح برخصتها في بياناتها الوصفية (المقدَّمة اليوم تصرّح بـ
CC0)، وتغطي تلك الرخصة النص المترجم لا غير. وكل تعريب يشير إليه الفهرس يبقى
تحت شروط أصحابه، أيًّا كانت.

---

## الدعم

إن نفعك السجلّ أو الفهرس: ضع نجمة على المستودع، وتابع
[cc1a2b](https://github.com/cc1a2b)، وشاركه مع فرق التعريب التي يدرجها لتصحّح
مدخلاتها بنفسها.

---

<div align="center">

**taarib-registry — الكتالوج الذي يقرؤه تعريب، وخريطة ما يوجد بجانبه.**

بناه [cc1a2b](https://github.com/cc1a2b).

</div>
