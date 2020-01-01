*** Settings ***
Library	Collections
Library	JsonValidator
Library	RequestsLibrary

Suite Setup	Connect to TDT

Default Tags	API 	RequestsLibrary

*** Variables ***
# ${Table}		TT3
${Table}		Demo 2
${Col 1}		Rand
# ${Col 2}		street_no_1
${Col 2}		D3
${Col 3}		road_name

# ${STT_MIN}			15
# ${STT_MAX}			45
${STT_MIN}			1
${STT_MAX}			5

*** Test cases ***

# GET /<table name>/<column name>
Get Hold Return Value
	FOR    ${index}    IN RANGE    10
		${resp}=	Get Request	TDT	/${Table}/${Col 2}
		Should Be Equal As Strings	${resp.status_code}	200
		${checkval}=	Set Variable    ${resp.json()['${Col 2}']}
		Standard Think Time
		# put the values back
		${resp}=	Put Request	TDT	/${Table}/${Col 2}/${checkval}
		Should Be Equal As Strings	${resp.status_code}	201
		Standard Think Time
	END



*** Keywords ***
Connect to TDT
	Create Session	TDT	http://localhost



Standard Think Time
	${number}    Evaluate    random.randint(${STT_MIN}, ${STT_MAX})    random
	Log      Standard Think Time (${number})
	Sleep    ${number}
