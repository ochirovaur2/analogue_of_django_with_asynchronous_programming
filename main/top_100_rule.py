# encoding: utf-8
import json
import sys
import re
sys.path.append("../../")
from utilies_dir import  jira_class, passwords


def classify_top_100(ticket_desc, ticket, email):
	# Load classes
	Jira = jira_class.get_class()
	
	# passwords of Jira Rest Api and Jira DB

	passwords_ = passwords.get_passwords()

	### load top_100 contracts and emails domains


	

	jira = Jira(passwords_['jira_rest_api']["user"], passwords_['jira_rest_api']["password"], passwords_['jira_db_production'])


	### get contracts from description 

	emails_and_contracts = jira.get_emails_and_contracts(ticket_desc)

	contracts = emails_and_contracts[1]

	## get domain from email
	domain = re.findall(r'@([a-z\d-]+)\.([a-z\d-]+)(\.[a-z\d-]+)?$', email.lower())

	domain = domain[0][0]


	## open top 100 contracts and email domains

	with open('../utilies_dir/top_100.json', encoding='utf-8') as f:
		file_content = f.read()
		top_100 = json.loads(file_content)

	# check if domain or contract in top 100


	top_100_flag = False

	if domain in top_100["email_domains"]:
		top_100_flag = True
		
	for contract in contracts:
		
		if contract.upper() in top_100["contracts"]:
			top_100_flag = True
			

	if top_100_flag:
		jira.update_priority("Critical", ticket)
		jira.append_label(ticket, "топ100")	

	return 1