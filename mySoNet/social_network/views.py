from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm  # Replace with your form name
from django.contrib.auth import login, logout
from .models import Post, Follow
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import SignUpForm 


def index(request):
  return render(request, 'index.html')

def gemihome(request):
    # Get all posts (or filter based on specific criteria)
    posts = Post.objects.all().order_by('-created_at')  # Order by most recent

    context = {'posts': posts}
    return render(request, 'gemihome.html', context)


def login(request):
    if request.method == 'POST':
        # If form is submitted
        form = LoginForm(request.POST)  # Use custom form if defined
        if form.is_valid():
            user = form.cleaned_data['user']  # Access authenticated user from form
            login(request, user)  # Log in the user
            return redirect('home')  # Redirect to homepage or desired URL after login
    else:
        # If GET request (form not submitted)
        form = LoginForm()  # Use custom form if defined

    context = {'form': form}
    return render(request, 'login.html', context)


@csrf_protect # Assuming you have a SignUpForm defined

def signup(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save()  # Creates and saves the user
      login(request, user)  # Log the user in automatically
      return redirect('home')  # Redirect to the home page after signup
  else:
    form = SignUpForm()
  return render(request, 'signup.html', {'form': form})


@login_required
def home(request, user_id):
    user = User.objects.get(pk=user_id)  # Get the current logged-in user

    # Optimized follower lookup using prefetching
    following = Follow.objects.filter(follower=user).select_related('following')
    # Get recent posts from users being followed
    posts = Post.objects.filter(author__in=following.values_list('following__id', flat=True)).order_by('-created_at')

    context = {'posts': posts}
    return render(request, 'home.html', context)