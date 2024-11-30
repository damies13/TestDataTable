# TestDataTable FAQ (frequently Asked Questions)

## There's been no updates for a while is this project abandoned?

No this project has not been abandoned, all features I intended to implement have been implemented, so it's effectively feature complete for now.

If you have features you'd like added or find a bug please raise a feature request or bug report. otherwise I'll rerun the regression suite with each python version and will update if needed.

## I don't like the colour scheme you used.

No problem, just change it to a colour scheme you like, see the [Theming](./InstallationAndConfiguration.md#theming-changing-the-colour-scheme) section in the documentation for details.

## Can I use TestDataTable with XYZ test tool?

As long as the test tool can be configured to make standard HTTP Rest calls (GET, POST, PUT and DELETE) you should be able to have your test script interact with TestDataTable. I have never come across a test tool that could not be configured to do this, so the answer is probably yes.

The minimum you will need are:
- GET /&lt;table name&gt;/&lt;column name&gt;	(to retrieve a value from a column)
	and
- PUT /&lt;table name&gt;/&lt;column name&gt;/&lt;value&gt;			(to send a value to a column)

The full details are available in the [API Documentation](./rest_api.md)

## I need to use a different port from port 80 for some reason

No problem, just change the [port number in the ini file configuration](./InstallationAndConfiguration.md#Configuration)

## I need multiple TestDataTable's but I only have one server to run them on

No problem, just create a seperate ini file for each instance you need. The minimum you will need to change in the [configuration](./InstallationAndConfiguration.md#Configuration) of each ini file is the bindport and dbfile settings, though you may want to also change the theme for each instance so your users can quickly and easily distinguish between them.

Simply use the -i or --ini command when launching each instance:
```
python TestDataTable.py -i <your ini file>
```

## I'm using Robot Framework do you have examples of how to use TestDataTable with Robot Framework?

Your in luck, we used Robot Framework for our Regression testing of TestDataTable. There are example with 2 libraries that are both quite easy to use. Those are the [REST Library](../Regression_Tests/TestDataTable-API_REST.robot) and the [Requests Library](../Regression_Tests/TestDataTable-API_requests.robot)

## I'm using JMeter do you have examples of how to use TestDataTable with JMeter?

Your in luck, [there are some examples with screen shots here](../TestTools/JMeter/JMeter.md)


## I'm using another test tool do you have examples of how to use TestDataTable with other tools?

Sorry not yet, to start with see FAQ: [Can I use TestDataTable with XYZ test tool?](#can-i-use-testdatatable-with-xyz-test-tool)

If you would like your favorite test tool added to the documentation for TestDataTable please create an [Issue](https://github.com/damies13/TestDataTable/issues) along the lines of "please document XYZ test tool for TestDataTable" and we will try to get to it for you.
