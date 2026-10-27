# النشر

## محلياً
`npm install && npm run setup && npm run migrate && npm run seed && npm run dev` ثم افتح `http://localhost:3100`. كلمة مرور المدير تُطبع عند `setup` (وتُحفظ في `.env.local`). `setup` يضع `ATHAR_ALLOW_PREVIEW=1` ليتيح لعب القضايا غير المعتمدة (معلَّمة «نسخة تجريبية»).

## متغيرات البيئة
| المتغير | الغرض |
|---|---|
| `ATHAR_SECRET` | ≥32 حرفاً؛ يوقّع رموز الحالة (تدويره يبطلها) |
| `ATHAR_DB_URL`, `ATHAR_DB_AUTH_TOKEN` | قاعدة libSQL (ملف أو Turso) |
| `ATHAR_ADMIN_EMAIL`, `ATHAR_ADMIN_PASSWORD` | إنشاء مدير عند `seed` |
| `ATHAR_ALLOW_PREVIEW` | `1` يسمح بلعب غير المنشور |
| `ATHAR_INSECURE_COOKIES` | `1` للتطوير على http فقط |
| `ATHAR_PLAY_RATE`, `ATHAR_API_RATE` | حدود الطلبات/دقيقة/IP |
| `ATHAR_AI_PROVIDER` | `local` فقط حالياً |

## إنتاج
1. `npm run build && npm run start` خلف HTTPS (لا تضبط `ATHAR_INSECURE_COOKIES`).
2. أزل `ATHAR_ALLOW_PREVIEW`؛ عندها لن تظهر إلا القضايا المنشورة بعد اكتمال البوابات السبع — **ولا توجد قضية كذلك حالياً**.
3. نسخة واحدة فقط (المحدّد في الذاكرة)؛ لتوسيع أفقي استبدل `ratelimit.ts` بمخزن مشترك.
4. قاعدة ملفية: احتفظ بنسخ احتياطية من `data/`. 
5. قبل الإطلاق: مراجعة قانونية للخصوصية لكل بلد، تدقيق علامة تجارية، مراجعة خبراء، تجربة مستخدمين. هذه شروط غير متحققة.

## فحوص قبل أي إصدار
`npm run verify && npm run build && npm run test:e2e && npm run check:library` (الأخير يحتاج `pip install clingo`).

## Vercel
- عند التشغيل على Vercel (بلا قرص دائم) يُنشئ `src/instrumentation.ts` المخطط ويستورد القضايا ويُنشئ المدير عند كل بدء بارد، على قاعدة `file:/tmp/athar.db`.
- **تنبيه:** هذه القاعدة مؤقتة. الحسابات وحالات اللعب المحفوظة بالحساب تُفقد عند البدء البارد. اللعب كضيف لا يتأثر لأن حالته في رمز موقّع عند المتصفح. للاستمرارية ضع `ATHAR_DB_URL` (رابط libSQL/Turso) و`ATHAR_DB_AUTH_TOKEN`.
- متغيرات لازمة: `ATHAR_SECRET` (≥32)، `ATHAR_ADMIN_EMAIL`، `ATHAR_ADMIN_PASSWORD`، و`ATHAR_ALLOW_PREVIEW=1` لعرض القضايا غير المنشورة بعلامة «معاينة» (لا قضية منشورة قبل اكتمال البوابات السبع).
- هو نموذج تجريبي؛ لا يُقدَّم للجمهور على أنه جاهز.
