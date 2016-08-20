import json
import re
import time
import boto3
import requests
from botocore.client import Config
import csv

'''
Given Zapier's 'stringified' representation of a json array, returns a python
array of objects.

e.g. 
IN

ops_email_events.date: 2016-07-20\nops_email_events.email: 57captains@noburestaurants.com\nops_email_events.event_type: email.open\nops_email_events.total: 13\n\nops_email_events.date: 2016-07-11\nops_email_events.email: 57captains@noburestaurants.com\nops_email_events.event_type: email.open\nops_email_events.total: 15\n\n

OUT

[
	{
		"ops_email_events.date" : "2016-07-20",
		"ops_email_events.email" : "57captains@noburestaurants.com",
		"ops_email_events.event_type" : "email.open",
		"ops_email_events.total", 13
	},
	{
		"ops_email_events.date" : "2016-07-11",
		"ops_email_events.email" : "57captains@noburestaurants.com",
		"ops_email_events.event_type" : "email.open",
		"ops_email_events.total", 15
	},
]

'''
def zapier_string_to_array(data):
	output = []
	for datum in data.split('\n\n'):
		item = {}
		for field in datum.split('\n'):
			key, value = field.split(':')
			item[key.strip()] = value.strip()
		output.append(item)
	return output

class CSVify(object):
	def __init__(self, filename, header):
		self.filename = time.strftime("%d%m%Y") + filename
		self.header = header
		self.csvfile = None

	def write(self, rows):
		with open('/tmp/' + self.filename, 'wb') as csvfile:

			writer = csv.writer(csvfile, delimiter=',')
			writer.writerow(self.header)
			for row in rows:
				try:
					cells = []
					for column in row.keys():
						cells.append(row[column])
					writer.writerow(cells)
				except:
					print("----------- BAD LINE -----------")
		self.uploadS3()

	def uploadS3(self):
		if self.filename is not None:
			s3_client = boto3.client('s3', 'us-west-2', config=Config(s3={'addressing_style': 'path'}))
			print "Uploading %s to s3" % self.filename
			s3_client.upload_file('/tmp/' + self.filename, 'venga-usage', time.strftime("%d%m%Y") +'/' + self.filename)
		else:
			print "Please Write A CSV File First"