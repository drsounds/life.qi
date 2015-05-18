from django.db import models
from django.contrib.auth.models import User
import datetime
import random

# Create your models here.
def _random_string(length=25):
    characters = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVv0123456789'
    output = ''
    for i in range(length):
        char = characters[random.randint(0, len(characters)-1)]
        output = output + char
    return output


class Currency(models.Model):
    id = models.CharField(max_length=25, blank=True, primary_key=True)
    def __unicode__(self):
        return self.id

class Account(models.Model):

    id = models.CharField(max_length=25, blank=True, primary_key=True)
    balance = models.FloatField()
    user = models.ForeignKey(User, related_name='accounted_user')
    currency = models.ForeignKey("Currency")
    name = models.CharField(max_length=255)
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Account, self).save(args, kwargs)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    id = models.CharField(max_length=25, blank=True, primary_key=True)
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Tag, self).save(args, kwargs)
    def __unicode__(self):
        return self.id

class Qi(models.Model):
    id = models.CharField(max_length=25, blank=True, primary_key=True)
    amount = models.FloatField()
    text = models.CharField(max_length=25)
    balance = models.FloatField()
    time = models.DateTimeField(default=datetime.datetime.now)
    account = models.ForeignKey(Account)
    user = models.ForeignKey(User, related_name='qi_user')
    currency = models.ForeignKey(Currency)
    tags = models.ManyToManyField(Tag, blank=True)
    transaction = models.ForeignKey("Transaction", null=True, blank=True)
    def user_disp(self):
        return self.user.username
        
    def amount_disp(self):
        return '<span style="float: right">%s@</span>' % (self.amount)

    def __unicode__(self):
        return '%s %s %s' % (self.amount, self.text, self.balance)

    amount_disp.allow_tags = True
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        self.account.balance += self.amount
        self.balance = self.account.balance
        self.account.save()
        super(Qi, self).save(args, kwargs)

    def delete(self):
    	super(Qi, self).delete(args)
    	self.account.balance -= self.amount
    	self.account.save()

class Transaction(models.Model):

    id = models.CharField(max_length=25, blank=True, primary_key=True)
    parent_transaction = models.ForeignKey("self", null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    amount = models.FloatField(default=0)
    time = models.DateTimeField(default=datetime.datetime.now)
    name = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(User, related_name='transaction_user')
    def __unicode__(self):
        return self.name
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Transaction, self).save(args, kwargs)


    def delete(self):
        super(Transaction, self).delete()

