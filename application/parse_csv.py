import os
from core.attribute import Attribute
from core.attribute_factory import AttributeFactory
from core.relation import Relation
from fastapi import UploadFile, HTTPException

async def parse_csv(file: UploadFile) -> Relation:
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
    
    # Instantiate a Relation Object
    relation = Relation(
        name="R",
        attributes=[],
        tuples=[],
        primary_key=None
    )

    # Read the first line of the file which should contain the attribute names
    attribute_names = file.file.readline().decode().strip().split(',')
    
    # Insert each record provided into the table we just created
    while True:
        line = file.file.readline().decode().strip()
        relation.tuples.append(line.split(','))
        if not line:
            # End of File
            break
    
    for index, attribute_name in enumerate(attribute_names):
        attribute = AttributeFactory.create_attribute(name=attribute_name.strip(), value=relation.tuples[0][index])
        relation.attributes.append(attribute)

    return relation
