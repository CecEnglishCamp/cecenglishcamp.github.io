import json
books = [
    ("Peter Rabbit","peter-rabbit",1,4),
    ("Little Red Riding Hood","red-riding-hood",5,8),
    ("Jack and the Beanstalk","jack-and-the-beanstalk",9,12),
    ("The Frog Prince","frog-prince",13,16),
    ("The Elves and the Shoemaker","elves-and-the-shoemaker",17,20),
    ("Thumbelina","thumbelina",21,24),
    ("The Emperor's New Clothes","emperors-new-clothes",25,28),
    ("Lucky Hans","lucky-hans",29,32),
    ("The Velveteen Rabbit","velveteen-rabbit",33,36),
]
def book_for(w):
    for title,slug,a,b in books:
        if a<=w<=b: return title,slug
    return "TBD","tbd"
weeks=[]
for w in range(1,37):
    title,slug=book_for(w); ww=f"{w:02d}"
    campa=lambda s:f"/camp-a/grade3/week{ww}{s}.html"
    read=lambda r:f"/library/camp-a-readings/grade3/{slug}/w{ww}_r{r}.html"
    write=f"/camp-a/writing/grade3/{slug}/w{ww}.html"
    review=f"/mom-teacher/grade3/{slug}/w{ww}.html"
    lf=f"/lostwords/{slug.replace('-','_')}_w{ww}.html"
    ls=f"/camp-a/speaking/grade3/{slug}/w{ww}.html"
    w1=(w==1)
    st=lambda built:"ready" if built else "pending"
    days={
      "monday":[{"type":"camp-a","title":"Day 1 종합세트","status":"ready","url":campa("a")},
                {"type":"reading","title":"Reading 1","status":st(w1),"url":read(1)}],
      "tuesday":[{"type":"listen-find","title":"Listen & Find","status":"pending","url":lf},
                 {"type":"look-speak","title":"Look & Speak","status":st(w1),"url":ls}],
      "wednesday":[{"type":"camp-a","title":"Day 2 종합세트","status":"ready","url":campa("b")},
                   {"type":"reading","title":"Reading 2","status":st(w1),"url":read(2)}],
      "thursday":[{"type":"writing","title":"Writing","status":st(w1),"url":write}],
      "friday":[{"type":"camp-a","title":"Day 3 종합세트","status":"ready","url":campa("c")}],
      "saturday":[{"type":"review","title":"Mom Teacher Review","status":st(w1),"url":review}],
    }
    weeks.append({"week":w,"book":title,"slug":slug,"days":days})
with open("grade3.json","w",encoding="utf-8") as f:
    json.dump({"grade":3,"weeks":weeks},f,ensure_ascii=False,indent=2)
print("grade3.json written:",len(weeks),"weeks")
