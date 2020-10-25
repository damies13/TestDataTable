#!/usr/bin/python
#
#	Test Data Table
#
#    Version v0.2.3
#




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
import uuid




class TDT_WebServer(BaseHTTPRequestHandler):
	def do_HEAD(self):
		core.debugmsg(7, " ")
		return

	def do_DELETE(self):
		core.debugmsg(7, " ")
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
		try:
			self.send_response(httpcode)
			self.send_header("Server", "Test Data Table v"+core.version)
			self.end_headers()
			self.wfile.write(bytes(message,"utf-8"))
		except BrokenPipeError as e:
			core.debugmsg(8, "Browser lost connection, probably closed by user")
		except Exception as e:
			core.debugmsg(6, "do_PUT:", e)
		return


	def do_PUT(self):
		core.debugmsg(7, " ")
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
				if len(tablename)<1:
					httpcode = 406
					message = '{"message": "table name cannot be blank"}'
				else:
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

				if len(columnname)<1:
					httpcode = 406
					message = '{"message": "column name cannot be blank"}'
				else:

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


			if not actionfound and len(patharr) == 5:
				actionfound = True
				# replace value by id?
				tablename = urllib.parse.unquote_plus(patharr[1])
				core.debugmsg(9, "tablename:", tablename)
				columnname = urllib.parse.unquote_plus(patharr[2])
				core.debugmsg(9, "columnname:", columnname)
				value_id = urllib.parse.unquote_plus(patharr[3])
				core.debugmsg(9, "value_id:", value_id)
				columnvalue = urllib.parse.unquote_plus(patharr[4])
				core.debugmsg(9, "columnvalue:", columnvalue)

				curr_id = core.value_exists(tablename, columnname, value_id)
				if curr_id:
					result = core.value_replace_byid(tablename, columnname, curr_id, columnvalue)
					if result:
						httpcode = 200
						message = '{"message": "value id:'+value_id+' replaced with value:'+columnvalue+' in column '+columnname+'"}'
					else:
						httpcode = 501
						message = '{"message": "An unknown error occoured replaceing '+value_id+' with '+columnvalue+' in column '+columnname+'"}'

				else:
					httpcode = 404
					message = '{"message": "the value/id ('+value_id+') you are trying to replace doesn\'t exist"}'




		except Exception as e:
			core.debugmsg(6, "do_PUT:", e)
			httpcode = 500
			message = str(e)

		try:
			self.send_response(httpcode)
			self.send_header("Server", "Test Data Table v"+core.version)
			self.end_headers()
			self.wfile.write(bytes(message,"utf-8"))
		except BrokenPipeError as e:
			core.debugmsg(8, "Browser lost connection, probably closed by user")
		except Exception as e:
			core.debugmsg(6, "do_PUT:", e)

		return
	def do_POST(self):
		core.debugmsg(7, " ")
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


				if columnname == "papaparse":
					actionfound = True
					data = json.loads(post_body)
					core.debugmsg(9, "data:", data)
					for row in data:
						core.debugmsg(9, "row:", row)
						for val in row:
							core.debugmsg(9, "val:", val)
							core.value_create(tablename, val, row[val])

					httpcode = 201
					message = '{"message": "values added to table: '+tablename+'"}'


		except Exception as e:
			core.debugmsg(6, "Exception:", e)
			httpcode = 500
			message = str(e)

		try:
			self.send_response(httpcode)
			self.send_header("Server", "Test Data Table v"+core.version)
			self.end_headers()
			self.wfile.write(bytes(message,"utf-8"))
		except BrokenPipeError as e:
			core.debugmsg(8, "Browser lost connection, probably closed by user")
		except Exception as e:
			core.debugmsg(6, "do_PUT:", e)
		return
	def do_GET(self):
		core.debugmsg(7, " ")
		httpcode = 200
		pathok = False
		try:
			parsed_path = urllib.parse.urlparse(self.path)
			core.debugmsg(8, "parsed_path:", parsed_path)
			if parsed_path.path == '/':
				pathok = True
				message  = "<html>"
				message += "<head>"

				# https://developers.google.com/speed/libraries#jquery-ui
				# Jquery




				message += "<script src=\""+core.config['Resources']['js_jquery']+"\"></script>"
				# Jquery UI
				message += "<link rel=\"stylesheet\" href=\""+core.config['Resources']['css_jqueryui']+"\">"
				message += "<script src=\""+core.config['Resources']['js_jqueryui']+"\"></script>"

				message += "<script src=\""+core.config['Resources']['js_papaparse']+"\"></script>"

				message += """	<style>
								.ui-tabs .ui-tabs-panel {
									padding: 0em 0em;
								}

								.tableFixHead          { overflow-y: auto; height: 88%; }
								.tableFixHead thead    { position: sticky; top: 0; width: 100%;}
								.tableFixHead thead th { position: sticky; top: 0; }
								/* .tableFixHead thead th span { float: left; } */
								.tableFixHead thead th span { float: left; padding-top: 5px; }
								.tableFixHead thead th span.ui-icon-close { position: absolute; top: 5px; right: 0px; }

								th, td { padding: 5px 10px; }

								.data-cell { min-width: 3em; }
								.has-value { background: #fff !important; }

								.ui-col-count { position: absolute; top: -5px; font-size: 0.7em; right: 20px; font-weight: normal; }

								#dialog-progress .ui-dialog-titlebar { display:none; }
								.progress-label { position: absolute; left: 40%; top: 28px; font-weight: bold; text-shadow: 1px 1px 0 #fff; }
								.ui-progressbar .ui-progressbar-value { height: 20px; }

								.ui-dialog { max-width: 90%; }

								</style> """


				message += "<script>"
				message += "var refreshinterval = 0;"
				message += "var refreshrunning = false;"
				# message += "var chunksize = 1048576;" # 1Mb
				message += "var chunksize = 1024*10;" # 1Mb
				message += "var chunkprocessed = 0;" # 1Mb
				message += "$(function() {"
				message += "	var tabs = $(\"#tables\" ).tabs();"

				message += "	$( \"#buttonbar\" ).controlgroup();"
				message += "	refresh();"



				message += "	dlgNewTable = $( \"#dialog-new-table\" ).dialog({"
				message += "		autoOpen: false,"
				message += "		height: \"auto\","
				message += "		width: \"auto\","
				message += "		modal: true,"
				message += "		buttons: {"
				message += "			Create: function() {"
				message += "				var tblname = $('#table-name').val();"
				message += "				console.log(\"#table-name: \" + $('#table-name'));"
				message += "				console.log(\"tblname: \" + tblname);"
				message += "				$.ajax({"
				message += "					url: '/'+tblname,"
				message += "					type: 'PUT',"
				message += "					dataType: 'json',"
				message += "					success: function(data) {"
				message += "						refresh();"
				message += "						setTimeout(function(){"
				message += "							$(\"li a:last\").trigger(\"click\");"
				message += "						}, 500);"
				message += "					}"
				message += "				});"
				message += "				$( this ).dialog( \"close\" );"
				message += "			},"
				message += "			Cancel: function() {"
				message += "				$( this ).dialog( \"close\" );"
				message += "			}"
				message += "		}"
				message += "	});"

				message += """ $('#table-name').keypress(function(e) {
									if (e.keyCode == $.ui.keyCode.ENTER) {
										var tblname = $('#table-name').val();
										console.log(\"#table-name: \" + $('#table-name'));
										console.log(\"tblname: \" + tblname);
										$.ajax({
											url: '/'+tblname,
											type: 'PUT',
											dataType: 'json',
											success: function(data) {
												refresh();
												setTimeout(function(){
													$("li a:last").trigger("click");
												}, 500);

											}
										});
										$( \"#dialog-new-table\" ).dialog( \"close\" );
									}
								}); """


				message += "	dlgDelTable = $( \"#dialog-delete-table\" ).dialog({"
				message += "		autoOpen: false,"
				message += "		height: \"auto\","
				message += "		width: \"auto\","
				message += "		modal: true,"
				message += "		buttons: {"
				message += "			Delete: function() {"
				message += "				tblname = $(\"#delete-table-name\").text();"
				message += "				console.log(\"tblname: \"+tblname);"
				message += "				$.ajax({"
				message += "					url: '/'+tblname,"
				message += "					type: 'DELETE',"
				message += "					dataType: 'json',"
				message += "					success: function(data) {"
				message += "						refresh();"
				message += "					}"
				message += "				});"
				message += "				$( this ).dialog( \"close\" );"
				message += "			},"
				message += "			Cancel: function() {"
				message += "				$( this ).dialog( \"close\" );"
				message += "			}"
				message += "		}"
				message += "	});"

				message += "	dlgAddColumn = $( \"#dialog-add-column\" ).dialog({"
				message += "		autoOpen: false,"
				message += "		height: \"auto\","
				message += "		width: \"auto\","
				message += "		modal: true,"
				message += "		buttons: {"
				message += "			Add: function() {"
				message += "				console.log(\"#column-name: \" + $('#column-name'));"
				message += "				var colname = $('#column-name').val();"
				message += "				console.log(\"colname: \" + colname);"
				message += "				var tblname = $('#column-table-name').text();"
				message += "				console.log(\"tblname: \" + tblname);"
				message += "				$.ajax({"
				message += "					url: '/'+tblname+'/'+colname,"
				message += "					type: 'PUT',"
				message += "					dataType: 'json',"
				message += "					success: function(data) {"
				message += "						refresh();"
				message += "					}"
				message += "				});"
				message += "				$( this ).dialog( \"close\" );"
				message += "			},"
				message += "			Cancel: function() {"
				message += "				$( this ).dialog( \"close\" );"
				message += "			}"
				message += "		}"
				message += "	});"

				message += """ $('#column-name').keypress(function(e) {
									if (e.keyCode == $.ui.keyCode.ENTER) {
										console.log(\"#column-name: \" + $('#column-name'));
										var colname = $('#column-name').val();
										console.log(\"colname: \" + colname);
										var tblname = $('#column-table-name').text();
										console.log(\"tblname: \" + tblname);
										$.ajax({
											url: '/'+tblname+'/'+colname,
											type: 'PUT',
											dataType: 'json',
											success: function(data) {
												refresh();
											}
										});
										$( \"#dialog-add-column\" ).dialog( \"close\" );
									}
								}); """

				# dialog-delete-column
				message += "	dlgDelColumn = $( \"#dialog-delete-column\" ).dialog({"
				message += "		autoOpen: false,"
				message += "		height: \"auto\","
				message += "		width: \"auto\","
				message += "		modal: true,"
				message += "		buttons: {"
				message += "			Delete: function() {"
				message += "				tblname = $(\"#delete-column-table\").text();"
				message += "				colname = $(\"#delete-column-name\").text();"
				message += "				console.log(\"tblname: \"+tblname);"
				message += "				$.ajax({"
				message += "					url: '/'+tblname+'/'+colname,"
				message += "					type: 'DELETE',"
				message += "					dataType: 'json',"
				message += "					success: function(data) {"
				message += "						var colhead = $('div[name=\"'+tblname+'\"]').find('th[name=\"'+colname+'\"]');"
				message += "						var colno = colhead.attr('colno');"
				message += "						colhead.remove();"
				message += "						$('td[colno=\"'+colno+'\"]').remove();"
				# message += "						refresh_table(tblname);"
				message += "						setTimeout(function(){"
				message += "							refresh_table(tblname);"
				message += "						}, 100);"
				message += "					}"
				message += "				});"
				message += "				$( this ).dialog( \"close\" );"
				message += "			},"
				message += "			Cancel: function() {"
				message += "				$( this ).dialog( \"close\" );"
				message += "			}"
				message += "		}"
				message += "	});"


				message += "	dlgProgress = $( \"#dialog-progress\" ).dialog({"
				message += "		autoOpen: false,"
				# message += "		classes: {\"no-close\": },"
				message += "		height: \"auto\","
				message += "		width: \"auto\","
				message += "		modal: false,"
				message += "	});"

				message += """	var progressbar = $("#dialog-progress").progressbar({
									value: false
								}); """


				message += """	dlgFileImport = $( \"#dialog-file-import\" ).dialog({
									autoOpen: false,
									height: \"auto\",
									width: \"auto\",
									modal: true,
									buttons: {
										Import: function() {
											$( this ).dialog( \"close\" );
											file_import_action();
										},
										Cancel: function() {
											$( this ).dialog( \"close\" );
										}
									}
								});"""

				# dialog-file-export
				message += """	dlgFileExport = $( \"#dialog-file-export\" ).dialog({
									autoOpen: false,
									height: \"auto\",
									width: \"auto\",
									modal: true,
									buttons: {
										Save: function() {
											/* $("#dialog-file-export output").css("display", "");
											$("#dialog-file-export output a").trigger("click"); */
											var a = document.getElementById("dialog-file-export").querySelector("output").querySelector("a");
											console.log("a:",a);
											a.click();
											$( this ).dialog( \"close\" );
											/* file_import_action(); */
										},
										Cancel: function() {
											$( this ).dialog( \"close\" );
										}
									}
								});"""



				message += "	tabs.on( \"click\", \"li span.ui-icon-close\", function() {"
				message += "		console.log( $( this ) );"
				message += "		console.log( $( this ).attr(\"table\") );"
				message += "		$(\"#delete-table-name\").text($( this ).attr(\"table\"));"
				message += "		dlgDelTable.dialog( \"open\" );"
				message += "	});"

				message += "	tabs.on( \"click\", \"th span.ui-icon-close\", function() {"
				message += "		console.log( $( this ) );"
				message += "		var tabactive = $( \"#tables\" ).tabs( \"option\", \"active\" );"
				message += "		console.log('tabactive:'+tabactive);"
				message += "		var tblname = $(\"#tables ul li:nth-child(\"+(tabactive+1)+\") a \").text();"
				message += "		console.log(\"tblname: \"+tblname);"
				message += "		var colname = $( this ).attr(\"column\");"
				message += "		console.log('colname: '+colname);"
				message += "		$(\"#delete-column-table\").text(tblname);"
				message += "		$(\"#delete-column-name\").text(colname);"
				message += "		dlgDelColumn.dialog( \"open\" );"
				message += "	});"

				message += "	tabs.on( \"click\", \"li.ui-tabs-tab\", function() {"
				message += "		console.log( $( this ) );"
				message += "		var tablename = $( this ).find('a').text();"
				message += "		console.log('tablename: '+tablename);"
				message += "		refreshrunning = false;"
				message += "		refresh_table(tablename);"
				message += "	});"


				message += "	$( \"#new-table\" ).button().on( \"click\", function() {"
				message += "		$('#table-name').val('');"
				message += "		dlgNewTable.dialog( \"open\" );"
				message += "	});"

				message += "	$( \"#new-column\" ).button().on( \"click\", function() {"
				message += "		var tabactive = $( \"#tables\" ).tabs( \"option\", \"active\" );"
				message += "		console.log('tabactive:'+tabactive);"
				message += "		var tblname = $(\"#tables ul li:nth-child(\"+(tabactive+1)+\") a \").text();"
				message += "		console.log(\"tblname: \"+tblname);"
				message += "		$(\"#column-table-name\").text(tblname);"
				message += "		$('#column-name').val('');"
				message += "		dlgAddColumn.dialog( \"open\" );"
				message += "	});"

				message += "	$( \"#import-file\" ).button().on( \"click\", function() {"
				message += "		$( \"#dialog-file-import-file\" ).val("");"
				message += "		dlgFileImport.dialog( \"open\" );"
				message += "	});"

				message += """	$( \"#export-file\" ).button().on( \"click\", function() {
									$('#export-file-table-name').val('');
									var active = $( "#tables" ).tabs( "option", "active" );
									console.log("active: " + active);
									var activetbl = $("#tables ul li:nth-child("+(active+1)+") a ").text();
									$('#export-file-table-name').val(activetbl);
									$("#dialog-file-export output").css("display", "None");
									dlgFileExport.dialog( \"open\" );
									file_export_preview();
								});"""



				message += "	$( \"#refresh\" ).button().on( \"click\", function() {"
				message += "		refresh();"
				message += "	});"

				message += "	$( \"#help\" ).button().on( \"click\", function() {"
				message += "		window.open(\"https://github.com/damies13/TestDataTable/blob/master/Doc/rest_api.md#rest-api\");"
				message += "	});"

				message += "	$( \"#auto-refresh\" ).on( \"selectmenuchange\", function() {"
				message += "		console.log(\"#auto-refresh:	this:\"+this);"
				message += "		refreshinterval = this.value;"
				message += "		auto_refresh(this.value);"
				message += "	});"



				# dialog-file-import-file
				message += "	$( \"#dialog-file-import-file\" ).on( \"change\", function() {"
				message += "		console.log(\"#dialog-file-import-file:	this:\"+this);"
				message += "		file_import_preview();"
				message += "	});"
				# dialog-file-import-delimiter
				message += "	$( \"#dialog-file-import-delimiter\" ).on( \"change\", function() {"
				message += "		console.log(\"#dialog-file-import-delimiter:	this:\"+this);"
				message += "		file_import_preview();"
				message += "	});"
				# dialog-file-import-header-row
				message += "	$( \"#dialog-file-import-header-row\" ).on( \"change\", function() {"
				message += "		console.log(\"#dialog-file-import-header-row:	this:\"+this);"
				message += "		file_import_preview();"
				message += "	});"
				# dialog-file-import-encoding
				message += "	$( \"#dialog-file-import-encoding\" ).on( \"change\", function() {"
				message += "		console.log(\"#dialog-file-import-encoding:	this:\"+this);"
				message += "		file_import_preview();"
				message += "	});"
				# dialog-file-import-comments
				message += "	$( \"#dialog-file-import-comments\" ).on( \"change\", function() {"
				message += "		console.log(\"#dialog-file-import-comments:	this:\"+this);"
				message += "		file_import_preview();"
				message += "	});"


				# dialog-file-export-file
				message += "	$( \"#dialog-file-export-file\" ).on( \"change\", function() {"
				message += "		console.log(\"#dialog-file-export-file:	this:\"+this);"
				message += "		file_export_preview();"
				message += "	});"
				# dialog-file-export-delimiter
				message += "	$( \"#dialog-file-export-delimiter\" ).on( \"change\", function() {"
				message += "		console.log(\"#dialog-file-export-delimiter:	this:\"+this);"
				message += "		file_export_preview();"
				message += "	});"
				# dialog-file-export-header-row
				message += "	$( \"#dialog-file-export-header-row\" ).on( \"change\", function() {"
				message += "		console.log(\"#dialog-file-export-header-row:	this:\"+this);"
				message += "		file_export_preview();"
				message += "	});"


				message += "});"

				message += """	function auto_refresh(value) {
									console.log("auto_refresh:	refreshinterval:"+refreshinterval);
									console.log("auto_refresh:	value:"+value);
									if (refreshinterval == value && value>0){
										setTimeout(function(){
											auto_refresh(value);
										}, value*1000);
										refresh();
									}
								};"""


				message += "function refresh() {"
				message += "	$.getJSON('tables', function(tables) { "
				message += "		refresh_tables(tables);"
				message += "	});"
				message += "};"

				message += """	function refresh_tables(tables) {
									var keeptables = [];
									for (var i = 0; i < tables.tables.length; i++) {
										console.log(tables.tables[i]);
										var tableid = tables.tables[i].tbl_id;
										var tablenme = tables.tables[i].table;
										var tabid = tableid.toString() +'_'+ tablenme.replace(' ', '_');
										keeptables.push(tabid);
										console.log("tabid: " + tabid);
										console.log($("[href='#"+tabid+"']").length);
										if (!$("[href='#"+tabid+"']").length){
											$("#tables").append('<div id="' + tabid + '" name="'+tablenme+'"  class=\"tableFixHead\"></div>');
											$("#tables ul").append('<li><a href="#' + tabid + '">'
												+ tablenme
												+ '</a> <span class="ui-icon ui-icon-close" role="presentation" table="'
												+ tablenme + '">Remove Tab</span></li>');
											$( "#tables" ).tabs( "refresh" );
										}
									}
									console.log("keeptables: " + keeptables);
									console.log($("#tables ul li").length);
									for (var i = 0; i < $("#tables ul li").length; i++) {
										console.log($("#tables ul li")[i]);
										var thistbl = $("#tables ul li:nth-child("+(i+1)+") a ").attr("href");
										thistbl = thistbl.substr(1);
										console.log("thistbl: "+thistbl);
										if (!keeptables.includes(thistbl)){
											console.log("remove thistbl: "+thistbl);
											$("#tables ul li:nth-child("+(i+1)+")").remove();
										}
									}
									var active = $( "#tables" ).tabs( "option", "active" );
									console.log("active: " + active);
									if (!active) {
										$( "#tables" ).tabs( "option", "active", 0 );
									}
									var active = $( "#tables" ).tabs( "option", "active" );
									console.log("active: " + active);
									var activetbl = $("#tables ul li:nth-child("+(active+1)+") a ").text();
									if (activetbl.length <1){
										active = 0;
										console.log("active: " + active);
										var activetbl = $("#tables ul li:nth-child("+(active+1)+") a ").trigger("click");
									} else {
										console.log("activetbl: "+activetbl);
										refresh_table(activetbl);
									}

								};"""

				message += """	function refresh_table(tablename) {
									if (!refreshrunning){
										refreshrunning = true;
										console.log("refresh_table: tablename:"+tablename);
										$.getJSON(tablename, function(tabledata) {
											refresh_table_data(tabledata);
										});
									}
								};"""

				message += """	function refresh_table_data(tabledata) {
									console.log("refresh_table_data_new: tabledata:", tabledata);
									var tbl_name = Object.keys(tabledata)[0];
									console.log("tbl_name: "+tbl_name);
									/* ensure columns */
									var tblid = $('div[name="'+tbl_name+'"]').attr('id');
									console.log("tblid: "+tblid);
									console.log($('div[name="'+tbl_name+'"] table').length);
									if (!$('div[name="'+tbl_name+'"] table').length){
										// console.log($('div[name="'+tbl_name+'"]'));
										$('div[name="'+tbl_name+'"]').append('<table id=\"table-'+tblid+'\"><thead><tr><th class="ui-widget-header">Row</th></tr></thead><tbody></tbody></table>');
									}
									var safecols = [];
									for (var i = 0; i < tabledata[tbl_name].length; i++) {
										var col_name = tabledata[tbl_name][i]["column"];
										console.log("col_name: "+col_name);
										var col_id = tabledata[tbl_name][i]["col_id"];
										var colno = tblid+'-'+col_id;
										console.log("colno: "+colno);
										safecols.push(colno);
										if (!$('table[id="table-'+tblid+'"] thead tr th[colno="'+colno+'"]').length){
											$('table[id="table-'+tblid+'"] thead tr').append('<th class="ui-widget-header" id="'+col_id+'" name="'+col_name+'" colno="'+colno+'"><span column="'+col_name+'" class="ui-icon ui-icon-close" role="presentation">Remove Column</span><span>'+col_name+'</span><span class="ui-col-count">(0)</span></div></th>');
										}
									}
									console.log("safecols: ",safecols);
									/* remove columns that no longer exist on the server */
									var dispcols = $('table[id="table-'+tblid+'"] thead tr th');
									console.log("dispcols: ",dispcols);
									for (var i = 0; i < dispcols.length; i++) {
										console.log("dispcols["+i+"]: ",dispcols[i]);
										var thiscolno = $(dispcols[i]).attr('colno');
										console.log("thiscolno: ",thiscolno);
										if (thiscolno && safecols.indexOf(thiscolno) < 0){
											/* remove column */
											console.log("remove thiscolno: ",thiscolno);
											$('th[colno=\"'+thiscolno+'\"]').remove();
											$('td[colno=\"'+thiscolno+'\"]').remove();
										}
									}

									/* start populating rows */
									refresh_table_data_row(0, tabledata);
								};"""

				message += """	function refresh_table_data_row(rt_row, tabledata) {
									console.log("refresh_table_data_row: rt_row: "+rt_row);
									/* console.log("refresh_table_data_row: rt_row: "+rt_row+"	tabledata:", tabledata); */
									var tbl_name = Object.keys(tabledata)[0];
									/* console.log("tbl_name: "+tbl_name); */
									var tblid = $('div[name="'+tbl_name+'"]').attr('id');
									/* console.log("tblid: "+tblid); */


									var tabactive = $( "#tables" ).tabs( "option", "active" );
									/* console.log('tabactive:'+tabactive); */
									var tabactivename = $("#tables ul li:nth-child("+(tabactive+1)+") a ").text();
									/* console.log("tabactive: "+tabactive); */

									if (tbl_name == tabactivename){

										/* ensure row exists */
										if (!$('div[name="'+tbl_name+'"] table tbody tr[id="'+rt_row+'"]').length){
											console.log('Insert rt_row: '+rt_row);
											$('div[name="'+tbl_name+'"] table tbody').append('<tr id="'+rt_row+'"><td class="ui-widget-header">'+(rt_row+1)+'</td></tr>');
										}

										var maxcount = 0;
										for (var k = 0; k < tabledata[tbl_name].length; k++) {
											/* ensure cells exists */
											var kcol_id = tabledata[tbl_name][k]['col_id'];
											if (!$('div[name="'+tbl_name+'"] table tbody tr[id="'+rt_row+'"] td[id="'+kcol_id+'-'+rt_row+'"]').length){
												/* console.log('Insert cell: '+kcol_id+'-'+rt_row); */
												$('div[name="'+tbl_name+'"] table tbody tr[id="'+rt_row+'"]').append('<td id="'+kcol_id+'-'+rt_row+'" val_id="" class="data-cell ui-state-default" colno="'+tblid+'-'+kcol_id+'">&nbsp;</td>');
												$('div[name="'+tbl_name+'"] table tbody tr[id="'+rt_row+'"] td[id="'+kcol_id+'-'+rt_row+'"]').on( "click", function() {
													table_cell_clicked($( this ));
												});
											}

											/* update column count */
											count = tabledata[tbl_name][k]["values"].length;
											/* console.log("count: "+count); */
											$('th[id="'+kcol_id+'"] span[class="ui-col-count"]').text("("+count+")");
											if (count>maxcount){
												maxcount = count
											}

											/* populate cell data */
											if (rt_row < count){

												editcell = $('div[name="'+tbl_name+'"]').find('#'+kcol_id+'-'+rt_row);
												if (!editcell.is("[currval]")){

													var value = tabledata[tbl_name][k]["values"][rt_row]["value"];
													var val_id = tabledata[tbl_name][k]["values"][rt_row]["val_id"];
													/* console.log("val_id: "+val_id+'  value: '+value); */

													editcell.empty();
													editcell.text(value);
													editcell.attr("val_id", val_id);
													if (!editcell.hasClass("has-value")){ editcell.toggleClass("has-value"); }
												}
											} else {
												/* depopulate cell data (ensure empty) */
												editcell = $('div[name="'+tbl_name+'"]').find('#'+kcol_id+'-'+rt_row);
												if (!editcell.is("[currval]")){
													editcell.empty();
													editcell.html("&nbsp;");
													editcell.attr("val_id", "");
													if (editcell.hasClass("has-value")){ editcell.toggleClass("has-value"); }
												}

											}

										}

										/* keep going? */
										if (rt_row < maxcount + 4) {
											var delay = 1;
											setTimeout(function(){
												refresh_table_data_row(rt_row+1, tabledata);
											}, delay);
										} else {
											refreshrunning = false;
											$("tr").filter(function() {
												return parseInt($(this).attr("id")) > (maxcount+4);
											}).remove();
										}

									}

								};"""



				# /* click to edit data values */
				message += """	function table_cell_clicked(cell) {
									console.log('td cell on click:');
									console.log(cell);
									console.log(cell.is("[lastclicked]"));
									if (cell.is("[lastclicked]")){
										console.log(cell.attr('lastclicked'));
										var lastclicked = cell.attr('lastclicked');
										console.log('lastclicked: '+lastclicked);
										var timediff = Date.now() - Number(lastclicked);
										console.log('timediff: '+timediff);
										if (timediff>300 && timediff<2000) {
											// enter edit mode
											var currval = "";
											if (cell.hasClass("has-value")){
												currval = cell.text();
											}
											console.log('currval: '+currval);
											cell.attr('currval', currval);
											cell.empty();
											cell.append("<input type='text' id='editcell'>");
											var inputfield = cell.find("#editcell");
											inputfield.val(currval);
											inputfield.focus();
											cell.removeAttr("lastclicked");
										} else {
											$("td[lastclicked]").removeAttr("lastclicked");
										}

									} else {
										// check if cell has input feild, if so do nothing
										if (!cell.find("#editcell").length){
											// next check if another cell has input feild, if so do end edit
											if ($("td[currval]").length){
												// exit cell edit
												var editcell = $("td[currval]");
												var prevval = editcell.attr("currval");
												var newval = editcell.find("#editcell").val();
												console.log('prevval: '+prevval+'	newval:'+newval);
												if (prevval != newval){
													// update cell value

													var val_id = editcell.attr("val_id");
													console.log('val_id: '+val_id);

													var colno = editcell.attr("colno");
													console.log('colno: '+colno);
													var columnname = $("th[colno='"+colno+"']").attr("name");
													console.log('columnname: '+columnname);

													var tbl_id = colno.split("-")[0];
													console.log('tbl_id: '+tbl_id);
													var tablename = $("#"+tbl_id).attr("name");
													console.log('tablename: '+tablename);

													var puturl = "";
													var resttype = 'PUT';
													if (val_id.length>0){
														if (newval.length<1){
															resttype = 'DELETE';
															puturl = "/"+tablename+"/"+columnname+"/"+val_id;
														} else {
															puturl = "/"+tablename+"/"+columnname+"/"+val_id+"/"+newval;
														}
													} else {
														puturl = "/"+tablename+"/"+columnname+"/"+newval;
													}
													console.log('resttype: '+resttype+'	puturl: '+puturl);
													$.ajax({
														url: puturl,
														type: resttype,
														dataType: 'json',
														success: function(data) {
															refresh();
														}
													});

												}
												editcell.empty();
												if (newval.length<1){
													editcell.html("&nbsp;");
													editcell.attr("val_id", "");
												} else {
													editcell.text(newval);
												}
												editcell.removeAttr("currval");
											}
											$("td[lastclicked]").removeAttr("lastclicked");
											cell.attr("lastclicked", Date.now());

										}
									}


								};"""

				message += """	function file_import_preview() {
									console.log("file_import_preview:");
									var file = $("#dialog-file-import-file").val();
									console.log("file_import_preview: file: "+file);
									var delim = $("#dialog-file-import-delimiter").val();
									console.log("file_import_preview: delim: '"+delim+"'");
									var hrow = $("#dialog-file-import-header-row").prop("checked");
									console.log("file_import_preview: hrow: "+hrow);
									var encd = $("#dialog-file-import-encoding").val();
									console.log("file_import_preview: encd: "+encd);
									var scmt = $("#dialog-file-import-comments").val();
									console.log("file_import_preview: scmt: "+scmt);

									if (scmt.length<1){
										scmt = false;
										console.log("file_import_preview: scmt: "+scmt);
									}

									console.log("file_import_preview: file obj: ");
									console.log($("#dialog-file-import-file")[0]['files'][0]);

									var config = {
										delimiter: delim,
										header: hrow,
										encoding: encd,
										comments: scmt,
										preview: 5,
										skipEmptyLines: true,
										complete: function(results) {
											console.log("Finished:", results.data);
											var keys = Object.keys(results.data[0])
											console.log(keys);
											console.log("file_import_preview: hrow: "+hrow);
											r = 0;
											$("#dialog-file-import-preview table").html("<tr id='preview-tablerow-"+r+"'></tr>");
											/* do columns */
											i = 0;

											var rowtemplate = `<tr id='preview-tablerow-zzrowzz'>`;
											for (var key in keys) {
												$("#preview-tablerow-"+r+"").append("<th class=\\"ui-widget-header\\"><input id=\\"preview-c"+i+"\\" type=\\"text\\" size=\\"10\\"></th>");
												console.log("#preview-c"+i+":", keys[key]);
												$("#preview-c"+i).val(keys[key]);
												rowtemplate += `<td id='preview-tablecell-zzrowzz-${i}' class=\\"data-cell ui-state-default\\">&nbsp;</td>`;

												i++;
											}
											rowtemplate += `</tr>`;
											console.log("rowtemplate:", rowtemplate);

											for (var row in results.data) {
												var rowdata = results.data[row];
												r++;
												/* $("#dialog-file-import-preview table").append("<tr id='preview-tablerow-"+r+"'></tr>"); */
												$("#dialog-file-import-preview table").append(rowtemplate.replace(/zzrowzz/g, r));
												console.log("rowtemplate:", rowtemplate.replace(/zzrowzz/g, r));

												i = 0;
												for (var key in rowdata) {
													/* $("#preview-tablerow-"+r+"").append("<td class=\\"ui-widget-header\\"><input id=\\"preview-c"+i+"\\" type=\\"text\\" size=\\"10\\"></th>"); */
													$("#preview-tablecell-"+r+"-"+i).text(rowdata[key].trim());
													i++;
												}
											}
										}
									}



									Papa.parse($("#dialog-file-import-file")[0]['files'][0], config);

								};"""

				# <tr><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><tr>


				# dialog-file-import-file
				# dialog-file-import-delimiter
				# dialog-file-import-header-row
				# dialog-file-import-encoding
				# dialog-file-import-comments
				message += """	function file_import_action() {
									console.log("file_import_action:");
									var file = $("#dialog-file-import-file").val();
									console.log("file_import_preview: file: "+file);
									var delim = $("#dialog-file-import-delimiter").val();
									console.log("file_import_preview: delim: '"+delim+"'");
									var hrow = $("#dialog-file-import-header-row").prop("checked");
									console.log("file_import_preview: hrow: "+hrow);
									var encd = $("#dialog-file-import-encoding").val();
									console.log("file_import_preview: encd: "+encd);
									var scmt = $("#dialog-file-import-comments").val();
									console.log("file_import_preview: scmt: "+scmt);

									if (scmt.length<1){
										scmt = false;
										console.log("file_import_preview: scmt: "+scmt);
									}

									console.log("file_import_preview: file obj: ");
									console.log($("#dialog-file-import-file")[0]['files'][0]);

									var size = $("#dialog-file-import-file")[0]['files'][0]['size'];
									console.log("file_import_preview: size: "+size);

									var tabactive = $( "#tables" ).tabs( "option", "active" );
									console.log('tabactive:'+tabactive);
									var tblname = $("#tables ul li:nth-child("+(tabactive+1)+") a ").text();
									console.log("tblname: "+tblname);

									/* 	# dialog-progress
										#  <div id="dialog-progress-bar"><div id="dialog-progress-msg"></div></div> */
									$("#dialog-progress-subject").text("Importing file: '"+$("#dialog-file-import-file")[0]['files'][0]['name']+"' into table: '"+tblname+"'");
									dlgProgress.dialog( \"open\" );
									$("#dialog-progress").css("min-height", "50px");
									$("#dialog-progress").prev().css("display","none");
									$("div[aria-describedby='dialog-progress']").css("top", "1%");
									$("div[aria-describedby='dialog-progress']").css("left", "1%");
									dlgProgressMsg = $("#dialog-progress-msg")
									dlgProgressMsg.text("Loading....");

									var colheads = $("#preview-tablerow-0 th input");
									console.log("file_import_preview: colheads: ",colheads);
									var columns = [];
									var col_name = "";
									for (var colno=0; colno<colheads.length; colno++){
										console.log("file_import_preview: colno: "+colno+"	colheads[colno]:", colheads[colno]);
										col_name = colheads[colno]['value'].trim();
										columns.push(col_name);
										/* PUT /<table name>/<column name> */

										var puturl = "/"+tblname+"/"+col_name;
										console.log("puturl:", puturl);
										$.ajax({
											url: puturl,
											dataType: 'text',
											type: 'put',
											success: function( data, textStatus, jQxhr ){
												console.log("Created col_name:", col_name);
											}
										});

									}
									console.log("columns: ", columns);
									var progresssize = 0;
									chunkprocessed = 0;

									var chunkInCount = 0;
									var chunkOutCount = 0;

									var config = {
										delimiter: delim,
										header: hrow,
										encoding: encd,
										comments: scmt,
										skipEmptyLines: true,
										worker: false,
										beforeFirstChunk: function(chunk) {
											var index = chunk.match( /\\r\\n|\\r|\\n/ ).index;
											var headings = chunk.substr(0, index).split( delim );
											for (var colno=0; colno<columns.length; colno++){
												headings[colno] = columns[colno];
											}
											return headings.join() + chunk.substr(index);
										},
										chunkSize: chunksize,
										chunk: function(results) {
											console.log("chunk:", results);
											console.log("chunk: data:", results.data);

											var posturl = "/"+tblname+"/papaparse";
											console.log("posturl:", posturl);

											var stbldata = JSON.stringify(results.data);
											console.log("stbldata:", stbldata);

											chunkInCount++;
											console.log("chunkInCount:", chunkInCount);

											$.ajax({
												url: posturl,
												dataType: 'text',
												type: 'post',
												data: stbldata,
												success: function( data, textStatus, jQxhr ){

													progresssize += chunksize;
													var pcnt = Math.round(progresssize/size * 100);
													if (pcnt>100){
														pcnt = 100;
														lastrow = true;
													}

													dlgProgressMsg.text(pcnt+"%");
													$("#dialog-progress").progressbar( "value", pcnt );
													chunkOutCount++;
													console.log("chunkOutCount:", chunkOutCount);
													if (chunkInCount==chunkOutCount){
														close_file_import_progress();
													}
												}
											});

										}
									}

									Papa.parse($("#dialog-file-import-file")[0]['files'][0], config);

								};"""

				message += """	function close_file_import_progress() {
									dlgProgressMsg.text(100+"%");
									$("#dialog-progress").progressbar( "value", 100 );
									setTimeout(function(){
										dlgProgress.dialog( \"close\" );
									}, 500);

									var tabactive = $( "#tables" ).tabs( "option", "active" );
									var tblname = $("#tables ul li:nth-child("+(tabactive+1)+") a ").text();
									console.log("tblname: "+tblname);
									refresh_table(tblname);
								};"""

				message += """	function file_import_delimiter_tab() {
									console.log("file_import_delimiter_tab: '	'");
									$("#dialog-file-import-delimiter").val("	");
									file_import_preview();
								};"""

				message += """	function file_export_delimiter_tab() {
									console.log("file_export_delimiter_tab: '	'");
									$("#dialog-file-export-delimiter").val("	");
									file_export_preview();
								};"""

				message += """	function file_export_preview() {
									console.log("file_export_preview:");
									var table = $("#export-file-table-name").val();
									var delim = $("#dialog-file-export-delimiter").val();
									if (delim.length<1){
										delim = ",";
									}

									fileext = "";
									switch(delim) {
										case ",":
  											fileext = ".csv";
											break;
										case "	":
  											fileext = ".tsv";
											break;
										default:
  											fileext = ".txt";
									}
									var d = new Date();
									var datestring = "_" + d.getFullYear() + ("0"+(d.getMonth()+1)).slice(-2) + ("0" + d.getDate()).slice(-2) + "_" + ("0" + d.getHours()).slice(-2) + ("0" + d.getMinutes()).slice(-2) + ("0" + d.getSeconds()).slice(-2);
									$("#dialog-file-export-filename").val(table + datestring + fileext);
									$("#dialog-file-export-preview textarea").val("loading table: "+table+" .......");

									var hrow = $("#dialog-file-export-header-row").prop("checked");

									var config = {
										delimiter: delim,
										header: hrow,
										skipEmptyLines: true
									}

									var geturl = "/"+table+"/papaparse";
									console.log("geturl:", geturl);
									$.ajax({
										url: geturl,
										success: function( data, textStatus, jQxhr ){

											window.URL = window.webkitURL || window.URL;

											console.log("data: ", data);
											$("#dialog-file-export-preview textarea").val("parseing table data: "+table+" .......");
											var text = Papa.unparse(data, config);
											$("#dialog-file-export-preview textarea").val(text);

											var output = $("#dialog-file-export output");
											var prevLink = $("#dialog-file-export output a");
											if (prevLink) {
												window.URL.revokeObjectURL(prevLink.href);
												$("#dialog-file-export output a").remove();
											}

											const MIME_TYPE = 'text/plain';
  											var bb = new Blob([text], {type: MIME_TYPE});

											var a = document.createElement('a');
											a.download = $("#dialog-file-export-filename").val();
											a.href = window.URL.createObjectURL(bb);
											a.textContent = 'Download ready';

											a.dataset.downloadurl = [MIME_TYPE, a.download, a.href].join(':');
											output.append(a);


										}
									});

								};"""



				message += "</script>"

				message += "<style>"
				message += "#buttonbar { float: right; }"
				message += "#version   { float: left; font-size: 30%; }"
				message += "#title     { float: left; }"
				message += "</style>"

				message += "<title>Test Data Table</title>"
				message += "</head>"
				message += "<body>"

				#
				# Dialogues
				#
				message += "<div id=\"dialog-new-table\" title=\"Create table\">"
				message += "<div>Create a new table</div>"
				message += "  <label for='table-name'>Table Name:</label>"
				message += "  <input id='table-name' type='text'>"
				message += "</div>"

				message += "<div id=\"dialog-delete-table\" title=\"Delete table?\">"
				message += "<div>Are you sure you want to delete the table \""
				message += "<span id='delete-table-name'></span>"
				message += "\"?</div>"
				message += "</div>"

				message += "<div id=\"dialog-add-column\" title=\"Add Column\">"
				# column-table-name
				message += "<div>Add column to table \""
				message += "<span id='column-table-name'></span>"
				message += "\"</div>"
				message += "  <label for='column-name'>Column Name:</label>"
				message += "  <input id='column-name' type='text'>"
				message += "</div>"

				message += "<div id=\"dialog-delete-column\" title=\"Delete column?\">"
				message += "<div>Are you sure you want to delete the column \""
				message += "<span id='delete-column-name'></span>"
				message += "\" from table \"<span id='delete-column-table'></span>"
				message += "\"?</div>"
				message += "</div>"


				message += """	<div id="dialog-progress" title="Progress">
									<div id="dialog-progress-subject">Progress</div>
									<!-- <br /> -->
									<div id="dialog-progress-bar"><div id="dialog-progress-msg" class="progress-label"></div></div>
								</div>"""

				message += """	<div id="dialog-file-import" title="Text File Import">
									<table>
									<tr><td colspan="5">
										<label for='dialog-file-import-file'>Select File:</label>
										<input id='dialog-file-import-file' type='file'>
									</td></tr>
									<tr><td>
										<label for='dialog-file-import-delimiter'>File Delimiter:</label>
										<input id='dialog-file-import-delimiter' type='text' size='5' maxlength='1' placeholder='auto'>
										<a href="javascript:file_import_delimiter_tab();" id='dialog-file-import-insert-tab'>tab</a>
									</td><td>
										<label for='dialog-file-import-header-row'>Header Row:</label>
										<input id='dialog-file-import-header-row' type='checkbox' checked='true'>
									</td><td>
										<label for='dialog-file-import-encoding'>Encoding:</label>
										<input type="text" id="dialog-file-import-encoding" placeholder="default" size="7">
									</td><td>
										<label for='dialog-file-import-comments'>Comment char:</label>
										<input type="text" size="7" maxlength="10" placeholder="default" id="dialog-file-import-comments">
									</td></tr>
									</table>
									<br>
									<div>Preview:</div>
									<div id='dialog-file-import-preview' style="overflow-x: auto;">
										<table>
											<thead>
												<tr>
													<th class="ui-widget-header"><input id="preview-c1" type="text" value="Column 1" size="10"></th>
													<th class="ui-widget-header"><input id="preview-c2" type="text" value="Column 2" size="10"></th>
													<th class="ui-widget-header"><input id="preview-c3" type="text" value="Column 3" size="10"></th>
													<th class="ui-widget-header"><input id="preview-c4" type="text" value="Column 4" size="10"></th>
													<th class="ui-widget-header"><input id="preview-c5" type="text" value="Column 5" size="10"></th>
												<tr>
											</thead>
										<tbody>
											<tr><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><tr>
											<tr><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><tr>
											<tr><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><tr>
											<tr><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><tr>
											<tr><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><td class="data-cell ui-state-default">&nbsp;</td><tr>
										</tbody>
										</table>
									</div>
								</div>"""

				message += """	<div id="dialog-file-export" title="Text File Export">
									<table>
									<tr><td>
										<label for='dialog-file-export-delimiter'>File Delimiter:</label>
										<input id='dialog-file-export-delimiter' type='text' size='5' maxlength='1' placeholder='auto'>
										<a href="javascript:file_export_delimiter_tab();" id='dialog-file-export-insert-tab'>tab</a>
									</td><td>
										<label for='dialog-file-export-header-row'>Header Row:</label>
										<input id='dialog-file-export-header-row' type='checkbox' checked='true'>
									</td></tr>
									<tr><td colspan="5">
										<label for='dialog-file-export-filename'>Output File:</label>
										<input id='dialog-file-export-filename' type='text' size='60'>
									</td></tr>
									</table>
									<input id='export-file-table-name' type='hidden'>
									<br>
									<div>Preview:</div>
									<div id='dialog-file-export-preview' style="overflow-x: auto;">
									<textarea class='data-cell ui-state-default' disabled='' rows='6' cols='80' style='resize:none;'></textarea>
									</div>
									<output style="display: None;"></output>
								</div>"""



				#
				# Main page
				#
				#version font-size: 30%;
				# <fieldset>
				# message += "<div id=\"title\" class=\"ui-widget\">Test Data Table</div>"
				# message += "<div id=\"version\" class=\"ui-state-disabled ui-widget\">Version " + core.version + "</div>"
				message += "<div id=\"buttonbar\">"
				# message += "	<button>Test Data Table</button>" # spacer
				# message += "	<button disabled><span style=\"font-size: 30%;\">Version "+core.version+"</span>&nbsp;</button>"
				message += "	<button id='new-table' class=\"ui-button ui-widget ui-corner-all ui-button-icon-only\" title=\"Add Table\"><span class=\"ui-icon ui-icon-calculator\"></span>Add Table</button>"
				message += "	<button id='new-column' class=\"ui-button ui-widget ui-corner-all ui-button-icon-only\" title=\"Add Column\"><span class=\"ui-icon ui-icon-grip-solid-vertical\"></span>Add Column</button>"
				message += "	<button>&nbsp;</button>" # spacer

				message += """	<button id='import-file' class='ui-button ui-widget ui-corner-all ui-button-icon-only' title="Import File">
									<span class='ui-icon ui-icon-folder-open'></span>
									Import File</button> """

				message += """	<button id='export-file' class='ui-button ui-widget ui-corner-all ui-button-icon-only' title="Export File">
									<span class='ui-icon ui-icon-disk'></span>
									Export File</button> """

				message += "	<button>&nbsp;</button>" # spacer
				message += "	<select id='auto-refresh'>"
				message += "		<option value='0' >Auto Refresh Off</option>"
				message += "		<option value='5' >Auto Refresh 5 seconds</option>"
				message += "		<option value='10' >Auto Refresh 10 seconds</option>"
				message += "		<option value='30' >Auto Refresh 30 seconds</option>"
				message += "		<option value='60' >Auto Refresh 1 minute</option>"
				message += "	</select>"
				message += "	<button id='refresh' class=\"ui-button ui-widget ui-corner-all ui-button-icon-only\" title=\"Refresh\"><span class=\"ui-icon ui-icon-refresh\"></span>Refresh</button>"
				message += "	<button id='help' class=\"ui-button ui-widget ui-corner-all ui-button-icon-only\" title=\" Help\nv" + core.version + "\"><span class=\"ui-icon ui-icon-help\"></span>Help</button>"
				message += "</div>"

				message += "<div style=\"height: 5%;\">"
				message += "</div>"

				message += "<div id='tables'>"
				message += "<ul>"
				message += "</ul>"
				message += "</div>"

				message += "</body>"
				message += "</html>"

			core.debugmsg(8, "parsed_path:", parsed_path)
			filename, fileext = os.path.splitext(parsed_path.path)
			core.debugmsg(8, "fileext:", fileext)
			if not pathok and len(fileext)>0:
				localfile = "."+parsed_path.path
				core.debugmsg(8, "localfile:", localfile)
				core.debugmsg(8, "path.exists:", os.path.exists(localfile))
				if os.path.exists(localfile):
					pathok = True
					core.debugmsg(8, "pathok:", pathok)

					core.debugmsg(9, "httpcode:", httpcode)
					self.send_response(httpcode)
					self.send_header("Server", "Test Data Table v"+core.version)
					self.end_headers()
					with open(localfile,"rb") as f:
						core.debugmsg(8, "file open for read")
						self.wfile.write(f.read())
					return


			core.debugmsg(8, "parsed_path:", parsed_path)
			if not pathok and parsed_path.path == '/tables':
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
				core.debugmsg(6, "tablename:", tablename)

				if columnname == "papaparse":
					tableid = core.table_exists(tablename)
					core.debugmsg(9, "tableid:", tableid)
					if tableid:
						pathok = True
						httpcode = 200

						jsonresp = []

						columnnames = core.table_columns(tablename)
						i = 0
						for col in columnnames:
							core.debugmsg(9, "col:", col)
							columndata = core.column_values(tablename, col["column"])
							core.debugmsg(9, "columndata:", columndata)
							j = 0
							for val in columndata:
								core.debugmsg(9, "val:", val)
								core.debugmsg(9, "j:", j, "	len(jsonresp):",len(jsonresp))
								if len(jsonresp)-1 < j:
									newrow = {}
									core.debugmsg(9, "newrow:", newrow)
									jsonresp.append(newrow)
								jsonresp[j][col["column"]] = val['value']
								j += 1

							# core.debugmsg(9, "jsonresp:", jsonresp)
							i += 1

						message = json.dumps(jsonresp)

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
				core.debugmsg(6, "columnid:", columnid)
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


				if columnname.isdigit():
					rownum = int(columnname)
					tableid = core.table_exists(tablename)
					core.debugmsg(8, "tableid:", tableid)
					if tableid:
						# pathok = True
						# httpcode = 200

						jsonresp = {}
						jsonresp[tablename] = {}

						columns = core.table_columns(tablename)
						core.debugmsg(8, "columns:", columns)
						for col in columns:
							core.debugmsg(8, "col:", col)
							column_name = col["column"]
							core.debugmsg(8, "column_name:", column_name)
							colvalues = core.column_values(tablename, column_name)
							core.debugmsg(8, "colvalues:", colvalues)
							core.debugmsg(8, "len(colvalues):", len(colvalues), "	rownum:", rownum)
							if len(colvalues) > rownum:
								pathok = True
								httpcode = 200
								valueid = colvalues[rownum]['val_id']
								core.debugmsg(8, "valueid:", valueid)

								data = core.value_consume_byid(tablename, column_name, valueid)
								if data is not None:
									jsonresp[tablename][column_name] = data["value"]


							else:
								jsonresp[tablename][column_name] = None

							# val_data = core.value_consume(tablename, column_name)
							# core.debugmsg(9, "val_data:", val_data)
							# if val_data is None:
							# 	jsonresp[tablename][column_name] = None
							# else:
							# 	jsonresp[tablename][column_name] = val_data["value"]

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

		try:
			core.debugmsg(9, "httpcode:", httpcode)
			self.send_response(httpcode)
			self.send_header("Server", "Test Data Table v"+core.version)
			self.end_headers()
			core.debugmsg(9, "message:", message)
			if message is not None:
				self.wfile.write(bytes(message,"utf-8"))
		except BrokenPipeError as e:
			core.debugmsg(8, "Browser lost connection, probably closed by user")
		except Exception as e:
			core.debugmsg(6, "do_PUT:", e)

		return
	def handle_http(self):
		core.debugmsg(7, " ")
		return
	def respond(self):
		core.debugmsg(7, " ")
		return

	# 	log_request is here to stop BaseHTTPRequestHandler logging to the console
	# 		https://stackoverflow.com/questions/10651052/how-to-quiet-simplehttpserver/10651257#10651257
	def log_request(self, code='-', size='-'):
		core.debugmsg(7, " ")
		pass

class TDT_Core:
	version="0.2.3"
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

		if 'DBFile' not in self.config['Server']:
			self.config['Server']['DBFile'] = "TestDataTable.sqlite3"
			self.saveini()


		if 'Resources' not in self.config:
			self.config['Resources'] = {}
			self.saveini()

		if 'js_jquery' not in self.config['Resources']:
			self.config['Resources']['js_jquery'] = 'https://unpkg.com/jquery@latest/dist/jquery.min.js'
			self.saveini()

		if 'js_jqueryui' not in self.config['Resources']:
			self.config['Resources']['js_jqueryui'] = 'https://code.jquery.com/ui/1.12.1/jquery-ui.min.js'
			self.saveini()

		if 'css_jqueryui' not in self.config['Resources']:
			self.config['Resources']['css_jqueryui'] = 'https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css'
			self.saveini()

		if 'js_papaparse' not in self.config['Resources']:
			self.config['Resources']['js_papaparse'] = 'https://unpkg.com/papaparse@latest/papaparse.min.js'
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
			dbfile = os.path.join(self.config['Server']['DataDir'], self.config['Server']['DBFile'])
			if not os.path.exists(dbfile):
				createschema = True
			# chaning this setting did help to speed up bulk inserts a little, but it
			# 	also slowed individual inserts, selects, deletes etc a lot!
			# I'll leave this here as we may want to try tuning this later, maybe a value of 200 or 500
			# 	might be optimal, 1000 is definatly too big, I think 500 might be too big as well.
			# 	But 200 might not be enought to make an appreciable speed up in bulk inserts. will need some testing
			queue_size = 100 # use default value
			# queue_size = 1000 # default is 100
			self.db = Sqlite3Worker(dbfile, queue_size)
			if createschema:
				# result = self.db.execute("CREATE TABLE tdt_tables (ID INTEGER, table_name TEXT, deleted DATETIME, PRIMARY KEY(ID AUTOINCREMENT))")
				result = self.db.execute("CREATE TABLE tdt_tables (ID TEXT, table_name TEXT, deleted DATETIME, PRIMARY KEY(ID))")
				self.debugmsg(6, "CREATE TABLE tdt_tables", result)

				# result = self.db.execute("CREATE TABLE tdt_columns (ID INTEGER, table_id NUMBER, column_name TEXT, deleted DATETIME, PRIMARY KEY(ID AUTOINCREMENT))")
				result = self.db.execute("CREATE TABLE tdt_columns (ID TEXT, table_id NUMBER, column_name TEXT, deleted DATETIME, PRIMARY KEY(ID))")
				self.debugmsg(6, "CREATE TABLE tdt_columns", result)

				# result = self.db.execute("CREATE TABLE tdt_data (ID INTEGER, column_id NUMBER, value TEXT, deleted DATETIME, PRIMARY KEY(ID AUTOINCREMENT))")
				result = self.db.execute("CREATE TABLE tdt_data (ID TEXT, column_id NUMBER, value TEXT, deleted DATETIME, PRIMARY KEY(ID))")
				self.debugmsg(6, "CREATE TABLE tdt_data", result)

				#  create indexes

				result = self.db.execute("CREATE INDEX \"tables_name\" ON \"tdt_tables\" (\"table_name\");")
				result = self.db.execute("CREATE INDEX \"tables_del\" ON \"tdt_tables\" (\"deleted\");")

				result = self.db.execute("CREATE INDEX \"columns_name\" ON \"tdt_columns\" (\"column_name\");")
				result = self.db.execute("CREATE INDEX \"columns_tbl_id\" ON \"tdt_columns\" (\"table_id\");")
				result = self.db.execute("CREATE INDEX \"columns_del\" ON \"tdt_columns\" (\"deleted\");")

				result = self.db.execute("CREATE INDEX \"data_value\" ON \"tdt_data\" (\"value\");")
				result = self.db.execute("CREATE INDEX \"data_col_id\" ON \"tdt_data\" (\"column_id\");")
				result = self.db.execute("CREATE INDEX \"data_del\" ON \"tdt_data\" (\"deleted\");")

				createschema = False
			# Never do this it changes the row id's and breaks the data
			else:
				# VACUUM frees up space and defragments the file, especially after large deletes
				results = self.db.execute("VACUUM")
				self.debugmsg(9, "VACUUM: results:", results)
				self.db.close()
				self.db = None
				self.db = Sqlite3Worker(dbfile)



		self.debugmsg(5, "run_web_server")
		self.webserver = threading.Thread(target=self.run_web_server)
		self.webserver.start()

		self.debugmsg(9, "end __init__")

	def mainloop(self):
		self.debugmsg(7, " ")
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
		self.debugmsg(7, " ")


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
		self.debugmsg(7, " ")
		# remove records where the deleted column has had a value set for more than 600 seconds (10 min)
		#   aka cleanup deleted records

		# -- identify records for cleanup
		# -- SELECT * FROM tdt_tables WHERE deleted < (strftime('%s', 'now') - 600)
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
		self.debugmsg(7, others)
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
		self.debugmsg(7, " ")
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
		self.debugmsg(7, " ")
		tables = []
		results = core.db.execute("SELECT ID, table_name from tdt_tables where deleted is NULL")
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
		self.debugmsg(7, tablename)
		# returns the table id if exists, else returns False
		id = False
		try:
			results = self.db.execute("SELECT ID, table_name FROM tdt_tables WHERE table_name = ? and deleted is NULL", [tablename])
			self.debugmsg(9, "results:", results)
			if len(results)>0:
				id = results[0][0]
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return id

	def table_create(self, tablename):
		self.debugmsg(7, tablename)
		# creates the table
		try:
			tableid = self.table_exists(tablename)
			self.debugmsg(9, "tableid:", tableid)
			if not tableid:
				results = self.db.execute("INSERT INTO tdt_tables (ID, table_name) VALUES (?,?)", [uuid.uuid4().hex, tablename])
				self.debugmsg(9, "results:", results)
				if results is None:
					return self.table_exists(tablename)
		except Exception as e:
			self.debugmsg(6, "Exception:", e)
		return False

	def table_columns(self, tablename):
		self.debugmsg(7, tablename)
		columns = []
		try:
			tableid = self.table_exists(tablename)
			self.debugmsg(9, "tableid:", tableid)
			if tableid:
				# results = self.db.execute("SELECT ID, table_id, column_name FROM tdt_columns WHERE table_id = ? and deleted is NULL", [tableid])
				results = self.db.execute(
					"SELECT c.ID, c.table_id, c.column_name, count(d.id) 'count' "
					"FROM tdt_columns c "
					"LEFT JOIN tdt_data d on c.id = d.column_id "
					"WHERE c.table_id = ? and c.deleted is NULL "
					"GROUP BY d.column_id "
					, [tableid])
				self.debugmsg(9, "results:", results)
				if len(results)>0:
					for res in results:
						self.debugmsg(8, "res:", res)
						retcol = {}
						retcol["column"] = res[2]
						retcol["col_id"] = res[0]
						retcol["count"] = res[3]
						columns.append(retcol)
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return columns

	def table_delete(self, tablename):
		self.debugmsg(7, tablename)
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
				res_table = core.db.execute("UPDATE tdt_tables SET deleted = strftime('%s', 'now') WHERE ID=?", [tableid])
				core.debugmsg(9, "res_table:", res_table)
				if res_table is None:
					return True
			else:
				return True
		except Exception as e:
			self.debugmsg(6, "Exception:", e)
		return False

	def column_exists(self, tablename, columnname):
		self.debugmsg(7, tablename, columnname)
		# returns the column id if exists, else returns False
		id = False
		try:
			tableid = self.table_exists(tablename)
			self.debugmsg(9, "tableid:", tableid)
			if tableid:
				results = self.db.execute("SELECT ID, table_id, column_name FROM tdt_columns WHERE table_id = ? and column_name = ? and deleted is NULL", [tableid, columnname])
				self.debugmsg(9, "results:", results)
				if len(results)>0:
					id = results[0][0]
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return id

	def column_create(self, tablename, columnname):
		self.debugmsg(7, tablename, columnname)
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
					results = self.db.execute("INSERT INTO tdt_columns (ID, table_id, column_name) VALUES (?,?,?)", [uuid.uuid4().hex, tableid, columnname])
					self.debugmsg(9, "results:", results)
					if results is None:
						return self.column_exists(tablename, columnname)
			else:
				return columnid
		except Exception as e:
			self.debugmsg(6, "Exception:", e)
		return False

	def column_values(self, tablename, columnname):
		self.debugmsg(7, tablename, columnname)
		values = []
		try:
			columnid = self.column_exists(tablename, columnname)
			self.debugmsg(8, "columnid:", columnid)
			if columnid:
				results = self.db.execute("SELECT ID, column_id, value FROM tdt_data WHERE column_id = ? and deleted is NULL", [columnid])
				self.debugmsg(8, "results:", results)
				if len(results)>0:
					for res in results:
						self.debugmsg(8, "res:", res)
						retcol = {}
						retcol["value"] = res[2]
						retcol["val_id"] = res[0]
						values.append(retcol)
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return values

	def column_delete(self, tablename, columnname):
		self.debugmsg(7, tablename, columnname)
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
				res_columns = core.db.execute("UPDATE tdt_columns SET deleted = strftime('%s', 'now') WHERE ID = ?", [columnid])
				core.debugmsg(9, "res_columns:", res_columns)
				if res_columns is None:
					return True

			else:
				return True
		except Exception as e:
			self.debugmsg(6, "Exception:", e)
		return False

	def value_exists(self, tablename, columnname, value):
		self.debugmsg(7, tablename, columnname, value)
		# returns the value id if exists, else returns False
		# 	useful for add if unique
		id = False
		try:
			columnid = self.column_exists(tablename, columnname)
			if columnid:
				results = self.db.execute("SELECT ID, column_id, value FROM tdt_data WHERE column_id = ? and (value = ? or ID = ?) and deleted is NULL", [columnid, value, value])
				self.debugmsg(9, "results:", results)
				if len(results)>0:
					id = results[0][0]
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return id

	def value_create(self, tablename, columnname, value):
		self.debugmsg(7, tablename, columnname, value)
		# creates the value
		try:
			columnid = self.column_exists(tablename, columnname)
			self.debugmsg(9, "columnid:", columnid)
			if not columnid:
				columnid = self.column_create(tablename, columnname)
				self.debugmsg(9, "columnid:", columnid)
			if columnid:
				results = self.db.execute("INSERT INTO tdt_data (ID, column_id, value) VALUES (?,?,?)", [uuid.uuid4().hex, columnid, value])
				self.debugmsg(9, "results:", results)
				if results is None:
					return self.value_exists(tablename, columnname, value)
		except Exception as e:
			self.debugmsg(6, "Exception:", e)
		return False

	def value_delete(self, tablename, columnname, value):
		self.debugmsg(7, tablename, columnname, value)
		try:
			valueid = self.value_exists(tablename, columnname, value)
			core.debugmsg(9, "valueid:", valueid)
			if valueid:
				res_data = core.db.execute("UPDATE tdt_data SET deleted = strftime('%s', 'now') WHERE ID = ?", [valueid])
				core.debugmsg(9, "res_data:", res_data)
				if res_data is None:
					return True
			else:
				return True
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return False

	def value_consume(self, tablename, columnname):
		self.debugmsg(7, tablename, columnname)
		try:
			columnid = self.column_exists(tablename, columnname)
			self.debugmsg(9, "columnid:", columnid)
			if columnid:
				# sqlite3.Warning: You can only execute one statement at a time.
				# 	Also didn't return any result
					# txn = ""
					# txn += "BEGIN TRANSACTION; \n\n"
					# txn += "CREATE TEMP TABLE _ConsumeValue AS \n"
					# txn += "SELECT * FROM tdt_data \n"
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
				results = self.db.execute("SELECT * FROM tdt_data WHERE deleted is NULL AND column_id = ? LIMIT 1;", [columnid])
				self.debugmsg(9, "results:", results)
				if len(results)>0:
					retval["val_id"] = results[0][0]
					resultu = self.db.execute("UPDATE tdt_data SET deleted = strftime('%s', 'now') WHERE ID = ?;", [retval["val_id"]])
					self.debugmsg(9, "resultu:", resultu)
					retval["value"] = results[0][2]
					return retval
			else:
				return None
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return None

	def value_consume_byid(self, tablename, columnname, value):
		self.debugmsg(7, tablename, columnname, value)
		try:
			val_id = self.value_exists(tablename, columnname, value)
			self.debugmsg(9, "val_id:", val_id)
			if val_id:
				retval = {}
				resultu = self.db.execute("UPDATE tdt_data SET deleted = strftime('%s', 'now') WHERE ID = ?;", [val_id])
				self.debugmsg(9, "resultu:", resultu)

				results = self.db.execute("SELECT * FROM tdt_data WHERE ID = ?;", [val_id])
				self.debugmsg(9, "results:", results)
				retval["val_id"] = results[0][0]
				retval["value"] = results[0][2]
				return retval
			else:
				return None
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return None

	def value_replace_byid(self, tablename, columnname, id, value):
		self.debugmsg(7, tablename, columnname, id, value)
		try:
			val_id = self.value_exists(tablename, columnname, id)
			self.debugmsg(9, "val_id:", val_id)
			if val_id:
				resultu = self.db.execute("UPDATE tdt_data SET value = ? WHERE ID = ?;", [value, val_id])
				self.debugmsg(9, "resultu:", resultu)
				if resultu is None:
					return True
				else:
					return False
			else:
				return False
		except Exception as e:
			self.debugmsg(6, "Exception:", e)

		return False



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
