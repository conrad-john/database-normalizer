from typing import List
from core.dependency import Dependency
from core.relation import Relation
from fastapi import HTTPException

def parse_dependencies(R: Relation, dependency_inputs: List[str]) -> List[Dependency]:
    # Input Validation
    if not dependency_inputs:
        raise HTTPException(status_code=400, detail=f"No Input String Provided for Dependency.")
            
    dependencies = []

    for input_string in dependency_inputs:
        if '->' not in input_string:
            raise HTTPException(status_code=400, detail=f"Input string for dependency was not in required format. Examples: 'X -> Y', 'X -> Y, Z'")

        split_input = input_string.split('->')
        if len(split_input) > 2:
            raise HTTPException(status_code=400, detail=f"This application does not support the input of multiple dependency chains (e.g. X -> Y -> Z). Please separate dependencies.")

        parent = split_input[0].strip()
        children = split_input[1].replace(" ", "").split(',')

        if parent not in [attribute.name for attribute in R.attributes]:
            raise HTTPException(status_code=400, detail=f"{parent} attribute name was not present in the list of attributes built from the CSV. Please check the spelling of your dependencies against your CSV.")

        for child in children:
            if child.strip() not in [attribute.name for attribute in R.attributes]:
                raise HTTPException(status_code=400, detail=f"{child} attribute name was not present in the list of attributes built from the CSV. Please check the spelling of your dependencies against your CSV.")

        dependencies.append(Dependency(parent=parent, children=children))

    return dependencies