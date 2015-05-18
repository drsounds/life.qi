from tastypie.resources import ModelResource
from qi.models import *
from tastypie.resources import Resource
from tastypie.bundle import Bundle
from tastypie import fields
from provider.constants import READ, WRITE, READ_WRITE
from tastypie_oauth.authentication import OAuth2ScopedAuthentication, OAuth20Authentication
from tastypie.authorization import DjangoAuthorization, Authorization
from qi.cors import *
from django.conf.urls import patterns, include, url
from django.core.paginator import Paginator, InvalidPage
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.http import Http404
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
class DashboardResource(BaseCorsResource):
    pass
class QiResource(CORSModelResource):
    id = fields.CharField(attribute='id')
    account = fields.ForeignKey('qi.api.AccountResource', 'account', full=True, null=True)
    currency = fields.ForeignKey('qi.api.CurrencyResource', 'currency', full=True)
    transaction = fields.ForeignKey('qi.api.TransactionResource', 'transaction', full=False)
    class Meta:
        queryset = Qi.objects.all().order_by('-time')
        resource_name = 'me/qis'
        authorization = Authorization()
        authentication = OAuth20Authentication()
        filtering = {
            'account': ALL_WITH_RELATIONS,
        }
        list_allowed_methods = ['get', 'post', 'put']
        detail_allowed_methods = ['get', 'put']
        always_return_data = True

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)
    
    def obj_create(self, bundle, **kwargs):
        return super(QiResource, self).obj_create(bundle, user=bundle.request.user)
    
    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle

class TransactionResource(CORSModelResource):
    id = fields.CharField(attribute='id')
    qis = fields.ToManyField('qi.api.QiResource', 'qi_set', full=True, null=True)
    name = fields.CharField()
    text = fields.CharField()
    class Meta:
        queryset = Transaction.objects.all().order_by('-time')
        resource_name = 'me/transactions'
        authorization = Authorization()
        authentication = OAuth20Authentication()
        list_allowed_methods = ['get', 'post', 'put']
        detail_allowed_methods = ['get', 'put', 'post']
        always_return_data = True

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)
    
    def obj_create(self, bundle, **kwargs):
        return super(TransactionResource, self).obj_create(bundle, user=bundle.request.user)
    
    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle

class AccountResource(CORSModelResource):
    id = fields.CharField(attribute='id')
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/transactions%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_transactions'), name="api_get_transactions"),
        ]

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)
    
    def obj_create(self, bundle, **kwargs):
        return super(AccountResource, self).obj_create(bundle, user=bundle.request.user)

    def get_transactions(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        account_id = kwargs['pk']
        qi_resource = QiResource()

        return qi_resource.get_list(request, filters={
            'account': account_id
        })

    def dehydrate(self, bundle):
        return bundle

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle

    class Meta:
        queryset = Account.objects.all().order_by('name')
        resource_name = 'me/accounts'
        authorization = Authorization()
        authentication = OAuth20Authentication()
        list_allowed_methods = ['get', 'post', 'put']
        detail_allowed_methods = ['get', 'put']
        always_return_data = True

class CurrencyResource(CORSModelResource):
    id = fields.CharField(attribute='id')

    class Meta:
        queryset = Currency.objects.all()
        resource_name = 'currencies'
        authorization = Authorization()
        authentication = OAuth20Authentication()
        always_return_data = True
