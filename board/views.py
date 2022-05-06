from django.shortcuts import redirect, render
from .models import Board,Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.
def index(req):
    
    pg = req.GET.get("page",1)
    cate = req.GET.get("cate","")
    kw = req.GET.get("kw","")
    if kw : 
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            try:
                from acc.models import User
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()
        elif cate == "con":
            b = Board.objects.filter(content__contains=kw)
        else:
            b = Board.objects.all()
    else:
         b= Board.objects.all() 

    b= b.order_by('-pubdate')   
    pag = Paginator(b,5)
    obj = pag.get_page(pg)
    content = {
        "bset" : obj,
        "kw":kw,
        "cate":cate
    }
    return render(req,"board/index.html",content)

def detail(req,bpk):
    b= Board.objects.get(id=bpk)
    r = b.reply_set.all()
    content = {
        "b" : b,
        "rset" : r,
        

        
       
    }
    return render(req,"board/detail.html",content)

def delete(req,bpk):
    b= Board.objects.get(id=bpk)
    if b.writer == req.user:
         b.delete()
    else: 
        messages.error(req,"당신 게시물 아니니 건들지 마시오 ") #경고메세지
    return redirect("board:index")

def create(req):
    if req.method == "POST":
        s = req.POST.get("sub")
        c = req.POST.get("con")
        Board(subject=s, writer=req.user,content=c ,pubdate =timezone.now()).save()
        return redirect("board:index")
    return render(req,"board/create.html")

def update(req,bpk):
    b = Board.objects.get(id=bpk)

    if b.writer != req.user:
        messages.error(req,"건들지 말라고 했을텐데..") # 경고 메세지 대기중
        return redirect("board:index")
        
    if req.method == "POST":
        s = req.POST.get("sub")
        c = req.POST.get("con")
        b.subject = s
        b.content = c
        b.save()
        return redirect("board:detail",bpk)
    content = {
        "b" : b
    }
    
    return render(req,"board/update.html",content)

def creply(req,bpk):
    b = Board.objects.get(id=bpk)
    c = req.POST.get("com")
    Reply(board=b,replyer =req.user, comment=c).save()
    return redirect("board:detail",bpk)

def dreply(req,bpk,rpk):
  r =  Reply.objects.get(id=rpk)
  if req.user == r.replyer: #모르는 사람이 댓글을 삭제 할 수 있기 때문에 인증을 해줘야 한다. 
    r.delete()
  else:
       messages.error(req,"너 댓글 아니잖아!!!!!!")
  return redirect("board:detail",bpk)

def likey(req,bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(req.user)
   
    return redirect("board:detail",bpk)

def unlikey(req,bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(req.user)
    return redirect("board:detail",bpk)
    