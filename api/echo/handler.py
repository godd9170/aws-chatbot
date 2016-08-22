from __future__ import print_function

import json
from urlparse import parse_qs
import logging


log = logging.getLogger()
log.setLevel(logging.DEBUG)

def handler(event, context):
	log.debug("Received event {}".format(json.dumps(event)))
	params = parse_qs(event['body'])

	try: 
		user = params['user_name'][0]
		command = params['command'][0]
		channel = params['channel_name'][0]
		command_text = params['text'][0]
	except:
		log.debug("Bad Params")

	response = {}
	response['response_type'] = "in_channel"
	response['text'] = "Hello {}".format(user)


	return response