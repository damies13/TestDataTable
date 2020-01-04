# TestDataTable FAQ (frequently Asked Questions)

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
