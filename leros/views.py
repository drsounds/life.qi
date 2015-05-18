from django.shortcuts import render_to_response
from leros.models import *
from django.db.models import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail
from django.http import HttpResponse
from provider.oauth2.models import Client
import simplejson
from leros.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv
import datetime
import logging 
import random

# Create your views here.
def dashboard(request):
    return render_to_response('leros/dashboard.html', {}, context_instance=RequestContext(request))

def booking(request, booking_id):
    booking = Booking.objects.filter(user=request.user, id=booking_id)
    return render_to_response('leros/booking/view.html', {'booking': booking}, context_instance=RequestContext(request))


def bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-time')
    paginator = Paginator(bookings, 25)
    page = 1
    if 'page' in request.GET:
        page = request.GET.get('page')
    try:
        bookings = paginator.page(page)
    except Exception,e:
        bookings = paginator.page(1)
    return render_to_response('leros/booking/index.html', {'bookings': bookings}, context_instance=RequestContext(request))



def edit_booking(request, id):
    booking = Booking.objects.get(id=id, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.save():
            return redirect('/booking/edit/' + booking.id + '/')
    
    form = BookingForm(instance=booking)
    return render_to_response('leros/booking/edit.html', {'form': form, 'booking': booking}, context_instance=RequestContext(request))

def delete_booking(request):
    activity = Booknig.objects.get(id=id)
    activity.delete()
    return redirect('/booking/')


def add_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        booking = form.save(False)
        booking.user = request.user
        booking.status = Status.objects.get(code=100)
        booking.save()
        if booking:
            return redirect('/booking/' + booking.id + '/')
    
    form = BookingForm()
    return render_to_response('leros/booking/add.html', {'form': form}, context_instance=RequestContext(request))

def activitys(request):
    activitys = Activity.objects.filter(user=request.user).order_by('-time')
    paginator = Paginator(activitys, 25)
    page = 1
    if 'page' in request.GET:
        page = request.GET.get('page')
    try:
        activitys = paginator.page(page)
    except Exception,e:
        activitys = paginator.page(1)
    
    return render_to_response('leros/activity/index.html', {'activitys': activitys}, context_instance=RequestContext(request))
def delete_activity(request, id):
    activity = Activity.objects.get(id=id)
    activity.delete()
    return redirect('/activity/')

def edit_activity(request, id):
    if request.method == 'POST':
        activity = Activity.objects.get(id=id, user=request.user)
        form = ActivityForm(request.POST, instance=activity)
        activity = form.save()
        if activity:
            return redirect('/activity/edit/' + activity.id + '/')
        else:
            return HttpResponse('Error')
    
    activity = Activity.objects.get(pk=id)
    form = ActivityForm(instance=activity)
    return render_to_response('leros/activity/edit.html', {'activity': activity, 'form': form}, context_instance=RequestContext(request))
def view_activity(request, id):
    activity = Activity.objects.get(user=request.user, id=id)
    return render_to_response('leros/activity/view.html', {'activity': activity}, context_instance=RequestContext(request))
def add_activity(request):

    if request.method == 'POST':
        form = ActivityForm(request.POST)
        activity = form.save(False)
        activity.user = request.user
        activity.save()
        if activity:
            return redirect('/activity/edit/' + activity.id + '/')
        else:
            return HttpResponse('Error')
    else:
        form = ActivityForm()
        return render_to_response('leros/activity/add.html', {'form': form}, context_instance=RequestContext(request))

def conditions(request):
    conditions = Condition.objects.filter(user=request.user).order_by('-time')

    paginator = Paginator(conditions, 25)

    page = 1
    if 'page' in request.GET:
        page = request.GET.get('page')

    try:
        conditions = paginator.page(page)
    except Exception, e:
        conditions = []

    return render_to_response('leros/condition/index.html', {'conditions': conditions}, context_instance=RequestContext(request))
