*** Settings ***
Resource 	CommandLine_Common.robot


*** Test Cases ***
Check for Hang if port can't be opened
	[Tags]	CommandLine		Issue #18 	ubuntu 	windows
	# port 80 doesn't fail on MacOS, only windows and linux, so set to port 1080 as there is already
	# 	a TDT instance running there (suite Setup) so should always fail here

	# [Server]
	# bindip =
	# bindport = 80
	# datadir = ${OUTPUT DIR}${/}${TEST NAME}
	# dbfile = TestDataTable.sqlite3
	&{server} = 	Create Dictionary 	bindport=80 	datadir=${OUTPUT DIR}${/}${TEST NAME}

	# [Resources]
	# js_jquery = https://unpkg.com/jquery@latest/dist/jquery.min.js
	# js_jqueryui = https://code.jquery.com/ui/1.12.1/jquery-ui.min.js
	# css_jqueryui = https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css
	# js_papaparse = https://unpkg.com/papaparse@latest/papaparse.min.js
	&{resources} = 	Create Dictionary

	&{inidata} = 	Create Dictionary 	Server=${server} 	Resources=${resources}

	Dict to INI 	${inidata} 		${OUTPUT DIR}${/}${TEST NAME}${/}TestDataTable.ini

	Open Test Data Table 	-i 	${OUTPUT DIR}${/}${TEST NAME}${/}TestDataTable.ini
	Wait For Test Data Table 	1min

	${stdout}= 	Show Log 	${OUTPUT DIR}${/}stdout.txt
	${stderr}= 	Show Log 	${OUTPUT DIR}${/}stderr.txt

	Should Contain    ${stdout}    Permission denied when trying

	[Teardown] 		Stop Test Data Table
