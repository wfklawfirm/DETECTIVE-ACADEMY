# نموذج البيانات

قاعدة libSQL/SQLite عبر ترحيلات SQL ثابتة (`migrations/001_init.sql`)، بلا ORM، مع `PRAGMA foreign_keys=ON` وقيود CHECK.

| الجدول | الغرض | ملاحظات خصوصية |
|---|---|---|
| `users` | حسابات (بريد، تجزئة scrypt، دور player/editor/reviewer/admin، `adult_confirmed`، `gentle_hooks`، `deleted_at`) | البالغون فقط حالياً |
| `sessions` | جلسات (تجزئة معرّف الجلسة لا المعرّف نفسه) | كعكة `athar_sid` httpOnly |
| `case_versions` | نسخة قضية: core/ui/scoring/qa JSON، `content_hash`، الحالة draft→in_review→approved→published/retired | الحقيقة هنا (خادم) |
| `case_reviews` | موافقات البوابات السبع مربوطة بـ `content_hash` | تتلاشى عند تغيّر المحتوى |
| `play_states` | حالة لعب لحسابات البالغين | تُحذف بحذف الحساب (CASCADE) |
| `review_tickets` | طلبات مراجعة الحجة المكتوبة (رمز، نص، درجات آلية) | `user_id` اختياري؛ الرمز يتيح المتابعة بلا هوية |
| `content_reports` | بلاغات (سلامة/حقوق/خطأ) | |
| `audit_log` | تدقيق: من فعل ماذا | بصمة IP مملّحة فقط |
| `hook_events` | ما عُرض من تلميحات للحسابات | للتحليل الداخلي فقط |
| `schema_migrations` | إصدارات الترحيل | |

**لا يُخزَّن:** تاريخ الميلاد، أسماء حقيقية، عناوين IP خام، نصوص حرة للاعبين غير المشاركة طوعاً للمراجعة.
**الاحتفاظ والحذف:** `deleteAccount` يمحو الحساب والحالات والجلسات؛ بيانات الجهاز تُمسح بمسح بيانات الموقع.
