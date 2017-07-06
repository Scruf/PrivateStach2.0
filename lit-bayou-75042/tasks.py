from __future__ import absolute_import
import django


import os, pandas, uuid, json
import celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Repricer.settings')
django.setup()
from django.conf import settings
from django.db import IntegrityError
from django.core.mail import send_mail
from newegg import models
from django.contrib.auth.models import User
from datetime import datetime
from ftplib import FTP
import logging
import csv

app = celery.Celery('tasks', backend='amqp', broker='amqp://fklrqsha:bI7dlKewJWG4iUrc43q4sCl7YyP4LEXp@clam.rmq.cloudamqp.com/fklrqsha')

@app.task
def send_email(self, send_to):
	print('sending')
	logging.basicConfig()
	logging.getLogger().setLevel(logging.INFO)
	send_mail("welcome","eggie","christianling917@gmail.com",[send_to],fail_silently=False)

@app.task
def file_upload(self, documentName, username, document,uuid_up):
	#cut here
	user=User.objects.get(username=username)
	doc=models.Document.objects.get(document='newegg/files/'+username+'_'+document)
	#KeyErrorprint("Uploading file %s"%str(document))
	pExcel=pandas.ExcelFile(doc.document)
	DataFrame = pExcel.parse(sheetname=0)
	datam=[]
	for data in DataFrame.to_dict(orient='records'):
		# data = data.update({'usename':username})
		data.update({'username':username})
		saving=True
		try:
			product = models.Product(seller_number = data['Seller Part #'], \
				 in_stock=True,\
				title = data['Title'], shipment=data['Shipping'],\
				country = data['Country'], currency = data['Currency'],\
				msrp = float(data['MSRP'].replace(',','')),\
				selling_price = float(data['Selling Price'].replace(',','')),\
				quantity = data['SBS Inventory'], is_active = False,\
				fullfilment_option = data['Fulfillment Option'],\
				client = User.objects.get(username=username))
			newegg_item_number = data['NE Item #']
			user=User.objects.get(username=username)
			if models.Product.objects.filter(client_id=user.id,newegg_item_number=newegg_item_number).exists():
				saving=False
			else:
				product.newegg_item_number=newegg_item_number
		except KeyError as key:
			saving=False
		if saving:
			product.save()
		dictionary={}
		for keys in data.keys():
			if pandas.isnull(data[keys]):
				dictionary[keys]=''
			else:
				dictionary[keys]=data[keys]
				
		#product.save()#uncomment this later. also save the datam
				#file_manager.upload(data)
		datam.append(dictionary)
		user=User.objects.get(username=username)
		client=models.Client.objects.get(user_id=user.id)
				
		ftp = FTP('23.229.228.132')#, 'eggie_files@bridgecloud.co', 'ea@TC@ew#oW')
		ftp.login(user = 'eggie_files@bridgecloud.co', passwd = 'ea@TC@ew#oW,')
		#ftp.connect()
		ftp.storbinary('STOR '+str(document)+uuid_up,open('newegg/files/'+username+'_'+document,'rb'))
		ftp.quit()
		with open('./newegg/files/'+str(username)+'_'+uuid_up+'.json', 'w') as outfile:
			json.dumps(datam, outfile)
			#stop cutting
	if saving:
		return {
			'status':200,
			'message':'your file '+document+', was uploaded successfully',
		}
	else:
		return {
				'status':400,
				'message':'your file '+document+' contains an error.',
			}

