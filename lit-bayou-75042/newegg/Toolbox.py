import psycopg2.extras
import psycopg2
from django.db import models
from django.db import connection
from django.shortcuts import render
from django.shortcuts import redirect
import psycopg2
import time

class Toolbox():
	def __init__(self):
		self.company_name 		= "eggie"
		self.software_version 	= "1.0"
		self.location_upload_tracking_costs = '/home/administrator/d2i/file_exchange/update_tracking/upload/'
		self.location_upload_amazon_settlements = '/home/administrator/d2i/file_exchange/amazon_settlements/upload/'
		self.PG_SQL_Host = '35.188.226.163'
		self.PG_SQL_DB = 'postgres'
		self.PG_SQL_Name = 'postgres'
		self.PG_SQL_Pass = 'WNNX7GtZ'

	def make_Connection_PGSQL(self):
		connection = psycopg2.connect(
			host 		= self.PG_SQL_Host,
			database 	= self.PG_SQL_DB,
			user 		= self.PG_SQL_Name,
			password 	= self.PG_SQL_Pass
			)
		return connection

	def make_Cursor_PGSQL(self, PGSQL_connection):
		return PGSQL_connection.cursor()

	def make_Connection_MSSQL(self):
		connection  	= pymssql.connect(
			server 		= self.MS_SQL_Host,
			user 		= self.MS_SQL_Name,
			password 	= self.MS_SQL_Pass,
			database 	= self.MS_SQL_DB
			)
		return connection

	def make_Cursor_MSSQL(self, MSSQL_connection):
		return MSSQL_connection.cursor()

	def make_Cursor_PGSQL_dict(self, PGSQL_connection):
		return PGSQL_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

	def addNotification(self,uid,_type,message):
		notif_cursor = connection.cursor()
		addNote_query = """SELECT public.usp_add_user_notification(
			'{}','{}','{}!')""".format(uid,_type,message)
		try:
			notif_cursor.execute(addNote_query)
		except Exception as ex:
			print(str(ex))
			print("Notification could not be added.")
		notif_cursor.close()

	def getNotifications(self,uid):
		notif_cursor = connection.cursor()
		notifications_query="""SELECT
					v_notification_type
					,v_notification_value
					,to_char(v_dateadded, 'MM/DD/YYYY')
					,v_ui_element
				FROM public.usp_get_user_notification('{}')
				ORDER BY v_dateadded DESC""".format(uid)
		notif_cursor.execute(notifications_query)

		notifications=[]
		for notification_block in notif_cursor.fetchall():
			current_notification = {"Type":     notification_block[0]
									,"Message": notification_block[1]
									,"Date":    notification_block[2]
									,"ui_element":    notification_block[3]}
			notifications.append(current_notification)
		notif_cursor.close()
		return notifications

	def getStandardContext(self,request, User = None):
		#	GET MINIMAL CONTENT FOR ANY VISITOR
		context = {}
		context['company_name'] = self.company_name
		context['software_version'] = self.software_version
		#	GET STANDARD CONTEXT FOR A LOGGED IN USER
		if User is not None:
			context['email'] = request.session['user']
			auth_user_id = User.objects.get(username=request.session['user']).id
			context['auth_user_id'] = auth_user_id
			context['notifications'] = self.getNotifications(auth_user_id)
			context['user'] = User.objects.get(username=request.session['user'])
			user_group_list=None
			if len(context['user'].groups.all()) > 0:
				context['group'] = user_group_list[0]['name']
			else:
				context['group'] = ""
		return context

	def validateRequest(self,request, redirect_url = None):
		pass
		# if 'user' not in request.session or request.session['user'] is None:
		# 	return redirect("../login/")
		# if 'user' in request.session and request.session['user'] is not None:
		# 	if redirect_url is not None:
		# 		return redirect(redirect_url)
		# 	else:
		# 		return redirect('../profile/')
