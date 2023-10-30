import logging
from core.relation import Relation
from core.dependency import Dependency
from application.parse_csv import parse_csv
from application.parse_dependencies import parse_dependencies
from application.determine_normal_form import determine_normal_form
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from typing import List

app = FastAPI(
    title="Database Normalizer API",
    description="Class project for CS5300, spins up a FastAPI application inside a Docker container with endpoints for taking in a database schema, determining its normal form, and generating SQL queries to achieve a specified higher level of normalization.",
)

@app.post("/normalize-database")
async def normalize_database(file: UploadFile, 
                             keys: List[str],
                             dependencies_input: List[str], 
                             target_normal_form: str = Query('1NF', enum=['1NF', '2NF', '3NF', 'BCNF', '4NF', '5NF']),
                             detect_current_normal_form: str = Query('Yes', enum=['Yes', 'No'])):

    # Parse the CSV file into a given relation
    print("\nStarting to Parse CSV file.\n")
    relation = await parse_csv(file, keys)
    print(f"\nFinished parsing CSV file.\n{relation.to_json()}\n")

    # Parse out the dependencies into a list of usable objects
    print("\nStarting to Parse Dependencies.\n")
    dependencies = await parse_dependencies(relation, dependencies_input)
    print(f"\nFinished parsing Dependencies.\n{[dependency.to_json() for dependency in dependencies]}\n")

    # Retrieve the Current Normal Form of the input relation if requested
    cnf = "Not Requested"
    print("\nGetting the current normal form of the relation.")
    if detect_current_normal_form == 'Yes':
        cnf = await determine_normal_form(relation, dependencies)
    print(f"\nCurrent Normal Form: {cnf}")



    return {"file_name": file.filename,
            "relation": relation,
            "dependencies": dependencies,
            "target_NF": target_normal_form,
            "current_NF": cnf}