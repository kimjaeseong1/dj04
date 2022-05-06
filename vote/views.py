
from email.errors import MessageError
from django.shortcuts import redirect, render
from .models import Topic,Choice
from django.utils import timezone
from django.contrib import messages
# Create your views here.

def index(req):
    t = Topic.objects.all()
    context = {
            "tset" : t
    }
    return render(req,"vote/index.html",context)

def detail(req,tpk):
    t = Topic.objects.get(id=tpk)
    c = t.choice_set.all()         #토픽들을 참조해줄 때  사용
    context = {
        "t" : t,
        "cset" : c
    }
    return render(req,"vote/detail.html",context)

def vote(req,tpk):
    t = Topic.objects.get(id=tpk)
    if not req.user in t.voter.all(): ##다중투표 불가 
        t.voter.add(req.user)
        cpk = req.POST.get("cho")
        
        c = Choice.objects.get(id=cpk)
        print(cpk)
        c.choicer.add(req.user)
    return redirect("vote:detail",tpk)


def cancel(req,tpk):
    t = Topic.objects.get(id=tpk)
    t.voter.remove(req.user)
    print(req.user.choice_set.all())
    req.user.choice_set.get(topic=t).choicer.remove(req.user) #많고 많은 초이스 중에 t인 친구 빼로기        
    return redirect("vote:detail",tpk)

def create(req):
    if req.method == "POST":
        s = req.POST.get("sub")
        c = req.POST.get("con")
        cn = req.POST.getlist("cname")
        cp = req.POST.getlist("cpic")
        cc = req.POST.getlist("ccom")
         
        t = Topic(subject = s,maker=req.user,content=c,pubdate=timezone.now())
        t.save()
        for name,pic,con in zip(cn,cp,cc):
            Choice(topic=t, name=name,pic=pic,con=con).save()
        return redirect("vote:index")

    return render(req,"vote/create.html")

def delete(req,tpk):
    t = Topic.objects.get(id=tpk)
    if req.user == t.maker: #아무나 삭제 못하게해준는 것 
        t.delete()
    else :
       messages.error(req,"나 이제 못 참아 ㅅㄱ") #혼내줌    

    return redirect("vote:index")