import math

from django.http import HttpResponseRedirect
from django.shortcuts import render
from board import models


def index(request):
    listsize, pagesize = 3, 3

    currentpage = int(request.GET['p']) if request.GET.get('p') is not None else 1

    # 1. 페이징을 위한 기본 데이터 계산
    totalcount = models.countall()
    pagecount = math.ceil(totalcount / listsize)
    blockcount = math.ceil(pagecount / pagesize)
    currentblock = math.ceil(currentpage / pagesize)

    # 2. 파라미터 page 값 검증

    # 3. 페이지 리스트를 렌더링 하기위한 데이터 값 계산
    beginpage = 1 if currentblock == 0 else (currentblock - 1) * pagesize + 1
    prevpage = (currentblock - 1) * pagesize if currentblock > 1 else 0
    nextpage = currentblock * pagesize + 1 if currentblock < blockcount else 0
    endpage = (beginpage - 1) + listsize if nextpage > 0 else pagecount

    # 4. 리스트 가져오기
    startindex = (currentpage - 1) * listsize
    boardlist = []
    for idx, board in enumerate(models.fiandall(startindex, listsize)):
        boardlist.append({
            'index': totalcount - (currentpage - 1)*listsize - idx,
            'board': board
        })

    # 5. 리스트 정보를 dict에 저장
    data = {
        'boardlist': boardlist,
        'currentpage': currentpage,
        'endpage': endpage,
        'range': range(beginpage, beginpage + listsize),
        'prevpage': prevpage,
        'nextpage': nextpage
    }

    return render(request, 'board/index.html', data)


def write(request):
    if request.session.get('authuser') is None:
        return HttpResponseRedirect('/')

    return render(request, 'board/write.html')


def add(request):
    if request.session.get('authuser') is None:
        return HttpResponseRedirect('/')

    title = request.POST['title']
    contents = request.POST['contents']
    user_id = request.session['authuser']['id']

    models.insert(title, contents, user_id)

    return HttpResponseRedirect('/board')


def view(request):
    board = models.findbyno(request.GET['no'])
    board.hit += 1
    board.save()

    return render(request, 'board/view.html', {'board': board})


def updateform(request):
    if request.session.get('authuser') is None:
        return HttpResponseRedirect('/')

    no = request.GET['no']
    userno = request.session['authuser']['no']

    board = models.findby_no_and_userno(no, userno)
    return render(request, 'board/modify.html', {'board': board})


def update(request):
    if request.session.get('authuser') is None:
        return HttpResponseRedirect('/')

    no = request.POST['no']
    userno = request.session['authuser']['id']
    title = request.POST['title']
    contents = request.POST['contents']

    models.update(title, contents, no, userno)

    return HttpResponseRedirect('/board/view?id=' + request.POST['id'])


def delete(request):
    if request.session.get('authuser') is None:
        return HttpResponseRedirect('/')

    board = models.delete(request.GET['no'], request.session['authuser']['no'])
    board.delete()

    return HttpResponseRedirect('/board')
