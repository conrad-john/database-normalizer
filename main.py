import os
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI()

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile):
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

    return {"filename": file.filename, "content_type": file.content_type}