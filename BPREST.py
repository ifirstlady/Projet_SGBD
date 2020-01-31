from flask import Flask
import json as simplejson
from flask_restful import Resource,Api
from flask_restful import reqparse
import os
import BlackPearlDB
import test

app= Flask(__name__)
api= Api(app)
parser = reqparse.RequestParser()


@app.route("/")


class Authentication(Resource):
	def get(self):
		return "For getting authenticated, make a form to give your Login and password by that way: blackpearldb -u login -p password. You have to get authenticated before anything."
	def post(self):
		global authentif
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('authentication', type=str, help='Authentication command')
			args = parser.parse_args()
			authentication = args['authentication']
			authentif = BlackPearlDB.authentification(authentication)
			return authentif

		except Exception as e:
				return {'error': str(e)}

class CreateUser(Resource):
	def get(self):
		return "To create a user, make a formular to enter the login and the password"
	def post(self):
		try: 
			parser = reqparse.RequestParser()
			parser.add_argument('login',type=str,help='User Login')
			parser.add_argument('password',type=str, help='User password')
			parser.add_argument('database',type=str,help='database to choose')
			args = parser.parse_args()
			login = args['login']
			password = args['password']
			database = args['database']
			chaine = ""
			chaine+="create "+"user "+login+" "+password
			print(chaine)
			return BlackPearlDB.create(chaine,database)

		except Exception as e:
				return {'error': str(e)}				

class CreateDatabase(Resource):
	def get(self):
		return "To create database, make a form to enter the name of the database."
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('database',type=str,help='The database name')
			args = parser.parse_args()
			database = args['database']
			chaine = ""
			chaine+="create "+"database "+database
			return BlackPearlDB.create(chaine,database)

		except Exception as e:
				return {'error': str(e)}				
	
class CreateTable(Resource):
	def get(self):
		return  "Make a form to create table in a database. One form per table"
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('database',type=str,help='database name')
			parser.add_argument('table',type=str,help='table name')
			args = parser.parse_args()
			database =args['database']
			table=args['table']
			chaine = ""
			chaine+="create "+"table "+table
			return BlackPearlDB.create(chaine,database)

		except Exception as e:
				return {'error': str(e)}

class DropDatabase(Resource):
	def get(Ressource):
		return "To drop database, make a form to enter the name of the database."
	def post(Ressource):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('database',type=str,help='Le nom de la base de donnees')
			args = parser.parse_args()
			database=args['database']
			chaine = ""
			chaine+="drop "+"database "+database
			return BlackPearlDB.drop(chaine,database)
					
		except Exception as e:
			return {'error': str(e)}

class DropTable(Resource):
	def get(Ressource):
		return "To drop table, make a form to enter the name of the table and its database."
	def post(Resource):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('database',type=str,help='database name')
			parser.add_argument('table',type=str,help='table name')
			args = parser.parse_args()
			database=args['database']
			table=args['table']
			chaine = ""
			chaine+="drop "+"table "+table
			return BlackPearlDB.drop(chaine,database)
					
		except Exception as e:
			return {'error': str(e)}

class AlterDatabase(Resource):
	def get(Ressource):
		return "To drop table, make a form to enter the name of the table and its database."
	def post(Resource):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('database',type=str,help='database name')
			parser.add_argument('New_Name',type=str,help='table name')
			args = parser.parse_args()
			database=args['database']
			New_Name=args['New_Name']
			chaine = ""
			chaine+="alter "+"database "+database+" "+"name="+New_Name
			return BlackPearlDB.alter(chaine,database)
			
		except Exception as e:
			return {'error': str(e)}

class AlterTable(Resource):
	def get(Ressource):
		return "To drop table, make a form to enter the name of the table and its database."
	def post(Resource):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('database',type=str,help='database name')
			parser.add_argument('table',type=str,help='table name')
			parser.add_argument('New_Name',type=str,help='table name')
			args = parser.parse_args()
			database=args['database']
			table=args['table']
			New_Name=args['New_Name']
			chaine = ""
			chaine+="alter "+"table "+table+" "+"name="+New_Name
			return BlackPearlDB.alter(chaine,database)
			
		except Exception as e:
			return {'error': str(e)}

class Insert(Resource):
	def get(Resource):
		return "To insert in a table, make a form to enter the information of the table."
	def post(Resource):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('database',type=str,help='database name')
			parser.add_argument('table',type=str,help='table name')
			parser.add_argument('attributes',type=str,help='table name')
			args = parser.parse_args()
			database=args['database']
			table=args['table']
			attributes=args['attributes']
			chaine = ""
			chaine+="insert "+"into "+table+" values "+attributes
			return test.insert(chaine,database)
			
		except Exception as e:
			return {'error': str(e)}

class Update(Resource):
	def get(Resource):
		return "To update a table, make a form to enter the information to update."
	def post(Resource):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('database',type=str,help='database name')
			parser.add_argument('table',type=str,help='table name')
			parser.add_argument('attribute',type=str,help='table name')
			parser.add_argument('new_value',type=str,help='table name')
			parser.add_argument('attribute_index',type=str,help='table name')
			parser.add_argument('value_index',type=str,help='table name')
			args = parser.parse_args()
			database=args['database']
			table=args['table']
			attribute = args['attribute']
			new_value=args['new_value']
			attribute_index = args['attribute_index']
			value_index = args['value_index']
			chaine = ""
			chaine+="update "+table+" set "+attribute+"="+new_value+" where "+attribute_index+"="+value_index
			return BlackPearlDB.update(chaine,database)
			
		except Exception as e:
			return {'error': str(e)}

class Delete(Resource):
	def get(Resource):
		return "To delete table, make a form to enter the information to delete."
	def post(Resource):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('database',type=str,help='database name')
			parser.add_argument('table',type=str,help='table name')
			parser.add_argument('attribute_index',type=str,help='table name')
			parser.add_argument('value_index',type=str,help='Valeur indiquant le tuple à supprimer')
			args = parser.parse_args()
			database=args['database']
			table=args['table']
			attribute_index=args['attribute_index']
			value_index=args['value_index']
			chaine = ""
			chaine+="delete "+"data "+"from "+table+" where "+attribute_index+"="+value_index
			return BlackPearlDB.delete(chaine,database)
			
		except Exception as e:
			return {'error': str(e)}

class Select(Resource):
	def get(Resource):
		return "To select information in a table, make a form to indicate them."
	def post(Resource):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('database',type=str,help='database name')
			parser.add_argument('table',type=str,help='table name')
			parser.add_argument('information',type=str,help='table name')
			args = parser.parse_args()
			database=args['database']
			table=args['table']
			information = args['information']
			chaine = ""
			chaine+="select "+information+" from "+table
			return BlackPearlDB.select(chaine,database)
			
		except Exception as e:
			return {'error': str(e)}

class Show(Resource):
	def get(Resource):
		return "To all tables or all databases, make a form to what you want to be showed."
	def post(Resource):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('show',type=str,help='database name')
			parser.add_argument('database',type=str,help='database name')
			args = parser.parse_args()
			database = args['database']
			show = args['show']
			chaine = ""
			chaine+="show "+show
			return BlackPearlDB.show(chaine,database)
			
		except Exception as e:
			return {'error': str(e)}
	
								
api.add_resource(DropDatabase, '/DropDatabase')
api.add_resource(DropTable, '/DropTable')
api.add_resource(CreateTable,'/CreateTable')
api.add_resource(CreateDatabase,'/CreateDatabase')
api.add_resource(CreateUser, '/CreateUser')
api.add_resource(Authentication,'/Authentication')
api.add_resource(AlterDatabase,'/AlterDatabase')
api.add_resource(AlterTable,'/AlterTable')
api.add_resource(Insert, '/Insert')
api.add_resource(Update, '/Update')
api.add_resource(Delete, '/Delete')
api.add_resource(Show, '/Show')
if __name__ == "__main__":
	app.run(port=8889, debug=True)