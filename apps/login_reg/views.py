from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
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
  return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect ('/')
    context = {
    'user' : User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'success.html', context)
