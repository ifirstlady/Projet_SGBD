import sys
import json as simplejson
import os
import BlackPearlDB

def insert(chaine,database):
	chaine = BlackPearlDB.replace(chaine)
	elements = chaine.split("#")
	if len(elements) < 4 or elements[1].upper() != "INTO":
		return "\n___________SYNTAX ERROR___________\n"
	tab = elements[4].split("(")
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
	if database == "":
		return "\n___________NO DATABASE SELECTED___________\n"
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