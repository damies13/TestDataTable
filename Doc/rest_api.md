# Rest Api

## Table operations

### GET /tables

Returns a list of tables

### PUT /&lt;table name&gt;

Creates the table

### DELETE /&lt;table name&gt;

Deletes the table

### GET /&lt;table name&gt;

Returns the complete table as a json object if the table exists

### GET /&lt;table name&gt;/columns

Returns a list of columns in the table if the table exists

### GET /&lt;table name&gt;/row

Returns the column name / value pairs for the first record in every column in the table and removes these records from the table

### GET /&lt;table name&gt;/&lt;id&gt;

Returns the column name / value pairs for every column in the table for the nominated row id and removes these records from the table

### POST /&lt;table name&gt;/row

With post body containing the column name / value pairs for every column in the table, append a new row with these values to the table.

Example post data:
```
{
	"data": [
		"<column name>": "<value>",
		"<column name>": "<value>",
		"<column name>": "<value>"
	]
}
```

This operation will fail if:
- not all columns in the table are in the post data
- columns in the table have different lengths


## Column operations

### GET /&lt;table name&gt;

Returns a list of columns in the table if the table exists

### PUT /&lt;table name&gt;/&lt;column name&gt;

Creates the column

### DELETE /&lt;table name&gt;/&lt;column name&gt;

Deletes the column

### GET /&lt;table name&gt;/&lt;column name&gt;

Retrieves the value from the first row in the column and removes it from the table

### GET /&lt;table name&gt;/&lt;column name&gt;/&lt;id&gt;

Retrieves a specific row's value in the column based on it's id and removes it from the table

### GET /&lt;table name&gt;/&lt;column name&gt;/all

Retrieves all the values in the column, does not remove any values

### PUT /&lt;table name&gt;/&lt;column name&gt;/&lt;value&gt;

Appends the value to the last row in the column

Example post data:
```
{
	"data": "<value>"
}
```
