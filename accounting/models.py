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

class Voucher(models.Model):
    time = models.DateTimeField(default=datetime.datetime.now)
    url = models.URLField(null=True,blank=True)
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=255, null=True, blank=True)



# Create your models here.
class Account(models.Model):
    id = models.CharField(max_length=25, blank=True, primary_key=True)
    balance = models.FloatField()
    user = models.ForeignKey(User)
    currency = models.ForeignKey(Currency)
    name = models.CharField(max_length=255)
    
    def transactions(self):
        _transactions = Transaction.objects.filter(user=self.user, account=self)
        transactions = []
        for _transaction in _transactions:
            transaction = {
                'name': _transaction.text,
                'time': _transaction.time,
                'debet': 0,
                'credit': 0
            }
            if _transaction.amount < 0:
                transaction['debet'] = -_transaction.amount
            if _transaction.amount > 0:
                transaction['credit'] = _transaction.amount
            transactions.append(transaction)

        return transactions
    def sum_debet(self):
        sum_debet = Transaction.objects.annotate(models.Sum(amount__lt=0))['amount__gt']
        return sum_debet

    def sum_credit(self):
        sum_credit = Transaction.objects.annotate(models.Sum(amount__gt=0))['amount__gt']
        return sum_credit

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

    def get_transactions(self, user):
        _transactions = Transaction.objects.filter(user=user)
        transactions = []
        for _transaction in _transactions:
            transaction = {
                'name': _transaction.text,
                'debet': 0,
                'credit': 0
            }
            if _transaction.amount < 0 :
                transaction['debet'] = -_transaction.amount
            if _transaction.amount > 0:
                transaction['credit'] = _transaction.amount
            transactions.append(transaction)

        sum_credits = Transaction.objects.annotate(Sum(amount__lt=0), user=user)['amount']
        sum_debits = Transaction.objects.annotate(Sum(amount__lt=0), user=user)['amount']
        return {
            'transactions': transactions,
            'sum_credits': sum_credits,
            'sum_debits': sum_debits
        }

    def __unicode__(self):
        return self.id

class Transaction(models.Model):
    id = models.CharField(max_length=25, blank=True, primary_key=True)
    amount = models.FloatField()
    text = models.CharField(max_length=25)
    balance = models.FloatField()
    time = models.DateTimeField(default=datetime.datetime.now)
    account = models.ForeignKey(Account)
    user = models.ForeignKey(User)
    currency = models.ForeignKey(Currency)
    tags = models.ManyToManyField(Tag, blank=True)
    voucher = models.ForeignKey(Voucher, null=True, blank=True)
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
        super(Transaction, self).save(args, kwargs)

    def delete(self):
        super(Transaction, self).delete(args)
        self.account.balance -= self.amount
        self.account.save()
