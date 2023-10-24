import os
import sqlite3
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI(
    title="Database Normalizer API",
    description="Class project for CS5300, spins up a FastAPI application inside a Docker container with endpoints for taking in a database schema, determining its normal form, and generating SQL queries to achieve a specified higher level of normalization.",
)

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile):
    """Upload a CSV file containing the schema and sample data you would like to assess normalization of. It will be parsed and loaded into an in-memory Db."""

    # Input Validation
    if not file.filename:
        raise HTTPException(status_code=400, detail="No File Provided.")

    allowed_extensions = {'.csv'}
    _, file_extension = os.path.splitext(file.filename)
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File extension must be .csv.")
    
    allowed_content_types = {'text/csv', 'application/vnd.ms-excel'}
    if file.content_type not in allowed_content_types:
        raise HTTPException(status_code=400, detail=f"File content_type is not text/csv. Content_Type: {file.content_type}")

    # Read the first line of the file which should contain the attribute names
    attribute_names = file.file.readline().decode().strip()
    
    # Create a list of SQL queries to output
    queries = []

    # Initialize in-memory SQLite Database
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()

    # Create a temporary relation with the given attribute names
    table_name = "TemporaryRelation"
    create_table_query = f"CREATE TABLE {table_name} ({attribute_names})"
    cursor.execute(create_table_query)
    queries.append(create_table_query)

    # Insert each record provided into the table we just created
    while True:
        line = file.file.readline().decode().strip()
        if not line:
            # End of File
            break
        formatted_values = ["'{}'".format(item) for item in line.split(',')]
        insert_query = f"INSERT INTO {table_name} ({attribute_names}) VALUES ({', '.join(formatted_values)})"
        cursor.execute(insert_query)
        queries.append(insert_query)

    # Commit the Changes to the Database
    connection.commit()

    # Close the Database Connection - this should remove the in-memory database
    connection.close()

    return {"queries_ran": queries}
    #return {"filename": file.filename, "content_type": file.content_type}