from typing import List
from core.dependency import Dependency
from core.relation import Relation
from core.attribute_factory import AttributeFactory
from core.attribute import Attribute
from application.determine_normal_form import determine_normal_form, isRelationIn1NF, isRelationIn2NF, isRelationIn3NF, isRelationInBCNF, isRelationIn4NF, isRelationIn5NF

async def normalize(relation: Relation, dependencies: List[Dependency], target_nf: str, current_nf: str) -> List[Relation]:
    # Convert/Get NF Integers for easier comparison
    target = get_nf_integer(target_nf)
    current = get_nf_integer(current_nf) if current_nf != "N/A" else get_nf_integer(determine_normal_form(relation))
    
    if target <= current:
        print(f"The Relationship is already normalized to {current_nf} which is equal to or higher than {target_nf}.")
        return [relation]
    
    subrelations = [relation]
    
    # Normalize from UNF to 1NF
    if target >= 1 and current < 1:
        normalized_subrelations = []
        for relation in subrelations:
            if isRelationIn5NF(relation):
                normalized_subrelations.append(relation)
                continue
            else:
                normalized_subrelations.append(normalize_to_1NF(relation))
        subrelations = normalized_subrelations
        current = 1

    # Normalize from 1NF to 2NF
    if target >= 2 and current < 2:
        normalized_subrelations = []
        for relation in subrelations:
            if isRelationIn2NF(relation):
                normalized_subrelations.append(relation)
                continue
            else:
                normalized_subrelations.append(normalize_to_2NF(relation))
        subrelations = normalized_subrelations
        current = 2

    # Normalize from 2NF to 3NF
    if target >= 3 and current < 3:
        normalized_subrelations = []
        for relation in subrelations:
            if isRelationIn3NF(relation):
                normalized_subrelations.append(relation)
                continue
            else:
                normalized_subrelations.append(normalize_to_3NF(relation))
        subrelations = normalized_subrelations
        current = 3

    # Normalize from 3NF to BCNF
    if target >= 4 and current < 4:
        normalized_subrelations = []
        for relation in subrelations:
            if isRelationInBCNF(relation):
                normalized_subrelations.append(relation)
                continue
            else:
                normalized_subrelations.append(normalize_to_BCNF(relation))
        subrelations = normalized_subrelations
        current = 4

    # Normalize from BCNF to 4NF
    if target >= 5 and current < 5:
        normalized_subrelations = []
        for relation in subrelations:
            if isRelationIn4NF(relation):
                normalized_subrelations.append(relation)
                continue
            else:
                normalized_subrelations.append(normalize_to_4NF(relation))
        subrelations = normalized_subrelations
        current = 5

    # Normalize from 4NF to 5NF
    if target >= 6 and current < 6:
        normalized_subrelations = []
        for relation in subrelations:
            if isRelationIn5NF(relation):
                normalized_subrelations.append(relation)
                continue
            else:
                normalized_subrelations.append(normalize_to_5NF(relation))
        subrelations = normalized_subrelations
        current = 6

    return subrelations

async def normalize_to_1NF(relation: Relation) -> List[Relation]:
    # Are all values atomic and are there any duplicate Attribute Names?
    attribute_names = []
    for attribute in relation.attributes:
        # If there's a non-atomic value, assume an error with the parser and set the bool to True so we don't get repeat warning logs.
        if not attribute.isAtomic:
            print(f"Warning: non-atomic value detected. Attribute: '{attribute.name}'. The data contract provided is not strict enough to properly enforce atomic values so I'm assuming error in my ability to parse your desired input.")
            attribute.isAtomic = True
        # If there's a duplicate attribute name
        if attribute.name in attribute_names:
            print(f"Relation is in UNF: {attribute.name} appears more than once as a column name.")
            # Alter the name and duplicate the dependencies
            renamed_attribute = f"Duplicate_{attribute.name}"
            new_dependencies = []
            for dependency in relation.dependencies:
                if attribute.name in dependency.parent:
                    new_dependencies.append(Dependency(parent=renamed_attribute, children=dependency.children))
                elif attribute.name in dependency.children:
                    stepchildren = [children for children in dependency.children if children != attribute.name]
                    stepchildren.append(renamed_attribute)
                    new_dependencies.append(Dependency(parent=dependency.parent, children=stepchildren))
            attribute.name = renamed_attribute
            relation.dependencies.append(new_dependencies)
            # Just in case the name is duplicated more than once, we'll end up with 'Duplicate_...Duplicate_{attribute.name}
            attribute_names.append(renamed_attribute)
        else:
            attribute_names.append(attribute.name)

    # Are all tuples unique? If not, remove duplicate data
    data_rows = []
    duplicate_row_indexes = []
    for index, t in enumerate(relation.tuples):
        row = ', '.join(t)
        if row in data_rows:
            duplicate_row_indexes.append(index)
        data_rows.append(row)
    if len(duplicate_row_indexes) > 0:
        deduped_rows = []
        for index, t in enumerate(relation.tuples):
            if index in duplicate_row_indexes:
                continue
            deduped_rows.append(t)
        relation.tuples = deduped_rows

    # Is there a Primary Key? If not, set one
    if len(relation.primary_key) < 1:
        keys = []
        for dependency in relation.dependencies:
            candidate_key = dependency.parent
            keys.append([attribute for attribute in relation.attributes if attribute.name == candidate_key])
        if len(keys) < 1:
            keys = relation.attributes

    return [relation]

async def normalize_to_2NF(relation: Relation) -> List[Relation]:
    raise NotImplementedError()

async def normalize_to_3NF(relation: Relation) -> List[Relation]:
    raise NotImplementedError()

async def normalize_to_BCNF(relation: Relation) -> List[Relation]:
    raise NotImplementedError()

async def normalize_to_4NF(relation: Relation) -> List[Relation]:
    raise NotImplementedError()

async def normalize_to_5NF(relation: Relation) -> List[Relation]:
    raise NotImplementedError()

def get_nf_integer(nf: str) -> int:
    nf_dict = {
        "UNF": 0,
        "1NF": 1,
        "2NF": 2,
        "3NF": 3,
        "BCNF": 4,
        "4NF": 5,
        "5NF": 6,
    }
    try:
        return nf_dict[nf]
    except Exception as e:
        raise ValueError(f"Invalid normal form: {nf}. The valid normal forms are {', '.join(nf_dict.keys())}. Exception: {e}")