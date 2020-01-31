import socket
import BlackPearlDB

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(("", 8888))
requete = input("> ")
socket.send(requete.encode())
auth = socket.recv(2048)
auth = auth.decode()

print(auth)

if auth == "\n___________CONNECTED___________\n":
	bloq = 0
	while 1:
		requete = input("BlackPearlDB > ") 
		socket.send(requete.encode())
		response = socket.recv(2048)
		response = response.decode()
		requete = BlackPearlDB.replace(requete)
		saisie = requete.split("#")
		print(response)

		if saisie[0].upper() == "QUIT":
			print(response)
			BlackPearlDB.quit()