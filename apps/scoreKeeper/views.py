from django.shortcuts import render, redirect, HttpResponse
import json

# Create your views here.
# def index(request):
#     print "FFS, WORK DAMN YOU"
    # return render(request, 'scoreKeeper/index.html')

def receiver(request):
    # print "I saw this"
    # data.request.get_json()
    # results = ""

    # for item in data:
    #     results += str(item['make']) + '\n'
    # print results
    print "this button works"
    return render(request, 'scoreKeeper/breakoutGame.html')