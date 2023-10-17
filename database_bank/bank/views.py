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



def temp_register(request):
    if request.POST:
        form = UserForm(request.POST)
        if not form.is_valid():
            return render(request, 'mybankapp/registration.html', {'is_busy': True, 'form': form})

        user = form.save()

        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        account = Account(username=user, owner=username, limit=1)

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
    return render(request, 'mybankapp/profile.html', context={'credits': request.user.account.credit.all(), 'account': request.user.account})



###### Kelbas ########


from django.views.generic import TemplateView


def pay_off_credit(request):
    if request.POST:
        credit_id = request.POST['credit_id']
        payment_amount = request.POST['payment_amount']

        user_account = request.user.account

        if user_account.balance < int(payment_amount):
            return render(request, "mybankapp/tmp.html", context={'not_enough' : True})

        if not Credit.objects.get(id=int(credit_id)).status:
            return render(request, "mybankapp/tmp.html", context={'is_closed' : True})

        user_account.balance -= int(payment_amount)

        user_credit = Credit.objects.get(id=int(credit_id))

        user_credit.amount -= int(payment_amount)

        if user_credit.amount <= 0:
            user_credit.status = False

        user_account.save()
        user_credit.save()

        return redirect('profile')

    return render(request, "mybankapp/tmp.html")



def request_credit(request):
    if request.method == 'POST':
        form = CreditRequestForm(request.POST)
        if form.is_valid():
            credit_data = form.cleaned_data
            print('bank')
            # Создайте новую запись о кредите
            new_credit = Credit(
                account=request.user.account,  # Предполагается, что у пользователя есть связанный счет
                amount=credit_data['amount'],
                interest_rate=credit_data['interest_rate'],
                term=credit_data['term']
            )
            new_credit.save()

            # Обновите счет пользователя и кредитный счет
            user_account = request.user.account
            user_account.balance += credit_data['amount']  # Уменьшаем счет на сумму кредита
            user_account.save()

            user_account.credit.add(new_credit)

            return redirect('profile')  # Перенаправьте пользователя на страницу успеха

    else:
        form = CreditRequestForm()

    return render(request, 'mybankapp/credit.html', {'form': form})