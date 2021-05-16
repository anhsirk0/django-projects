from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    cash = models.FloatField(default=10000)
    def __str__(self):
        return f"{self.username}, {self.cash} $"

class Share(models.Model):
    user = models.ForeignKey(User, related_name="share", on_delete=models.CASCADE)
    symbol = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    no_of_share = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} , {self.symbol}, {self.no_of_share}, {self.price}"


class History(models.Model):
    user = models.ForeignKey(User, related_name="history", on_delete=models.CASCADE)
    symbol = models.CharField(max_length=64)
    no_of_share = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} , {self.symbol}, {self.no_of_share}, {self.price}, {self.time}"
