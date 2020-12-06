*** Settings ***
Library    TDT
# Library    TDT     http://localhost

Suite Setup		TDT Client Init
Suite Teardown	TDT Client End


*** Variables ***
${table}=	TDTClientTest
${column}=	Column A
${tstval}=	test value

*** Test Cases ***

Send Value
	${resp}=	TDT Send Value		${table}	${column}		${tstval}
	Should Be Equal As Strings  	201 	${resp}

Get Value
	${value1}=	TDT Get Value		${table}	${column}
	Should Be Equal 	${tstval}	${value1}
	${value2}=	TDT Get Value		${table}	${column}
	Should Not Be Equal 	${tstval}	${value2}
	Should Be Empty    ${value2}
	# return value
	TDT Send Value		${table}	${column}		${value1}

Send Value Unique
	${resp}=	TDT Send Value Unique		${table}	${column}		${tstval}_zzz
	Should Be Equal As Strings  	201 	${resp}
	${resp}=	TDT Send Value Unique		${table}	${column}		${tstval}_zzz
	Should Be Equal As Strings  	200 	${resp}

Send Row
	&{dict} =	Create Dictionary	c1=xyz	c2=abc	c3=123
	${resp}=	TDT Send Row		${table}	${dict}
	Should Be Equal As Strings  	201 	${resp}

Get Row
	TDT Send Value		${table}	Column B	Another value
	TDT Send Value		${table}	Column C	Column C value
	TDT Send Value		${table}	Column D	Column D value
	${values}=	TDT Get Row		${table}
	Should Be Equal 	${values['Column D']} 	Column D value
	TDT Send Row		${table}	${values}

Delete Column
	TDT Send Value		${table}	Column Del	Another value
	${resp}=	TDT Delete Column	${table}	Column Del
	Should Be Equal As Strings  	200 	${resp}

Delete Table
	${resp}=	TDT Delete Table	${table}
	Should Be Equal As Strings  	200 	${resp}

*** Keywords ***
TDT Client Init
	${secs} =	Get Time	epoch
	Set Suite Variable	${table}	TDTTest_${secs}

TDT Client End
	TDT Delete Table	${table}


#
