*** Settings ***
Library       REST    localhost

*** Test cases ***
Create Table regression 1
	PUT	/regression+1
	Output
	Number	response status	201
	${msg}	Output	$.message
	Should Be Equal	"${msg}"	"table regression 1 created"

Show Tables
	GET	/tables
	Output
	Number	response status	200

Table regression 1 exists
	GET	/tables
	Output
	Number	response status	200
	${tbl_id}	Output	$.tables[?(@.table=="regression 1")].id
	${tbl_name}	Output	$.tables[?(@.table=="regression 1")].table
	Should Be Equal	"${tbl_name}"	"regression 1"

Create Table regression 1 again
	PUT	/regression+1
	Output
	Number	response status	200
	${msg}	Output	$.message
	Should Be Equal	"${msg}"	"table regression 1 exists"
	GET	/tables
	Number	response status	200
	${tbl_name}	Output	$.tables[?(@.table=="regression 1")].table
	Should Be Equal	"${tbl_name}"	"regression 1"

Create Column Col_A
	PUT	/regression+1/Col_A
	Output
	# Expect Response	{ "status": "200" }	merge=true
	Number	response status	201
	${msg}	Output	$.message
	Should Be Equal	"${msg}"	"column Col_A created"

Create Column Col_A again
	PUT	/regression+1/Col_A
	Output
	# Expect Response	{ "status": "200" }	merge=true
	Number	response status	200
	${msg}	Output	$.message
	Should Be Equal	"${msg}"	"column Col_A exists"


Create Column Col_B and Col_C
	PUT	/regression+1/Col_B
	Output
	Number	response status	201
	PUT	/regression+1/Col_C
	Output
	Number	response status	201

Post row of data
	POST	/regression+1/row	{"Col_A":"Value A","Col_B":"Value B","Col_C":"Value C"}
	Output
	Number	response status	201
	POST	/regression+1/row	{"Col_A":"Value X", "Col_B":"Value Y", "Col_C":"Value Z"}
	Number	response status	201

Get Table regression 1
	GET	/regression+1
	Output
	Number	response status	200

Get Table regression 1 columns
	GET	/regression+1/columns
	Output
	Number	response status	200

Get Table regression 1 row
	GET	/regression+1/row
	Output
	Number	response status	200

# DELETE /<table name>/<column name>
Delete Column Col_C
	DELETE	/regression+1/Col_C
	Output
	Number	response status	200

# GET /<table name>/<column name>
Get Column Col_A
	GET	/regression+1/Col_A
	Output
	Number	response status	200

# PUT /<table name>/<column name>/<value>
Add value to Column Col_A
	PUT	/regression+1/Col_A/Value+1
	Output
	Number	response status	201

Add more values to Column Col_A
	PUT	/regression+1/Col_A/Value+2
	Number	response status	201
	PUT	/regression+1/Col_A/Value+3
	Number	response status	201
	PUT	/regression+1/Col_A/Value+4
	Number	response status	201
	PUT	/regression+1/Col_A/Value+5
	Number	response status	201
	PUT	/regression+1/Col_A/Value+6
	Number	response status	201

# GET /<table name>/<column name>/all
Get all values for Column Col_A
	GET	/regression+1/Col_A
	Output
	Number	response status	200

# GET /<table name>/<column name>/<id>
Get value by id from Column Col_A
	GET	/regression+1/Col_A/${id}
	Output
	Number	response status	200


Delete Table regression 1
	DELETE	/regression+1
	Output
	# Expect Response	{ "status": "200" }	merge=true
	Number	response status	200

Table regression 1 removed
	GET	/tables
	Output
	Number	response status	200
	Missing	$.tables[?(@.table=="regression 1")]
