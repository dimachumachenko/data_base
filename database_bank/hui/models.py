from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    # Добавьте другие поля, которые вы хотите хранить о пользователях, например, email, телефон и т. д.

    def __str__(self):
        return self.user.username
