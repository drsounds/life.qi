from django.shortcuts import render_to_response, get_object_or_404
from django.template import *
from django.views.generic import *
from accounting.models import *
import random
# Create your views here.
def dashboard(request):
    accounts = []
   
    accounts = Account.objects.filter(user=request.user, currency=Currency.objects.get(id='SEK'))
  
    return render_to_response('accounting/dashboard.html', {'accounts': accounts}, context_instance=RequestContext(request))

