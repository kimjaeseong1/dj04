from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from .models import User
from django.contrib.auth.hashers import check_password
from django.contrib import messages
# Create your views here.
def index(req):
    return render(req,"acc/index.html")

def login_user(req):
    if req.method == "POST":
        un = req.POST.get("uname")
        up = req.POST.get("upass")
        u = authenticate(username=un,password=up)
        if u :
            login(req,u)
            messages.success(req, f"{u}!! WELCOME :)")
            return render(req,"acc/index.html")

        else:
           messages.error(req,"계정정보가 일치하지 않습니다") #메세지 넣어줄곳! 사용자에 지금 온 요청에 실어준다. 
        
    return render (req,"acc/login.html")

def logout_user(req):
    logout(req)
    return redirect("acc:index")

def profile(req):
    return render(req,"acc/profile.html")

def signup(req):
    if req.method == "POST":
        un = req.POST.get("uname")
        up = req.POST.get("upass")
        uc = req.POST.get("ucomm")
        pi  = req.FILES.get("upic") 
        User.objects.create_user(username=un, password=up,comment=uc, pic=pi)
        return redirect("acc:login")

    return render(req,"acc/signup.html")

def update(req):
    if req.method == "POST":
        u = req.user
        up = req.POST.get("upass")
        uc = req.POST.get("ucomm")
        pi  = req.FILES.get("upic") 
        ue = req.POST.get("umail")
        if up:
            u.set_password(up)
        if pi:
            u.pic = pi
        u.comment = uc
        u.email = ue
        u.save()
        login(req, u)
        return redirect("acc:profile")
    return render(req,"acc/update.html")

def delete(req):
    pw = req.POST.get("pwck")
    if check_password(pw,req.uesr.password):
        req.user.delete()
        return redirect("acc:index")
    else:
        messages.error(req,"건들지 마세요!  ")
        
    return redirect("acc:profile")
    