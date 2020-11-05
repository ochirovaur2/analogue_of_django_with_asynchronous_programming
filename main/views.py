# encoding: utf-8
import json
from .top_100_rule import classify_top_100



def index(req):
	try:

		req = json.loads(req)
		
		ticket_desc = req["sum_desc"]
		ticket = req["ticket_num"]
		email = req['email']

		classify_top_100(ticket_desc, ticket, email)
	except:
		pass
	return 1