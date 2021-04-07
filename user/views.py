from django.http import HttpResponseRedirect
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
