import os
import socket
import threading
import BlackPearlDB
from random import randint
import test
class ClientThread(threading.Thread):
    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
    def run(self):    
        print("Connected host: %s %s" % (self.ip, self.port, ))
        r = self.clientsocket.recv(2048)
        requete = r.decode()
        auth = BlackPearlDB.authentification(requete)
        self.clientsocket.send(auth.encode())
        if auth == "\n___________CONNECTED___________\n":
                database = ""
                base_init =""
                tampon = ""
                bloq = 0
                while 1:
                    receive = self.clientsocket.recv(2048)
                    requete = receive.decode()
                    requete = BlackPearlDB.replace(requete)
                    reqtab = requete.split("#")
    
                #CHOOSING A DATABASE
                    if reqtab[0].upper() == "USE":
                        if len(reqtab) < 2:
                            use = "\n___________SYNTAX ERROR___________\n" 
                        else:
                            temp = reqtab[1]
                            if os.path.exists("data/"+temp+".json"):
                                database = temp
                                use = "\n___________DATABASE CHANGED___________\n"
                            else:
                                use = "\n___________DATABASE DOES NOT EXISTS___________\n"
                        self.clientsocket.send(use.encode())
                #LDD
                    if reqtab[0].upper() == "CREATE":
                        if bloq == 1:
                            create = "\n___________NOT DISPONIBLE___________\n" 
                        else:
                            create = BlackPearlDB.create(requete,database)
                        self.clientsocket.send(create.encode())

                    if reqtab[0].upper() == "DROP":
                        if bloq == 1:
                            drop = "\n___________NOT DISPONIBLE___________\n"
                        else:
                            drop = BlackPearlDB.drop(requete,database) 
                        self.clientsocket.send(drop.encode())

                    if reqtab[0].upper() == "ALTER":
                        if bloq == 1:
                            alter = "\n___________NOT DISPONIBLE___________\n" 
                        else:
                            alter = BlackPearlDB.alter(requete,database)
                        self.clientsocket.send(alter.encode())

                #LMD
                    if reqtab[0].upper() == "INSERT":
                        insert = test.insert(requete,database)
                        self.clientsocket.send(insert.encode())

                    if reqtab[0].upper() == "UPDATE":
                        update = BlackPearlDB.update(requete,database)
                        self.clientsocket.send(update.encode())

                    if reqtab[0].upper() == "DELETE":
                        delete = BlackPearlDB.delete(requete,database)
                        self.clientsocket.send(delete.encode())

                #LED
                    if reqtab[0].upper() == "SELECT":
                        if bloq == 1:
                            select = "\n___________NOT DISPONIBLE___________\n" 
                        else:
                            select = BlackPearlDB.select(requete,database)
                        self.clientsocket.send(select.encode())

                #SHOWING DATA
                    if reqtab[0].upper() == "SHOW":
                        if bloq == 1:
                            show = "\n___________NOT DISPONIBLE___________\n"  
                        else:
                            show = BlackPearlDB.show(requete,database)
                        self.clientsocket.send(show.encode())
        
                #STOPPING THE PROGRAM
                    if reqtab[0].upper() == "QUIT":
                            if bloq == 1:
                                quit = "\n___________NOT DISPONIBLE___________\n"  
                            else:
                                quit ="\n___________GOOD BYE___________\n"
                            self.clientsocket.send(quit.encode())
    
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",8888))
while True:
    tcpsock.listen(3)
    print( "Listening...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()