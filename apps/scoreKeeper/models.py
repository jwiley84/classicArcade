from __future__ import unicode_literals
# from apps.login_reg.models import *
from django.db import models
from ..login_reg.models import *

# Create your models here.

class scoreManager(models.Manager):
    def scoreCreator(self, scoreObj):
        results = {}
        results['newScore'] = self.create(totalScore=scoreObj['score'], game =Game.objects.get(id = scoreObj['game']), player = User.objects.get(id = scoreObj['user']))
        # else: results['visitorPlayer'] = "visitor"
        print "*****New Score created*****"
        return results;

class Game(models.Model):
    title = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __repr__(self):
        return self.title

class Score(models.Model):
    totalScore = models.IntegerField()
    #one game can have many scores
    game = models.ForeignKey(Game, related_name = "gameScores")
    #one player can have many scores
    player = models.ForeignKey('login_reg.User', related_name = "playerScores")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = scoreManager()
    def __repr__(self):
        return '{} {} {}'.format(self.player.username, self.game.title, self.totalScore)

