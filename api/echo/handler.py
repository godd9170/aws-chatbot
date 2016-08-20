from __future__ import print_function

import json
import logging


log = logging.getLogger()
log.setLevel(logging.DEBUG)

def handler(event, context):
	log.debug("Received event {}".format(json.dumps(event)))

	response = {'success' : 'true'}
	# if event.get('method') == 'POST':
	# 	try:
	# 		response['Success'] = "Nice"
	# 	except:
	# 		response['Error'] = "Invalid"
	# else:
	# 	response['Error'] = "Invalid"
	return response