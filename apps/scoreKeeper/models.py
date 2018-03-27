from __future__ import unicode_literals
# from apps.login_reg.models import *
from django.db import models

# Create your models here.
class Game(models.Model):
    gameTitle = models.CharField(max_length = 255)
    # total_score = models.IntegerField()
    score = models.ManyToManyField('login_reg.User', related_name = "scores")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
