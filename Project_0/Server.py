import sys
import socket

#Create Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind Socket to port
port = int(sys.argv[1])
server_socket.bind(('', port))

#Have socket listen
server_socket.listen(1)

#Accept client connection
c, address = server_socket.accept()

while True:
	#Get client message
	message = c.recv(1024)

	if not message:
		break

	#Decode, Edit, Encode & Send message
	edited_message = message.decode().swapcase()
	c.sendall(edited_message.encode())

#Close
c.close()
server_socket.close()
