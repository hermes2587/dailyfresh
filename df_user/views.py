from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect


def register(request):
    return render(request, 'df_user/register.html')


def register_handle(request):
    uname = request.POST.get('user_name')
    pwd = request.POST.get('pwd')
    cpwd = request.POST.get('cpwd')
    ueamil = request.POST.get('email')

    if pwd != cpwd:
        return redirect("/user/register")
    user = UserInfo()
    user.uname = uname
    user.upwd = pwd
    user.uemail = ueamil
    user.save()
    return redirect("/user/login")


def register_exist(request):
    uname = request.GET.get("uname")
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({"count": count})


def login(request):
    uname = request.COOKIES.get("uname","")
    return render(request, "df_user/login.html", {"error_name": 0, "error_password": 0, "uname": uname, "upwd": ""})


def login_handle(request):
    error_password = 0
    error_name = 0
    post = request.POST
    uname = post.get("username")
    upwd = post.get("pwd")
    print(request.COOKIES)
    user_name_list = UserInfo.objects.filter(uname=uname)
    if len(user_name_list) == 1:
        if user_name_list[0].upwd == upwd:
            error_password = 0
        else:
            error_password = 1
    else:
        error_name = 1
    if error_name == 0 and error_password == 0:
        response = HttpResponseRedirect("/user/info")
        if post.get("jizhu") == "1":
            response.set_cookie("uname", uname)
        else:
            response.set_cookie("uname", max_age=-1)
        request.session["user_id"] = user_name_list[0].id
        request.session["uname"] = user_name_list[0].uname
        return response
    else:
        return render(request, "df_user/login.html", {"error_name": error_name, "error_password": error_password,
                                                      "uname": uname, "upwd": upwd})


def info(request):
    user_id = request.session.get("user_id", "")
    user = UserInfo.objects.get(id=user_id)
    uname = user.uname
    uphone = user.uphone
    uaddress = user.uaddress
    return render(request, "df_user/user_center_info.html", {"uname": uname, "uphone": uphone, "uaddress": uaddress})


def order(request):

    return render(request, "df_user/user_center_order.html")


def site(request):
    user_id = request.session.get("user_id", "")
    if user_id == "":
        return redirect("/user/login/")
    user = UserInfo.objects.get(id=user_id)
    if request.method == "POST":
        user.ushou = request.POST.get("ushou")
        user.uaddress = request.POST.get("uaddress")
        user.uphone = request.POST.get("uphone")
        user.uyoubian = request.POST.get("uyoubian")
    return render(request,"df_user/user_center_site.html", {"user": user})