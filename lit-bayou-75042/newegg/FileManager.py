'''
FileManager.py
'''

from pymongo import MongoClient
from datetime import datetime

class FileManager:

	def __init__(self):
		client = MongoClient('mongodb://heroku_w93nqzb3:8tfafs8i19ocoh3pkm2njdc880@ds151078.mlab.com:51078/heroku_w93nqzb3')
		self.db = client.heroku_w93nqzb3

	def upload(self, json_obj):
		print(json_obj)
		self.db.files.insert_one(json_obj)


if __name__ == '__main__':
	file = FileUploader()
	file.upload()
