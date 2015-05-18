from tastypie.resources import ModelResource
from qi.models import *
from tastypie.resources import Resource
from tastypie.bundle import Bundle
from tastypie import fields
from provider.constants import READ, WRITE, READ_WRITE
from tastypie_oauth.authentication import OAuth20Authentication
from tastypie.authorization import DjangoAuthorization
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

    class Meta:
        queryset = Qi.objects.all().order_by('-time')
        resource_name = 'me/qis'
        authorization = DjangoAuthorization()
        authentication = OAuth20Authentication()
        filtering = {
            'account': ALL_WITH_RELATIONS,
        }
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)
    
    def obj_create(self, bundle, **kwargs):
        return super(QiResource, self).obj_create(bundle, user=bundle.request.user)
    
    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle

class TransactionResource(CORSModelResource):
    id = fields.CharField(attribute='id')
    qis = fields.ToManyField('qi.api.QiResource', 'qi_set', full=True)
    class Meta:
        queryset = Transaction.objects.all().order_by('-time')
        resource_name = 'me/transactions'
        authorization = DjangoAuthorization()
        authentication = OAuth20Authentication()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)
    
    def obj_create(self, bundle, **kwargs):
        return super(QiResource, self).obj_create(bundle, user=bundle.request.user)
    
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
        return super(QiAccountResource, self).obj_create(bundle, user=bundle.request.user)

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
        authorization = DjangoAuthorization()
        authentication = OAuth20Authentication()

class CurrencyResource(CORSModelResource):
    id = fields.CharField(attribute='id')

    class Meta:
        queryset = Currency.objects.all()
        resource_name = 'currencies'
        authorization = DjangoAuthorization()
        authentication = OAuth20Authentication()
