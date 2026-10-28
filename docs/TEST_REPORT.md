# تقرير الاختبارات — أثر (2026-10-28)

## الوضع الحالي: ✅ كل الاختبارات ناجحة

### اختبارات الوحدة (Vitest)
| الملف | عدد الاختبارات | الحالة |
|---|---|---|
| assets.test.ts | 1 | ✅ |
| books.test.ts | 6 | ✅ |
| cases.test.ts | 15 | ✅ |
| engine.test.ts | 28 | ✅ |
| forensic-cards.test.ts | 3 | ✅ |
| heritage.test.ts | 8 | ✅ |
| hints.test.ts | 12 | ✅ |
| labs.test.ts | 10 | ✅ |
| mastery.test.ts | 14 | ✅ |
| reference.test.ts | 12 | ✅ |
| research.test.ts | 9 | ✅ |
| seasons.test.ts | 10 | ✅ |
| sources.test.ts | 10 | ✅ |
| **المجموع** | **332** | **✅ 13/13 ملفاً** |

### اختبارات e2e (Playwright)
التشغيل: موبايل Pixel 7 (390px، ar) + سطح مكتب 1366px

| الاختبار | موبايل | سطح مكتب |
|---|---|---|
| صفحة الهبوط + أول hook مختلف عند إعادة التحميل | ✅ | ✅ |
| تدفق الإعداد → البرنامج التعليمي → مقابلة الصدق | ✅ | ✅ |
| **a11y (داكن): كل صفحة بلا انتهاكات axe جسيمة + لا تمرير أفقي** | ✅ | ✅ |
| **a11y (فاتح): كل صفحة بلا انتهاكات axe جسيمة + لا تمرير أفقي** | ✅ | ✅ |
| a11y: صفحة بوابة العمر + القائمة المنزلقة | ✅ | ✅ |
| لا تمرير أفقي عند 320px لكل صفحة | ✅ | ✅ |
| تبديل الثيم + ثبات عبر إعادة التحميل | ✅ | ✅ |
| تبديل الحجم + تقليل الحركة | ✅ | ✅ |
| القائمة: فتح + حبس التركيز + الإغلاق بـ Escape | ✅ | ✅ |
| شريط التنقل السفلي: 5 وجهات | ✅ | ✅ |
| manifest + أيقونات المنصة | ✅ | ✅ |
| a11y (داكن): تبويبات مساحة اللعب | ✅ | ✅ |
| a11y (فاتح): تبويبات مساحة اللعب | ✅ | ✅ |
| تقليل الحركة يُزيل الانيميشن | ✅ | ✅ |
| الاستوديو مغلق للمجهولين؛ المسؤول يسجل الدخول | ✅ | ✅ |
| CSRF: رفض الطلبات ذات المنشأ المختلف | ✅ | ✅ |
| التدفق الكامل من البرنامج التعليمي → الاستنتاج → الإحاطة | ✅ | ✅ |
| مختبر آمن: تصنيف → إخفاء التغذية الراجعة → إعادة المحاولة | ✅ | ✅ |
| **المجموع** | **20** | **20** |
| **الكل** | **40/40** | **✅** |

### الصفحات المفحوصة بـ axe (40 صفحة)
```
/ /start /home /cases /case/c000_lost_notebook /academy /academy/A1
/challenges /profile /account /privacy /report /review/ABC123
/knowledge /knowledge/KO-RS-05-001 /sources /labs /labs/SAFE_LABS-01
/skills /gallery /credits /studio /sounds /icons /season /glossary
/methods /biases /reasoning /rulebook /atlas /archetypes
/heritage /heritage/poe-rue-morgue /books /books/BK-741 /books/drills
/labs/SAFE_LABS-30 /academy/educators /no-such-page
```

### التحقق من المحتوى
- ✅ `npm run check:cases`: 30 قضية تجتاز (مسار إثبات مزدوج + لا فرضية بلا نفي)
- ✅ `npx tsx scripts/leak-scan.ts`: 0 تسريبات (لا تداخل 4-gram بين المرئي والمخفي)
- ✅ `bash scripts/check-library.sh`: ASP — مساران منفصلان للإثبات

### بناء الإنتاج
```
npm run build  →  ✅ ناجح
مسارات ثابتة:  49
مسارات ديناميكية: 5
حجم .next:  543 MB
```
