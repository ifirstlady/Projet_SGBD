import sys
import json as simplejson
import os

def replace(chaine):
	chaine1=""
	j=0
	for i in range(0,len(chaine)):
		if chaine[i] == " ": 
			if chaine[i-1] == " " or chaine[i-1] == "," or chaine[i-1] == "=" or chaine[i+1] == "," or chaine[i+1] == "=" or chaine[i+1] == "(" or i==0:
				pass
			else:
				chaine1+="#" 
		else:
			if chaine[i] !="(":
				chaine1+=chaine[i]
		if chaine[i] == "(":
				chaine1 += "#("	
	return chaine1

def authentification(chaine):
	chaine = replace(chaine)
	elements = chaine.split("#");
	if len(elements) < 5:
		return "\n___________SYNTAX ERROR___________\n"
	if elements[0].upper() == "BLACKPEARLDB" and elements[1] == "-u":
		if elements[3] == "-p":
			if len(elements) > 4:
				user = elements[2]
				password = elements[4]
				auth = Check(user,password)
				return auth
			else:
				return "\n___________SYNTAX ERROR___________\n"
		if elements[3] != "-p":
			return "\n___________SYNTAX ERROR___________\n"
	else:
		return "\n___________SYNTAX ERROR___________\n"

def Check(user,password):
	with open("data/users.json","r") as f :
		chaine = f.read()
	if chaine[0] != "[":
		chaine = "["+chaine+"]"
	liste = simplejson.loads(chaine)
	verif = False
	for dict in liste:
		if dict["id"] == user:
			if dict["password"] == password:
				verif = True
				break
	if verif == True:
		return "\n___________CONNECTED___________\n"
	else:
		return "\n___________NOT CONNECTED___________\n"
	f.close()

#LDD
def create(chaine,database):
	chaine = replace(chaine)
	elements = chaine.split("#");

	#CREATING A database
	if elements[1].upper() == "DATABASE":
		if len(elements) < 3:
			return "\n___________SYNTAX ERROR___________\n"
		if os.path.exists("data/"+elements[2]+".json"):
			return "\n___________DATABASE ALREADY EXISTS___________\n"
		else:
			with open("data/"+elements[2]+".json","w") as f:
				f.write('')
			f.close()
			return "\n___________DATABASE CREATED___________\n"

	#CREATING A TABLE
	if elements[1].upper() == "TABLE":
		if len(elements) < 3:
			return "\n___________SYNTAX ERROR___________\n"
		if database == "":
			return "\n___________NO DATABASE SELECTED___________\n"
		with open("data/"+database+".json","r") as f:	
			size = os.path.getsize("data/"+database+".json")
			if size == 0:
				liste = {}
			else:
				liste = simplejson.load(f)
				for dict in liste:
					if dict == elements[2]:
						return "\n___________TABLE ALREADY EXISTS___________\n"
		liste[elements[2]] = []
		with open("data/"+database+".json","w") as g:
			simplejson.dump(liste,g,indent = 4)
		f.close()
		g.close()
		return "\n___________TABLE CREATED___________\n"

	#CREATING AN USER
	if elements[1].upper() == "USER":
		if len(elements) < 4:
			return "\n___________SYNTAX ERROR Userr___________\n"
		login = elements[2]
		password = elements[3]
		with open("data/users.json","r") as f :
			chaine = f.read()
			if chaine[0] != "[":
				chaine = "["+chaine+"]"
			liste = simplejson.loads(chaine)
		f.close()
		exist = False
		for dict in liste:
			if dict["id"] == login:
				if dict["password"] == password:
					exist = True
					break
		if exist == True:
			return "\n___________USER ALREADY EXISTS___________\n"
		liste.append({"id":login,"password":password})
		with open("data/users.json","w") as g:
			simplejson.dump(liste,g,indent =4)
		g.close()
		return "\n___________USER CREATED___________\n"
	else:
		return "\n___________SYNTAX ERROR User___________\n"

def drop(chaine,database):
	chaine = replace(chaine)
	elements = chaine.split("#")
	if len(elements) < 3:
		return "\n___________SYNTAX ERROR___________\n"
	#DROPPING A database
	if elements[1].upper() == "DATABASE":
		if os.path.exists("data/"+elements[2]+".json"):
			os.remove("data/"+elements[2]+".json")
			return "\n___________DATABASE DELETED___________\n"
		else:
			return "\n___________DATABASE DOES NOT EXISTS___________\n"
	#DROPPING A TABLE
	if elements[1].upper() == "TABLE":
		if database == "":
			return "\n___________NO DATABASE SELECTED___________\n"
		with open("data/"+database+".json","r") as f:	
			size = os.path.getsize("data/"+database+".json")
			if size == 0:
				return "\n___________DATABASE EMPTY___________\n"
			else:
				exist = False
				liste = simplejson.load(f)
				for dict in liste:
					if dict == elements[2]:
						del liste[dict]
						exist = True
						break
			if exist == False:
				return "\n___________TABLE DOES NOT EXISTS___________\n"
		with open("data/"+database+".json","w") as g:
			simplejson.dump(liste,g,indent = 4)
		f.close()
		g.close()
		return "\n___________TABLE DELETED___________\n"
	else:
		return "\n___________SYNTAX ERROR___________\n"

def alter(chaine,database):
	chaine = replace(chaine)
	elements = chaine.split("#")
	if len(elements) < 4 or elements[3].split("=")[0].upper() != "NAME":
		return "\n___________SYNTAX ERROR___________\n"
	new_name = elements[3].split("=")[1]

	#ALTERING A DATABASE
	if elements[1].upper() == "DATABASE":
		if os.path.exists("data/"+elements[2]+".json"):
			os.rename("data/"+elements[2]+".json","data/"+new_name+".json")
			return "\n___________DATABASE ALTERED___________\n"
		else:
			return "\n___________DATABASE DOES NOT EXISTS___________\n"

	#ALTERING A TABLE
	if elements[1].upper() == "TABLE":
		if database == "":
			return "\n___________NO DATABASE SELECTED___________\n"
		with open("data/"+database+".json","r") as f:	
			size = os.path.getsize("data/"+database+".json")
			if size == 0:
				return "\n___________DATABASE EMPTY___________\n"
			else:
				exist = False
				liste = simplejson.load(f)
				for dict in liste:
					if dict == elements[2]:
						dict = new_name
						exist = True
						break
			if exist == False:
				return "\n___________TABLE DOES NOT EXISTS___________\n"
		with open("data/"+database+".json","w") as g:
			simplejson.dump(liste,g,indent = 4)
		f.close()
		g.close()
		return "\n___________TABLE ALTERED___________\n"
	if elements[1].upper() != "DATABASE" and elements[1].upper() != "TABLE":
		return "\n___________SYNTAX ERROR___________\n"


#LMD
def insert(chaine,database):
	chaine = replace(chaine)
	elements = chaine.split("#")
	if len(elements) < 4 or elements[1].upper() != "INTO":
		return "\n___________SYNTAX ERROR___________\n"
	if database == "":
		return "\n___________NO DATABASE SELECTED___________\n"
	element = elements[4]
	tab = element.split("(")
	tab = tab[1].split(")")
	tab = tab[0].split(",")
	attr = []
	data = []
	for ch in tab:
		t = ch.split("=")
		attr.append(t[0])
		data.append(t[1])
	d = {}
	for i in range(0,len(attr)):
		d[attr[i]] = data[i]
	with open("data/"+database+".json","r") as f:	
		size = os.path.getsize("data/"+database+".json")
		if size == 0:
			liste = {}
		else:
			liste = simplejson.load(f)
			exist = False
			for dict in liste:
				if dict == elements[2]:
					exist =True
					t = []
					if not liste[dict]:
						liste[dict].append(d)
					else:
						for cle in liste[dict][0].keys():
							t.append(cle)
						if t == attr:
							liste[dict].append(d)
						else:
							return "\n___________INCORRECT ATTRIBUTE___________\n"
				if exist == False:
					return "\n___________TABLE DOES NOT EXISTS___________\n"
	with open("data/"+database+".json","w") as g:
		simplejson.dump(liste,g,indent = 4)
	f.close()
	g.close()
	return "\n___________INSERTION DONE___________\n"

def update(chaine,database):
	if database == "":
		return "\n___________NO DATABASE SELECTED___________\n"
	chaine = replace(chaine)
	elements = chaine.split("#")

	if len(elements) < 6 or elements[2].upper() != "SET" or elements[4].upper() != "WHERE":
		return "\n___________SYNTAX ERROR___________\n"
	with open("data/"+database+".json","r") as f:
		size = os.path.getsize("data/"+database+".json")
		if size == 0:
			return "\n___________DATABASE EMPTY___________\n"
		liste = simplejson.load(f)
		elem_ch = elements[3].split("=")[0]
		new_value = elements[3].split("=")[1]
		elem_ind =  elements[5].split("=")[0]
		value = elements[5].split("=")[1]
		exist = False
		for dict in liste:
			if dict == elements[1]:
				exist = True
				for i in range(0,len(liste[dict])):
					if liste[dict][i][elem_ind] == value:
						liste[dict][i][elem_ch] = new_value
		if exist == False:
			return "\n___________TABLE DOS NOT EXISTS___________\n"
	with open("data/"+database+".json","w") as g:
		simplejson.dump(liste,g,indent=4)
	return "\n___________UPDATE DONE___________\n"

def delete(chaine,database):
	if database == "":
		return "\n___________NO DATABASE SELECTED___________\n"
	chaine = replace(chaine)
	elements = chaine.split("#")

	if len(elements) < 6 or elements[1].upper() != "DATA" or elements[2].upper() != "FROM" or elements[4].upper() != "WHERE":
		return "\n___________SYNTAXE ERROR___________\n" 
	tab = elements[5].split(",")
	attr = []
	value = []
	for e in tab:
		attr.append(e.split("=")[0])
		value.append(e.split("=")[1])
	with open("data/"+database+".json","r") as f:
		size = os.path.getsize("data/"+database+".json")
		if size == 0:
			return "\n___________DATABASE EMPTY___________\n"
		liste = simplejson.load(f)
		exist = False
		for dict in liste:
			if dict == elements[3]:
				exist = True
				for e in liste[dict]:
					x=0
					verif = True
					while(x < len(attr) and verif==True):
						if e[attr[x]] == value[x]:
							x +=1
						else:
							verif=False
					if verif == True:
						liste[dict].remove(e)
		if exist == False:
			return "\n___________TABLE DOS NOT EXISTS___________\n"
	with open("data/"+database+".json","w") as g:
		simplejson.dump(liste,g,indent=4)
	return "\n___________DELETION DONE___________\n"

#LED
def select(chaine,database):
	if database == "":
		return "\n___________NO DATABASE SELECTED___________\n"
	chaine = replace(chaine)
	elements = chaine.split("#")

	if len(elements) < 4:
		return "\n___________SYNTAX ERROR___________\n"
	if elements[1] == "*":
		with open("data/"+database+".json","r") as f:
			liste = simplejson.load(f)
		exist = False
		attr_1 = []
		data_1 = []
		for dict in liste:
			if dict == elements[3]:
				exist =True
				d = liste[dict]
				for e in d:
					for attr,data in e.items():
						if attr in attr_1:
							pass
						else:
							attr_1.append(attr)
						data_1.append(data)
				attr_2 = ""
				data_2 = ""
				for e in attr_1:
					attr_2 +="|  "+e+"  |"
				for e in data_1:
					data_2 +="|  "+e+"  |"
				return attr_2+" --> "+data_2 
		if exist == False:
			return "\n___________TABLE DOES NOT EXISTS___________\n"
	else:
		attr_0= elements[1].split(",")
		with open("data/"+database+".json","r") as f:
			liste = simplejson.load(f)
		exist = False
		attr_1 = []
		data_1 = []
		for dict in liste:
			if dict == elements[3]:
				exist = True
				d = liste[dict]
				for e in d:
					for attr,data in e.items():
						if attr in attr_0:
							if attr in attr_1:
								pass
							else:
								attr_1.append(attr)
							data_1.append(data)		
				attr_2 = ""
				data_2 = ""
				for e1 in attr_1:
					attr_2 += "| "+e1+" |"
				for e2 in data_1:
					data_2 += "| "+e2+" |"
				return attr_2+" --> "+data_2 
		if exist == False:
			return "\n___________TABLE DOES NOT EXISTS___________\n"

#SHOWING DATA
def show(chaine,database):
	chaine = replace(chaine)
	elements = chaine.split("#")
	if len(elements) < 2:
		return "\n___________SYNTAX ERROR___________\n"
	if elements[1].upper() == "DATABASES": 
		dossier = os.listdir("data")
		ch = ""
		for chaine in dossier:
			ch+="|  "+chaine+"  |"
		return ch	
	else:
		if elements[1].upper() == "TABLES":
			if database == "":
				return "\n___________NO DATABASE SELECTED___________\n"
			with open("data/"+database+".json","r") as f:
				size = os.path.getsize("data/"+database+".json")
				if size == 0:
					return "\n___________SYNTAX ERROR___________\n"
				liste = simplejson.load(f)
				ch=""
				for dict in liste:
					ch+="|  "+dict+"  |"
				return ch
		else:
			return "\n___________SYNTAX ERROR___________\n"

#STOPPING THE PROGRAM
def quit():
	sys.exit(0)