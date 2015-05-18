from django.test import TestCase

# Create your tests here.
from provider.oauth2.models import Client, AccessToken
import datetime
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from qi.models import *
from qi.api import *
import json

def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           print( "obj.%s = %s" % (attr, getattr(obj, attr)))

class AccountResourceTest(ResourceTestCase):
	fixtures = ['test_entries.json']

	def setUp(self):
		super(AccountResourceTest, self).setUp()
		self.username = 'drsounds'
		self.password = 'pass'
		self.user = User.objects.create_user(self.username, 'drsounds@gmail.com', self.password)
		self.currency_yog, i = Currency.objects.get_or_create(id='YOG')
		self.currency_karma, i = Currency.objects.get_or_create(id='Karma')
		self.currency_yog.save()
		self.currency_karma.save()
		self.client = Client(client_type=0, redirect_uri='http', url='http://', name='Test client', user=self.user)
		self.client.save()

		self.account_1 = Account(user=self.user, currency=self.currency_yog, name='Test account 1', balance=0)
		self.account_1.save()
		
		self.account_2 = Account(user=self.user, currency=self.currency_karma, name='Music karma', balance=0)
		self.account_2.save()

		self.account_3 = Account(user=self.user, currency=self.currency_karma, name='Job account', balance=0)
		self.account_3.save()

		# Create test qi transactions

		self.transaction_1 = Transaction(user=self.user, name='Test transaction', text='Test transaction', amount=0, time=datetime.datetime.now())
		self.transaction_1.save()
		self.qi_1 = Qi(transaction=self.transaction_1, user=self.user, account=self.account_1, amount=-100, currency=self.currency_yog, balance=0, time=datetime.datetime.now(), text="Dr. Sounds")
		self.qi_1.save()
		self.qi_2 = Qi(transaction=self.transaction_1, user=self.user, account=self.account_2, amount=100, currency=self.currency_yog, balance=0, time=datetime.datetime.now(), text='dr. Sounds')
		self.qi_2.save()
		self.access_token = AccessToken(scope=6, user=self.user, token='test2', client=self.client, expires=datetime.datetime.now()  + datetime.timedelta(days=1))
		self.access_token.save()
		

	def get_credentials(self):
		return 'OAuth ' + self.access_token.token

	def test_get_account_list_json(self):
		resp = self.api_client.get('/qi/api/v1/me/accounts/', format='json', authentication=self.get_credentials())
		self.assertValidJSONResponse(resp)
		data = self.deserialize(resp)
		print json.dumps(data['objects'])

	def test_get_transaction_list_json(self):
		resp = self.api_client.get('/qi/api/v1/me/accounts/' + self.account_1.id + '/transactions/', format='json', authentication=self.get_credentials())
		print resp
		self.assertValidJSONResponse(resp)
		data = self.deserialize(resp)
		print json.dumps(data['objects'])

	def test_create_transaction(self):
		# Create new transaction
		
		resp = self.api_client.get('/qi/api/v1/me/accounts/', format='json', authentication=self.get_credentials())
		print resp
		self.assertValidJSONResponse(resp)
		data = self.deserialize(resp)
		primary_account = data['objects'][0]
		music_karma_account = data['objects'][1]
		job_account = data['objects'][2]

		resp = self.api_client.post('/qi/api/v1/me/transactions/', data={
			'name': 'Duva',
			'amount': 100,
			'text': '',	
			'currency': '/v1/currencies/YOG',
		}, format='json', authentication=self.get_credentials())
		print resp
		duva_transaction = self.deserialize(resp)

		qi_1 = self.api_client.post('/qi/api/v1/me/qis/', data={
			'name': 'Duva',
			'amount': -100,
			'transaction': '/v1/me/transactions/' + duva_transaction['id'] + '/',
			'account': '/v1/me/accounts/' + music_karma_account['id'] + '/',
			'currency': '/v1/currencies/YOG/',
		}, format='json', authentication=self.get_credentials())

		# self.assertValidJSONResponse(qi_1)
		data = self.deserialize(qi_1)

		qi_2 = self.api_client.post('/qi/api/v1/me/qis/', data={
			'name': 'Duva',
			'amount': 100,
			'transaction': '/v1/me/transactions/' + duva_transaction['id'] + '/',
			'account': '/v1/me/accounts/' + job_account['id'] + '/',
			'currency': '/v1/currencies/YOG',
		}, format='json', authentication=self.get_credentials())
		print qi_2
		# self.assertValidJSONResponse(qi_2)
		data = self.deserialize(qi_2)
"""
class APITest(TestCase):
	fixtures = ['test_entries.json']
	headers = {
		'Authorization': 'OAuth ' + self.access_token
	}
	def setUp(self):
		print "Logging in"
		client = Client.objects.all()[0]
		payload = {'grant_type': 'password', 'client_secret': client.client_secret, 'username': 'testuser', 'password': 'test123', 'client_id': client.client_id}
		response = requests.post('http://portal.aquajogging.se/oauth/access_token', data=payload)
		print response.text

		data = response.json()
		self.access_token = data['access_token']
		pass

	def test_list_accounts(self):
		
		r = requests.get('http://portal.aquajogging.se/api/v1/me/accounts', headers=self.headers)
		assert r.status_code == 200
		print r.text

	def test_get_first_account(self):
		r = requests.get('http://portal.aquajogging.se/api/v1/me/accounts/JAQqalilHdhpaeQqIrug2JIfg/', headers=self.headers)
		assert r.status_code == 200
		print r.text

	def test_get_first_account_transactions(self):
		r = requests.get('http://portal.aquajogging.se/api/v1/me/accounts/JAQqalilHdhpaeQqIrug2JIfg/transactions/', headers=self.headers)
		assert r.status_code == 200
		print r.text

	def test_get_general_transactions(self):
		r = requests.get('http://portal.aquajogging.se/api/v1/me/transactions', headers=headers)
		assert r.status_code == 200
		print r.text

	def test_add_account(self):
		return
		payload = {
			'name': 'test account',
			'amount': 0,
		}

		headers = {
			'Authorization': 'OAuth ' + self.access_token
		}
		r = requests.post('http://portal.aquajogging.se/qi/api/v1/me/accounts', payload=payload)
		assert r.status_code == 201
		print r.text
"""