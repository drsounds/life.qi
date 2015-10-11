from django.db import models
from django.contrib.auth.models import User
import datetime
class Category(models.Model):
    title = models.CharField(max_length=255)
    def __unicode__(self):
        return self.title   

class StatusCode(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    def __unicode__(self):
        return self.title

class State(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    def __unicode__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=255)
    def __unicode__(self):
        return self.title

class Outcome(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    def __unicode__(self):
        return self.title   

# Create your models here.
class Opportunity(models.Model):
    parent_opportunity = models.ForeignKey("self", null=True, blank=True)
    outcome = models.ForeignKey(Outcome)
    affection = models.FloatField() # Negative affection - threat, positive affection opportunity
    priority = models.IntegerField(default=1)
    category = models.ForeignKey(Category)
    description = models.TextField()
    status = models.ForeignKey(StatusCode)
    added = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(default=datetime.datetime.now)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    state = models.ForeignKey(State)
    def __unicode__(self):
        return self.title

class Inquery(models.Model):
    affection = models.FloatField(default=0, null=True, blank=True) # Negative affection - threat, positive affection opportunity
    opportunity = models.ForeignKey(Opportunity)
    time = models.DateTimeField()
    status = models.ForeignKey(StatusCode)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, null=True, blank=True)