from django.db import models
from django.contrib.auth.models import *
# Create your models here.
import datetime
import random
import math
def _random_string(length=25):
    characters = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVv0123456789'
    output = ''
    for i in range(length):
        char = characters[random.randint(0, len(characters)-1)]
        output = output + char
    return output


class Status(models.Model):
    code = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    def __unicode__(self):
        return '%d %s' % (self.code, self.title)


class Account(models.Model):
    user = models.ForeignKey(User, related_name='account_user')
    id = models.CharField(max_length=255, primary_key=True, blank=True)
    amount = models.FloatField()
    currency = models.CharField(max_length=5)
    def __unicode__(self):
        return '%s (%d %s)' % (self.user.username, self.amount, self.currency)
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Account, self).save(args, kwargs)


class Transaction(models.Model):
    id = models.CharField(max_length=255, primary_key=True, blank=True)
    amount = models.FloatField()
    account = models.ForeignKey(Account)
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Transaction, self).save(args, kwargs)

class Sex(models.Model):
    id = models.CharField(max_length=255, primary_key=True, blank=True)
    bio = models.BooleanField()
    def save(self, *args, **kwargs):
        # self.id = _random_string(3)
        super(Sex, self).save(args, kwargs)
    def __unicode__(self):
        return self.id

class Condition(models.Model):
    """
    BMI calculation taken from
    http://www.markazits.com/diet/bmi.php
    """
    id = models.CharField(max_length=255, primary_key=True, blank=True)
    user = models.ForeignKey(User, related_name='condition_user')
    date = models.DateField(default=datetime.datetime.today)
    weight = models.FloatField()    # Body weight
    hip = models.FloatField()       #
    stomach = models.FloatField()   #
    height = models.FloatField()    # 
    age = models.IntegerField()     #
    sex = models.ForeignKey(Sex)    
    
    # Mental condition
    mental_clarity = models.FloatField()
    mental_affectivity = models.FloatField()
    mental_elastics = models.FloatField()
    
      
    def bmi(self):
        return self.weigth / (self.height * self.height)
    
    def integrity(self):
        return 'Unknown'
    
    def middlequote(self):
        return (self.stomach / self.hip)
    
    def __unicode__(self):
        return self.user.username
    
    def fat_quote(self, type = 'YMCA'):
        if type == 'YMCA':
            factor = 98.42
            if self.sex.bio:
                factor = 76.76
            
            fat = (-factor + (4.15 * self.middlequote) - (0.82 * self.weight)) / self.weight
            return fat
        else:
            factor = 16.2
            if self.sex.bio:
                factor = 5.4
            fat = (1.2 * self.bmi()) + (0.23 * self.age) - factor
            return fat
             
        
    
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(State, self).save(args, kwargs)

class Place(models.Model):
    title = models.CharField(max_length=255)
    def __unicode__(self):
        return self.title

class Sport(models.Model):
    id = models.CharField(max_length=255, primary_key=True, blank=True)
    name = models.CharField(max_length=255)
    aquatic = models.BooleanField()
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id == ''    :
            self.id = _random_string(25)
        super(Sport, self).save(args, kwargs)

class Booking(models.Model):
    """
    Each aqua session is considered as a HTTP Request against the facility that are started upon the preparation and
    the status code thus reflects that
    """
    id = models.CharField(max_length=255, primary_key=True, blank=True)
    time = models.DateTimeField(default=datetime.datetime.now)
    user = models.ForeignKey(User)
    clothed = models.BooleanField(default=False)
    status = models.ForeignKey(Status)
    place = models.ForeignKey("Place")
    duration = models.IntegerField()
    eating = models.BooleanField(default=False)
    stacktrace = models.TextField(null=True,blank=True)
    sport = models.ForeignKey("Sport")
    flow = models.TextField(null=True, blank=True)
    placed = models.DateTimeField(default=datetime.datetime.now)
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.place.title
    
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Booking, self).save(args, kwargs)


class Facility(models.Model):
    id = models.CharField(max_length=255, primary_key=True, blank=True)
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name
    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Facility, self).save(args, kwargs)


class Activity(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    sport = models.ForeignKey(Sport)
    user = models.ForeignKey(User, related_name='activity_user')
    facility = models.ForeignKey(Facility)
    time = models.DateTimeField(default=datetime.datetime.now)
    duration = models.IntegerField()
    qi = models.FloatField(default=0,blank=True)
    units = models.FloatField()
    def __unicode__(self):
        return self.sport.name

    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = _random_string(25)
        super(Activity, self).save(args, kwargs)
        