

import signal
import os
import configparser
import argparse
import threading
import socket
import inspect

import time
from datetime import datetime

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer, HTTPServer
import urllib.parse
import json

# https://pypi.org/project/sqlite3worker/
# pip3 install sqlite3worker
from sqlite3worker import Sqlite3Worker





class TDT_WebServer(BaseHTTPRequestHandler):
	def do_HEAD(self):
		return

	def do_DELETE(self):
		actionfound = False
		httpcode = 500
		try:
			parsed_path = urllib.parse.urlparse(self.path)
			message = '{"path":"'+str(parsed_path)+'", "message": "Unsupported method"}'
			core.debugmsg(8, "parsed_path:", parsed_path)
			patharr = parsed_path.path.split("/")
			core.debugmsg(8, "patharr:", patharr)
			if not actionfound and len(patharr) == 2:
				actionfound = True
				# delete table
				tablename = urllib.parse.unquote_plus(patharr[1])
				core.debugmsg(9, "tablename:", tablename)

				deltbl = core.table_delete(tablename)

				if deltbl:
					httpcode = 200
					message = '{"message": "table '+tablename+' deleted"}'

				else:
					httpcode = 404
					message = '{"message": "table '+tablename+' does not exists"}'


			if not actionfound and len(patharr) == 3:
				actionfound = True
				# delete column
				tablename = urllib.parse.unquote_plus(patharr[1])
				core.debugmsg(9, "tablename:", tablename)
				columnname = urllib.parse.unquote_plus(patharr[2])
				core.debugmsg(9, "columnname:", columnname)

				delcol = core.column_delete(tablename, columnname)
				if delcol:
					httpcode = 200
					message = '{"message": "column '+columnname+' deleted"}'

				else:
					httpcode = 404
					message = '{"message": "column '+columnname+' does not exists"}'



			if not actionfound and len(patharr) == 4:
				actionfound = True
				# delete column
				tablename = urllib.parse.unquote_plus(patharr[1])
				core.debugmsg(9, "tablename:", tablename)
				columnname = urllib.parse.unquote_plus(patharr[2])
				core.debugmsg(9, "columnname:", columnname)
				columnvalue = urllib.parse.unquote_plus(patharr[3])
				core.debugmsg(9, "columnvalue:", columnvalue)

				delcol = core.value_delete(tablename, columnname, columnvalue)
				if delcol:
					httpcode = 200
					message = '{"message": "value '+columnvalue+' deleted"}'

				else:
					httpcode = 404
					message = '{"message": "value '+columnvalue+' does not exists"}'




		except Exception as e:
			core.debugmsg(6, "do_DELETE:", e)
			httpcode = 500
			message = str(e)
		self.send_response(httpcode)
		self.end_headers()
		self.wfile.write(bytes(message,"utf-8"))
		return


	def do_PUT(self):
		actionfound = False
		httpcode = 500
		try:
			parsed_path = urllib.parse.urlparse(self.path)
			message = '{"path":"'+str(parsed_path.path)+'", "message": "Unsupported method"}'
			core.debugmsg(8, "parsed_path:", parsed_path)
			patharr = parsed_path.path.split("/")
			core.debugmsg(8, "patharr:", patharr)

			if not actionfound and len(patharr) == 2:
				actionfound = True
				# create table
				tablename = urllib.parse.unquote_plus(patharr[1])
				core.debugmsg(9, "tablename:", tablename)

				tableid = core.table_exists(tablename)
				core.debugmsg(9, "tableid:", tableid)
				if tableid:
					httpcode = 200
					message = '{"message": "table '+tablename+' exists"}'
				else:
					tableid = core.table_create(tablename)
					core.debugmsg(9, "tableid:", tableid)
					if tableid:
						httpcode = 201
						message = '{"message": "table '+tablename+' created"}'


			if not actionfound and len(patharr) == 3:
				actionfound = True
				# create column
				tablename = urllib.parse.unquote_plus(patharr[1])
				core.debugmsg(9, "tablename:", tablename)
				columnname = urllib.parse.unquote_plus(patharr[2])
				core.debugmsg(9, "columnname:", columnname)

				columnid = core.column_exists(tablename, columnname)
				core.debugmsg(9, "columnid:", columnid)
				if columnid:
					httpcode = 200
					message = '{"message": "column '+columnname+' exists"}'
				else:
					columnid = core.column_create(tablename, columnname)
					core.debugmsg(9, "columnid:", columnid)
					if columnid:
						httpcode = 201
						message = '{"message": "column '+columnname+' created"}'


			if not actionfound and len(patharr) == 4:
				actionfound = True
				# append value to column
				tablename = urllib.parse.unquote_plus(patharr[1])
				core.debugmsg(9, "tablename:", tablename)
				columnname = urllib.parse.unquote_plus(patharr[2])
				core.debugmsg(9, "columnname:", columnname)
				columnvalue = urllib.parse.unquote_plus(patharr[3])
				core.debugmsg(9, "columnvalue:", columnvalue)

				valueid = core.value_create(tablename, columnname, columnvalue)
				core.debugmsg(9, "valueid:", valueid)
				if valueid:
					httpcode = 201
					message = '{"message": "value '+columnvalue+' added to column '+columnname+'"}'



		except Exception as e:
			core.debugmsg(6, "do_PUT:", e)
			httpcode = 500
			message = str(e)
		self.send_response(httpcode)
		self.end_headers()
		self.wfile.write(bytes(message,"utf-8"))
		return
	def do_POST(self):
		actionfound = False
		httpcode = 500
		try:
			parsed_path = urllib.parse.urlparse(self.path)
			message = '{"path":"'+str(parsed_path.path)+'", "message": "Unsupported method"}'
			core.debugmsg(8, "parsed_path:", parsed_path)
			patharr = parsed_path.path.split("/")
			core.debugmsg(8, "patharr:", patharr)

			content_len = int(self.headers.get('Content-Length'))
			core.debugmsg(8, "content_len:", content_len)
			post_body = self.rfile.read(content_len)
			core.debugmsg(8, "post_body:", post_body)

			if not actionfound and len(patharr) == 3:
				# create column
				tablename = urllib.parse.unquote_plus(patharr[1])
				core.debugmsg(9, "tablename:", tablename)
				columnname = urllib.parse.unquote_plus(patharr[2])
				core.debugmsg(9, "columnname:", columnname)

				if columnname == "row":
					actionfound = True
					tableid = core.table_exists(tablename)
					core.debugmsg(9, "tableid:", tableid)
					if tableid:
						# now parse the post data and check all the columns exist
						#
						data = json.loads(post_body)
						core.debugmsg(9, "data:", data)
						for col in data.keys():
							result = core.value_create(tablename, col, data[col])
							core.debugmsg(9, "result:", result)
							if not result:
								httpcode = 500
								message = '{"message": "unable to put value '+data[col]+' into column '+col+' of table '+tablename+'"}'

						httpcode = 201
						message = '{"message": "values added to table: '+tablename+'"}'


					else:
						httpcode = 404
						message = '{"message": "table '+tablename+' not found"}'

		except Exception as e:
			core.debugmsg(6, "Exception:", e)
			httpcode = 500
			message = str(e)
		self.send_response(httpcode)
		self.end_headers()
		self.wfile.write(bytes(message,"utf-8"))
		return
	def do_GET(self):
		httpcode = 200
		pathok = False
		try:
			parsed_path = urllib.parse.urlparse(self.path)
			core.debugmsg(8, "parsed_path:", parsed_path)
			if (parsed_path.path == '/'):
				pathok = True
				message  = "<html>"
				message += "<head>"


				# https://developers.google.com/speed/libraries#jquery-ui
				# Jquery
				message += "<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js\"></script>"
				# Jquery UI
				message += "<link rel=\"stylesheet\" href=\"https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/base/jquery-ui.css\">"
				message += "<script src=\"https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js\"></script>"

				message += "<script>"
				message += "$(function() {"
				message += "	$(\"#tables\" ).tabs();"
				message += "	$( \"#buttonbar\" ).controlgroup();"
				message += "	$.getJSON('tables', function(tables) { "
				message += "		for (var i = 0; i < tables.tables.length; i++) {"
				# message += "			console.log(tables.Data[i]);"
				# message += "			//Do something"
				# https://jqueryui.com/tabs/#manipulation <== how to do add and remove tabs
				message += "			$(\"#tables\").append('<div id=\"' + tables.tables[i].id +'_'+ tables.tables[i].table + '\"></div>'); "
				message += "			$(\"#tables ul\").append('<li><a href=\"#' + tables.tables[i].id +'_'+ tables.tables[i].table + '\">' + tables.tables[i].table + '</a> <span class=\"ui-icon ui-icon-close\" role=\"presentation\">Remove Tab</span></li>'); "
				message += "			$( \"#tables\" ).tabs( \"refresh\" );"
				message += "		}"
				message += "		var active = $( \"#tables\" ).tabs( \"option\", \"active\" );"
				message += "		if (!active) {"
				# message += "			console.log(\"active: \" + active);"
				message += "			$( \"#tables\" ).tabs( \"option\", \"active\", 0 );"
				message += "		}"
				message += "	});"
				message += "});"
				message += "</script>"

				message += "<style>"
				message += "#buttonbar { float: right; }"
				message += "</style>"

				message += "<title>Test Data Table</title>"
				message += "</head>"
				message += "<body>"

				# <fieldset>
				message += "<div id=\"buttonbar\">"
				message += "	<button id='new-table' class=\"ui-button ui-widget ui-corner-all ui-button-icon-only\" title=\"Add Table\"><span class=\"ui-icon ui-icon-calculator\"></span>Add Table</button>"
				message += "	<button id='new-column' class=\"ui-button ui-widget ui-corner-all ui-button-icon-only\" title=\"Add Column\"><span class=\"ui-icon ui-icon-grip-solid-vertical\"></span>Add Column</button>"
				message += "	<button>&nbsp;</button>" # spacer
				# message += "	<button></button>" # spacer
				message += "	<select id='auto-refresh'>"
				message += "		<option value='0' >Auto Refresh Off</option>"
				message += "		<option value='1' >Auto Refresh 1 second</option>"
				message += "		<option value='5' >Auto Refresh 5 seconds</option>"
				message += "		<option value='10' >Auto Refresh 10 second</option>"
				message += "		<option value='60' >Auto Refresh 1 minute</option>"
				message += "	</select>"
				message += "	<button id='refresh' class=\"ui-button ui-widget ui-corner-all ui-button-icon-only\" title=\"Refresh\"><span class=\"ui-icon ui-icon-refresh\"></span>Refresh</button>"
				message += "	<button id='help' class=\"ui-button ui-widget ui-corner-all ui-button-icon-only\" title=\"Help\"><span class=\"ui-icon ui-icon-help\"></span>Help</button>"
				message += "</div>"
				message += "<div>"
				message += "<p>&nbsp;<br></p>"
				message += "&nbsp;<br>"
				message += "</div>"

				message += "<div id='tables'>"
				message += "<ul>"
				message += "</ul>"
				message += "</div>"
				# message += "<div id='tableframes'>"
				# message += "</div>"


				message += "</body>"
				message += "</html>"

			core.debugmsg(8, "parsed_path:", parsed_path)
			if (parsed_path.path == '/tables'):
				pathok = True
				message = ""
				jsonresp = {}
				jsonresp["tables"] = core.tables_getall()
				message = json.dumps(jsonresp)

			core.debugmsg(8, "parsed_path:", parsed_path)
			patharr = parsed_path.path.split("/")
			core.debugmsg(8, "patharr:", patharr)
			if not pathok and len(patharr) == 2:
				tablename = urllib.parse.unquote_plus(patharr[1])
				core.debugmsg(9, "tablename:", tablename)

				tableid = core.table_exists(tablename)
				core.debugmsg(9, "tableid:", tableid)
				if tableid:
					pathok = True
					httpcode = 200
					jsonresp = {}
					jsonresp[tablename] = core.table_columns(tablename)
					i = 0
					for col in jsonresp[tablename]:
						core.debugmsg(9, "col:", col)
						jsonresp[tablename][i]["values"] = core.column_values(tablename, col["column"])
						i += 1
					message = json.dumps(jsonresp)

			if not pathok and len(patharr) == 3:
				tablename = urllib.parse.unquote_plus(patharr[1])
				core.debugmsg(9, "tablename:", tablename)
				columnname = urllib.parse.unquote_plus(patharr[2])
				core.debugmsg(9, "tablename:", tablename)

				if columnname == "columns":
					tableid = core.table_exists(tablename)
					core.debugmsg(9, "tableid:", tableid)
					if tableid:
						pathok = True
						httpcode = 200

						jsonresp = {}
						jsonresp[tablename] = core.table_columns(tablename)

						message = json.dumps(jsonresp)

				if columnname == "row":
					tableid = core.table_exists(tablename)
					core.debugmsg(9, "tableid:", tableid)
					if tableid:
						pathok = True
						httpcode = 200

						jsonresp = {}
						jsonresp[tablename] = {}

						columns = core.table_columns(tablename)
						core.debugmsg(9, "columns:", columns)
						for col in columns:
							core.debugmsg(9, "col:", col)
							column_name = col["column"]
							core.debugmsg(9, "column_name:", column_name)
							val_data = core.value_consume(tablename, column_name)
							core.debugmsg(9, "val_data:", val_data)
							if val_data is None:
								jsonresp[tablename][column_name] = None
							else:
								jsonresp[tablename][column_name] = val_data["value"]

						message = json.dumps(jsonresp)


				columnid = core.column_exists(tablename, columnname)
				core.debugmsg(9, "columnid:", columnid)
				if columnid:
					pathok = True
					httpcode = 200
					val_data = core.value_consume(tablename, columnname)
					if val_data is None:
						jsonresp = {columnname : None}
					else:
						jsonresp = {columnname : val_data["value"]}
					core.debugmsg(9, "jsonresp:", jsonresp)
					message = json.dumps(jsonresp)


			if not pathok and len(patharr) == 4:
				tablename = urllib.parse.unquote_plus(patharr[1])
				core.debugmsg(9, "tablename:", tablename)
				columnname = urllib.parse.unquote_plus(patharr[2])
				core.debugmsg(9, "tablename:", tablename)
				columntype = urllib.parse.unquote_plus(patharr[3])
				core.debugmsg(9, "columntype:", columntype)

				if columntype == "all":
					pathok = True
					httpcode = 200

					jsonresp = {}
					jsonresp[columnname] = core.column_values(tablename, columnname)

					message = json.dumps(jsonresp)

				data = core.value_consume_byid(tablename, columnname, columntype)
				if data is not None:
					pathok = True
					httpcode = 200
					jsonresp = {}
					jsonresp[columnname] = data["value"]
					message = json.dumps(jsonresp)


			core.debugmsg(8, "parsed_path:", parsed_path)
			if not pathok:
				httpcode = 404
				core.debugmsg(9, "httpcode:", httpcode)
				message = None
				# message = "Unrecognised request: {}".format(parsed_path.path)
				# core.debugmsg(9, "message:", message)
		except Exception as e:
			core.debugmsg(6, "do_GET:", e)
			httpcode = 500
			message = str(e)

		core.debugmsg(9, "httpcode:", httpcode)
		self.send_response(httpcode)
		self.end_headers()
		core.debugmsg(9, "message:", message)
		if message is not None:
			self.wfile.write(bytes(message,"utf-8"))
		return
	def handle_http(self):
		return
	def respond(self):
		return

	# 	log_request is here to stop BaseHTTPRequestHandler logging to the console
	# 		https://stackoverflow.com/questions/10651052/how-to-quiet-simplehttpserver/10651257#10651257
	def log_request(self, code='-', size='-'):
		pass

class TDT_Core:
	version = "v0.0.1"
	debuglvl = 0

	tdt_ini = None
	save_ini = True

	dbcleanup = None
	webserver = None
	httpserver = None
	db = None

	appstarted = False
	keeprunning = True

	def __init__(self, master=None):
		self.debugmsg(0, "Test Data Table Server")
		self.debugmsg(0, "	Version", self.version)
		signal.signal(signal.SIGINT, self.on_closing)

		self.debugmsg(9, "ArgumentParser")
		# Check for command line args
		parser = argparse.ArgumentParser()
		parser.add_argument('-g', '--debug', help='Set debug level, default level is 0')
		parser.add_argument('-v', '--version', help='Display the version and exit', action='store_true')
		parser.add_argument('-i', '--ini', help='path to alternate ini file')
		parser.add_argument('-d', '--dir', help='Data directory')
		parser.add_argument('-e', '--ipaddress', help='IP Address to bind the server to')
		parser.add_argument('-p', '--port', help='Port number to bind the server to')
		self.args = parser.parse_args()

		self.debugmsg(6, "self.args: ", self.args)

		if self.args.debug:
			self.debuglvl = int(self.args.debug)

		if self.args.version:
			exit()

		self.debugmsg(6, "ConfigParser")
		self.config = configparser.ConfigParser()
		scrdir = os.path.abspath(os.path.dirname(__file__))
		self.debugmsg(6, "scrdir: ", scrdir)

		self.tdt_ini = os.path.join(scrdir, "TestDataTable.ini")
		if self.args.ini:
			self.save_ini = False
			self.debugmsg(5, "self.args.ini: ", self.args.ini)
			self.tdt_ini = self.args.ini

		if os.path.isfile(self.tdt_ini):
			self.debugmsg(9, "tdt_ini: ", self.tdt_ini)
			self.config.read(self.tdt_ini)
		else:
			self.saveini()


		if 'Server' not in self.config:
			self.config['Server'] = {}
			self.saveini()

		if 'BindIP' not in self.config['Server']:
			self.config['Server']['BindIP'] = ''
			self.saveini()

		if 'BindPort' not in self.config['Server']:
			self.config['Server']['BindPort'] = "80"
			self.saveini()

		if 'DataDir' not in self.config['Server']:
			self.config['Server']['DataDir'] = scrdir
			self.saveini()


		if self.args.dir:
			self.save_ini = False
			self.debugmsg(5, "self.args.dir: ", self.args.dir)
			DataDir = os.path.abspath(self.args.dir)
			self.debugmsg(5, "DataDir: ", DataDir)
			self.config['Server']['DataDir'] = DataDir

		if self.args.ipaddress:
			self.save_ini = False
			self.debugmsg(5, "self.args.ipaddress: ", self.args.ipaddress)
			self.config['Server']['BindIP'] = self.args.ipaddress

		if self.args.port:
			self.save_ini = False
			self.debugmsg(5, "self.args.port: ", self.args.port)
			self.config['Server']['BindPort'] = self.args.port


		# https://pypi.org/project/sqlite3worker/
		#
		# Connect db
		#
		if self.db is None:
			createschema = False
			if not os.path.exists(self.config['Server']['DataDir']):
				os.mkdir(self.config['Server']['DataDir'])
			dbfile = os.path.join(self.config['Server']['DataDir'], "TestDataTable.sqlite3")
			if not os.path.exists(dbfile):
				createschema = True
			self.db = Sqlite3Worker(dbfile)
			if createschema:
				result = self.db.execute("CREATE TABLE tdt_tables (table_name TEXT, deleted DATETIME)")
				self.debugmsg(6, "CREATE TABLE tdt_tables", result)

				result = self.db.execute("CREATE TABLE tdt_columns (table_id NUMBER, column_name TEXT, deleted DATETIME)")
				self.debugmsg(6, "CREATE TABLE tdt_columns", result)

				result = self.db.execute("CREATE TABLE tdt_data (column_id NUMBER, value TEXT, deleted DATETIME)")
				self.debugmsg(6, "CREATE TABLE tdt_data", result)

				createschema = False


		self.debugmsg(5, "run_web_server")
		self.webserver = threading.Thread(target=self.run_web_server)
		self.webserver.start()

		self.debugmsg(9, "end __init__")

	def mainloop(self):
		self.debugmsg(5, "appstarted:", self.appstarted)
		while not self.appstarted:
			self.debugmsg(9, "sleep(1)")
			time.sleep(1)
			self.debugmsg(9, "appstarted:", self.appstarted)

		self.debugmsg(5, "keeprunning:", self.keeprunning)
		i = 0
		while self.keeprunning:
			time.sleep(1)
			if i > 9:
				self.debugmsg(9, "keeprunning:", self.keeprunning)
				i = 0
				# run_db_cleanup
				self.dbcleanup = threading.Thread(target=self.run_db_cleanup)
				self.dbcleanup.start()
			i +=1

		self.debugmsg(5, "mainloop ended")

	def run_web_server(self):


		srvip = self.config['Server']['BindIP']
		srvport = int(self.config['Server']['BindPort'])
		if len(srvip)>0:
			srvdisphost = srvip
			ip = ipaddress.ip_address(srvip)
			self.debugmsg(5, "ip.version:", ip.version)
			if ip.version == 6 and sys.version_info < (3, 8):
				self.debugmsg(0, "Python 3.8 or higher required to bind to IPv6 Addresses")
				pyver = "{}.{}.{}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2])
				self.debugmsg(0, "Python Version:",pyver,"	IP Version:", ip.version, "	IP Address:", srvip)
				srvip = ''
				srvdisphost = socket.gethostname()
		else:
			srvdisphost = socket.gethostname()


		server_address = (srvip, srvport)
		try:
			self.httpserver = ThreadingHTTPServer(server_address, TDT_WebServer)
		except PermissionError:
			self.debugmsg(0, "Permission denied when trying :",server_address)
			self.on_closing()
			return False
		except Exception as e:
			self.debugmsg(5, "e:", e)
			self.on_closing()
			return False


		self.appstarted = True
		self.debugmsg(5, "appstarted:", self.appstarted)
		self.debugmsg(0, "Starting Test Data Table Server", "http://{}:{}/".format(srvdisphost, srvport))
		self.httpserver.serve_forever()

	def run_db_cleanup(self):
		# remove records where the deleted column has had a value set for more than 600 seconds (10 min)
		#   aka cleanup deleted records

		# -- identify records for cleanup
		# -- SELECT ROWID, * FROM tdt_tables WHERE deleted < (strftime('%s', 'now') - 600)
		# -- DELETE FROM tdt_data WHERE deleted < (strftime('%s', 'now') - 36000);
		results = self.db.execute("DELETE FROM tdt_data WHERE deleted < (strftime('%s', 'now') - 600);")
		core.debugmsg(9, "tdt_data: results:", results)
		# -- DELETE  FROM tdt_columns WHERE deleted < (strftime('%s', 'now') - 36000);
		results = self.db.execute("DELETE FROM tdt_columns WHERE deleted < (strftime('%s', 'now') - 600);")
		core.debugmsg(9, "tdt_columns: results:", results)
		# -- DELETE  FROM tdt_tables WHERE deleted < (strftime('%s', 'now') - 36000);
		results = self.db.execute("DELETE FROM tdt_tables WHERE deleted < (strftime('%s', 'now') - 600);")
		core.debugmsg(9, "tdt_tables: results:", results)

	def on_closing(self, *others):
		if self.appstarted:
			self.keeprunning = False

			self.debugmsg(5, "Close Web Server")
			try:
				# self.debugmsg(0, "Shutdown Agent Server")
				self.httpserver.shutdown()
				self.appstarted = False
			except Exception as e:
				self.debugmsg(9, "Exception:", e)
				pass

			if self.db is not None:
				self.debugmsg(5, "Close DB")
				try:
					self.db.close()
					self.db = None
				except Exception as e:
					self.debugmsg(9, "Exception:", e)
					pass

	def saveini(self):
		if self.save_ini:
			with open(self.tdt_ini, 'w') as configfile:    # save
			    self.config.write(configfile)

	def debugmsg(self, lvl, *msg):
		msglst = []
		prefix = ""

		# print("debugmsg: debuglvl:", self.debuglvl," >= lvl:",lvl,"	msg:", msg)

		if self.debuglvl >= lvl:
			try:
				if self.debuglvl >= 4:
					stack = inspect.stack()
					the_class = stack[1][0].f_locals["self"].__class__.__name__
					the_method = stack[1][0].f_code.co_name
					the_line = stack[1][0].f_lineno
					# print("RFSwarmBase: debugmsg: I was called by {}.{}()".format(str(the_class), the_method))
					prefix = "{} | {}: {}({}): [{}:{}]	".format(datetime.now().isoformat(sep=' ',timespec='seconds'), str(the_class), the_method, the_line, self.debuglvl, lvl)
					# <36 + 1 tab
					# if len(prefix.strip())<36:
					# 	prefix = "{}	".format(prefix)
					# <32 + 1 tab
					if len(prefix.strip())<32:
						prefix = "{}	".format(prefix)
					# <28 + 1 tab
					# if len(prefix.strip())<28:
					# 	prefix = "{}	".format(prefix)
					# <24 + 1 tab
					if len(prefix.strip())<24:
						prefix = "{}	".format(prefix)

					msglst.append(str(prefix))

				for itm in msg:
					msglst.append(str(itm))
				print(" ".join(msglst))
			except Exception as e:
				# print("debugmsg: Exception:", e)
				pass

	#
	#	reusable table, column and vlaue functions
	#

	def tables_getall(self):
		tables = []
		results = core.db.execute("SELECT rowid, table_name from tdt_tables where deleted is NULL")
		core.debugmsg(9, "results:", results)
		for row in results:
			# core.debugmsg(9, "row:", row)
			# message += str(row)
			rowdict = {}
			rowdict["table"] = row[1]
			rowdict["tbl_id"] = row[0]
			tables.append(rowdict)
		return tables

	def table_exists(self, tablename):
		# returns the table id if exists, else returns False
		id = False
		try:
			results = self.db.execute("SELECT rowid, table_name FROM tdt_tables WHERE table_name = ? and deleted is NULL", [tablename])
			self.debugmsg(9, "results:", results)
			if len(results)>0:
				id = results[0][0]
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return id

	def table_create(self, tablename):
		# creates the table
		try:
			tableid = self.table_exists(tablename)
			self.debugmsg(9, "tableid:", tableid)
			if not tableid:
				results = self.db.execute("INSERT INTO tdt_tables (table_name) VALUES (?)", [tablename])
				self.debugmsg(9, "results:", results)
				if results is None:
					return self.table_exists(tablename)
		except Exception as e:
			self.debugmsg(6, "Exception:", e)
		return False

	def table_columns(self, tablename):
		columns = []
		try:
			tableid = self.table_exists(tablename)
			self.debugmsg(9, "tableid:", tableid)
			if tableid:
				results = self.db.execute("SELECT rowid, table_id, column_name FROM tdt_columns WHERE table_id = ? and deleted is NULL", [tableid])
				self.debugmsg(9, "results:", results)
				if len(results)>0:
					for res in results:
						self.debugmsg(9, "res:", res)
						retcol = {}
						retcol["column"] = res[2]
						retcol["col_id"] = res[0]
						columns.append(retcol)
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return columns

	def table_delete(self, tablename):
		try:
			tableid = self.table_exists(tablename)
			self.debugmsg(9, "tableid:", tableid)
			if tableid:
				table_cols = self.table_columns(tablename)
				for col in table_cols:
					self.debugmsg(9, "col:", col)
					delcol = self.column_delete(tablename, col["column"])
					if not delcol:
						return False
				res_table = core.db.execute("UPDATE tdt_tables SET deleted = strftime('%s', 'now') WHERE ROWID=?", [tableid])
				core.debugmsg(9, "res_table:", res_table)
				if res_table is None:
					return True
			else:
				return True
		except Exception as e:
			self.debugmsg(6, "Exception:", e)
		return False

	def column_exists(self, tablename, columnname):
		# returns the column id if exists, else returns False
		id = False
		try:
			tableid = self.table_exists(tablename)
			self.debugmsg(9, "tableid:", tableid)
			if tableid:
				results = self.db.execute("SELECT rowid, table_id, column_name FROM tdt_columns WHERE table_id = ? and column_name = ? and deleted is NULL", [tableid, columnname])
				self.debugmsg(9, "results:", results)
				if len(results)>0:
					id = results[0][0]
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return id

	def column_create(self, tablename, columnname):
		# creates the column
		try:
			columnid = self.column_exists(tablename, columnname)
			self.debugmsg(9, "columnid:", columnid)
			if not columnid:
				tableid = self.table_exists(tablename)
				self.debugmsg(9, "tableid:", tableid)
				if not tableid:
					tableid = self.table_create(tablename)
					self.debugmsg(9, "tableid:", tableid)
				if tableid:
					results = self.db.execute("INSERT INTO tdt_columns (table_id, column_name) VALUES (?,?)", [tableid, columnname])
					self.debugmsg(9, "results:", results)
					if results is None:
						return self.column_exists(tablename, columnname)
		except Exception as e:
			self.debugmsg(6, "Exception:", e)
		return False

	def column_values(self, tablename, columnname):
		values = []
		try:
			columnid = self.column_exists(tablename, columnname)
			self.debugmsg(9, "columnid:", columnid)
			if columnid:
				results = self.db.execute("SELECT rowid, column_id, value FROM tdt_data WHERE column_id = ? and deleted is NULL", [columnid])
				self.debugmsg(9, "results:", results)
				if len(results)>0:
					for res in results:
						self.debugmsg(9, "res:", res)
						retcol = {}
						retcol["value"] = res[2]
						retcol["val_id"] = res[0]
						values.append(retcol)
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return values

	def column_delete(self, tablename, columnname):
		try:
			columnid = self.column_exists(tablename, columnname)
			self.debugmsg(9, "columnid:", columnid)
			if columnid:
				# remove data
				res_data = core.db.execute("UPDATE tdt_data SET deleted = strftime('%s', 'now') WHERE column_id = ?", [columnid])
				core.debugmsg(9, "res_data:", res_data)
				if res_data is not None:
					return False

				# remove column
				res_columns = core.db.execute("UPDATE tdt_columns SET deleted = strftime('%s', 'now') WHERE rowid = ?", [columnid])
				core.debugmsg(9, "res_columns:", res_columns)
				if res_columns is None:
					return True

			else:
				return True
		except Exception as e:
			self.debugmsg(6, "Exception:", e)
		return False

	def value_exists(self, tablename, columnname, value):
		# returns the value id if exists, else returns False
		# 	useful for add if unique
		id = False
		try:
			columnid = self.column_exists(tablename, columnname)
			if columnid:
				results = self.db.execute("SELECT rowid, column_id, value FROM tdt_data WHERE column_id = ? and (value = ? or ROWID = ?) and deleted is NULL", [columnid, value, value])
				self.debugmsg(9, "results:", results)
				if len(results)>0:
					id = results[0][0]
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return id

	def value_create(self, tablename, columnname, value):
		# creates the value
		try:
			columnid = self.column_exists(tablename, columnname)
			self.debugmsg(9, "columnid:", columnid)
			if not columnid:
				columnid = self.column_create(tablename, columnname)
				self.debugmsg(9, "columnid:", columnid)
			if columnid:
				results = self.db.execute("INSERT INTO tdt_data (column_id, value) VALUES (?,?)", [columnid, value])
				self.debugmsg(9, "results:", results)
				if results is None:
					return self.value_exists(tablename, columnname, value)
		except Exception as e:
			self.debugmsg(6, "Exception:", e)
		return False

	def value_delete(self, tablename, columnname, value):
		try:
			valueid = self.value_exists(tablename, columnname, value)
			core.debugmsg(9, "valueid:", valueid)
			if valueid:
				res_data = core.db.execute("UPDATE tdt_data SET deleted = strftime('%s', 'now') WHERE rowid = ?", [valueid])
				core.debugmsg(9, "res_data:", res_data)
				if res_data is None:
					return True
			else:
				return True
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return False

	def value_consume(self, tablename, columnname):
		try:
			columnid = self.column_exists(tablename, columnname)
			self.debugmsg(9, "columnid:", columnid)
			if columnid:
				# sqlite3.Warning: You can only execute one statement at a time.
				# 	Also didn't return any result
					# txn = ""
					# txn += "BEGIN TRANSACTION; \n\n"
					# txn += "CREATE TEMP TABLE _ConsumeValue AS \n"
					# txn += "SELECT ROWID, * FROM tdt_data \n"
					# txn += "WHERE deleted is NULL \n"
					# txn += "	AND column_id = 29 \n"
					# txn += "LIMIT 1; \n\n"
					# txn += "UPDATE tdt_data SET deleted = strftime('%s', 'now') WHERE rowid = (SELECT rowid from _ConsumeValue); \n\n"
					# txn += "SELECT * from _ConsumeValue; \n\n"
					# txn += "DROP TABLE _ConsumeValue; \n\n"
					# txn += "END TRANSACTION; \n"
					# self.debugmsg(9, "txn:", txn)
					# results = self.db.execute(txn)

				retval = {}
				results = self.db.execute("SELECT ROWID, * FROM tdt_data WHERE deleted is NULL AND column_id = ? LIMIT 1;", [columnid])
				self.debugmsg(9, "results:", results)
				if len(results)>0:
					retval["val_id"] = results[0][0]
					resultu = self.db.execute("UPDATE tdt_data SET deleted = strftime('%s', 'now') WHERE rowid = ?;", [retval["val_id"]])
					self.debugmsg(9, "resultu:", resultu)
					retval["value"] = results[0][2]
					return retval
			else:
				return None
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return None

	def value_consume_byid(self, tablename, columnname, value):
		try:
			val_id = self.value_exists(tablename, columnname, value)
			self.debugmsg(9, "val_id:", val_id)
			if val_id:
				retval = {}
				resultu = self.db.execute("UPDATE tdt_data SET deleted = strftime('%s', 'now') WHERE rowid = ?;", [val_id])
				self.debugmsg(9, "resultu:", resultu)

				results = self.db.execute("SELECT ROWID, * FROM tdt_data WHERE ROWID = ?;", [val_id])
				self.debugmsg(9, "results:", results)
				retval["val_id"] = results[0][0]
				retval["value"] = results[0][2]
				return retval
			else:
				return None
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return None


	# def value_create_unique(self, tablename, columnname, value):
	# 	# creates the value
	# 	return False

# web = TDT_WebServer()
core = TDT_Core()

try:
	core.mainloop()
except KeyboardInterrupt:
	core.on_closing()
except Exception as e:
	core.debugmsg(1, "self.Exception:", e)
	core.on_closing()
