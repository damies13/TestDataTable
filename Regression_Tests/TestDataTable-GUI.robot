*** Settings ***
Library           SeleniumLibrary

Suite Setup		Open TDT GUI
Suite Teardown	Close Browser

Default Tags	GUI

*** Variables ***
${BROWSER}		ff
# ${BROWSER}		chrome


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
	Should Contain	${helptitle}	TestDataTable/rest_api.md at master
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

	Input Text	id:table-name	Regression GUI
	Click Button    Create
	Wait Until Element Is Visible	xpath: //a[text()='Regression GUI']

Select Table
	[Tags]	Tabs	Table
	${handle} =	Select Window 	MAIN
	Wait Until Element Is Visible	xpath: //li/a[text()='Regression GUI']
	Click Element    xpath: //li/a[text()='Regression GUI']
	Wait Until Element Is Visible	xpath: //li[@aria-selected='true']/a[text()='Regression GUI']

Create New Column
	[Tags]	Button	Create	Column	Dialogues
	${handle} =	Select Window 	MAIN
	Wait Until Element Is Visible	xpath: //li/a[text()='Regression GUI']
	Click Element    xpath: //li/a[text()='Regression GUI']
	Wait Until Element Is Visible	xpath: //li[@aria-selected='true']/a[text()='Regression GUI']
	Click Button	Add Column
	Wait Until Element Is Enabled	xpath: //span[contains(@class, 'ui-dialog-title') and contains(text(), 'Add Column')]
	Capture Page Screenshot
	Input Text	id:column-name	GUI Column A
	Click Button    Add
	Wait Until Element Is Visible	xpath: //div[@name='Regression GUI']//th/span[text()='GUI Column A']

Add value to column
	[Tags]	Create	Column	Values
	${handle}=	Select Window 	MAIN
	# //div[@name="Demo 2"]//td[@id="1-0"]/text()
	Wait Until Element Is Visible	xpath: //div[@name="Regression GUI"]//td[@id="0-0"]
	Wait until page does not contain element  xpath: //div[@name="Regression GUI"]//td[@id="0-0" and contains(@class, "has-value")]
	Page Should Not Contain Element	xpath: //div[@name="Regression GUI"]//td/input
	Click Element	xpath: //div[@name="Regression GUI"]//td[@id="0-0"]
	Sleep    0.3
	Click Element	xpath: //div[@name="Regression GUI"]//td[@id="0-0"]
	Wait Until Element Is Visible	xpath: //div[@name="Regression GUI"]//td[@id="0-0"]/input
	Input Text	xpath: //div[@name="Regression GUI"]//td[@id="0-0"]/input	Column A Row 0
	Click Element	xpath: //div[@name="Regression GUI"]//td[@id="0-3"]
	Wait Until Element Is Not Visible	xpath: //div[@name="Regression GUI"]//td[@id="0-0"]/input
	Wait until page contains element  xpath: //div[@name="Regression GUI"]//td[@id="0-0" and contains(@class, "has-value")]
	${result}=	Get Text    xpath: //div[@name="Regression GUI"]//td[@id="0-0"]
	Should Be Equal As Strings	${result}	Column A Row 0

Add some test data
	[Tags]	Create	Column	Values
	${handle} =	Select Window 	MAIN
	FOR    ${index}    IN RANGE    10
		${incell}=	Evaluate    ${index}+1
		${outcell}=	Evaluate    ${index}+5
		Value Edit Mode	xpath: //div[@name="Regression GUI"]//td[@id="0-${incell}"]
		Input Text	xpath: //div[@name="Regression GUI"]//td[@id="0-${incell}"]/input	Column A Row ${incell}
		Click Element	xpath: //div[@name="Regression GUI"]//td[@id="0-${outcell}"]
	END
	Click Button	Add Column
	Wait Until Element Is Enabled	xpath: //span[contains(@class, 'ui-dialog-title') and contains(text(), 'Add Column')]
	Input Text	id:column-name	GUI Column B
	Click Button    Add
	Wait Until Element Is Visible	xpath: //div[@name='Regression GUI']//th/span[text()='GUI Column B']
	FOR    ${index}    IN RANGE    11
		${incell}=	Evaluate    ${index}+0
		${outcell}=	Evaluate    ${index}+3
		Value Edit Mode	xpath: //div[@name="Regression GUI"]//td[@id="1-${incell}"]
		Input Text	xpath: //div[@name="Regression GUI"]//td[@id="1-${incell}"]/input	Column B Row ${incell}
		Click Element	xpath: //div[@name="Regression GUI"]//td[@id="1-${outcell}"]
	END
	Capture Page Screenshot

Edit Value
	[Tags]	Update	Values
	${col}=	Set Variable    0
	${row}=	Set Variable    3
	${result}=	Get Text    xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${result}	Column A Row ${row}
	Value Edit Mode	xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]
	# Press Keys	None	ARROW_RIGHT
	Input Text	xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]/input	${result} abc
	${outcell}=	Evaluate    ${row}+3
	Click Element	xpath: //div[@name="Regression GUI"]//td[@id="${col}-${outcell}"]
	${result}=	Get Text    xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${result}	Column A Row ${row} abc

Replace Value
	[Tags]	Update	Values
	${col}=	Set Variable    0
	${row}=	Set Variable    5
	${result}=	Get Text    xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${result}	Column A Row ${row}
	Value Edit Mode	xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]
	Clear Element Text	xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]/input
	Input Text	xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]/input	my new value
	${outcell}=	Evaluate    ${row}+3
	Click Element	xpath: //div[@name="Regression GUI"]//td[@id="${col}-${outcell}"]
	${result}=	Get Text    xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${result}	my new value

Remove Last Value
	[Tags]	Delete	Values
	${col}=	Set Variable    1
	${row}=	Set Variable    10
	${startval}=	Get Text    xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${startval}	Column B Row ${row}
	Value Edit Mode	xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]
	Clear Element Text	xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]/input
	${outcell}=	Evaluate    ${row}+3
	Click Element	xpath: //div[@name="Regression GUI"]//td[@id="${col}-${outcell}"]
	${endval}=	Get Text    xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]
	Should Not Be Equal As Strings	${endval}	${startval}
	Should Be Equal As Strings	"${endval}"	" "
	Wait until page does not contain element  xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}" and contains(@class, "has-value")]


Remove 3rd Value
	[Tags]	Delete	Values
	${col}=	Set Variable    1
	${row}=	Set Variable    3
	${lastrow}=	Set Variable    9
	${nextrow}=	Evaluate	${row}+1
	${startvalue}=	Get Text    xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]
	Should Be Equal As Strings	${startvalue}	Column B Row ${row}
	Value Edit Mode	xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]
	Clear Element Text	xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]/input
	${outcell}=	Evaluate    ${row}+3
	Click Element	xpath: //div[@name="Regression GUI"]//td[@id="${col}-${outcell}"]
	${endval}=	Get Text    xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}"]
	Should Not Be Equal As Strings	${endval}	${startvalue}
	Should Be Equal As Strings	${endval}	Column B Row ${nextrow}
	Wait until page does not contain element  xpath: //div[@name="Regression GUI"]//td[@id="${col}-${lastrow}" and contains(@class, "has-value")]
	Wait until page contains element  xpath: //div[@name="Regression GUI"]//td[@id="${col}-${row}" and contains(@class, "has-value")]
	Wait until page contains element  xpath: //div[@name="Regression GUI"]//td[@id="${col}-${nextrow}" and contains(@class, "has-value")]


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
	Click Button    Delete
	Wait Until Element Is Not Visible	xpath: //th[@name="GUI Column B"]


Remove Table
	[Tags]	Delete	Table	Dialogues
	${handle} =	Select Window 	MAIN
	# Wait Until Element Is Enabled	xpath: //a[text()='Regression GUI']/../span
	Wait Until Element Is Visible	xpath: //a[text()='Regression GUI']/../span
	Click Element    xpath: //a[text()='Regression GUI']/../span
	# 					  //span[@table="Regression GUI"]
	Wait Until Element Is Enabled	xpath: //span[contains(@class, 'ui-dialog-title') and contains(text(), 'Delete table')]
	Capture Page Screenshot
	Click Button    Delete
	Wait Until Element Is Not Visible	xpath: //span[contains(@class, 'ui-tabs-anchor') and contains(text(), 'Regression GUI')]


*** Keywords ***
Open TDT GUI
	Open Browser	about:blank	${BROWSER}
	Go To	http://localhost/

Value Edit Mode
	[Arguments]	${locator}
	Click Element	${locator}
	Sleep    0.3
	Click Element	${locator}
