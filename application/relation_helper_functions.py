from typing import List
from core.attribute import Attribute
from core.relation import Relation
from core.dependency import Dependency

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

def split_tuples_v2(R: Relation, A_Attributes: List[Attribute], B_Attributes: List[Attribute]) -> (List[List[str]], List[List[str]]):
    # Get just the attribute names
    a_attribute_names = [att.name for att in A_Attributes]
    b_attribute_names = [att.name for att in B_Attributes]
    # Get staying_indexes and going_indexes
    a_indexes = []
    b_indexes = []
    for index, attribute in enumerate(R.attributes):
        if attribute.name in a_attribute_names:
            a_indexes.append(index)
        if attribute.name in b_attribute_names:
            b_indexes.append(index)
    # make two subsets of the original tuples mapped to the indexes we just pulled
    a_tuples = []
    b_tuples = []
    for row in R.tuples:
        new_a_tuple = [row[i] for i in a_indexes]
        new_b_tuple = [row[i] for i in b_indexes]
        a_tuples.append(new_a_tuple)
        b_tuples.append(new_b_tuple)
    return (a_tuples, b_tuples)

def get_relation_name(keys: List[Attribute]) -> str:
    keyNames = [key.name for key in keys]
    return ''.join(keyNames)

def get_relevant_dependencies(R: Relation, attributes: List[Attribute]) -> List[Dependency]:
    dependencies = []
    for dep in R.dependencies:
        if parent_attribute_present(dep, attributes) and subset_of_children_attribute_present(dep, attributes):
            modified_dep = get_required_dependency_data(dep, attributes)
            dependencies.append(modified_dep)
    return dependencies

def get_required_dependency_data(dep: Dependency, attributes: List[Attribute]) -> Dependency:
    if all_dependency_attributes_present(dep, attributes):
        return dep
    attribute_names = [att.name for att in attributes]
    dependency_subset = Dependency(parent=dep.parent, children=[child for child in dep.children if child in attribute_names])
    return dependency_subset

def parent_attribute_present(dep: Dependency, attributes: List[Attribute]) -> bool:
    # Get just the attribute names
    attribute_names = [att.name for att in attributes]
    if dep.parent not in attribute_names:
        return False
    return True

def subset_of_children_attribute_present(dep: Dependency, attributes: List[Attribute]) -> bool:
    # Get just the attribute names
    attribute_names = [att.name for att in attributes]
    for child in dep.children:
        if child in attribute_names:
            return True
    return False

def all_dependency_attributes_present(dep: Dependency, attributes: List[Attribute]) -> bool:
    # Get just the attribute names
    attribute_names = [att.name for att in attributes]
    if dep.parent not in attribute_names:
        return False
    for child in dep.children:
        if child not in attribute_names:
            return False
    return True

def split_attributes_by_parent_and_descendants(attributes: List[Attribute], parent: str, descendants: List[str]) -> (List[Attribute], List[Attribute]):
    a_attributes = []
    b_attributes = []

    for att in attributes:
        # If it is part of the dependency, it is broken out
        if att.name in descendants or att.name == parent:
            a_attributes.append(att)
        # If it is not part of the dependency, it is kept EXCEPT for the parent which is kept as a foreign key
        if att.name not in descendants:
            b_attributes.append(att)
    
    # Logic check...
    if len(a_attributes) < 2:
        raise Exception(f"Cannot have a resulting relation with fewer than two attributes.")
    if len(b_attributes) < 2:
        raise Exception(f"Cannot have a resulting relation with fewer than two attributes.")
    
    return (a_attributes, b_attributes)

def split_relation(R: Relation, A_Attributes: List[Attribute], B_Attributes: List[Attribute]) -> (Relation, Relation):
    # Split the data
    (a_tuples, b_tuples) = split_tuples_v2(R, A_Attributes, B_Attributes)
    # Build relation name
    a_name = get_relation_name(A_Attributes)
    b_name = get_relation_name(B_Attributes)
    # Get dependencies
    a_dependencies = get_relevant_dependencies(R, A_Attributes)
    b_dependencies = get_relevant_dependencies(R, B_Attributes)
    # Split the keys
    a_keys = [key for key in R.primary_keys if key.name in [att.name for att in A_Attributes]]
    b_keys = [key for key in R.primary_keys if key.name in [att.name for att in B_Attributes]]

    A = Relation(
                name=f"{a_name}s",
                attributes=A_Attributes,
                tuples=a_tuples,
                primary_keys=a_keys,
                dependencies=a_dependencies
            )
    B = Relation(
                name=f"{b_name}s",
                attributes=B_Attributes,
                tuples=b_tuples,
                primary_keys=b_keys,
                dependencies=b_dependencies
            )
    
    return (A, B)