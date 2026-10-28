import glob,json,re,sys,os
sys.path.insert(0,'.')
from outline import OUT
FR="../frag/"; REPO="/home/claude/athar/"
SRC="/mnt/user-data/uploads/game learning/"
FILES={"BK-741":"741 الطب الشرعي ومسرح الجريمة والبحث الجنائي (أحمد بسيوني أبو الروس، مديحة الخضري).txt",
"BK-853":"853 الطب الشرعي العملي (الياس الصائغ).txt","BK-843":"843 الأسلحة النارية في الطب الشرعي - حسين شحرور.txt","BK-04425":"04425_طرق الإنجاب في الطب الحديث وحكمها الشرعي.txt"}
def norm(s):
    s=re.sub(r'[ً-ٰٟـ]','',s)
    s=re.sub('[أإآٱ]','ا',s).replace('ى','ي').replace('ة','ه')
    s=re.sub(r'[^\w\s]',' ',s)
    return re.sub(r'\s+',' ',s).strip().split()
def sh(w,n=8): return {" ".join(w[i:i+n]) for i in range(len(w)-n+1)}
kos=set(json.load(open(REPO+"content/knowledge/ko_names.json")))
# merge
rows=[]
for f in sorted(glob.glob(FR+"f*.py")):
    ns={}; exec(open(f).read(),ns)
    for t in ns["C"]: rows.append((ns["B"],)+tuple(t))
order={b:i for i,b in enumerate(OUT)}
rows.sort(key=lambda r:(order[r[0]],r[2],r[3]))
secs={b:{s[0]:s for s in v} for b,v in OUT.items()}
def sec_of(b,l):
    for s in OUT[b]:
        if s[2]<=l<=s[3]: return s
    raise Exception((b,l))
shingles=set()
if os.path.isdir(SRC):
    for b,fn in FILES.items():
        shingles|=sh(norm(open(SRC+fn,encoding="utf-8",errors="ignore").read()))
print("source shingles",len(shingles))
concepts=[];bad=[]
for i,r in enumerate(rows,1):
    b,_sec,l1,l2,title,summ,use,lim,myth,age,safety,skill,kl,gl=r
    s=sec_of(b,l1)
    assert s[4]=="included" or b=="BK-04425",(b,l1,s)
    for k in kl: assert k in kos,(i,k)
    txt=" ".join([title,summ,use,lim,myth or ""])
    hit=sh(norm(txt))&shingles
    if hit: bad.append((i,b,l1,len(hit),list(hit)[0]))
    concepts.append(dict(id=f"BKC-{i:03d}",book_id=b,section_id=s[0],section_title_ar=s[1],
      ref_ar=f"{s[1]} (الأسطر {l1}–{l2})",line_start=l1,line_end=l2,title_ar=title,summary_ar=summ,
      investigation_use_ar=use,limits_ar=lim,myth_ar=myth or None,age_band=age,safety_level=safety,skill=skill,
      linked_ko_ids=kl,glossary=gl))
print("concepts",len(concepts),"shingle hits",len(bad))
for x in bad: print(x)
cnt={}
for c in concepts: cnt[(c["book_id"],c["section_id"])]=cnt.get((c["book_id"],c["section_id"]),0)+1
META={
"BK-741":dict(title_ar="الطب الشرعي ومسرح الجريمة والبحث الجنائي",authors_ar=["أحمد بسيوني أبو الروس","مديحة الخضري"],year=2008,edition_ar="الطبعة الثانية",
  hook_ar="بين جثة صامتة ومسرح مبعثر، من يقرأ الأثر أولاً يكسب القضية."),
"BK-853":dict(title_ar="الطب الشرعي العملي (الجزء الأول)",authors_ar=["إلياس الصائغ"],year=1997,edition_ar="الجزء الأول",
  hook_ar="ملفات قديمة تحمل حالات حقيقية مجهولة الأسماء: ماذا كان يمكن أن يخبرنا الجسد؟"),
"BK-843":dict(title_ar="الأسلحة النارية في الطب الشرعي",authors_ar=["حسين شحرور"],year=2004,edition_ar="",
  hook_ar="الأثر يخبرك بما حدث، لا بمن فعله: تعلّم الفرق قبل أن تتهم أحداً."),
"BK-04425":dict(title_ar="طرق الإنجاب في الطب الحديث وحكمها الشرعي",authors_ar=["بكر أبو زيد"],year=None,edition_ar="",
  hook_ar="كتاب مغلق في ملفنا: لماذا نبقيه خارج واجهة المراهقين؟"),
}
books=[]
for b in OUT:
    secs_out=[]
    for s in OUT[b]:
        secs_out.append(dict(id=s[0],title_ar=s[1],line_start=s[2],line_end=s[3],inclusion=s[4],reason_code=s[5],reason_ar=s[6],note_count=cnt.get((b,s[0]),0)))
    inc=sum(1 for s in secs_out if s["inclusion"]=="included")
    books.append(dict(id=b,**META[b],rights="protected",use="concept-notes-only",
      rights_note_ar="كتاب محمي بحقوق النشر. لا يُخزَّن نصه في المنصة؛ نكتب ملاحظات مفاهيم بصياغتنا مع إحالة إلى موضع الفكرة في الكتاب.",
      teen_facing=(b!="BK-04425"),
      sections=secs_out,section_count=len(secs_out),included_count=inc,excluded_count=len(secs_out)-inc,
      note_count=sum(s["note_count"] for s in secs_out)))
json.dump(dict(version=1,expert_review="pending",books=books),open(REPO+"content/knowledge/books/books.json","w",encoding="utf-8") if os.makedirs(REPO+"content/knowledge/books",exist_ok=True) is None else None,ensure_ascii=False,indent=1)
json.dump(dict(version=1,expert_review="pending",concepts=concepts),open(REPO+"content/knowledge/books/concepts.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
# drills
ns={};exec(open("drills_a.py").read(),ns);A=ns["D"];exec(open("drills_b.py").read(),ns);Bd=ns["D"]
drills=[]
for i,(sk,sc,q,opts,ans,ex,hint) in enumerate(A+Bd,1):
    correct=opts[ans]; others=[o for j,o in enumerate(opts) if j!=ans]
    pos=(i*5+1)%len(opts); lst=others[:]; lst.insert(pos,correct)
    drills.append(dict(id=f"DRL-{i:03d}",skill=sk,scenario_ar=sc,question_ar=q,
      options=[dict(id="abcd"[j],text_ar=t) for j,t in enumerate(lst)],answer_id="abcd"[pos],explanation_ar=ex,
      age_band="all",safety_level="safe",linked_ko_ids=[]))
json.dump(dict(version=1,expert_review="pending",drills=drills),open(REPO+"content/knowledge/books/drills.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("drills",len(drills))
for b in books: print(b["id"],b["note_count"],b["included_count"],b["excluded_count"])
