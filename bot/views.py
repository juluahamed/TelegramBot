from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bot import bot
from bot.sendsms import send

@csrf_exempt
def index(request):
    if request.method == "POST":
        print("Printing Request")
        print(json.loads(request.body.decode("utf-8")))
        update = json.loads(request.body.decode("utf-8"))
        bot.handle_update(update)
        return HttpResponse('OK')
    return HttpResponse("This page is merely serving a bot. May be someday I'll be a proper webpage'")

@csrf_exempt
def autoHealthcheck(request):
    if request.method == "POST":
        if request.body.decode("utf-8") == "x5d6f3qalp4Exq.s2m2ld":
            update = {'auto': True}
            bot.handle_update(update)
            return HttpResponse('OK')
        else:
            pass
    return HttpResponse("This page is merely serving a bot. May be someday I'll be a proper webpage'")

@csrf_exempt
def serverDown(request):
    if request.method == "POST":
        if request.body.decode("utf-8") == "x7h2l09chtD2O518sgt":
            message = "IMPORTANT! The server is Down"
            send(message)
            return HttpResponse('OK')
        else:
            pass
    return HttpResponse("Nothing to see here. Just an empty page")
