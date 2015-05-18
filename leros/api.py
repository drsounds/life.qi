from tastypie.resources import ModelResource
from leros.models import *
from tastypie.resources import Resource
from tastypie.bundle import Bundle
from tastypie import fields
from aquajogging.authenticate import OAuth20Authentication
from aquajogging.authorization import OAuth20Authorization
from tastypie.authorization import DjangoAuthorization
from aquajogging.api import BaseCorsResource
import datetime

class SportResource(BaseCorsResource):
    title = fields.CharField(attribute='name')
    id = fields.CharField(attribute='id')

    class Meta:
        queryset = Sport.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'sport'
        authorization = DjangoAuthorization()
        authentication = OAuth20Authentication()

class FacilityResource(BaseCorsResource):
    title = fields.CharField(attribute='name')
    id = fields.CharField(attribute='id')

    class Meta:
        queryset = Facility.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'facility'
        authorization = DjangoAuthorization()
        authentication = OAuth20Authentication()

class StatusResource(BaseCorsResource):
    title = fields.CharField(attribute='title')
    code = fields.CharField(attribute='code')
    class Meta:
        resource_name = 'status'
        object_class = Status
        queryset = Status.objects.all()
        authorization = OAuth20Authorization()
        authentication = OAuth20Authentication()


class ActivityResource(BaseCorsResource):
    name = fields.CharField(attribute='name')
    id = fields.CharField(attribute='id')
    class Meta:
        resource_name = 'activity'
        object_class = Activity
        authorization = OAuth20Authorization()
        authentication = OAuth20Authentication()

class BookingResource(BaseCorsResource):
    id = fields.CharField(attribute='id')
    status = fields.ForeignKey(StatusResource, 'status', null=True, full=True)
    class Meta:
        queryset = Booking.objects.all()
        resource_name = 'booking'
        authorization = OAuth20Authorization()
        authentication = OAuth20Authentication()
