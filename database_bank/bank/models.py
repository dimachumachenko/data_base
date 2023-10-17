from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User







# Модель Счета


class Credit(models.Model):

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term = models.IntegerField()
    status = models.BooleanField(default=True)

    def getStatus(self):
        if self.status:
            return 'Действителен'
        return 'Погашен'


class Account(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, to_field='username')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    owner = models.CharField(max_length=150, unique=True)
    open_date = models.DateField(auto_now_add=True, blank=True)
    close_date = models.DateField(auto_now_add=True, blank=True)
    active = models.BooleanField(default=True)
    limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    credit = models.ManyToManyField(Credit)
    currency = models.CharField(max_length=15, default="RUB")

# Модель Транзакции
class Transaction(models.Model):

    sender_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions_sent')
    receiver_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

# Модель Кредиты

# Модель Платежи_по_кредитам
class CreditPayment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()

# Модель Вклады
class Deposit(models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term = models.IntegerField()

# Модель Платежи_по_вкладам
class DepositPayment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.TimeField()
    date = models.DateField()

# Модель Валюты
class Currency(models.Model):

    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField()

# Модель Курсы_валют
class CurrencyExchangeRate(models.Model):

    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='exchanges_from')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='exchanges_to')
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    update_date = models.DateField()

# Модель Отделения
class Branch(models.Model):

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10)
    open_date = models.DateField()
    manager_name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    employees_count = models.IntegerField()
    average_age = models.IntegerField()
    description = models.TextField()
    website = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    specialization = models.CharField(max_length=100)

# Модель Кредитные_истории
class CreditHistory(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    loan_start_date = models.DateField()
    loan_end_date = models.DateField()
    status = models.CharField(max_length=50)
    payments = models.TextField()

# Модель Кредитные_заявки
class LoanApplication(models.Model):


    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    application_date = models.DateField()


class Person(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    person_age = models.IntegerField(null=True)
    # bank_branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, to_field='owner', null=True)
    # person_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
    # deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE)
    # transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    # credit_history=models.ForeignKey(CreditHistory, on_delete=models.CASCADE)


