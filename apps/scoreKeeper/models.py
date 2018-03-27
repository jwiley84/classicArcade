from __future__ import unicode_literals
# from apps.login_reg.models import *
from django.db import models

# Create your models here.

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
    def __repr__(self):
        return '{} {} {}'.format(self.player, self.game, self.totalScore)

