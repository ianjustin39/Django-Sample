from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime


def hello_world(request):
    return HttpResponse("Hello World!")


def hello_html(request):
    return render(request, 'index.html', {
        'data': 'hello html!!!', # 回傳給剛剛設定html內的{{data}}
        'current_time': str(datetime.now()), # 回傳給剛剛設定html內的{{current_time}}
    })
