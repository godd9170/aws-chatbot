from __future__ import print_function

import json
import logging
from eventsPOST import add_events

log = logging.getLogger()
log.setLevel(logging.DEBUG)

def handler(event, context):
	log.debug("Received event {}".format(json.dumps(event)))
	response = {}
	if event.get('method') == 'POST':
		try:
			data = event.get('body').get('attachment').get('data')
			response = add_events(data)
		except:
			response['Error'] = "Invalid Body: Please post json with 'body > attachment > data' hierarchy."
	else:
		response['Error'] = "Invalid Method"
	return response