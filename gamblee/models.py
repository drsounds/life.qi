from django.db import models
from django.contrib.auth.models import User
import datetime
class Company(models.Model):
    title = models.CharField(max_length=255)
    def __unicode__(self):
        return self.title

class Account(models.Model):
    user = models.ForeignKey(User, related_name='game_user')
    balance = models.FloatField(default=0.0)
    max_plays_per_week = models.IntegerField(default=2)

class Game(models.Model):
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company)
    cost = models.FloatField(default=10)
    def __unicode__(self):
        return self.title

class Play(models.Model):
    time = models.DateTimeField(default=datetime.datetime.now)
    prize = models.FloatField(default=0)
    cost = models.FloatField(default=10)
    account = models.ForeignKey(Account)
    game = models.ForeignKey(Game)
    def won(self):
        return self.prize > 0

    def save(self, *args, **kwargs):
        self.account.balance = self.account.balance - self.cost
        self.account.balance = self.account.balance + self.prize
        self.account.save()
        super(Play, self).save(args, kwargs)
