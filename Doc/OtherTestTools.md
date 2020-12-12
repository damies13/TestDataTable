# Other Test Tools

If the test tool you are using is not listed here with examples of how to use it with TestDataTable, it does not mean you can't, it just means we don't have an example yet.

As long as the test tool can be configured to make standard HTTP Rest calls (GET, POST, PUT and DELETE) you should be able to have your test script interact with TestDataTable. I have never come across a test tool that could not be configured to do this, so the answer is probably yes.

The minimum you will need are:
- GET /&lt;table name&gt;/&lt;column name&gt;	(to retrieve a value from a column)
	and
- PUT /&lt;table name&gt;/&lt;column name&gt;/&lt;value&gt;			(to send a value to a column)

The full details are available in the [API Documentation](./rest_api.md)

Once you have it working with your test tool please share with us so we can add some examples here and help others.
