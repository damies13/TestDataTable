*** Settings ***
Library	Collections
Library	JsonValidator
Library	RequestsLibrary

Suite Setup	Connect to TDT

Default Tags	API 	RequestsLibrary

*** Variables ***
# ${Table}		TT3
${Table}		TT20
${Col 1}		GC_20k
${Col 2}		BNE_20k

# ${STT_MIN}			15
# ${STT_MAX}			45
${STT_MIN}			1
${STT_MAX}			5

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



*** Keywords ***
Connect to TDT
	[Documentation] 	Connect to TDT: http://localhost
	Create Session	TDT	http://localhost
	Log 	Connect to TDT:http://localhost

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
