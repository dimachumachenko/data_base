from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import path, reverse_lazy
from django.views.generic import CreateView

from . import views
from django.contrib.auth import views as auth_views, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, UserManager
from django.contrib import messages
from .forms import NewUserForm, UserForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import CreditRequestForm
from .models import Account, Credit
# Create your views here.

def home(request):

    context = {}

    if request.user.is_authenticated:
        context.update({'is_authenticated' : True})

    return render(request, 'mybankapp/home.html', context=context)

def search(request):
    # Здесь вы можете добавить логику для обработки поисковых запросов
    # и передать результаты поиска в шаблон
    return render(request, 'mybankapp/search.html')


def temp_register(request):
    if request.POST:
        form = UserForm(request.POST)
        if not form.is_valid():
            return render(request, 'mybankapp/registration.html', {'is_busy': True, 'form': form})

        user=form.save()

        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        account=Account(username=user,owner=1,limit=1)

        account.save()
        user = authenticate(request, username=username, password=password)

        login(request, user)

        return redirect('profile')

    return render(request, 'mybankapp/registration.html')

def temp_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'mybankapp/login.html', context={"is_failed": True})
        login(request, user)
        return redirect('home')
    return render(request, 'mybankapp/login.html')

@login_required
def temp_logout(request):
    logout(request)
    return redirect('home')

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
    return render(request=request, template_name="mybankapp/login.html", context={"form": form})


###### Kelbas ########


from django.views.generic import TemplateView



class RegistrationView(CreateView):
    template_name = 'mybankapp/registration.html'
    model = User
    fields = ['username', 'password', ]


class DbViewer(TemplateView):
    template_name = 'mybankapp/db.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest']



def request_credit(request):
    if request.method == 'POST':
        form = CreditRequestForm(request.POST)
        if form.is_valid():
            credit_data = form.cleaned_data
            print('hui')
            # Создайте новую запись о кредите
            new_credit = Credit(
                account=request.user,  # Предполагается, что у пользователя есть связанный счет
                amount=credit_data['amount'],
                interest_rate=credit_data['interest_rate'],
                term=credit_data['term']
            )
            new_credit.save()

            # Обновите счет пользователя и кредитный счет
            user_account = request.user.account
            user_account.balance -= credit_data['amount']  # Уменьшаем счет на сумму кредита
            user_account.credit_balance += credit_data['amount']  # Увеличиваем кредитный счет на сумму кредита
            user_account.save()

            return redirect('success_page')  # Перенаправьте пользователя на страницу успеха

    else:
        form = CreditRequestForm()

    return render(request, 'mybankapp/credit.html', {'form': form})