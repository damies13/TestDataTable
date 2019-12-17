# Rest Api

## Table operations

### GET /tables

Returns a list of tables

### PUT /<table name>

Creates the table

### DELETE /<table name>

Deletes the table

### GET /<table name>

Returns a list of columns in the table if the table exists

### GET /<table name>/row

Returns the column name / value pairs for the first record in every column in the table and removes these records from the table

### POST /<table name>/row

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

### GET /<table name>

Returns a list of columns in the table if the table exists

### PUT /<table name>/<column name>

Creates the column

### DELETE /<table name>/<column name>

Deletes the column

### GET /<table name>/<column name>

Retrieves the value from the first row in the column and removes it from the table

### POST /<table name>/<column name>

Appends the data value to the last row in the column

Example post data:
```
{
	"data": "<value>"
}
```
