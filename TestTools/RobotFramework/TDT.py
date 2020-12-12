import requests

class TDT:

	tdt_server = None

	def __init__(self, uri="http://localhost"):
		global tdt_server
		if len(uri)>0:
			tdt_server = uri

	def tdt_send_value(self, table, column, value):
		print(tdt_server + "/" + table + "/" + column )
		response = requests.put(tdt_server + "/" + table + "/" + column + "/" + value)
		print(response)
		return response.status_code

	def tdt_send_value_unique(self, table, column, value):
		print(tdt_server + "/" + table + "/" + column )
		response = requests.get(tdt_server + "/" + table + "/" + column + "/all")
		if (response.status_code == 200):
			json=response.json()
			print(json)
			values = [row['value'] for row in json[column]]
			print(values)
			if value not in values:
				response = requests.put(tdt_server + "/" + table + "/" + column + "/" + value)
				print(response)
		else:
			response = requests.put(tdt_server + "/" + table + "/" + column + "/" + value)
			print(response)
		return response.status_code

	def tdt_get_value(self, table, column):
		print(tdt_server + "/" + table + "/" + column )
		response = requests.get(tdt_server + "/" + table + "/" + column)
		if (response.status_code == 200):
			json=response.json()
			if (json[column] == None):
				return ""
			else:
				return json[column]
		elif (response.status_code == 404):
			raise Exception("Column or Table does not exist")
		else:
			raise Exception(response)


	def tdt_send_row(self, table, data):
		print(tdt_server + "/" + table + "/row" )
		print(data)
		response = requests.post(tdt_server + "/" + table + "/row" , json=data)
		print(response)
		return response.status_code


	def tdt_get_row(self, table):
		print(tdt_server + "/" + table + "/row" )
		response = requests.get(tdt_server + "/" + table + "/row" )
		if (response.status_code == 200):
			json=response.json()
			if (table in json):
				return json[table]
			else:
				return None
		elif (response.status_code == 404):
			raise Exception("Table does not exist")
		else:
			raise Exception(response)

	def tdt_delete_column(self, table, column):
		print(tdt_server + "/" + table + "/" + column )
		response = requests.delete(tdt_server + "/" + table + "/" + column)
		print(response)
		return response.status_code

	def tdt_delete_table(self, table):
		print(tdt_server + "/" + table )
		response = requests.delete(tdt_server + "/" + table )
		print(response)
		return response.status_code
