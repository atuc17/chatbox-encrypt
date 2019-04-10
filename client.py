import socket
from threading import Thread
import sys
from aes import *
import threading
from ec import *
import random
import tkinter

if len(sys.argv) == 1:
	exit
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((sys.argv[1], 12345))
keys = []

# key = str(1234567812345678)
# share key
E, G = generate_curve()
p = E.p()
a = E.a()
b = E.b()
Gx = G.x()
Gy = G.y()
public_key = str(p) + " " + str(a) + " " + str(b) + " " + str(Gx) + " " + str(Gy)
sock.send(bytes(public_key, "utf-8"))

#recieve share key
nClient = random.random() * 100000
exchanged_key = sock.recv(1024).decode("utf-8").split(" ")
F, Q = gen_curve(int(exchanged_key[0]), int(exchanged_key[1]))
key = nClient * Q
#send Pb
pClient = nClient * G
Qx = pClient.x()
Qy = pClient.y()
keyClient = str(Qx) + " " + str(Qy)
sock.send(bytes(keyClient, "utf-8"))


aes_key = str(key.x() * key.y())
i = 0
while len(aes_key[i:]) != 16:
	i += 1
ex_key = bytes(aes_key[i:], "utf-8")
print(ex_key)
keys.append(ex_key)

def sendMsg(event=None):

	# while True:
		# if sock.recv(1024):
		#	print(sock.recv(1024).decode("utf-8"))
		# mess = input(">")
		# msg = bytes(mess, "utf-8")
		mess = my_msg.get()
		my_msg.set("")
		msg = bytes(mess, "utf-8")
		if msg == b"quit":
			sock.close()
			top.quit()
			return
		else:
			enc_msg = encrypt(msg, ex_key)
			sock.send(bytes(enc_msg, "utf-8"))
def listenMsg():
	key = str(1234567812345678)
	while True:
		msg = sock.recv(1024) #.decode("utf-8")
		dec_msg = decrypt(msg.decode("utf-8"), keys[0])
		if not msg:
			break
		# print(dec_msg)
		msg_list.insert(tkinter.END, bytes(dec_msg, "utf-8"))

top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", sendMsg)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=sendMsg)
send_button.pack()

# top.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = Thread(target=listenMsg)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
"""
thread1 = threading.Thread(target=sendMsg)
thread2 = threading.Thread(target=listenMsg)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
"""
sock.close()
