from django.shortcuts import render_to_response, get_object_or_404
from qi.models import *
from django.template import *
from django.views.generic import *
# Create your views here.

def dashboard(request):
    qi_accounts = []
    try:
        qi_accounts = Account.objects.filter(user=request.user, currency=Currency.objects.get(id='YOG'))
    except Exception, e:
        print e
        qi_accounts = []

    karma_accounts = []
    try:
        karma_accounts = Account.objects.filter(user=request.user, currency=Currency.objects.get(id='Karma'))

    except:
        karma_accounts = []
    return render_to_response('qi/dashboard.html', {'qi_accounts': qi_accounts, 'karma_accounts': karma_accounts}, context_instance=RequestContext(request))

def account(request, id=None):
    account = None
    try:
        account = Account.objects.get(id=id, user=request.user)
    except:
        account = Account(user=request.user, currency=Currency.objects.get(id='YOG'), balance=0)
        account.save()
    
    transactions = []
    transactions = account.qi_set.order_by('-time')


    qis = Qi.objects.filter(account=account).order_by('-time')
    return render_to_response('qi/account/view.html', {'account': account, 'transactions': transactions}, context_instance=RequestContext(request))

class QiList(ListView):
    model = Qi
    context_object_name = 'qis'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(QiList, self).get_context_data(**kwargs)
        return context
    def get_queryset(self):
        self.account = get_object_or_404(Account, id=self.kwargs['id'])
        return Qi.objects.filter(account=self.account).order_by('-time')

class AccountList(ListView):
    model = Account
    context_object_name = 'accounts'

    def get_queryset(self):
        accounts = Account.objects.filter(user=self.request.user)
        return accounts