from typing import List
from core.dependency import Dependency
from core.relation import Relation
from core.attribute_factory import AttributeFactory
from core.attribute import Attribute
from application.determine_normal_form import determine_normal_form, isRelationIn1NF, isRelationIn2NF, isRelationIn3NF, isRelationInBCNF, isRelationIn4NF, isRelationIn5NF

async def normalize(relation: Relation, dependencies: List[Dependency], target_nf: str, current_nf: str) -> List[Relation]:
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

async def normalize_to_1NF(relation: Relation, dependencies: List[Dependency]) -> List[Relation]:
    
    raise NotImplementedError()

async def normalize_to_2NF(relation: Relation, dependencies: List[Dependency]) -> List[Relation]:
    raise NotImplementedError()

async def normalize_to_3NF(relation: Relation, dependencies: List[Dependency]) -> List[Relation]:
    raise NotImplementedError()

async def normalize_to_BCNF(relation: Relation, dependencies: List[Dependency]) -> List[Relation]:
    raise NotImplementedError()

async def normalize_to_4NF(relation: Relation, dependencies: List[Dependency]) -> List[Relation]:
    raise NotImplementedError()

async def normalize_to_5NF(relation: Relation, dependencies: List[Dependency]) -> List[Relation]:
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