import socket
from threading import Thread
import random
from aes import *
from ec import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = []
clients = {}
keys = {}
sock.bind(('0.0.0.0', 12345))
sock.listen(10)

def accept_connect():
	while True:
		client, client_address = sock.accept()
		connections.append(client)
		Thread(target=handle_message, args=(client, client_address)).start()

def handle_message(client, client_addr):
	# key = str(1234567812345678)

	# recieve public key
	public_key = client.recv(1024).decode("utf-8")
	numbers = public_key.split(" ")

	E, G = generate_curve()
	#send Pa
	nServer = random.random() * 100000
	pServer = nServer*G
	Px = pServer.x()
	Py = pServer.y()
	keyServer = str(Px) + " " + str(Py)
	client.send(bytes(keyServer, "utf-8"))
	# recieve Pa
	exchanged_key = client.recv(1024).decode("utf-8").split(" ")
	F, P = gen_curve(int(exchanged_key[0]), int(exchanged_key[1]))
	key = nServer * P
	aes_key = str(key.x() * key.y())
	i = 0
	while len(aes_key[i:]) != 16:
		i += 1
	ex_key = bytes(aes_key[i:], "utf-8")
	print(ex_key)
	print("welcome {0} to the chat\n".format(client_addr))
	# handle user name
	# client.send(b"Enter your name: \n")
	#name = client.recv(1024).decode("utf-8")

	keys[client] = ex_key

	while True:
		data = decrypt(client.recv(1024).decode("utf-8"), ex_key)
		if not data:
			break
		if data == b"quit":
			connections.remove(client)
			del keys[clinet]
		print(data)
		try:
			broadcast(bytes(data, "utf-8"))
		except:
			print("error")

def broadcast(msg):
	for connection in connections:
		enc_msg = encrypt(msg, keys[connection])
		connection.send(bytes(enc_msg, "utf-8"))

'''
t = Thread(target=accept_connect)
t.daemon = True;
t.start()
t.join()
'''
accept_connect()
sock.close()
