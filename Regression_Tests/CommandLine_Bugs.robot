*** Settings ***
Resource 	CommandLine_Common.robot


*** Test Cases ***
Check for Hang if port can't be opened
	[Tags]	CommandLine		Issue #18
	Open Test Data Table
	Wait For Test Data Table 	5min

	${stdout}= 	Show Log 	${OUTPUT DIR}${/}stdout.txt
	${stderr}= 	Show Log 	${OUTPUT DIR}${/}stderr.txt

	Should Contain    ${stdout}    Permission denied when trying

	[Teardown] 		Stop Test Data Table
