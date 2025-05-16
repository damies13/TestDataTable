*** Settings ***
Resource    environment.robot

# https://github.com/MarketSquare/robotframework-browser
Library   Browser

Suite Setup		Open TDT GUI
Suite Teardown 	TDT GUI End Test

Test Tags	GUI 	ubuntu 	macos 	windows

*** Variables ***
# ${BROWSER}		ff
# chromium | firefox | webkit
${BROWSER}		chromium
${TABLENAME}		Regression_GUI_Browser_Chromium
${IMPORTCOL} 		Street Data %{MATRIX_PYTHON} %{MATRIX_PLATFORM}


*** Test Cases ***    Expression    Expected

Table names with multiple spaces
	[Tags] 	Create 	Table 	Issue-#17

	# Create Some Tables with Data In them
	FOR 	${i} 	IN RANGE 	3
		# 	PUT /<table name>/<column name>/<value>
		# PUT On Session 		TDT 	/Business Process Table ${i}/Test Column/Value ${i}
		# DELETE On Session 		TDT 	/Business_Process_Table_${i}
		&{res}= 	HTTP 	/Business Process Table ${i}/Test Column/Value ${i} 	PUT

		VAR 	${tablename} 	Business Process Table ${i}
		VAR 	${tablevalue} 	Value ${i}

	END

	Go To	http://${TDT_Host}/
	Take Screenshot

	VAR 	${tablename} 	Business Process Table 2

	Wait For Elements State 	//li/a[text()='${tablename}'] 	visible
	Click	//li/a[text()='${tablename}']
	Take Screenshot


	VAR 	${col_name} 	Test Column
	VAR 	${row_num} 		0

	${col_id}=	Get Attribute	//div[@name='${TABLENAME}']//th[span[text()='${col_name}']]	id

	${result}=	Get Text    //div[@name="${tablename}"]//td[@id="${col_id}-${row_num}"]
	Should Be Equal As Strings	${result}	${tablevalue}


*** Keywords ***
Open TDT GUI
	# ${orig timeout} = 	Set Selenium Timeout 	30 seconds
	# Open Browser	about:blank	${BROWSER}
	New Browser 	${BROWSER}	False
	New Page
	Set Browser Timeout 	60
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
	No Operation

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
