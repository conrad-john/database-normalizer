from typing import List
from core.relation import Relation

def get_list_of_key_names(relation: Relation) -> List[str]:
        return [att.name for att in relation.primary_keys]
    
def get_list_of_attribute_names(relation: Relation) -> List[str]:
        return [att.name for att in relation.attributes]

def areRelationsEquivalent(A: Relation, B: Relation) -> bool:
    if A.name != B.name:
        return False
    if len(A.attributes) != len(B.attributes):
        return False 
    A_attribute_names = [att.name for att in A.attributes]
    B_attribute_names = [att.name for att in B.attributes]
    if sorted(A_attribute_names) != sorted(B_attribute_names):
        return False
    if len(A.primary_keys) != len(B.primary_keys):
        return False
    A_key_names = [att.name for att in A.primary_keys]
    B_key_names = [att.name for att in B.primary_keys]
    if sorted(A_key_names) != sorted(B_key_names):
        return False
    if len(A.dependencies) != len(B.dependencies):
        return False
    for A_dependency in A.dependencies:
        dependency_matched = False
        matching_B_dependency = [dep for dep in B.dependencies if dep.parent == A_dependency.parent]
        for B_dependency in matching_B_dependency:
            if sorted(A_dependency.children) == sorted(B_dependency.children):
                dependency_matched = True
                break
            if dependency_matched:
                break
        if not dependency_matched:
            return False
    if len(A.tuples) != len(B.tuples):
        return False
    for A_tuple in A.tuples:
        matching_B_tuple = [B_t for B_t in B.tuples if sorted(B_t) == sorted(A_tuple)]
        if not matching_B_tuple:
            return False
    return True