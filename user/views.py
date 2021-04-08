from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from user import models


def joinform(request):
    return render(request, 'user/joinform.html')


def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')


def join(request):
    name = request.POST["name"]
    email = request.POST["email"]
    password = request.POST["password"]
    gender = request.POST["gender"]

    models.insert(name, email, password, gender)

    return HttpResponseRedirect('/user/joinsuccess')


def loginform(request):
    return render(request, 'user/loginform.html')


def login(request):
    email = request.POST["email"]
    password = request.POST["password"]

    result = models.findby_email_and_password(email, password)
    if result is None:
        return HttpResponseRedirect('/user/loginform?result=fail')

    # login 처리
    print(type(result))
    request.session["authuser"] = result

    return HttpResponseRedirect('/')


def logout(request):
    del request.session["authuser"]
    return HttpResponseRedirect('/')


def updateform(request):
    # Access Control(접근 제어)
    authuser = request.session.get("authuser")
    if authuser is None:
        return HttpResponseRedirect('/')

    no = request.session['authuser']['no']

    # 1. 데이터를 가져오기
    result = models.findbyno(no)
    data = {'user': result}

    return render(request, 'user/updateform.html', data)


def update(request):
    no = request.session['authuser']['no']
    name = request.POST['name']
    password = request.POST['password']
    gender = request.POST['gender']

    models.update(no, name, password, gender)
    request.session['authuser'] = {'no': no, 'name': name}

    return HttpResponseRedirect('/user/updateform')
