from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from ..scoreKeeper.models import *
import bcrypt

def index(request):
    return render(request, 'log_reg.html')

def registration(request):
  results = User.objects.register_validation(request.POST)

  if results[0]:
    request.session['user_id'] = results[1].id
    request.session['name'] = results[1].name
    print "******* You're registered! ******"
    return redirect('/user/success')
  
  else:
    for err in results[1]:
      messages.error(request, err)
    return redirect('/user')
    
def login(request):
  results = User.objects.login_validation(request.POST)

  if results[0]:
    request.session['user_id'] = results[1].id 
    print "******* logged in yo! ******"
    return redirect('/user/success')
  else:
    for err in results[1]:
      messages.error(request, err)
  return redirect('/user')

def logout(request):
  request.session.flush()
  print "++++++++ You logged out ++++++++++"
  return redirect('/user')

def success(request):
  if 'user_id' not in request.session:
      return redirect ('/user')
  context = {
    'user' : User.objects.get(id=request.session['user_id']),    
    'top' : Score.objects.filter(player=request.session['user_id']).order_by('-totalScore')[:10]
    }
  return render(request, 'success.html', context)

def profile(request, id):
  user = User.objects.get(id=id)
  context ={
    'user' : user,
    'top' : Score.objects.filter(player=user).order_by('-totalScore')[:10]
  }
  return render(request, 'profile.html', context)

