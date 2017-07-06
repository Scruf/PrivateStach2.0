from django.db import models, connection

class Helper():

	def __init__(self):
		pass

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
