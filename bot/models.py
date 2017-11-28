from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Server(models.Model):
	"""Model class for server details"""
	name = models.CharField(max_length=50, unique=True)
	description = models.CharField(max_length=100, default='')
	ip = models.CharField(max_length=20, default= '')
	created = models.DateTimeField(auto_now=True)
	modified = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ('name',)


class Transaction(models.Model):
	"""Each interaction with target server is assumed
	a Transaction. Model class holds transaction details"""
	TR_TYPES = (
		('D', 'On Demand'),
		('A', 'Automatic'),
		)

	STATUSES = (
		('S', 'Success'),
		('F', 'Failure'),
		('U', 'Unknown'),
		)

	timestamp = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUSES, default='U')
	chat_id = models.IntegerField(default=0)
	tr_type = models.CharField(max_length=10, choices=TR_TYPES, default='A')
	server = models.ForeignKey(Server)
	
	def __str__(self):
		return str(self.id)

	class Meta:
		ordering = ('timestamp',)

class Errorlog(models.Model):
	transaction = models.ForeignKey(Transaction)
	description = models.CharField(max_length=500, default='')

	def __str__(self):
		return str(self.id)

