import feedparser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
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
from .forms import UserForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import CreditRequestForm
from .models import Account, Credit, Person
from django.views.generic.list import ListView
from .models import News
from django.contrib.syndication.views import Feed
import xml.etree.ElementTree as ET
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

        person = Person(username=user)

        person.save()

        account_rub = Account.objects.create(currency="RUB", person=person)
        account_usd = Account.objects.create(currency="USD", person=person)
        account_eur = Account.objects.create(currency="EUR", person=person)

        person.account_set.add(account_eur, account_usd, account_rub)

        person.save()

        user = authenticate(request, username=username, password=password)

        login(request, user)

        return redirect('profile', currency='RUB')

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
def profile(request, currency):
    if not currency:
        currency = "RUB"

    return render(
        request,
        'mybankapp/profile.html',
        context={
            'credits': request.user.person.account_set.get(currency=currency).credit.all(),
            'account': request.user.person.account_set.get(currency=currency),
            'currency': currency
        }
    )






from django.views.generic import TemplateView


def pay_off_credit(request, currency):
    if request.POST:
        credit_id = request.POST['credit_id']
        payment_amount = request.POST['payment_amount']

        user_account = request.user.person.account_set.get(currency=currency)

        if user_account.balance < int(payment_amount):
            return render(request, "mybankapp/tmp.html", context={'not_enough': True})

        if not Credit.objects.get(id=int(credit_id)).status:
            return render(request, "mybankapp/tmp.html", context={'is_closed': True})

        user_account.balance -= int(payment_amount)

        user_credit = Credit.objects.get(id=int(credit_id))

        user_credit.amount -= int(payment_amount)

        if user_credit.amount <= 0:
            user_credit.status = False

        user_account.save()
        user_credit.save()

        return redirect('profile', currency=currency)

    return render(request, "mybankapp/pay_off_credit.html")


def request_credit(request, currency):
    if request.method == 'POST':
        form = CreditRequestForm(request.POST)
        if form.is_valid():
            credit_data = form.cleaned_data
            # Создайте новую запись о кредите
            new_credit = Credit(
                account=request.user.person.account_set.get(currency=currency),  # Предполагается, что у пользователя есть связанный счет
                amount=credit_data['amount'],
                interest_rate=credit_data['interest_rate'],
                term=credit_data['term']
            )
            new_credit.save()

            # Обновите счет пользователя и кредитный счет
            user_account = request.user.person.account_set.get(currency=currency)
            user_account.balance += credit_data['amount']  # Уменьшаем счет на сумму кредита
            user_account.save()

            user_account.credit.add(new_credit)

            return redirect('profile', currency=currency)  # Перенаправьте пользователя на страницу успеха

    else:
        form = CreditRequestForm()

    return render(request, 'mybankapp/credit.html', {'form': form})


def tmp(request):
    return render(request, 'mybankapp/tmp.html', context={
        'user_counter': len(Person.objects.all()),
        'stat_1': len(Account.objects.all().filter(currency="RUB").filter(balance__lt=1000000)),
        'stat_2': len(Account.objects.all().filter(currency="USD").filter(balance__lt=1000000)),
        'stat_3': len(Account.objects.all().filter(currency="EUR").filter(balance__lt=1000000)),
        'stat_4': len(Account.objects.all().filter(currency="RUB").filter(balance__gte=1000000).filter(balance__lt=10000000)),
        'stat_5': len(Account.objects.all().filter(currency="USD").filter(balance__gte=1000000).filter(balance__lt=10000000)),
        'stat_6': len(Account.objects.all().filter(currency="EUR").filter(balance__gte=1000000).filter(balance__lt=10000000)),
        'stat_7': len(Account.objects.all().filter(currency="RUB").filter(balance__gte=10000000)),
        'stat_8': len(Account.objects.all().filter(currency="USD").filter(balance__gte=10000000)),
        'stat_9': len(Account.objects.all().filter(currency="EUR").filter(balance__gte=10000000)),
    })


def search(request):
    if request.POST:
        username = None
        filtered_accounts = None
        if 'username' in request.POST:
            filtered_accounts = Account.objects.all()
        else:
            username = request.POST['username']
            filtered_accounts = Account.objects.all().filter(person_id=Person.objects.all().get(username=username).id)

        min_balance = request.POST['min_balance']
        filtered_accounts = filtered_accounts.filter(balance__gt=min_balance)
        max_balance = request.POST['max_balance']
        if int(max_balance) != 0:
            filtered_accounts = filtered_accounts.filter(balance__lt=max_balance)

        return render(request, 'mybankapp/search.html', context={
            'persons': Person.objects.all(),
            'username': username,
            'accounts': filtered_accounts
        })

    return render(request, 'mybankapp/search.html', context={
        'persons': Person.objects.all(),
    })

def make_rss(request):
    # rss_url = 'https://www.vedomosti.ru/rss/news.xml'
    rss_url = 'http://feeds.bbci.co.uk/news/world/rss.xml'
    feed = feedparser.parse(rss_url)

    description = ''

    for entry in feed.entries:
        if 'description' in feed.entries[0]:
            description = entry.description
        try:
            new = News(title=entry.title, link=entry.link, content=description)
            new.save()
        except IntegrityError as e:
            pass

    context = {
        'feed': News.objects.all()[::-1][:10]
    }

    return render(request, 'mybankapp/news_list.html', context=context)


def create_news(request):
    if request.POST:
        title = request.POST['title']
        content = request.POST['content']
        link = request.POST['link']
        try:
            new = News(title=title, content=content, link=link)
            new.save()
        except IntegrityError as e:
            pass
        return redirect('news_list')
    return render(request, 'mybankapp/create_news.html')


def add_rss(request):
    if request.POST:
        link = request.POST['link']
        feed = feedparser.parse(link)

        description = ''

        for entry in feed.entries:
            if 'description' in feed.entries[0]:
                description = entry.description
            try:
                new = News(title=entry.title, link=entry.link, content=description)
                new.save()
            except IntegrityError as e:
                pass

        context = {
            'feed': News.objects.all()[::-1][:10]
        }

        return render(request, 'mybankapp/news_list.html', context=context)
    return render(request, 'mybankapp/add_rss.html')

def datas_as_xml(reqest):
    data_from_db=Account.objects.all()

    root=ET.Element("data")

    for item in data_from_db:
        xml_element=ET.fromstring(item.as_xml())
        root.append(xml_element)


    xml_string=ET.tostring(root,encoding='utf-8', method='xml')
    return HttpResponse(xml_string,content_type='application/xml')
from xml.etree.ElementTree import Element, SubElement, tostring

def data_as_xml(request):

    data_from_db = Credit.objects.all()  # Получаем данные из базы

    root = Element("data")

    for item in data_from_db:
        xml_element = Element("item")
        # Преобразуем логические значения в строки перед добавлением в XML
        SubElement(xml_element, "amount").text = str(item.amount)
        SubElement(xml_element, "interest_rate").text = str(item.interest_rate)
        SubElement(xml_element, "term").text = str(item.term)
        SubElement(xml_element, "status").text = str(item.status)
        print(f"Amount: {item.amount}, Interest Rate: {item.interest_rate}, Term: {item.term}, Status: {item.status}")

        root.append(xml_element)

        xml_string = tostring(root, encoding='unicode')

        # Создаем HTTP-ответ с XML-данными
        #response = HttpResponse(xml_string)
        #return response


    xml_string = tostring(root, encoding='unicode')
    return render(request, 'mybankapp/xml.html', {'xml_data': xml_string})






