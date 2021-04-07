from django.shortcuts import render


def joinform(request):
    return render(request, 'user/joinform.html')
