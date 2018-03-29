from django.shortcuts import render, redirect, HttpResponse
import json, urllib
from ..login_reg.models import User
from .models import *


# Create your views here.
def index(request):
    if ('user_id') in request.session:
        context = {
            'user': request.session['user_id'],
            # 'game':
        }
    return render(request, 'scoreKeeper/index.html')
 
def receiver(request):
    score = 0;
    if request.is_ajax():
        # django hsaprint "Almost Yay!"
        if request.method == 'POST':
            # print "YAY!"
            rawData = json.dumps(request.body)
            # print rawData
            strScore = rawData.split("=") #should return "score", "###"
            # print "strScore:", strScore
            print strScore[1][:-1]
            score = int(strScore[1][:-1])
            print "score: " + str(score)
    if ('user_id') in request.session:
        scoreSet = {
            'user': request.session['user_id'], 
            'score': score,
            'game': request.session['game_id']
        }
        print scoreSet
        newScore = Score.objects.scoreCreator(scoreSet)
    print request.session['user_id']
    return redirect('/games')
    
def playGame(request, id):
    request.session['game_id'] = Game.objects.get(id=id).id
    gID = request.session['game_id']
    if (gID == 1):
        return render(request, 'scoreKeeper/breakoutGame.html')
    if (gID == 2):
        return render(request, 'scoreKeeper/tetrisGame.html')
    if (gID == 3):
        return render(request, 'scoreKeeper/pacmanGame.html')

def highScores(request):
    if 'user_id' not in request.session:
        return redirect ('/user')
    breakout = Game.objects.filter(title='breakout')
    top = Score.objects.filter(game=breakout).order_by('-totalScore')[:10]
    context = {
        'top' : top,
        }
    return render(request, 'scoreKeeper/highScores.html', context)
 

    ## TODO ##
    #beautify
    #fix the css on Breakout
    #multiple levels for BO
    #tetris

