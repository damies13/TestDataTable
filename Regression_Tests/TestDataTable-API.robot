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
