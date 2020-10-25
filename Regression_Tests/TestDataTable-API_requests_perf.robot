*** Settings ***
Resource    environment.robot

Library	Collections
Library	JsonValidator
Library	RequestsLibrary
Library  String

Suite Setup	Connect to TDT

Default Tags	API 	RequestsLibrary

*** Variables ***

# ${Table}		TT3
${Table}		TT20
${Col 1}		GC_20k
${Col 2}		BNE_20k

${STT_MIN}			15
${STT_MAX}			45
# ${STT_MIN}			1
# ${STT_MAX}			2

*** Test cases ***
Get Hold Return Value GC
	FOR    ${index}    IN RANGE    10
		${column}=	Set Variable	${Col 1}
		Get TDT Value	${Table}	${column}
		Standard Think Time
		# put the values back
		Return TDT Value	${Table}	${column}	${${column}}
		Standard Think Time
	END

# GET /<table name>/<column name>
Get Hold Return Value BNE
	FOR    ${index}    IN RANGE    10
		${column}=	Set Variable	${Col 2}
		Get TDT Value	${Table}	${column}
		Standard Think Time
		# put the values back
		Return TDT Value	${Table}	${column}	${${column}}
		Standard Think Time
	END

Data cycle test
	FOR    ${index}    IN RANGE    10
		Create Perf_P1 Value
		${column}=	Set Variable	P1
		Standard Think Time
		${p1val}=	Get Perf Column 	${column}
		Standard Think Time
		${column}=	Set Variable	P2
		Set Perf Column 	${column}	${p1val}
		Standard Think Time
		${p2val}=	Get Perf Column 	${column}
		Standard Think Time
		${column}=	Set Variable	P3
		Set Perf Column 	${column}	${p2val}
		Standard Think Time
	END
	${column}=	Set Variable	P3
	Delete Perf Column	${column}
	Standard Think Time

Short Data cycle test
	Create Perf_P1 Value
	${column}=	Set Variable	P1
	Standard Think Time
	${p1val}=	Get Perf Column 	${column}
	Standard Think Time
	${column}=	Set Variable	P2
	Set Perf Column 	${column}	${p1val}
	Standard Think Time
	${p2val}=	Get Perf Column 	${column}
	Standard Think Time

	${column}=	Set Variable	${p2val}
	Set Perf Column 	${column}	${p2val}
	Standard Think Time
	Delete Perf Column	${column}

	${column}=	Set Variable	P3
	Set Perf Column 	${column}	${p2val}
	Standard Think Time
	${column}=	Set Variable	P3
	Delete Perf Column	${column}
	Standard Think Time

*** Keywords ***
Connect to TDT
	[Documentation] 	Connect to TDT: http://${TDT_Host}
	Create Session	TDT	http://${TDT_Host}
	Log 	Connect to TDT:http://${TDT_Host}

Get TDT Value
	[Arguments] 	${table}	${column}
	[Documentation] 	Get TDT Value /${table}/${column}
	${resp}=	Get Request	TDT	/${table}/${column}
	Should Be Equal As Strings	${resp.status_code}	200
	# ${TDT["${column}"]}=	Set Variable    ${resp.json()['${column}']}
	${checkval}=	Set Variable    ${resp.json()['${column}']}
	Set Global Variable    ${${column}}    ${checkval}
	[return]	${checkval}

Return TDT Value
	[Arguments] 	${table}	${column}	${value}
	[Documentation] 	Return TDT Value /${table}/${column}
	${resp}=	Put Request	TDT	/${table}/${column}/${value}
	Should Be Equal As Strings	${resp.status_code}	201


Standard Think Time
	${number}    Evaluate    random.randint(${STT_MIN}, ${STT_MAX})    random
	Log      Standard Think Time (${number})
	Sleep    ${number}


Create Perf_P1 Value
	[Documentation] 	Create Value in Table Perf Col P1
	${number}    Evaluate    random.randint(5, 30)    random
	${RANDVAL}= 	Generate Random String	${number}
	Put Request	TDT	/Perf/P1/${RANDVAL}
	[Return]	${RANDVAL}

Get Perf Column
	[Arguments] 	${column}
	[Documentation] 	Get Value from Perf ${column}
	${resp}=	Get Request	TDT	/Perf/${column}
	Should Be Equal As Strings	${resp.status_code}	200
	[return]	${resp.json()['${column}']}

Set Perf Column
	[Arguments] 	${column}	${value}
	[Documentation] 	Set Value to Perf ${column}
	${resp}=	Put Request	TDT	/Perf/${column}/${value}
	Should Be Equal As Strings	${resp.status_code}	201

Delete Perf Column
	[Arguments] 	${column}
	[Documentation] 	Delete Value from Perf ${column}
	${resp}=	Delete Request	TDT	/Perf/${column}
	Should Be Equal As Strings	${resp.status_code}	200
