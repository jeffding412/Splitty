from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

# the index function is called when root is visited
def index(request):
    return render(request, 'splitty/index.html')

# the logout function is called to clear cookies
def logout(request):
    request.session.clear()
    return redirect('/')

# the login function is called when login form is submitted
def login(request):
    # checks for form input erros
    request.session['errors'] = User.objects.validator(request.POST)

    if len(request.session['errors']):
        # redirect the user back to the form to fix the errors
        return redirect('/')

    # checks if there is already a user with the posted username
    user = User.objects.filter(username=request.POST['username'])

    # if no user with same username
    if len(user) == 0:
        # generate password hash and create user
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(username=request.POST['username'],password_hash=pw_hash)
        request.session['user_id'] = user.id
    else:
        # user exists
        request.session['user_id'] = user[0].id

    return redirect('/') # reroute this next page