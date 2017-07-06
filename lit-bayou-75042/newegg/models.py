from django.db import models
from django.contrib.auth.models import User
import os
from datetime import datetime

class Client(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,db_column='auth_user_id')
	phone_number = models.CharField(max_length=12, default=False)
	client_id = models.IntegerField(default=0,db_column='id')
	seller_id = models.CharField(default=False,max_length=200,db_column='newegg_seller_id')
	authorization = models.CharField(default=False,max_length=200,db_column='newegg_authorization')
	referral_code = models.CharField(default=None,max_length=200,db_column='referral_code')
	newegg_secretkey = models.CharField(default=None, max_length=200,db_column='newegg_secretkey')
	commitment_time_hours = models.IntegerField(default=None,db_column='commitment_time_hours')

	class Meta:
		db_table = 'app_client'


class Product(models.Model):
	seller_number 		= models.CharField(max_length=100)
	newegg_item_number 	= models.CharField(max_length=100)
	title 				= models.CharField(max_length=500)
	country 			= models.CharField(max_length=10)
	currency 			= models.CharField(max_length=10)
	msrp 				= models.DecimalField(max_digits=100,decimal_places=2)
	quantity 			= models.IntegerField()
	selling_price 		= models.DecimalField(max_digits=100,decimal_places=2)
	is_active 			= models.BooleanField(default=False)
	in_stock 			= models.BooleanField(default=True)
	fullfilment_option 	= models.CharField(max_length=100)
	shipment 			= models.CharField(max_length=100)
	#for later, add eggie_strategy_id
	client 				= models.ForeignKey(User,on_delete=models.CASCADE)
	price_min 			= models.DecimalField(default=0.00, max_digits=18, decimal_places=2)
	price_max 			= models.DecimalField(default=0.00, max_digits=18, decimal_places=2)
	dateadded 			= models.DateTimeField(auto_now_add=True,db_column='dateadded')
	dateupdated 		= models.DateTimeField(auto_now_add=True,db_column='dateupdated')
	dateexpired 		= models.DateTimeField(default='5003-01-01 00:00',db_column='dateexpired')

	class Meta:
		db_table = 'app_product'

	def __str__(self):
		return self.newegg_item_number+" "+'$'+str(self.selling_price)+" "+self.title


def file_handler(instance, filename):
	path = 'newegg/files'
	username = User.objects.get(id=instance.client.user_id).username
	file_name = username + '_'+filename
	print("---------------------------")
	print(file_name)
	print("---------------------------")
	return os.path.join(path,file_name)

class Document(models.Model):
	description = models.CharField(max_length=255)
	document = models.FileField(upload_to=file_handler)
	upload_at = models.DateTimeField(auto_now_add=True)
	client = models.ForeignKey(Client,on_delete=models.CASCADE)

	class Meta:
		db_table = 'app_document'



# Create your models here.
