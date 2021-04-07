from django.shortcuts import render


def index(request):
    return render(request, 'board/index.html')


def view(request):
    return render(request, 'board/view.html')
