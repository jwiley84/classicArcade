from django.conf.urls import url
from . import views 

urlpatterns = [ 
    url(r'^$', views.index),
    url(r'^receiver', views.receiver),
    url(r'^playGame', views.playGame),
    url(r'^(?P<id>\d+)', views.playGame), #display the particular game
    ]