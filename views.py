from django.shortcuts import render, redirect, HttpResponse
import json, urllib
from ..login_reg.models import User
from .models import *
import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
from plotly.graph_objs import *

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

def metrics(request) :
    if 'user_id' in request.session :
        games = Game.objects.all()
        gamesArr = []
        for game in games:
            gamesArr.append(game.id)
    
        scoreDict = {} 
        for i in range(1, len(gamesArr)):
            query = Score.objects.filter(player = request.session['user_id'], game = i)
            if query:
                scoreDict[i] = query

        gameNum = []
        gameSet = []
        gameScore = []
        gameSubset = []
        for key in scoreDict:
            count = 0
            print 'game ', key
            for val in scoreDict[key]:
                count += 1
                gameNum.append(count)
                gameScore.append(val.totalScore)
            gameSubset.append(gameNum)
            gameNum = []
            gameSubset.append(gameScore)
            gameScore = []
            gameSet.append(gameSubset)
            gameSubset = []
        print "gameSet:" , gameSet
        
        
    graphNo = 0
    graphs = []
    context = {
        'graphs': graphs
    }
    for i in range(0, len(gameSet)):
        graphNo += 1
        user = request.session['user_id']
        gameName = Game.objects.get(id=i+1).title
        trace = go.Scatter(x = gameSet[i][0], y = gameSet[i][1])
        data = [trace]
        layout = go.Layout(title=gameName, width=800, height=640)
        fig = go.Figure(data=data, layout=layout)
        py.plot(data, filename='a-simple-plot.png', auto_open=False)

        graph = "scoreKeeper/" + str(user) + "-" + str(graphNo) + ".png"
        graphs.append(graph)

        py.image.save_as(fig, filename="apps/scoreKeeper/static/{}".format(graph))
    
    return render(request, 'scoreKeeper/metrics.html', context)
def highScores(request):
    breakout = Game.objects.filter(title='breakout')
    topBO = Score.objects.filter(game=breakout).order_by('-totalScore')[:10]
    tetris = Game.objects.filter(title='tetris')
    topT = Score.objects.filter(game=tetris).order_by('-totalScore')[:10]
    context = {
        'topBO' : topBO,
        'topT' : topT
        }
    return render(request, 'scoreKeeper/highScores.html', context)

    ## TODO ##
    #beautify
    #fix the css on Breakout
    #multiple levels for BO
    #tetris

