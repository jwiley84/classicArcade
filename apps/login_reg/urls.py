from django.conf.urls import url
from . import views         


urlpatterns = [
url(r'^$', views.index),
url(r'^reg$', views.registration),
url(r'^login$', views.login),
url(r'^logout$', views.logout),
url(r'^success$', views.success),
url(r'^profile/(?P<id>\d+)$', views.profile),

]
