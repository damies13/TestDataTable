

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
		self.send_response(httpcode)
		self.end_headers()
		self.wfile.write(bytes(message,"utf-8"))
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
		self.send_response(httpcode)
		self.end_headers()
		self.wfile.write(bytes(message,"utf-8"))
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

		except Exception as e:
			core.debugmsg(6, "Exception:", e)
			httpcode = 500
			message = str(e)
		self.send_response(httpcode)
		self.end_headers()
		self.wfile.write(bytes(message,"utf-8"))
		return
	def do_GET(self):
		core.debugmsg(7, " ")
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

				message += """	<style>
								.ui-tabs .ui-tabs-panel {
									padding: 0em 0em;
								}

								.tableFixHead          { overflow-y: auto; height: 80%; }
								.tableFixHead thead    { position: sticky; top: 0; background:#f6f6f6; width: 100%;}	/* background:#e9e9e9; */
								.tableFixHead thead th { position: sticky; top: 0; }
								/* .tableFixHead thead th span.ui-icon-close { margin-top: -.8em; margin-right: -.7em; float: right;} */
								.tableFixHead thead th span { float: left; }
								/* .tableFixHead thead th span.ui-icon-close { position: absolute; top: 2px; right: -1px; } */
								.tableFixHead thead th span.ui-icon-close { position: absolute; top: 5px; right: 0px; }


								/* Just common table stuff. Really. */
								/* table  { width: 100%; } */
								/* table  { border-collapse: collapse; width: 100%; } */
								/* table  { border-collapse: collapse; } */
								th, td { padding: 5px 10px; }
								th     {  border: 1px solid #c5c5c5; color: #454545; padding: 10px 15px 5px 10px;}	/* background:#f6f6f6; */
								td.data-cell { background: #e6e6e6; border: 1px solid #c5c5c5; color: #454545; }
								td.has-value { background: #fefefe; border: 1px solid #c5c5c5; color: #454545; }

								</style> """



				message += "<script>"
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
				message += "					success: function(data) {"
				message += "						var colhead = $('div[name=\"'+tblname+'\"]').find('th[name=\"'+colname+'\"]');"
				message += "						var colno = colhead.attr('colno');"
				message += "						$('td[colno=\"'+colno+'\"]').remove();"
				message += "						colhead.remove();"
				message += "						refresh_table(tblname);"
				message += "					}"
				message += "				});"
				message += "				$( this ).dialog( \"close\" );"
				message += "			},"
				message += "			Cancel: function() {"
				message += "				$( this ).dialog( \"close\" );"
				message += "			}"
				message += "		}"
				message += "	});"


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

				message += "	$( \"#refresh\" ).button().on( \"click\", function() {"
				message += "		refresh();"
				message += "	});"

				message += "	$( \"#help\" ).button().on( \"click\", function() {"
				message += "		window.open(\"https://github.com/damies13/TestDataTable/blob/master/Doc/rest_api.md#rest-api\");"
				message += "	});"

				message += "});"


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
									console.log("activetbl: "+activetbl);
									refresh_table(activetbl);

								};"""

				message += """	function refresh_table(tablename) {
									console.log("refresh_table: tablename:"+tablename);
									$.getJSON(tablename, function(tabledata) {
										refresh_table_data(tabledata);
									});
								};"""

				message += """	function refresh_table_data(tabledata) {
									console.log("refresh_table_data: tabledata:");
									console.log(tabledata);
									var tbl_name = Object.keys(tabledata)[0];
									console.log("tbl_name: "+tbl_name);
									var tblid = $('div[name="'+tbl_name+'"]').attr('id');
									console.log("tblid: "+tblid);
									console.log($('div[name="'+tbl_name+'"] table').length);
									if (!$('div[name="'+tbl_name+'"] table').length){
										// console.log($('div[name="'+tbl_name+'"]'));
										$('div[name="'+tbl_name+'"]').append('<table id=\"table-'+tblid+'\"><thead><tr></tr></thead><tbody></tbody></table>');
									}
									var r = 0;
									for (var i = 0; i < tabledata[tbl_name].length; i++) {
										var col_name = tabledata[tbl_name][i]["column"];
										var col_id = tabledata[tbl_name][i]["col_id"];
										console.log("col_name: "+col_name);
										if (!$('table[id="table-'+tblid+'"] thead tr th[name="'+col_name+'"]').length){
											$('table[id="table-'+tblid+'"] thead tr').append('<th id="'+col_id+'" name="'+col_name+'" colno="'+tblid+'-'+i+'"><span column="'+col_name+'" class="ui-icon ui-icon-close" role="presentation">Remove Column</span><span>'+col_name+'</span></div></th>');
										}

										// for each value in column
										var count = 0;
										console.log("count: "+count);
										count = tabledata[tbl_name][i]["values"].length;
										console.log("count: "+count);
										for (var j=0; j < count; j++){
											r=j;
											var value = tabledata[tbl_name][i]["values"][j]["value"];
											var val_id = tabledata[tbl_name][i]["values"][j]["val_id"];
											console.log("val_id: "+val_id+'  value: '+value);
											// make sure table row exists
											if (!$('div[name="'+tbl_name+'"] table tbody tr[id="'+j+'"]').length){
												console.log('Insert row: '+j);
												$('div[name="'+tbl_name+'"] table tbody').append('<tr id="'+j+'"></tr>');
											}
											// insert blank cells if not exist
											for (var k = 0; k < tabledata[tbl_name].length; k++) {
												if (!$('div[name="'+tbl_name+'"] table tbody tr[id="'+j+'"] td[id="'+k+'-'+j+'"]').length){
													console.log('Insert cell: '+k+'-'+j);
													$('div[name="'+tbl_name+'"] table tbody tr[id="'+j+'"]').append('<td id="'+k+'-'+j+'" val_id="" class="data-cell" colno="'+tblid+'-'+k+'">&nbsp;</td>');
												}
											}
											// update cell data
											console.log('update cell: '+i+'-'+j);
											editcell = $('div[name="'+tbl_name+'"]').find('#'+i+'-'+j);
											editcell.text(value);
											editcell.attr("val_id", val_id);
											if (!editcell.hasClass("has-value")){ editcell.toggleClass("has-value"); }


										}
									}
									console.log('r: '+r);
									if (r>0){ r += 1; }
									for (var i = 0; i < tabledata[tbl_name].length; i++) {
										var count = 0;
										console.log("count: "+count);
										count = r+5;
										console.log("count: "+count);
										for (var j=r; j < count; j++){
											if (!$('div[name="'+tbl_name+'"] table tbody tr[id="'+j+'"]').length){
												console.log('Insert row: '+j);
												$('div[name="'+tbl_name+'"] table tbody').append('<tr id="'+j+'"></tr>');
											}
											for (var k = 0; k < tabledata[tbl_name].length; k++) {
												if (!$('div[name="'+tbl_name+'"] table tbody tr[id="'+j+'"] td[id="'+k+'-'+j+'"]').length){
													console.log('Insert cell: '+k+'-'+j);
													$('div[name="'+tbl_name+'"] table tbody tr[id="'+j+'"]').append('<td id="'+k+'-'+j+'" val_id="" class="data-cell" colno="'+tblid+'-'+k+'">&nbsp;</td>');
												}
											}
										}
									}

								};"""


				message += "</script>"

				message += "<style>"
				message += "#buttonbar { float: right; }"
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


				#
				# Main page
				#

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
		self.debugmsg(7, tablename)
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
		self.debugmsg(7, tablename)
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
		self.debugmsg(7, tablename)
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
		self.debugmsg(7, tablename, columnname)
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
					results = self.db.execute("INSERT INTO tdt_columns (table_id, column_name) VALUES (?,?)", [tableid, columnname])
					self.debugmsg(9, "results:", results)
					if results is None:
						return self.column_exists(tablename, columnname)
		except Exception as e:
			self.debugmsg(6, "Exception:", e)
		return False

	def column_values(self, tablename, columnname):
		self.debugmsg(7, tablename, columnname)
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
		self.debugmsg(7, tablename, columnname, value)
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
		self.debugmsg(7, tablename, columnname, value)
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
		self.debugmsg(7, tablename, columnname, value)
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
		self.debugmsg(7, tablename, columnname, value)
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

	def value_replace_byid(self, tablename, columnname, id, value):
		self.debugmsg(7, tablename, columnname, id, value)
		try:
			val_id = self.value_exists(tablename, columnname, id)
			self.debugmsg(9, "val_id:", val_id)
			if val_id:
				resultu = self.db.execute("UPDATE tdt_data SET value = ? WHERE rowid = ?;", [value, val_id])
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
