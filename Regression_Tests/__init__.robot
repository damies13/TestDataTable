*** Settings ***
Library 	OperatingSystem
Library 	Process
Library 	Collections

Suite Setup			Run TestDataTable

*** Variables ***
${TDT_portno} 		1080
${TDT_pyfile} 		${EXECDIR}${/}testdatatable${/}TestDataTable.py
${TDT_cmd} 		python3 	${TDT_pyfile}
${TDT_process} 		None

*** Keywords ***

Run TestDataTable
	[Arguments]		${options}=None
	IF  ${options} == None
		${options}= 	Create List
	END
	Append To List 	${options} 	-p 	${TDT_portno}
	Log to console 	${\n}\${options}: ${options}
	# ${process}= 	Start Process 	python3 	${pyfile_agent}  @{options}  alias=Agent 	stdout=${OUTPUT DIR}${/}stdout_agent.txt 	stderr=${OUTPUT DIR}${/}stderr_agent.txt
	${process}= 	Start Process 	${TDT_cmd}  @{options}  alias=TDT 	stdout=${OUTPUT DIR}${/}stdout_TDT.txt 	stderr=${OUTPUT DIR}${/}stderr_TDT.txt
	Set Test Variable 	$TDT_process 	${process}
