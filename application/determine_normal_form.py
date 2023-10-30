from typing import List
from core.dependency import Dependency
from core.relation import Relation
from core.attribute_factory import AttributeFactory

async def determine_normal_form(relation: Relation, dependencies: List[Dependency]) -> str:
    if not isRelationIn1NF(relation):
        return "UNF"
    if not isRelationIn2NF(relation, dependencies):
        return "1NF"
    if not isRelationIn3NF(relation, dependencies):
        return "2NF"
    if not isRelationInBCNF(relation, dependencies):
        return "3NF"
    if not isRelationIn4NF(relation, dependencies):
        return "BCNF"
    if not isRelationIn5NF(relation, dependencies):
        return "4NF"
    return "5NF"

def isRelationIn1NF(relation: Relation) -> bool:
    # Are all values atomic and are there any duplicate Attribute Names?
    attribute_names = []
    for attribute in relation.attributes:
        if not attribute.isAtomic:
            print(f"Relation is in UNF: {attribute.name} is not atomic.")
            return True
        if attribute.name in attribute_names:
            print(f"Relation is in UNF: {attribute.name} appears more than once as a column name.")
            return True
        attribute_names.append(attribute.name)
    
    # Are there any duplicate Tuples?
    data_rows = []
    for t in relation.tuples:
        row = ', '.join(t)
        if row in data_rows:
            print(f"Relation is in UNF: there are duplicate rows in the table. Duplicate Row: {row}")
            return True
        data_rows.append(row)

    # Are all columns of data the same data type?
    for index, attribute in enumerate(relation.attributes):
        for t in relation.tuples:
            data_type = AttributeFactory.get_data_type(t[index])
            if attribute.data_type != data_type:
                print(f"Relation is in UNF: data type is not consistent in Column '{attribute.name}'. Expected: {attribute.data_type}. Actual: {data_type}")
                return True
    
    return False

def isRelationIn2NF(relation: Relation, dependencies: List[Dependency]) -> bool:
    return False

def isRelationIn3NF(relation: Relation, dependencies: List[Dependency]) -> bool:
    return False

def isRelationInBCNF(relation: Relation, dependencies: List[Dependency]) -> bool:
    return False

def isRelationIn4NF(relation: Relation, dependencies: List[Dependency]) -> bool:
    return False

def isRelationIn5NF(relation: Relation, dependencies: List[Dependency]) -> bool:
    return False