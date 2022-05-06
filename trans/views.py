from django.shortcuts import render
from googletrans import Translator
import googletrans

# Create your views here.


def index(req):   
    context = {
        "nd" : googletrans.LANGUAGES
    } ##없으면 오류가 난다. 
    if req.method == "POST":
        b = req.POST.get("bf")
        f = req.POST.get("fr")
        t = req.POST.get("to")
        trans = Translator()
        af=trans.translate(b,src=f, dest=t)
        context.update({     ##update로 딕셔너리 전체를 추가를해줄 수 있다. 
            "af" : af.text,
            "bf" : b,
            "fr" : f,
            "to" : t,
            
        })
    return render(req,"trans/index.html",context)