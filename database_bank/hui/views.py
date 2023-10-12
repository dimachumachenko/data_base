from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import path, reverse_lazy
from django.views.generic import CreateView

from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.

def home(request):
    return render(request, 'mybankapp/home.html')

def search(request):
    # Здесь вы можете добавить логику для обработки поисковых запросов
    # и передать результаты поиска в шаблон
    return render(request, 'mybankapp/search.html')

def register(request):
    if request.method == 'POST':

        user = User(
            username=request.POST['username'],
            password=request.POST['password1'],
            email=request.POST['email'],
        )

        user = user.save()

        messages.success(request, "Registration successful.")
        return redirect('login')
        # messages.error(request,"Unsuccessful registration. Invalid information.")
    form=NewUserForm()

    return render(request, 'mybankapp/register.html', {'form': form})



@login_required
def profile(request):
    return render(request, 'mybankapp/profile.html')

def user_login(request):
    if request.method=='POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("hui:profile")
            else:
                messages.error(request, "Invalid username or password.")

        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="hui/login.html", context={"form": form})





