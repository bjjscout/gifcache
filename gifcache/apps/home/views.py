from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import LoginForm, SignupForm
from ..users.models import Profile
import random
import os


# Returns number of saved GIFs in my static/img folder
def get_saved_gifs():
    gif_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static\\img\\')
    files = []
    for (dirpath, dirnames, filenames) in os.walk(gif_dir):
        files.extend(filenames)
        break
    return len([f for f in files if f.endswith('gif')])


# Create your views here.
def error404(request):
    return render(request, 'home/404.html')


def error500(request):
    return render(request, 'home/500.html')


def index(request):
    logged_in = False
    if request.user.is_authenticated():
        logged_in = True

    random_gif = random.choice(xrange(get_saved_gifs()))

    context = {
        'title': 'Home',
        'logged_in': logged_in,
        'username': request.user.username,
        'random_gif': random_gif
        }

    return render(request, 'home/home.html', context)


def login_view(request):
    logged_in = False
    if request.user.is_authenticated():
        logged_in = True

    context = {
        'title': 'Login',
        'form': LoginForm(),
        'logged_in': logged_in,
        'username': request.user.username,
        'random_gif': random.choice(xrange(get_saved_gifs()))
        }
    return render(request, 'home/login.html', context)


def logout_view(request):
    logout(request)
    context = {
        'title': 'Home',
        'message': 'You have been succesfully logged out!',
        'random_gif': random.choice(xrange(get_saved_gifs()))
    }
    return render(request, 'home/home.html', context)


def authenticate_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/u/%s' % str(user.username))
        else:
            context = {
                'title': 'Login',
                'form': LoginForm(),
                'message': 'This account has been deactivated, please create a new one.',
                'random_gif': random.choice(xrange(get_saved_gifs()))
            }
            return render(request, 'home/login.html', context)
    else:
        context = {
            'title': 'Login',
            'form': LoginForm(),
            'message': 'Invalid Login, please try again.',
            'random_gif': random.choice(xrange(get_saved_gifs()))
        }
        return render(request, 'home/login.html', context)


def signup(request):
    print request.user.username
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            message = 'Account Created!'
            print message
    else:
        form = SignupForm()
    context = {
        'form': form,
        'title': 'Signup',
        'random_gif': random.choice(xrange(get_saved_gifs()))
    }
    return render(request, 'home/signup.html', context=context)


def create_account(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            nickname = request.POST['nickname']
            u = User.objects.create_user(username=username, password=password, email=email, first_name=nickname)
            p = Profile(owner=u)
            u.save()
            p.save()
            request.user.username = username
            context = {
                'name': nickname,
                'username': username,
                'random_gif': random.choice(xrange(get_saved_gifs()))
            }
            return render(request, 'home/account_created.html', context)
        else:
            context = {
                'form': form
            }
            return render(request, 'home/signup.html', context)
    else:
        form = SignupForm()
        random_gif = random.choice(xrange(get_saved_gifs()))
        return render(request, 'home/signup.html', {'form': form, 'random_gif': random_gif})