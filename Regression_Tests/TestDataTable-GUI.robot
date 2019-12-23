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
