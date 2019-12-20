*** Settings ***
Library	Collections
Library	JsonValidator
Library	RequestsLibrary

Suite Setup	Connect to TDT

*** Test cases ***
Create Table regression 1
	${resp}=	Put Request	TDT	/regression+1
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	201
	Should Be Equal	"${resp.json()['message']}"	"table regression 1 created"

Show Tables
	${resp}=	Get Request	TDT	/tables
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	200

Table regression 1 exists
	${resp}=	Get Request	TDT	/tables
	Log	${resp}
	log	${resp.json()}
	log	${resp.content}
	Should Be Equal As Strings	${resp.status_code}	200
	# ${tbl_id}	Output	$.tables.[?(@.table=='regression 1')].id
	# ${tbl_id}	Output	$.tables[?(@.table=='regression 1')].id
	# ${tbl_name}	Output	$.tables[?(@.table=='regression 1')].table
	# Should Be Equal	"${tbl_name}"	"regression 1"
	# Element should exist    ${json_example}    .author:contains("Evelyn Waugh")
	# ${tbl_result}	Dictionary Should Contain Value    ${resp.json()['tables']}    "regression 1"
	${text}=	Convert To String	${resp.content}
	# ${test}=	Element should exist	${text}	.tables[@.table is "regression 1"]
	# # ${json_elements}= | Select elements  |  ${json_example}  |  .author:contains("Evelyn Waugh")~.price
	# ${tbl_id}=	Select elements	${text}	.tables[@.table is "regression 1"].id
	# ${tbl_name}=	Select elements	${text}	.tables[@.table is "regression 1"].table

	# .author:contains("Evelyn Waugh")~.price
	# ${tbl}=	Select elements	${text}	.table:contains("regression 1")
	# ${tbl}=	Select elements	${text}	.table:contains("regression 1")~.
	${tbl_id}=	Select elements	${text}	.table:contains("regression 1")~.id
	${tbl_name}=	Select elements	${text}	.table:contains("regression 1")~.table
	Should Be Equal	"${tbl_name[0]}"	"regression 1"

Create Table regression 1 again
	${resp}=	Put Request	TDT	/regression+1
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200
	Should Be Equal	"${resp.json()['message']}"	"table regression 1 exists"
	${resp}=	Get Request	TDT	/tables
	Should Be Equal As Strings	${resp.status_code}	200
	${text}=	Convert To String	${resp.content}
	${tbl_name}=	Select elements	${text}	.table:contains("regression 1")~.table
	Should Be Equal	"${tbl_name[0]}"	"regression 1"


Create Column Col_A
	${resp}=	Put Request	TDT	/regression+1/Col_A
	Log	${resp}
	# Expect Response	{ "status": "200" }	merge=true
	Should Be Equal As Strings	${resp.status_code}	201
	Should Be Equal	"${resp.json()['message']}"	"column Col_A created"

Create Column Col_A again
	${resp}=	Put Request	TDT	/regression+1/Col_A
	Log	${resp}
	# Expect Response	{ "status": "200" }	merge=true
	Should Be Equal As Strings	${resp.status_code}	200
	Should Be Equal	"${resp.json()['message']}"	"column Col_A exists"


Create Column Col_B and Col_C
	${resp}=	Put Request	TDT	/regression+1/Col_B
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	Put Request	TDT	/regression+1/Col_C
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	201

Post row of data
	${resp}=	Post Request	TDT	/regression+1/row	{"Col_A":"Value A","Col_B":"Value B","Col_C":"Value C"}
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	Post Request	TDT	/regression+1/row	{"Col_A":"Value X", "Col_B":"Value Y", "Col_C":"Value Z"}
	Should Be Equal As Strings	${resp.status_code}	201

Get Table regression 1
	${resp}=	Get Request	TDT	/regression+1
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	200

Get Table regression 1 columns
	${resp}=	Get Request	TDT	/regression+1/columns
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	200

Get Table regression 1 row
	${resp}=	Get Request	TDT	/regression+1/row
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	200

# DELETE /<table name>/<column name>
Delete Column Col_C
	${resp}=	Delete Request	TDT	/regression+1/Col_C
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	200

# GET /<table name>/<column name>
Get Column Col_A
	${resp}=	Get Request	TDT	/regression+1/Col_A
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	200

# PUT /<table name>/<column name>/<value>
Add value to Column Col_A
	${resp}=	Put Request	TDT	/regression+1/Col_A/Value+1
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	201

Add more values to Column Col_A
	${resp}=	Put Request	TDT	/regression+1/Col_A/Value+2
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	Put Request	TDT	/regression+1/Col_A/Value+3
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	Put Request	TDT	/regression+1/Col_A/Value+4
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	Put Request	TDT	/regression+1/Col_A/Value+5
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	Put Request	TDT	/regression+1/Col_A/Value+6
	Should Be Equal As Strings	${resp.status_code}	201

# GET /<table name>/<column name>/all
Get all values for Column Col_A
	${resp}=	Get Request	TDT	/regression+1/Col_A
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	200

# GET /<table name>/<column name>/<id>
Get value by id from Column Col_A
	${resp}=	Get Request	TDT	/regression+1/Col_A/${id}
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	200


Delete Table regression 1
	${resp}=	Delete Request	TDT	/regression+1
	Log	${resp}
	# Expect Response	{ "status": "200" }	merge=true
	Should Be Equal As Strings	${resp.status_code}	200

Table regression 1 removed
	${resp}=	Get Request	TDT	/tables
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	200
	# Missing	$.tables[?(@.table=="regression 1")]
	${text}=	Convert To String	${resp.content}
	${tbl_name}=	Select elements	${text}	.table:contains("regression 1")~.table
	# Element should not exist	${text}	.tables[?(@.table=="regression 1")]
	Element should not exist	${text}	.table:contains("regression 1")


*** Keywords ***
Connect to TDT
	Create Session	TDT	http://localhost
