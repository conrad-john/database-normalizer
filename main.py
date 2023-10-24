import os
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI(
    title="Database Normalizer API",
    description="Class project for CS5300, spins up a FastAPI application inside a Docker container with endpoints for taking in a database schema, determining its normal form, and generating SQL queries to achieve a specified higher level of normalization.",
)

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile):
    """Upload a CSV file containing the schema and sample data you would like to assess normalization of."""
    # Input Validation
    allowed_extensions = {'.csv'}
    _, file_extension = os.path.splitext(file.filename)
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File extension must be .csv.")
    
    allowed_content_types = {'text/csv', 'application/vnd.ms-excel'}
    if file.content_type not in allowed_content_types:
        raise HTTPException(status_code=400, detail=f"File content_type is not text/csv. Content_Type: {file.content_type}")
    
    file_content = await file.read()

    # Add contents to an in Memory Database
    # If the Database already contains a schema, raise an exception and prompt the user to a new 

    return {"filename": file.filename, "content_type": file.content_type}