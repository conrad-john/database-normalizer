import os
import sqlite3
from core.relation import Relation
from core.dependency import Dependency
from application.parse_csv import parse_csv
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from typing import List

app = FastAPI(
    title="Database Normalizer API",
    description="Class project for CS5300, spins up a FastAPI application inside a Docker container with endpoints for taking in a database schema, determining its normal form, and generating SQL queries to achieve a specified higher level of normalization.",
)

@app.post("/normalize-database/")
async def normalize_database(file: UploadFile, 
                             dependencies: List[str], 
                             target_normal_form: str = Query('1NF', enum=['1NF', '2NF', '3NF', 'BCNF', '4NF', '5NF']),
                             detect_current_normal_form: str = Query('Yes', enum=['Yes', 'No'])):

    relation = await parse_csv(file)

    return {"file_name": file.filename,
            "relation_name": relation.name,
            "dependencies": dependencies,
            "target_NF": target_normal_form,
            "current_NF": detect_current_normal_form}

'''
@app.post("/upload-csv/")
async def upload_csv(file: UploadFile, response_model=Relation):
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

    # Initialize in-memory SQLite Database
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()

    # Insert each record provided into the table we just created
    records = 0
    while True:
        line = file.file.readline().decode().strip()
        if not line:
            # End of File
            break
        formatted_values = ["'{}'".format(item) for item in line.split(',')]
        insert_query = f"INSERT INTO {table_name} ({attribute_names}) VALUES ({', '.join(formatted_values)})"
        cursor.execute(insert_query)
        records += 1

    # Commit the Changes to the Database
    connection.commit()

    # Close the Database Connection - this should remove the in-memory database
    connection.close()

    # Create the list of strings necessary for the next endpoint - POST Add-Dependency
    attribute_strings = attribute_names.split(',')

    return {"message": f"{file.filename} successfully parsed and put into in-memory database {table_name} with {records} records found.", "attribute_names": attribute_strings, "queries_ran": queries}

@app.post("/add-dependency/", response_model=Dependency)
async def add_dependency(input: str, attribute_names: List[str]) -> Dependency:
    """Add dependencies for the relation in the format 'X -> Y, ..., Z'"""
    # Input Validation
    if not input:
        raise HTTPException(status_code=400, detail=f"No Input String Provided for Dependency.")
    if '->' not in input:
        raise HTTPException(status_code=400, detail=f"Input string for dependency was not in required format. Examples: 'X -> Y', 'X -> Y, Z'")
    
    split_input = input.split('->')
    if len(split_input) > 2:
        raise HTTPException(status_code=400, detail=f"This application does not support the input of multiple dependency chains (e.g. X -> Y -> Z). Please separate dependencies.")
    
    parent = split_input[0].strip()
    children_string = split_input[1]
    children = children_string.replace(" ", "").split(',')

    if parent not in attribute_names:
        raise HTTPException(status_code=400, detail=f"{parent} attribute name was not present in the list of attributes built from the CSV. Please check the spelling of your dependencies against your CSV.")

    for child in children:
        if child.strip() not in attribute_names:
            raise HTTPException(status_code=400, detail=f"{child} attribute name was not present in the list of attributes built from the CSV. Please check the spelling of your dependencies against your CSV.")

    dependency = Dependency(parent=parent, children=children)

    return dependency
'''
# @app.get("/current-normal-form/")
# async def get_current_normal_form()