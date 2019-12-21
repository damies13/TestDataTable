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
	log	${resp.json()}
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
	log	${resp.json()}
	# Expect Response	{ "status": "200" }	merge=true
	Should Be Equal As Strings	${resp.status_code}	201
	Should Be Equal	"${resp.json()['message']}"	"column Col_A created"

Create Column Col_A again
	${resp}=	Put Request	TDT	/regression+1/Col_A
	Log	${resp}
	log	${resp.json()}
	# Expect Response	{ "status": "200" }	merge=true
	Should Be Equal As Strings	${resp.status_code}	200
	Should Be Equal	"${resp.json()['message']}"	"column Col_A exists"

Gat value from empty column
	${resp}=	Get Request	TDT	/regression 1/Col_A
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200
	${checkval1}=	Set Variable    ${resp.json()['Col_A']}
	Should Be Equal As Strings	${checkval1}	None


Create Column Col_B and Col_C
	${resp}=	Put Request	TDT	/regression+1/Col_B
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	Put Request	TDT	/regression+1/Col_C
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	201

Post row of data
	${resp}=	Post Request	TDT	/regression+1/row	{"Col_A":"Value A","Col_B":"Value B","Col_C":"Value C"}
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	Post Request	TDT	/regression+1/row	{"Col_A":"Value X", "Col_B":"Value Y", "Col_C":"Value Z"}
	Should Be Equal As Strings	${resp.status_code}	201

Get all values for Column Col_A
	${resp}=	Get Request	TDT	/regression+1/Col_A/all
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200


Get Table regression 1 columns
	${resp}=	Get Request	TDT	/regression+1/columns
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200

Get Table regression 1 row
	${resp}=	Get Request	TDT	/regression+1/row
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200
	Should Be Equal As Strings	${resp.json()['regression 1']['Col_C']}	Value C
	# return data row to table
	${json_string}=    evaluate    json.dumps(${resp.json()['regression 1']})    json
	${resp}=	Post Request	TDT	/regression+1/row	${json_string}
	Should Be Equal As Strings	${resp.status_code}	201


# DELETE /<table name>/<column name>
Delete Column Col_C
	${resp}=	Delete Request	TDT	/regression+1/Col_C
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200

# GET /<table name>/<column name>
Get Column Col_A
	${resp}=	Get Request	TDT	/regression 1/Col_A
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200
	${checkval1}=	Set Variable    ${resp.json()['Col_A']}
	${resp}=	Get Request	TDT	/regression 1/Col_A
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200
	${checkval2}=	Set Variable    ${resp.json()['Col_A']}
	Should Not Be Equal    ${checkval1}    ${checkval2}
	# put the values back
	${resp}=	Put Request	TDT	/regression 1/Col_A/${checkval2}
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	Put Request	TDT	/regression 1/Col_A/${checkval1}
	Should Be Equal As Strings	${resp.status_code}	201

# PUT /<table name>/<column name>/<value>
Add value to Column Col_A
	${resp}=	Put Request	TDT	/regression 1/Col_A/Value 1
	Log	${resp}
	log	${resp.json()}
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

Delete Value 4 from Column Col_A
	${resp}=	Delete Request	TDT	/regression 1/Col_A/Value 4
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200


Get Table regression 1
	${resp}=	Get Request	TDT	/regression+1
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200

# GET /<table name>/<column name>/all
Get all values for Column Col_A for Value Id's
	${resp}=	Get Request	TDT	/regression+1/Col_A/all
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200
	log	${resp.json()["Col_A"]}
	log	${resp.json()["Col_A"][-1]}
	log	${resp.json()["Col_A"][-1]["val_id"]}
	# ${value_id}=	Set Variable    ${resp.json()["Col_A"][0]["val_id"]}
	Set Global Variable    ${value_id}    ${resp.json()["Col_A"][-1]["val_id"]}

# GET /<table name>/<column name>/<id>
Get value by id from Column Col_A
	${resp}=	Get Request	TDT	/regression+1/Col_A/${value_id}
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200

Table doesn't exist
	${resp}=	Get Request	TDT	/regression 1998
	Log	${resp}
	# log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	404

Table doesn't exist - columns
	${resp}=	Get Request	TDT	/regression 1999/columns
	Log	${resp}
	# log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	404

Column doesn't exist
	${resp}=	Get Request	TDT	/regression 1/joe citizen 2019
	Log	${resp}
	# log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	404

Value Id doesn't exist
	${badval}=	Evaluate    ${value_id} * 2
	${resp}=	Get Request	TDT	/regression+1/Col_A/${badval}
	Log	${resp}
	# log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	404

Delete Table regression 1
	${resp}=	Delete Request	TDT	/regression+1
	Log	${resp}
	log	${resp.json()}
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

Add value to create column and table
	${resp}=	Put Request	TDT	/Regression+Create/Col+Create/Value+Create
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	201
	Log	"Cleanup table Regression Create"
	${resp}=	Delete Request	TDT	/Regression+Create
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200

Create Demo Data
	${resp}=	Put Request	TDT	/Demo/Demo+1/data+value+1
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	Put Request	TDT	/Demo/Demo+1/data+value+2
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	Put Request	TDT	/Demo/Demo+1/data+value+3
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	Put Request	TDT	/Demo/Demo+2/data+value+21
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	Put Request	TDT	/Demo/Demo+2/data+value+22
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	Put Request	TDT	/Demo/Demo+2/data+value+23
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	Put Request	TDT	/Demo 2/Demo 3/data value 1
	Should Be Equal As Strings	${resp.status_code}	201



*** Keywords ***
Connect to TDT
	Create Session	TDT	http://localhost
