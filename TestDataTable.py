

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
	def do_POST(self):
		httpcode = 200
		try:
			parsed_path = urllib.parse.urlparse(self.path)
			core.debugmsg(8, "parsed_path:", parsed_path)
			message = "{'path':'"+parsed_path+"'}"
				# core.debugmsg(8, "jsonresp:", jsonresp)
				# message = json.dumps(jsonresp)
			# else:
			# 	httpcode = 404
			# 	message = "Unrecognised request: '{}'".format(parsed_path)

		except Exception as e:
			core.debugmsg(6, "do_POST:", e)
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
				message += "		for (var i = 0; i < tables.Data.length; i++) {"
				# message += "			console.log(tables.Data[i]);"
				# message += "			//Do something"
				# https://jqueryui.com/tabs/#manipulation <== how to do add and remove tabs
				message += "			$(\"#tables\").append('<div id=\"' + tables.Data[i].id +'_'+ tables.Data[i].table + '\"></div>'); "
				message += "			$(\"#tables ul\").append('<li><a href=\"#' + tables.Data[i].id +'_'+ tables.Data[i].table + '\">' + tables.Data[i].table + '</a> <span class=\"ui-icon ui-icon-close\" role=\"presentation\">Remove Tab</span></li>'); "
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

			if (parsed_path.path == '/tables'):
				pathok = True
				message = ""
				jsonresp = {}
				jsonresp["Data"] = []

				results = core.db.execute("SELECT rowid, table_name from tdt_tables where deleted is NULL")
				core.debugmsg(9, "results:", results)
				for row in results:
					core.debugmsg(9, "row:", row)
					# message += str(row)
					rowdict = {}
					rowdict["id"] = row[0]
					rowdict["table"] = row[1]
					jsonresp["Data"].append(rowdict)

				message = json.dumps(jsonresp)

			if not pathok:
				httpcode = 404
				message = "Unrecognised request: '{}'".format(parsed_path)
		except Exception as e:
			core.debugmsg(6, "do_GET:", e)
			httpcode = 500
			message = str(e)

		self.send_response(httpcode)
		self.end_headers()
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



# web = TDT_WebServer()
core = TDT_Core()

try:
	core.mainloop()
except KeyboardInterrupt:
	core.on_closing()
except Exception as e:
	core.debugmsg(1, "self.Exception:", e)
	core.on_closing()
