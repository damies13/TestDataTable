*** Settings ***
Resource    environment.robot

# https://github.com/MarketSquare/robotframework-browser
Library   Browser

Suite Setup		Open TDT GUI
Suite Teardown	TDT GUI End Test

Default Tags	GUI

*** Variables ***
# ${BROWSER}		ff
# chromium | firefox | webkit
${BROWSER}		firefox
${TABLENAME}		Regression_GUI_Browser_FireFox


*** Test Cases ***    Expression    Expected

Open Help
	[Tags]	Button	Help
	${handle_main}=	Get Page Ids	CURRENT
	Take Screenshot
	${maintitle}=	Get Title
	# Click Button 	Help
	Click	//button[@id="help"]
	${handle}=	Switch Page 	NEW
	Wait For Elements State 	"Rest Api"	visible
	# Get Text	"Rest Api"
	Take Screenshot
	${helptitle}=	Get Title
	Should Contain	${helptitle}	TestDataTable/Doc/rest_api.md at master
	Close Page
	${handle}=	Switch Page 	${handle_Main[0]}

Click Refresh Button
	[Tags]	Button
	${handle_main}=	Get Page Ids	CURRENT
	# Click Button	Refresh
	Click	//button[@title="Refresh"]

Create New Table
	[Tags]	Button	Create	Table	Dialogues
	${handle_main}=	Get Page Ids	CURRENT
	Click	//button[@title="Add Table"]
	Wait For Elements State 	//span[contains(@class, 'ui-dialog-title') and contains(text(), 'Create table')]	enabled
	Take Screenshot
	Fill Text	input#table-name	${TABLENAME}
	Click 	"Create"
	Wait For Elements State 	//a[text()='${TABLENAME}']	visible

Select Table
	[Tags]	Tabs	Table
	${handle_main}=	Get Page Ids	CURRENT
	Wait For Elements State 	//li/a[text()='${TABLENAME}'] 	visible
	Click	//li/a[text()='${TABLENAME}']
	Wait For Elements State 	//li[@aria-selected='true']/a[text()='${TABLENAME}']	visible

Create New Column
	[Tags]	Button	Create	Column	Dialogues
	${handle_main}=	Get Page Ids	CURRENT
	Wait For Elements State 	//li/a[text()='${TABLENAME}'] 	visible
	Click	//li/a[text()='${TABLENAME}']
	Wait For Elements State 	//li[@aria-selected='true']/a[text()='${TABLENAME}']	visible
	# Click Button	Add Column
	Click	//button[@title="Add Column"]
	Wait For Elements State 	//span[contains(@class, 'ui-dialog-title') and contains(text(), 'Add Column')]	enabled
	Take Screenshot
	Fill Text	input#column-name	GUI Column A
	Click 	"Add"
	Wait For Elements State 	//div[@name='${TABLENAME}']//th/span[text()='GUI Column A']	visible
	${col_a_id}=	Get Attribute	//div[@name='${TABLENAME}']//th/span[text()='GUI Column A']/..	id
	Set Global Variable 	${col_a_id} 	${col_a_id}

Add value to column
	[Tags]	Create	Column	Values
	Wait For Elements State 	//div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]	visible
	Wait For Elements State 	//div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0" and contains(@class, "has-value")]	detached
	Wait For Elements State 	//div[@name="${TABLENAME}"]//td/input 	detached
	Click	//div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]
	Sleep    0.3
	Click	//div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]
	Take Screenshot
	Wait For Elements State 	//div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]/input	visible
	Fill Text	//div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]/input	Column A Row 0
	Click	//div[@name="${TABLENAME}"]//td[@id="${col_a_id}-3"]
	Wait For Elements State 	//div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]/input	hidden
	Wait For Elements State 	//div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0" and contains(@class, "has-value")]	visible
	${result}=	Get Text    //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-0"]
	Should Be Equal As Strings	${result}	Column A Row 0

Add some test data
	[Tags]	Create	Column	Values
	FOR    ${index}    IN RANGE    10
		${incell}=	Evaluate    ${index}+1
		${outcell}=	Evaluate    ${index}+3
		Value Edit Mode 	//div[@name="${TABLENAME}"]//td[@id="${col_a_id}-${incell}"]
		Fill Text	//div[@name="${TABLENAME}"]//td[@id="${col_a_id}-${incell}"]/input	Column A Row ${incell}
		Click	//div[@name="${TABLENAME}"]//td[@id="${col_a_id}-${outcell}"]
		# Wait until page contains element  //div[@name="${TABLENAME}"]//td[@id="${col_a_id}-${incell}" and contains(@class, "has-value")]
		Wait For Elements State 	//div[@name="${TABLENAME}"]//td[@id="${col_a_id}-${incell}" and contains(@class, "has-value")]	visible
	END
	# Click Button	Add Column
	Click	//button[@title="Add Column"]
	Wait For Elements State 	//span[contains(@class, 'ui-dialog-title') and contains(text(), 'Add Column')]	enabled
	Fill Text	input#column-name	GUI Column B
	Click 	"Add"
	Wait For Elements State 	//div[@name='${TABLENAME}']//th/span[text()='GUI Column B']	visible
	${col_b_id}=	Get Attribute	//div[@name='${TABLENAME}']//th/span[text()='GUI Column B']/..	id
	Set Global Variable 	${col_b_id} 	${col_b_id}
	FOR    ${index}    IN RANGE    11
		${incell}=	Evaluate    ${index}+0
		${outcell}=	Evaluate    ${index}+3
		Value Edit Mode 	//div[@name="${TABLENAME}"]//td[@id="${col_b_id}-${incell}"]
		Fill Text	//div[@name="${TABLENAME}"]//td[@id="${col_b_id}-${incell}"]/input	Column B Row ${incell}
		Click	//div[@name="${TABLENAME}"]//td[@id="${col_b_id}-${outcell}"]
	END
	Take Screenshot

Edit Value
	[Tags]	Update	Values
	${col}=	Set Variable    ${col_a_id}
	${row}=	Set Variable    3
	${result}=	Get Text    //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${result}	Column A Row ${row}
	Value Edit Mode	//div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Take Screenshot
	# Press Keys	None	ARROW_RIGHT
	Fill Text	//div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]/input	${result} abc
	${outcell}=	Evaluate    ${row}+3
	Click	//div[@name="${TABLENAME}"]//td[@id="${col}-${outcell}"]
	${result}=	Get Text    //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${result}	Column A Row ${row} abc

Replace Value
	[Tags]	Update	Values
	${col}=	Set Variable    ${col_a_id}
	${row}=	Set Variable    5
	${result}=	Get Text    //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${result}	Column A Row ${row}
	Value Edit Mode	//div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Clear Text	//div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]/input
	Fill Text	//div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]/input	my new value
	${outcell}=	Evaluate    ${row}+3
	Click	//div[@name="${TABLENAME}"]//td[@id="${col}-${outcell}"]
	${result}=	Get Text    //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${result}	my new value

Remove Last Value
	[Tags]	Delete	Values
	${col}=	Set Variable    ${col_b_id}
	${row}=	Set Variable    10
	${startval}=	Get Text    //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${startval}	Column B Row ${row}
	Value Edit Mode	//div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Clear Text	//div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]/input
	${outcell}=	Evaluate    ${row}+3
	Click	//div[@name="${TABLENAME}"]//td[@id="${col}-${outcell}"]
	${endval}=	Get Text    //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Take Screenshot
	Should Not Be Equal As Strings	${endval}	${startval}
	# Should Be Equal As Strings	"${endval}"	" "
	# " " != " "
	Wait until page does not contain element  //div[@name="${TABLENAME}"]//td[@id="${col}-${row}" and contains(@class, "has-value")]


Remove 3rd Value
	[Tags]	Delete	Values
	${col}=	Set Variable    ${col_b_id}
	${row}=	Set Variable    3
	${lastrow}=	Set Variable    9
	${nextrow}=	Evaluate	${row}+1
	${startvalue}=	Get Text    //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${startvalue}	Column B Row ${row}
	Value Edit Mode	//div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Clear Text	//div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]/input
	${outcell}=	Evaluate    ${row}+3
	Click	//div[@name="${TABLENAME}"]//td[@id="${col}-${outcell}"]
	Wait until page does not contain element  //div[@name="${TABLENAME}"]//td[@id="${col}-${lastrow}" and contains(@class, "has-value")]
	Wait until page contains element  //div[@name="${TABLENAME}"]//td[@id="${col}-${row}" and contains(@class, "has-value")]
	Wait until page contains element  //div[@name="${TABLENAME}"]//td[@id="${col}-${nextrow}" and contains(@class, "has-value")]
	${endval}=	Get Text    //div[@name="${TABLENAME}"]//td[@id="${col}-${row}"]
	Should Not Be Equal As Strings	${endval}	${startvalue}
	Should Be Equal As Strings	${endval}	Column B Row ${nextrow}


Remove Column
	[Tags]	Delete	Column	Dialogues
	# //th[@name="Ninja"]/span[contains(@class, "ui-icon-close")]
	Wait Until Element Is Visible	//th[@name="GUI Column B"]/span[contains(@class, "ui-icon-close")]
	Click    //th[@name="GUI Column B"]/span[contains(@class, "ui-icon-close")]
	Wait Until Element Is Enabled	//span[contains(@class, 'ui-dialog-title') and contains(text(), 'Delete column')]
	Wait Until Element Is Visible	id=dialog-delete-column
	${dialogueMsg}= 	Get Text    id=dialog-delete-column
	Take Screenshot
	Click    //div[@id='dialog-delete-column']/..//button[text()='Delete']
	Wait Until Element Is Not Visible	//th[@name="GUI Column B"]


Import Data From File
	[Tags]	Create	Column	Values	Import
	# Click Button	Import File
	Click	id=import-file
	Wait Until Element Is Enabled	//span[contains(@class, 'ui-dialog-title') and contains(text(), 'Text File Import')]
	Take Screenshot
	# Click    id=dialog-file-import-file
	Choose File 	id=dialog-file-import-file 	${CURDIR}${/}testdata${/}GC_5k.csv
	Take Screenshot
	${hdrrow0}= 	Get Text 	id=preview-c0
	Should Be Equal As Strings	${hdrrow0}	Rand
	${hdrrow1}= 	Get Text 	id=preview-c1
	Should Be Equal As Strings	${hdrrow1}	street_no_1
	${hdrrow2}= 	Get Text 	id=preview-c2
	Should Be Equal As Strings	${hdrrow2}	road_name
	Click    id=dialog-file-import-header-row
	${nohdrow1}= 	Get Text 	id=preview-c1
	Should Be Equal As Strings	${nohdrow1}	1
	${datacell1}= 	Get Text	id=preview-tablecell-1-1
	Should Be Equal As Strings	${hdrrow1}	${datacell1}
	Take Screenshot
	Click    id=dialog-file-import-header-row
	Click    	"tab"
	${delim}= 	Get Text 	id=dialog-file-import-delimiter
	Should Be Equal As Strings		${delim}	\t
	# Wait Until Keyword Succeeds    10s    200ms    Textfield Should Contain    id=dialog-file-import-delimiter    \t
	${hdrrow0_delim}= 	Get Text 	id=preview-c0
	Should Be Equal As Strings	${hdrrow0_delim}	${hdrrow0},${hdrrow1},${hdrrow2}
	Take Screenshot
	${datacell0}= 	Get Text	id=preview-tablecell-1-0
	${newhdr}=		Set Variable    Street Data
	Fill Text		id=preview-c0	${newhdr}
	${chknewhdr}= 	Get Text 	id=preview-c0
	Should Be Equal As Strings	${newhdr}	${newhdr}
	Take Screenshot
	Click    "Import"
	# Wait Until Element Is Visible	id=dialog-progress-bar
	Wait Until Element Is Visible	id=dialog-progress-subject
	# Wait Until Element Contains	id=dialog-progress-msg	Loading
	Wait Until Element Is Visible	//*[@id="dialog-progress-msg" and contains(text(), "Loading")]
	Take Screenshot
	# Wait Until Element Contains	id=dialog-progress-msg	%
	Wait Until Element Is Visible	//*[@id="dialog-progress-msg" and contains(text(), "%")]
	Take Screenshot
	# Wait Until Element Contains	id=dialog-progress-msg	100%
	Wait Until Element Is Visible	//*[@id="dialog-progress-msg" and contains(text(), "100%")]
	Sleep    1
	Take Screenshot
	# Wait Until Element Is Not Visible	id=dialog-progress-bar
	Wait Until Element Is Not Visible	id=dialog-progress-subject
	Wait Until Element Is Visible	//*[@name="Street Data"]
	Take Screenshot
	${colid}=	Get Attribute	//*[@name="Street Data"]	id
	${chk1strow}= 	Get Text	id=${colid}-0
	Should Be Equal As Strings	${datacell0}	${chk1strow}


Export Data To File
	[Tags]	Table	Column	Values	Export
	Wait Until Element Is Visible	//*[@name="Street Data"]
	${colid}=	Get Attribute	//*[@name="Street Data"]	id
	${chk1strow}= 	Get Text	id=${colid}-0
	Click	id=export-file
	Wait Until Element Is Enabled	//span[contains(@class, 'ui-dialog-title') and contains(text(), 'Text File Export')]
	Take Screenshot
	Wait Until Keyword Succeeds    60s    200ms    Textarea Should Contain 	//div[@id='dialog-file-export-preview']/textarea		Street Data
	Take Screenshot
	${filename}= 	Get Text 	id=dialog-file-export-filename
	Should Contain 	${filename} 	.csv
	Textarea Should Contain 	//div[@id='dialog-file-export-preview']/textarea		Street Data
	Textarea Should Contain 	//div[@id='dialog-file-export-preview']/textarea		"${chk1strow}"
	Click    id=dialog-file-export-header-row
	${txtarea}= 	Get Text 	//div[@id='dialog-file-export-preview']/textarea
	Should Not Contain		${txtarea}		Street Data
	Take Screenshot
	Click    id=dialog-file-export-header-row
	Wait Until Keyword Succeeds    60s    200ms    Textarea Should Contain 	//div[@id='dialog-file-export-preview']/textarea		Street Data
	Click    	id=dialog-file-export-insert-tab
	${delim}= 	Get Text 	id=dialog-file-export-delimiter
	Should Be Equal As Strings		${delim}	\t
	Wait Until Keyword Succeeds    60s    200ms    Textarea Should Contain 	//div[@id='dialog-file-export-preview']/textarea		Street Data
	Textarea Should Contain 	//div[@id='dialog-file-export-preview']/textarea		${chk1strow}
	${txtarea}= 	Get Text 	//div[@id='dialog-file-export-preview']/textarea
	Should Not Contain		${txtarea}		"${chk1strow}"
	${filename}= 	Get Text 	id=dialog-file-export-filename
	Should Contain 	${filename} 	.tsv
	Take Screenshot
	Fill Text		id=dialog-file-export-delimiter	|
	Click    id=dialog-file-export-filename
	${filename}= 	Get Text 	id=dialog-file-export-filename
	Should Contain 	${filename} 	.txt
	# $x('//div[@id="dialog-file-export"]/..//button[text()="Cancel"]')
	# Click Button    Cancel
	Take Screenshot
	Click    //div[@id="dialog-file-export"]/..//button[text()="Cancel"]

Remove Table
	[Tags]	Delete	Table	Dialogues
	${handle_main}=	Get Page Ids	CURRENT
	Wait For Elements State 	//li/a[text()='${TABLENAME}'] 	visible
	Click	//a[text()='${TABLENAME}']/../span
	Wait For Elements State 	//span[contains(@class, 'ui-dialog-title') and contains(text(), 'Delete table')]	enabled
	Take Screenshot
	Click	"Delete"
	Wait For Elements State 	//span[contains(@class, 'ui-tabs-anchor') and contains(text(), '${TABLENAME}')]	detached


*** Keywords ***
Open TDT GUI
	# ${orig timeout} = 	Set Selenium Timeout 	30 seconds
	# Open Browser	about:blank	${BROWSER}
	New Browser 	${BROWSER}	False
	New Page
	Set Browser Timeout 	30
	Go To	http://${TDT_Host}/
	# Go To	http://localhost/


TDT GUI End Test
	# give some time for background jobs to finish
	Sleep    10
	Close Browser


Value Edit Mode
	[Arguments]	${locator}
	Click	${locator}
	Sleep    0.3
	Click	${locator}


# SeleniumLibrary simulation Functions
Wait until page does not contain element
	[Arguments]	${locator}
	Wait For Elements State 	${locator}	detached

Wait until page contains element
	[Arguments]	${locator}
	Wait For Elements State 	${locator}	attached

Wait Until Element Is Visible
	[Arguments]	${locator}
	Wait For Elements State 	${locator}	visible

Wait Until Element Is Enabled
	[Arguments]	${locator}
	Wait For Elements State 	${locator}	enabled

Wait Until Element Is Not Visible
	[Arguments]	${locator}
	Wait For Elements State 	${locator}	hidden

Wait Until Element Contains
	[Arguments]	${locator}	${file}


Choose File
	[Arguments]	${locator}	${file}
	# Choose File 	id=dialog-file-import-file 	${CURDIR}${/}testdata${/}GC_5k.csv
	# Upload File    ${file}
	# Click          ${locator}
	# Seems the way it used to work was a mix between `Upload File By Selector` and `Promise To Upload File`
	Upload File By Selector 		${locator} 		${file}


Textarea Should Contain
	[Arguments]	${locator}	${value}
	# ${filename}= 	Get Text 	id=dialog-file-export-filename
	# Should Contain 	${filename} 	.csv
	# Textarea Should Contain 	//div[@id='dialog-file-export-preview']/textarea		Street Data
	${text}= 	Get Text 	${locator}
	Should Contain	${text}	${value}


#
