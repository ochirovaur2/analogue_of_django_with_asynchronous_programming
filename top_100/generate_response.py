import re
import sys
sys.path.append("../")
from main.views import *
from main.urls import *


def generate_body(code, url):
	if code == 404:
		return '<h1>404</h1><p>Not found</p>'
	if code == 405:
		return '<h1>405</h1><p>Method not allowed</p>'
		return '{"a": "1"}'

	return URLS[url]


def generate_headers(method, url):
	if not method == 'POST':
		return ('HTTP/1.1 405 Method not allowed\n\n', 405)

	if not url in URLS:
		return ('HTTP/1.1 404 Not found\n\n', 404)

	return ('HTTP/1.1 200 OK\n\n', 200)


def parse_request(request):
	
	parsed = request.split(' ')
	method = parsed[0]
	url = parsed[1]

	body = re.search(r'{.+}', str(request))
	try:
		return (method, url, body.group(0))
	except:
		return (method, url, '{}')


def generate_response(request):
	method, url, req_body = parse_request(request)
	headers, code = generate_headers(method, url)
	
	body = generate_body(code, url)
	
	return (headers + str(body(req_body))).encode()