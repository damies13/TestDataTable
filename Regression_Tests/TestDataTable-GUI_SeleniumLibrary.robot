*** Settings ***
Resource    environment.robot

Library           SeleniumLibrary

Suite Setup		Open TDT GUI
Suite Teardown	TDT GUI End Test

Default Tags	GUI

*** Variables ***
# ${BROWSER}		ff
${BROWSER}		chrome
${TABLENAME}		Regression_GUI_Selenium_Chrome


*** Test Cases ***    Expression    Expected


Open Help
	[Tags]	Button	Help
	${handle} =	Select Window 	MAIN
	Capture Page Screenshot
	${maintitle}=	Get Title
	Click Button	Help
	# ${handle} =	Switch Window	NEW
	${handle} =	Select Window	NEW	120
	Wait Until Page Contains	Rest Api
	# Wait Until Element Is Visible	Table operations	60
	Capture Page Screenshot
	# ${handle} =	Select Window	TestDataTable/rest_api
	${helptitle}=	Get Title
	# TestDataTable/rest_api.md at master · damies13/TestDataTable
	Should Contain	${helptitle}	TestDataTable/Doc/rest_api.md at master
	Close Window
	# ${handle} =	Switch Window 	MAIN
	${handle} =	Select Window	${maintitle}

Click Refresh Button
	[Tags]	Button
	${handle} =	Select Window 	MAIN
	Click Button	Refresh

Create New Table
	[Tags]	Button	Create	Table	Dialogues
	${handle} =	Select Window 	MAIN
	Click Button	Add Table
	# Click Button	id:new-table
	Wait Until Element Is Enabled	xpath: //span[contains(@class, 'ui-dialog-title') and contains(text(), 'Create table')]
	Capture Page Screenshot

	Input Text	id:table-name	${TABLENAME}
	Click Button    Create
	Wait Until Element Is Visible	xpath: //a[text()='${TABLENAME}']

Select Table
	[Tags]	Tabs	Table
	${handle} =	Select Window 	MAIN
	Wait Until Element Is Visible	xpath: //li/a[text()='${TABLENAME}']
	Click Element    xpath: //li/a[text()='${TABLENAME}']
	Wait Until Element Is Visible	xpath: //li[@aria-selected='true']/a[text()='${TABLENAME}']

Create New Column
	[Tags]	Button	Create	Column	Dialogues
	${handle} =	Select Window 	MAIN
	Wait Until Element Is Visible	xpath: //li/a[text()='${TABLENAME}']
	Click Element    xpath: //li/a[text()='${TABLENAME}']
	Wait Until Element Is Visible	xpath: //li[@aria-selected='true']/a[text()='${TABLENAME}']
	Click Button	Add Column
	Wait Until Element Is Enabled	xpath: //span[contains(@class, 'ui-dialog-title') and contains(text(), 'Add Column')]
	Capture Page Screenshot
	Input Text	id:column-name	GUI Column A
	Click Button    Add
	Wait Until Element Is Visible	xpath: //div[@name='${TABLENAME}']//th/span[text()='GUI Column A']
	${col_a_id}=	Get Element Attribute	xpath: //div[@name='${TABLENAME}']//th/span[text()='GUI Column A']/..	id
	Set Global Variable 	${col_a_id} 	${col_a_id}

Add value to column
	[Tags]	Create	Column	Values
	${handle}=	Select Window 	MAIN
	# //div[@name="Demo 2"]//td[@id="${col_a_id}-0"]/text()
	Wait Until Element Is Visible	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]
	Wait until page does not contain element  xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0" and contains(@class, "has-value")]
	Page Should Not Contain Element	xpath: //div[@name="${TABLENAME}"]//td/input
	Click Element	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]
	Sleep    0.3
	Click Element	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]
	Capture Page Screenshot
	Wait Until Element Is Visible	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]/input
	Input Text	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]/input	Column A Row 0
	Click Element	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-3"]
	Wait Until Element Is Not Visible	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]/input
	Wait until page contains element  xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0" and contains(@class, "has-value")]
	${result}=	Get Text    xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]
	Should Be Equal As Strings	${result}	Column A Row 0

Add some test data
	[Tags]	Create	Column	Values
	${handle} =	Select Window 	MAIN
	FOR    ${index}    IN RANGE    10
		${incell}=	Evaluate    ${index}+1
		${outcell}=	Evaluate    ${index}+3
		Value Edit Mode	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-${incell}"]
		Input Text	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-${incell}"]/input	Column A Row ${incell}
		Click Element	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-${outcell}"]
		Wait until page contains element  xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-${incell}" and contains(@class, "has-value")]
	END
	Click Button	Add Column
	Wait Until Element Is Enabled	xpath: //span[contains(@class, 'ui-dialog-title') and contains(text(), 'Add Column')]
	Input Text	id:column-name	GUI Column B
	Click Button    Add
	Wait Until Element Is Visible	xpath: //div[@name='${TABLENAME}']//th/span[text()='GUI Column B']
	${col_b_id}=	Get Element Attribute	xpath: //div[@name='${TABLENAME}']//th/span[text()='GUI Column B']/..	id
	Set Global Variable 	${col_b_id} 	${col_b_id}
	FOR    ${index}    IN RANGE    11
		${incell}=	Evaluate    ${index}+0
		${outcell}=	Evaluate    ${index}+3
		Value Edit Mode	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_b_id}-${incell}"]
		Input Text	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_b_id}-${incell}"]/input	Column B Row ${incell}
		Click Element	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_b_id}-${outcell}"]
	END
	Capture Page Screenshot

Edit Value
	[Tags]	Update	Values
	${col}=	Set Variable    ${col_a_id}
	${row}=	Set Variable    3
	${result}=	Get Text    xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${result}	Column A Row ${row}
	Value Edit Mode	xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Capture Page Screenshot
	# Press Keys	None	ARROW_RIGHT
	Input Text	xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]/input	${result} abc
	${outcell}=	Evaluate    ${row}+3
	Click Element	xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${outcell}"]
	${result}=	Get Text    xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${result}	Column A Row ${row} abc

Replace Value
	[Tags]	Update	Values
	${col}=	Set Variable    ${col_a_id}
	${row}=	Set Variable    5
	${result}=	Get Text    xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${result}	Column A Row ${row}
	Value Edit Mode	xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Clear Element Text	xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]/input
	Input Text	xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]/input	my new value
	${outcell}=	Evaluate    ${row}+3
	Click Element	xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${outcell}"]
	${result}=	Get Text    xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${result}	my new value

Remove Last Value
	[Tags]	Delete	Values
	${col}=	Set Variable    ${col_b_id}
	${row}=	Set Variable    10
	${startval}=	Get Text    xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${startval}	Column B Row ${row}
	Value Edit Mode	xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Clear Element Text	xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]/input
	${outcell}=	Evaluate    ${row}+3
	Click Element	xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${outcell}"]
	${endval}=	Get Text    xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Should Not Be Equal As Strings	${endval}	${startval}
	Should Be Equal As Strings	"${endval}"	" "
	Wait until page does not contain element  xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}" and contains(@class, "has-value")]


Remove 3rd Value
	[Tags]	Delete	Values
	${col}=	Set Variable    ${col_b_id}
	${row}=	Set Variable    3
	${lastrow}=	Set Variable    9
	${nextrow}=	Evaluate	${row}+1
	${startvalue}=	Get Text    xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${startvalue}	Column B Row ${row}
	Value Edit Mode	xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Clear Element Text	xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]/input
	${outcell}=	Evaluate    ${row}+3
	Click Element	xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${outcell}"]
	Wait until page does not contain element  xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${lastrow}" and contains(@class, "has-value")]
	Wait until page contains element  xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}" and contains(@class, "has-value")]
	Wait until page contains element  xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${nextrow}" and contains(@class, "has-value")]
	${endval}=	Get Text    xpath: //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Should Not Be Equal As Strings	${endval}	${startvalue}
	Should Be Equal As Strings	${endval}	Column B Row ${nextrow}


Remove Column
	[Tags]	Delete	Column	Dialogues
	${handle} =	Select Window 	MAIN
	# //th[@name="Ninja"]/span[contains(@class, "ui-icon-close")]
	Wait Until Element Is Visible	xpath: //th[@name="GUI Column B"]/span[contains(@class, "ui-icon-close")]
	Click Element    xpath: //th[@name="GUI Column B"]/span[contains(@class, "ui-icon-close")]
	Wait Until Element Is Enabled	xpath: //span[contains(@class, 'ui-dialog-title') and contains(text(), 'Delete column')]
	Wait Until Element Is Visible	id: dialog-delete-column
	${dialogueMsg}= 	Get Text    id: dialog-delete-column
	Capture Page Screenshot
	Click Button    xpath: //div[@id='dialog-delete-column']/..//button[text()='Delete']
	Wait Until Element Is Not Visible	xpath: //th[@name="GUI Column B"]


Import Data From File
	[Tags]	Create	Column	Values	Import
	${handle} =	Select Window 	MAIN
	# Click Button	Import File
	Click Button	id:import-file
	Wait Until Element Is Enabled	xpath: //span[contains(@class, 'ui-dialog-title') and contains(text(), 'Text File Import')]
	Capture Page Screenshot
	# Click Element    id:dialog-file-import-file
	Choose File 	id:dialog-file-import-file 	${CURDIR}/GC_5k.csv
	Capture Page Screenshot
	${hdrrow0}= 	Get Value	id:preview-c0
	Should Be Equal As Strings	${hdrrow0}	Rand
	${hdrrow1}= 	Get Value	id:preview-c1
	Should Be Equal As Strings	${hdrrow1}	street_no_1
	${hdrrow2}= 	Get Value	id:preview-c2
	Should Be Equal As Strings	${hdrrow2}	road_name
	Click Element    id:dialog-file-import-header-row
	${nohdrow1}= 	Get Value	id:preview-c1
	Should Be Equal As Strings	${nohdrow1}	1
	${datacell1}= 	Get Text	id:preview-tablecell-1-1
	Should Be Equal As Strings	${hdrrow1}	${datacell1}
	Capture Page Screenshot
	Click Element    id:dialog-file-import-header-row
	Click Link    	tab
	${delim}= 	Get Value	id:dialog-file-import-delimiter
	Should Be Equal As Strings		${delim}	\t
	# Wait Until Keyword Succeeds    10s    200ms    Textfield Should Contain    id:dialog-file-import-delimiter    \t
	${hdrrow0_delim}= 	Get Value	id:preview-c0
	Should Be Equal As Strings	${hdrrow0_delim}	${hdrrow0},${hdrrow1},${hdrrow2}
	Capture Page Screenshot
	${datacell0}= 	Get Text	id:preview-tablecell-1-0
	${newhdr}=		Set Variable    Street Data
	Input Text		id:preview-c0	${newhdr}
	${chknewhdr}= 	Get Value	id:preview-c0
	Should Be Equal As Strings	${newhdr}	${newhdr}
	Capture Page Screenshot
	Click Button    Import
	Wait Until Element Is Visible	id:dialog-progress-bar
	Wait Until Element Contains	id:dialog-progress-msg	Loading
	Capture Page Screenshot
	Wait Until Element Contains	id:dialog-progress-msg	%
	Capture Page Screenshot
	Wait Until Element Contains	id:dialog-progress-msg	100%
	Capture Page Screenshot
	Wait Until Element Is Not Visible	id:dialog-progress-bar
	Wait Until Element Is Visible	name:Street Data
	Capture Page Screenshot
	${colid}=	Get Element Attribute	name:Street Data	id
	${chk1strow}= 	Get Text	id:${colid}-0
	Should Be Equal As Strings	${datacell0}	${chk1strow}


Export Data To File
	[Tags]	Table	Column	Values	Export
	${handle} =	Select Window 	MAIN
	Wait Until Element Is Visible	name:Street Data
	${colid}=	Get Element Attribute	name:Street Data	id
	${chk1strow}= 	Get Text	id:${colid}-0
	Click Button	id:export-file
	Wait Until Element Is Enabled	xpath: //span[contains(@class, 'ui-dialog-title') and contains(text(), 'Text File Export')]
	Capture Page Screenshot
	${filename}= 	Get Value	id:dialog-file-export-filename
	Should Contain 	${filename} 	.csv
	Textarea Should Contain 	xpath://div[@id='dialog-file-export-preview']/textarea		Street Data
	Textarea Should Contain 	xpath://div[@id='dialog-file-export-preview']/textarea		"${chk1strow}"
	Click Element    id:dialog-file-export-header-row
	${txtarea}= 	Get Value	xpath://div[@id='dialog-file-export-preview']/textarea
	Should Not Contain		${txtarea}		Street Data
	Capture Page Screenshot
	Click Element    id:dialog-file-export-header-row
	Wait Until Keyword Succeeds    60s    200ms    Textarea Should Contain 	xpath://div[@id='dialog-file-export-preview']/textarea		Street Data
	Click Link    	id:dialog-file-export-insert-tab
	${delim}= 	Get Value	id:dialog-file-export-delimiter
	Should Be Equal As Strings		${delim}	\t
	Wait Until Keyword Succeeds    60s    200ms    Textarea Should Contain 	xpath://div[@id='dialog-file-export-preview']/textarea		Street Data
	Textarea Should Contain 	xpath://div[@id='dialog-file-export-preview']/textarea		${chk1strow}
	${txtarea}= 	Get Value	xpath://div[@id='dialog-file-export-preview']/textarea
	Should Not Contain		${txtarea}		"${chk1strow}"
	${filename}= 	Get Value	id:dialog-file-export-filename
	Should Contain 	${filename} 	.tsv
	Capture Page Screenshot
	Input Text		id:dialog-file-export-delimiter	|
	Click Element    id:dialog-file-export-filename
	${filename}= 	Get Value	id:dialog-file-export-filename
	Should Contain 	${filename} 	.txt
	# $x('//div[@id="dialog-file-export"]/..//button[text()="Cancel"]')
	# Click Button    Cancel
	Capture Page Screenshot
	Click Button    xpath://div[@id="dialog-file-export"]/..//button[text()="Cancel"]

Remove Table
	[Tags]	Delete	Table	Dialogues
	${handle} =	Select Window 	MAIN
	# Wait Until Element Is Enabled	xpath: //a[text()='${TABLENAME}']/../span
	Wait Until Element Is Visible	xpath: //a[text()='${TABLENAME}']/../span
	Click Element    xpath: //a[text()='${TABLENAME}']/../span
	# 					  //span[@table="${TABLENAME}"]
	Wait Until Element Is Enabled	xpath: //span[contains(@class, 'ui-dialog-title') and contains(text(), 'Delete table')]
	Capture Page Screenshot
	Click Button    Delete
	Wait Until Element Is Not Visible	xpath: //span[contains(@class, 'ui-tabs-anchor') and contains(text(), '${TABLENAME}')]


Table with some spaces
	[Tags]	Button	Create	Table	Column	Values	Dialogues
	${handle} =	Select Window 	MAIN

	# Create Table
	Click Button	Add Table
	# Click Button	id:new-table
	Wait Until Element Is Enabled	xpath: //span[contains(@class, 'ui-dialog-title') and contains(text(), 'Create table')]
	Capture Page Screenshot
	${TABLENAME}= 	Set Variable	Table with some Spaces
	Input Text	id:table-name	${TABLENAME}
	Click Button    Create
	Wait Until Element Is Visible	xpath: //a[text()='${TABLENAME}']

	# Add Column
	Wait Until Element Is Visible	xpath: //li/a[text()='${TABLENAME}']
	Click Element    xpath: //li/a[text()='${TABLENAME}']
	Wait Until Element Is Visible	xpath: //li[@aria-selected='true']/a[text()='${TABLENAME}']
	Click Button	Add Column
	Wait Until Element Is Enabled	xpath: //span[contains(@class, 'ui-dialog-title') and contains(text(), 'Add Column')]
	Capture Page Screenshot
	Input Text	id:column-name	Col with spaces
	Click Button    Add
	Wait Until Element Is Visible	xpath: //div[@name='${TABLENAME}']//th/span[text()='Col with spaces']
	${col_a_id}=	Get Element Attribute	xpath: //div[@name='${TABLENAME}']//th/span[text()='Col with spaces']/..	id

	# Add Value
	Wait Until Element Is Visible	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]
	Wait until page does not contain element  xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0" and contains(@class, "has-value")]
	Page Should Not Contain Element	xpath: //div[@name="${TABLENAME}"]//td/input
	Click Element	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]
	Sleep    0.3
	Click Element	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]
	Capture Page Screenshot
	Wait Until Element Is Visible	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]/input
	Input Text	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]/input	abc123
	Click Element	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-3"]
	Wait Until Element Is Not Visible	xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]/input
	Wait until page contains element  xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0" and contains(@class, "has-value")]
	${result}=	Get Text    xpath: //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]
	Should Be Equal As Strings	${result}	abc123

Remove Table with some spaces
	[Tags]	Delete	Table	Dialogues
	Remove Table	Table with some Spaces

Remove Table undefined
	[Tags]	Table
	${passed} =	Run Keyword And Return Status	Remove Table	undefined
	Run keyword if	${passed} 	Fail	Table undefined should not exist


*** Keywords ***
Open TDT GUI
	${orig timeout} = 	Set Selenium Timeout 	30 seconds
	Open Browser	about:blank	${BROWSER}
	Go To	http://${TDT_Host}/

TDT GUI End Test
	# give some time for background jobs to finish
	Sleep    10
	Close Browser


Value Edit Mode
	[Arguments]	${locator}
	Click Element	${locator}
	Sleep    0.3
	Click Element	${locator}


Remove Table
	[Arguments]	${TABLENAME}
	Wait Until Element Is Visible	xpath: //a[text()='${TABLENAME}']/../span
	Click Element    xpath: //a[text()='${TABLENAME}']/../span
	Wait Until Element Is Enabled	xpath: //span[contains(@class, 'ui-dialog-title') and contains(text(), 'Delete table')]
	Capture Page Screenshot
	Click Button    Delete
	Wait Until Element Is Not Visible	xpath: //span[contains(@class, 'ui-tabs-anchor') and contains(text(), '${TABLENAME}')]
