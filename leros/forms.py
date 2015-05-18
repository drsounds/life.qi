# -*- coding: utf-8 -*-
from django import forms
from leros.models import *
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('sport', 'duration', 'time', 'facility', 'units')

class ConditionForm(forms.ModelForm):
    class Meta:
        model = Condition
        fields = ('sex', 'weight', 'stomach', 'hip', 'mental_clarity', 'mental_affectivity', 'mental_elastics')

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('time',  'duration')