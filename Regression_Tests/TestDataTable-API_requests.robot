*** Settings ***
Resource    environment.robot

Library	Collections
Library	JsonValidator
Library	RequestsLibrary

Library	OperatingSystem
Library	String

Suite Setup	Connect to TDT

Default Tags	API 	RequestsLibrary

*** Test cases ***
Create Blank Table
	[Tags]	Create	Table	Negative Case
	${resp}=	PUT On Session	TDT	/ 	expected_status=406
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	406
	Should Be Equal	"${resp.json()['message']}"	"table name cannot be blank"

Create Table regression 1
	[Tags]	Create	Table
	${resp}=	PUT On Session	TDT	/regression+1 	expected_status=201
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	201
	Should Be Equal	"${resp.json()['message']}"	"table regression 1 created"

Show Tables
	[Tags]	Table
	${resp}=	GET On Session	TDT	/tables
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200

Table regression 1 exists
	[Tags]	Table
	${resp}=	GET On Session	TDT	/tables
	Log	${resp}
	log	${resp.json()}
	log	${resp.content}
	Should Be Equal As Strings	${resp.status_code}	200
	${text}=	Convert To String	${resp.content}
	${tbl_id}=	Select elements	${text}	.table:contains("regression 1")~.tbl_id
	${tbl_name}=	Select elements	${text}	.table:contains("regression 1")~.table
	Should Be Equal	"${tbl_name[0]}"	"regression 1"

Create Table regression 1 again
	[Tags]	Create	Table	Negative Case
	${resp}=	PUT On Session	TDT	/regression+1
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200
	Should Be Equal	"${resp.json()['message']}"	"table regression 1 exists"
	${resp}=	GET On Session	TDT	/tables
	Should Be Equal As Strings	${resp.status_code}	200
	${text}=	Convert To String	${resp.content}
	${tbl_name}=	Select elements	${text}	.table:contains("regression 1")~.table
	Should Be Equal	"${tbl_name[0]}"	"regression 1"

Create Blank Column
	[Tags]	Create	Column	Negative Case
	${resp}=	PUT On Session	TDT	/regression+1/ 	expected_status=406
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	406
	Should Be Equal	"${resp.json()['message']}"	"column name cannot be blank"

Create Column Col_A
	[Tags]	Create	Column
	${resp}=	PUT On Session	TDT	/regression+1/Col_A 	expected_status=201
	Log	${resp}
	log	${resp.json()}
	# Expect Response	{ "status": "200" }	merge=true
	Should Be Equal As Strings	${resp.status_code}	201
	Should Be Equal	"${resp.json()['message']}"	"column Col_A created"

Create Column Col_A again
	[Tags]	Create	Column	Negative Case
	${resp}=	PUT On Session	TDT	/regression+1/Col_A
	Log	${resp}
	log	${resp.json()}
	# Expect Response	{ "status": "200" }	merge=true
	Should Be Equal As Strings	${resp.status_code}	200
	Should Be Equal	"${resp.json()['message']}"	"column Col_A exists"

Get value from empty column
	[Tags]	Column	Negative Case
	${resp}=	GET On Session	TDT	/regression 1/Col_A
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200
	${checkval1}=	Set Variable    ${resp.json()['Col_A']}
	Should Be Equal As Strings	${checkval1}	None


Create Column Col_B and Col_C
	[Tags]	Create	Column
	${resp}=	PUT On Session	TDT	/regression+1/Col_B 	expected_status=201
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	PUT On Session	TDT	/regression+1/Col_C 	expected_status=201
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	201

Post row of data
	[Tags]	Create	Values
	${resp}=	POST On Session	TDT	/regression+1/row	{"Col_A":"Value A","Col_B":"Value B","Col_C":"Value C"} 	expected_status=201
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	POST On Session	TDT	/regression+1/row	{"Col_A":"Value X", "Col_B":"Value Y", "Col_C":"Value Z"} 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	POST On Session	TDT	/regression+1/row	{"Col_A":"Value D", "Col_B":"Value E", "Col_C":"Value F"} 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	POST On Session	TDT	/regression+1/row	{"Col_A":"Value G", "Col_B":"Value H", "Col_C":"Value I"} 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	POST On Session	TDT	/regression+1/row	{"Col_A":"Value J", "Col_B":"Value K", "Col_C":"Value L"} 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201

Get all values for Column Col_A
	[Tags]	Values
	${resp}=	GET On Session	TDT	/regression+1/Col_A/all
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200


Get Table regression 1 columns
	[Tags]	Table
	${resp}=	GET On Session	TDT	/regression+1/columns
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200
	Should Be Equal As Strings	${resp.json()['regression 1'][0]['count']}	5

Get Table regression 1 row
	[Tags]	Values
	${resp}=	GET On Session	TDT	/regression+1/row
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200
	Should Be Equal As Strings	${resp.json()['regression 1']['Col_C']}	Value C
	# return data row to table
	${json_string}=    evaluate    json.dumps(${resp.json()['regression 1']})    json
	${resp}=	POST On Session	TDT	/regression+1/row	${json_string}
	Should Be Equal As Strings	${resp.status_code}	201

Get Table regression 1 row 2
	[Documentation]	Get the third row of data (0,1,2)
	[Tags]	Values
	${resp}=	GET On Session	TDT	/regression+1/2
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200
	Should Be Equal As Strings	${resp.json()['regression 1']['Col_C']}	Value I
	# return data row to table
	${json_string}=    evaluate    json.dumps(${resp.json()['regression 1']})    json
	${resp}=	POST On Session	TDT	/regression+1/row	${json_string} 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201

Get Table regression 1 row 100
	[Documentation]	Get the 100th row of data
	...		as there are less than 10 rows, this should return 404 not found
	[Tags]	Values
	${resp}=	GET On Session	TDT	/regression+1/99 	expected_status=404
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	404

# DELETE /<table name>/<column name>
Delete Column Col_C
	[Tags]	Delete	Column
	${resp}=	DELETE On Session	TDT	/regression+1/Col_C
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200

# GET /<table name>/<column name>
Get Column Col_A
	[Tags]	Column
	${resp}=	GET On Session	TDT	/regression 1/Col_A
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200
	${checkval1}=	Set Variable    ${resp.json()['Col_A']}
	${resp}=	GET On Session	TDT	/regression 1/Col_A
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200
	${checkval2}=	Set Variable    ${resp.json()['Col_A']}
	Should Not Be Equal    ${checkval1}    ${checkval2}
	# put the values back
	${resp}=	PUT On Session	TDT	/regression 1/Col_A/${checkval2} 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	PUT On Session	TDT	/regression 1/Col_A/${checkval1} 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201

# PUT /<table name>/<column name>/<value>
Add value to Column Col_A
	[Tags]	Create	Values
	${resp}=	PUT On Session	TDT	/regression 1/Col_A/Value 1 	expected_status=201
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	201

Add more values to Column Col_A
	[Tags]	Create	Values
	${resp}=	PUT On Session	TDT	/regression+1/Col_A/Value+2 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	PUT On Session	TDT	/regression+1/Col_A/Value+3 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	PUT On Session	TDT	/regression+1/Col_A/Value+4 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	PUT On Session	TDT	/regression+1/Col_A/Value+5 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	PUT On Session	TDT	/regression+1/Col_A/Value+6 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201

Delete Value 4 from Column Col_A
	[Tags]	Delete	Values
	${resp}=	DELETE On Session	TDT	/regression 1/Col_A/Value 4
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200


Get Table regression 1
	[Tags]	Table
	${resp}=	GET On Session	TDT	/regression+1
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200


Replace value by current value
	[Tags]	Create	Values
	${resp}=	PUT On Session	TDT	/regression+1/Col_A/Value X/New Value X
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200

# GET /<table name>/<column name>/all
Get all values for Column Col_A for Value Id's
	[Tags]	Values
	${resp}=	GET On Session	TDT	/regression+1/Col_A/all
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200
	log	${resp.json()["Col_A"]}
	log	${resp.json()["Col_A"][-1]}
	log	${resp.json()["Col_A"][-1]["val_id"]}
	# ${value_id}=	Set Variable    ${resp.json()["Col_A"][0]["val_id"]}
	Set Global Variable    ${value_id}    ${resp.json()["Col_A"][-1]["val_id"]}

Replace value by id
	[Tags]	Create	Values
	${resp}=	PUT On Session	TDT	/regression+1/Col_A/${value_id}/New Value
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200

# GET /<table name>/<column name>/<id>
Get value by id from Column Col_A
	[Tags]	Values
	${resp}=	GET On Session	TDT	/regression+1/Col_A/${value_id}
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200
	Should Be Equal As Strings	${resp.json()["Col_A"]}	New Value

Table doesn't exist
	[Tags]	Table	Negative Case
	${resp}=	GET On Session	TDT	/regression 1998 	expected_status=404
	Log	${resp}
	# log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	404

Table doesn't exist - columns
	[Tags]	Table	Negative Case
	${resp}=	GET On Session	TDT	/regression 1999/columns 	expected_status=404
	Log	${resp}
	# log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	404

Column doesn't exist
	[Tags]	Column	Negative Case
	${resp}=	GET On Session	TDT	/regression 1/joe citizen 2019 	expected_status=404
	Log	${resp}
	# log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	404

Value Id doesn't exist
	[Tags]	Values	Negative Case
	# ${badval}=	Evaluate    ${value_id} * 2
	${badval}=	Set Variable	5c1d0000920000000000000000000000
	${resp}=	GET On Session	TDT	/regression+1/Col_A/${badval} 	expected_status=404
	Log	${resp}
	# log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	404

Delete Table regression 1
	[Tags]	Table	Delete
	${resp}=	DELETE On Session	TDT	/regression+1
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200

Table regression 1 removed
	[Tags]	Table	Delete
	${resp}=	GET On Session	TDT	/tables
	Log	${resp}
	Should Be Equal As Strings	${resp.status_code}	200
	# Missing	$.tables[?(@.table=="regression 1")]
	${text}=	Convert To String	${resp.content}
	${tbl_name}=	Select elements	${text}	.table:contains("regression 1")~.table
	# Element should not exist	${text}	.tables[?(@.table=="regression 1")]
	Element should not exist	${text}	.table:contains("regression 1")

Add value to create column and table
	[Tags]	Create	Table	Column	Values
	${resp}=	PUT On Session	TDT	/Regression+Create/Col+Create/Value+Create 	expected_status=201
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	201
	Log	"Cleanup table Regression Create"
	${resp}=	DELETE On Session	TDT	/Regression+Create
	Log	${resp}
	log	${resp.json()}
	Should Be Equal As Strings	${resp.status_code}	200

Create Demo Data
	[Tags]	Create	Values
	${resp}=	PUT On Session	TDT	/Demo/Demo+1/data+value+1 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	PUT On Session	TDT	/Demo/Demo+1/data+value+2 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	PUT On Session	TDT	/Demo/Demo+1/data+value+3 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	PUT On Session	TDT	/Demo/Demo+2/data+value+21 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	PUT On Session	TDT	/Demo/Demo+2/data+value+22 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	PUT On Session	TDT	/Demo/Demo+2/data+value+23 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201
	${resp}=	PUT On Session	TDT	/Demo 2/Demo 3/data value 1 	expected_status=201
	Should Be Equal As Strings	${resp.status_code}	201

Prep for Perf Tests
	${Table}=		Set Variable    TT20
	${Col 1}=		Set Variable    GC_20k
	${Col 2}=		Set Variable    BNE_20k
	${filedata}= 		Get File 		${CURDIR}${/}testdata${/}${Col 1}.csv
	@{filelines}= 	Split To Lines 		${filedata}
	FOR 	${line} 	IN 	@{filelines}
		# ${resp}=	POST On Session	TDT	/${Table}/row	{"${Col 1}":"${line}"} 	expected_status=201
		${resp}=	PUT On Session	TDT	/${Table}/${Col 1}/${line} 	expected_status=201
	END
	${filedata}= 		Get File 		${CURDIR}${/}testdata${/}${Col 2}.csv
	@{filelines}= 	Split To Lines 		${filedata}
	FOR 	${line} 	IN 	@{filelines}
		# ${resp}=	POST On Session	TDT	/${Table}/row	{"${Col 1}":"${line}"} 	expected_status=201
		${resp}=	PUT On Session	TDT	/${Table}/${Col 2}/${line} 	expected_status=201
	END

*** Keywords ***
Connect to TDT
	Create Session	TDT	http://${TDT_Host}
