from django.shortcuts import render, redirect, HttpResponse
import json, urllib


# Create your views here.
def index(request):
    return render(request, 'scoreKeeper/index.html')
 
def receiver(request):
    if request.is_ajax():
        print "Almost Yay!"
        if request.method == 'POST':
            print "YAY!"
            rawData = json.dumps(request.body)
            strScore = rawData.split("=") #should return "score", "###"
            # print strScore[1][:-1]
            score = int(strScore[1][:-1])
            # print type(score)
    return redirect('/')

def playGame(request):
    return render(request, 'scoreKeeper/breakoutGame.html')