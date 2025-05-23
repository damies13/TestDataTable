*** Settings ***
Library 	OperatingSystem
Library 	Process
# Library 	DatabaseLibrary
Library 	String
Library 	Collections

*** Variables ***
${tdt_pyfile}		${EXECDIR}${/}testdatatable${/}TestDataTable.py
${cmd_tdt} 			python3

*** Keywords ***
Set Platform
	Set Platform By Python
	Set Platform By Tag

Set Platform By Python
	${system}= 		Evaluate 	platform.system() 	modules=platform

	IF 	"${system}" == "Darwin"
		Set Suite Variable    ${platform}    macos
	END
	IF 	"${system}" == "Windows"
		Set Suite Variable    ${platform}    windows
	END
	IF 	"${system}" == "Linux"
		Set Suite Variable    ${platform}    ubuntu
	END

Set Platform By Tag
	# [Arguments]		${ostag}
	Log 	${OPTIONS}
	Log 	${OPTIONS}[include]
	Log 	${OPTIONS}[include][0]
	${ostag}= 	Set Variable 	${OPTIONS}[include][0]

	IF 	"${ostag}" == "macos-latest"
		Set Suite Variable    ${platform}    macos
	END
	IF 	"${ostag}" == "windows-latest"
		Set Suite Variable    ${platform}    windows
	END
	IF 	"${ostag}" == "ubuntu-latest"
		Set Suite Variable    ${platform}    ubuntu
	END

Show Log
	[Arguments]		${filename}
	Log 		${\n}-----${filename}----- 		console=True
	${filedata}= 	Get File 	${filename} 		encoding=SYSTEM 		encoding_errors=ignore
	Log 		${filedata} 		console=True
	Log 		-----${filename}-----${\n} 		console=True
	RETURN 		${filedata}

Read Log
	[Arguments]		${filename}
	Log 		${filename}
	${filedata}= 	Get File 	${filename} 		encoding=SYSTEM 		encoding_errors=ignore
	Log 		${filedata}
	RETURN 		${filedata}

Clean Up Old Files
		[Tags]	ubuntu-latest 	macos-latest 	windows-latest
		# cleanup previous output
		Log To Console    ${OUTPUT DIR}
		Remove File    ${OUTPUT DIR}${/}*.txt
		Remove File    ${OUTPUT DIR}${/}*.png
		# Remove File    ${OUTPUT DIR}${/}sikuli_captured${/}*.*

Open Test Data Table
	[Arguments]		@{appargs}
	${var}= 	Get Variables
	Log 	${var}
	${cmdtdt_process}= 	Start Process 	${cmd_tdt} 	${tdt_pyfile} 	@{appargs}    alias=TDT 	stdout=${OUTPUT DIR}${/}stdout.txt 	stderr=${OUTPUT DIR}${/}stderr.txt
	Set Suite Variable 	$cmdtdt_process 	${cmdtdt_process}

Wait For Test Data Table
	[Arguments]		${timeout}=15min
	${result}= 	Wait For Process		${cmdtdt_process} 	timeout=${timeout} 	on_timeout=terminate
	# Should Be Equal As Integers 	${result.rc} 	0
	# Log to console 	Manager exited with: ${result.rc}

	TRY
		Log 	Test Data Table exited with: ${result.rc} 		console=true

		Copy File 	${result.stdout_path} 	${OUTPUT DIR}${/}${TEST NAME}${/}stdout_tdt.txt
		Copy File 	${result.stderr_path} 	${OUTPUT DIR}${/}${TEST NAME}${/}stderr_tdt.txt

		Log 	stdout_path: ${result.stdout_path} 	console=True
		Log 	stdout: ${result.stdout} 	console=True
		Log 	stderr_path: ${result.stderr_path} 	console=True
		Log 	stderr: ${result.stderr} 	console=True
	EXCEPT 	AS 	${error}
		Log 	error: ${error} 		console=true
	END

Stop Test Data Table
	${running}= 	Is Process Running 	${cmdtdt_process}
	IF 	${running}
		Sleep	3s
		IF  '${platform}' == 'windows'	# Send Signal To Process keyword does not work on Windows
			${result}= 	Terminate Process		${cmdtdt_process}
		ELSE
			Send Signal To Process 	SIGINT 	${cmdtdt_process}
			${result}= 	Wait For Process 	${cmdtdt_process}	timeout=30	on_timeout=kill
		END
	ELSE
		TRY
			# get result var for process even if not running any more
			${result}= 	Get Process Result		${cmdtdt_process}
		EXCEPT 	AS 	${error}
			Log 	error: ${error} 		console=true
		END
	END

	TRY
		Copy File 	${result.stdout_path} 	${OUTPUT DIR}${/}${TEST NAME}${/}stdout_tdt.txt
		Copy File 	${result.stderr_path} 	${OUTPUT DIR}${/}${TEST NAME}${/}stderr_tdt.txt

		Log to console 	Terminate Manager Process returned: ${result.rc} 	console=True
		Log 	stdout_path: ${result.stdout_path} 	console=True
		Log 	stdout: ${result.stdout} 	console=True
		Log 	stderr_path: ${result.stderr_path} 	console=True
		Log 	stderr: ${result.stderr} 	console=True
	EXCEPT 	AS 	${error}
		Log 	error: ${error} 		console=true
	END

Dict to INI
	[Arguments]		${data} 	${inifile}=${OUTPUT DIR}${/}${TEST NAME}${/}${TEST NAME}.ini

	FOR    ${key}    ${value}    IN    &{data}
		Append To File 	${inifile} 		[${key}]\n
		FOR    ${subkey}    ${subvalue}    IN    &{value}
			Append To File 	${inifile} 		${subkey} =${subvalue}\n
		END
		Append To File 	${inifile} 		\n
	END






#
