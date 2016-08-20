import sys, os
import json
import logging
import re
import time
import datetime
from xml.etree import ElementTree as ET

# OS Path Hack to import modules from the common directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.insert(0, './common')

from Salesforce import SFDC
from utils import zapier_string_to_array, CSVify

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def login():
	sf_api = SFDC(
		user_name = os.environ['SFDC_USER'], 
		password = os.environ['SFDC_PASSWORD'], 
		token = os.environ['SFDC_TOKEN']
	)

	login_response = sf_api.login()
	log.debug("Login Response XML {}".format(login_response))
	login_response = ET.fromstring(login_response)
	log.debug("Login Response Dict {}".format(login_response))

	result_pre_text = '{http://schemas.xmlsoap.org/soap/envelope/}Body/{urn:partner.soap.sforce.com}loginResponse/{urn:partner.soap.sforce.com}result/{urn:partner.soap.sforce.com}'

	try:
		sessionId = login_response[0][0][0][4].text
		log.debug("SessionId {}".format(sessionId))
	except IndexError:
		log.debug("Failed Login")
		sys.exit("Error: Salesforce login information may be incorrect")

	instance = login_response.find(result_pre_text + 'metadataServerUrl').text
	instance = re.search('://(.*).salesforce.com', instance)
	instance = instance.group(1)
	log.debug("Instance: {}".format(instance))

	sf_api.setSession(instance, sessionId)
	log.debug("Login Success")
	return sf_api, instance, sessionId


# ---
# unique_emails()
# ---
# data: An array of usage objects
# emailkey: the key of the email value in each element of the data array
# ---
def unique_emails(data, emailkey):
	emails = []
	for event in data:
		try:
			if event.get(emailkey) not in emails:
				emails.append(event.get('ops_email_events.email'))
		except:
			print "Malformed Data"

	return emails

# ---
# add_events()
# ---
# data: An array of usage objects
# ---
def add_events(data):
	log.debug("Logging into Salesforce")
	sf_api, instance, sessionId = login()

	# fix the zapier json array
	data = zapier_string_to_array(data) 

	# Get Unique Emails for Contact Query
	unique_emails = unique_emails(data, 'ops_email_events.email')

	#Get Contacts From Salesforce Where Email is one of the unique emails
	log.debug("Retrieving SF Contacts")
	contacts = sf_api.query_contacts(unique_emails)
	sf_contacts = {}
	for contact in contacts:
		sf_contacts[contact['Email']] = contact['Id']

	log.debug("Found: {}".format(sf_contacts))

	#Get User Usage History Types
	log.debug("Retrieving SF Event Types")
	events = sf_api.query_usage_history_types()
	sf_events = {}
	for event in events:
		sf_events[event['Name']] = event['Id']

	log.debug("Found: {}".format(sf_events))

	#Instantiate the insert array
	user_usage_history_insert = []
	#Instantiate the mismatch array
	user_usage_history_mismatches = []


	#Merge data event with contact
	for datum in data:
		row = {}
		try:
			sf_contact_id = sf_contacts[datum.get('ops_email_events.email')]
			sf_event_id = sf_events[datum.get('ops_email_events.event_type')]
			unix_time = time.mktime(datetime.datetime.strptime(datum.get('ops_email_events.date'), "%Y-%m-%d").timetuple())
			row['Contact__c'] = sf_contact_id
			row['User_Usage_History_Event_Type__c'] = sf_event_id
			row['Event_Date_Created_UNIX__c'] = unix_time
			row['Count__c'] = datum.get('ops_email_events.total')
			user_usage_history_insert.append(row)
		except KeyError, e:
			log.debug("Key Error: {}".format(str(e)))
			user_usage_history_mismatches.append(datum)
		except:
			log.debug("Matching Error")

	#Log Bad Emails
	log.debug("Unmatched Emails: {}".format(user_usage_history_mismatches))



	object_to_update = "User_Usage_History__c"
	fields = {'Event_Date_Created_UNIX__c' : 'Event_Date_Created_UNIX__c', 'User_Usage_History_Event_Type__c': 'User_Usage_History_Event_Type__c', 'Contact__c': 'Contact__c', 'Count__c' : 'Count__c'}

	#Insert Into User Usage History Table
	log.debug("Creating SF Bulk Job")

	job_response = sf_api.create_job(instance, sessionId, 'insert', object_to_update, 'XML' )
	job_response = ET.fromstring(job_response)

	jobId = job_response[0].text


	#XMLify the JSON rows
	xml_object = sf_api.json_to_xml_rows(user_usage_history_insert, fields)
	log.debug("XML: {}".format(xml_object))

	batch = 0
	for xml_batch in xml_object.items():
		batch += 1
		log.debug(xml_batch[1])
		sf_api.add_batch(instance, sessionId, jobId, xml_batch[1])
		# print batch

	log.debug("Closing job")
	sf_api.close_job(instance, sessionId, jobId)


	return {"Response" : "Success!" }

