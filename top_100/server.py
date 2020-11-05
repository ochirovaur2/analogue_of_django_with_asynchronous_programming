import socket
from select import select
from .generate_response import generate_response
from .settings import *

to_read = {}


def server(tasks):
	
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
	server_socket.bind(ADDR)
	print(f'Server start at: http://{ADDR[0]}:{str(ADDR[1])}')
	server_socket.listen()

	while True:
		
		yield ('read', server_socket)
		
		client_socket, addr = server_socket.accept()
		print(client_socket)
		if addr[0] in ALLOWED_HOSTS:
			print(f'Connection from: {addr[0]}')
			tasks.append(client(client_socket))
		else:
			print(f'Connection refused from: {addr[0]}')
			client_socket.close()


def client(client_socket):
	
	
	yield ('read', client_socket)

	full_request = ''

	while True:
		request = client_socket.recv(1024)

		if len(request) <= 0:
			break

		full_request += request.decode('utf-8')
	
	response = generate_response(full_request)
			
	client_socket.send(response)
		
	client_socket.close()
		

def runserver():
	tasks = []
	
	tasks.append(server(tasks))
	
	while True:
		
		while not tasks:
			
			ready_to_read, _, _ = select(to_read,[], [])
			
			for sock in ready_to_read:
				tasks.append(to_read.pop(sock))

		try:
		
			task = tasks.pop(0)
			
			reason, sock = next(task)
			
			if reason == 'read':
			
				to_read[sock] = task
			
		except StopIteration:
			print('Done')