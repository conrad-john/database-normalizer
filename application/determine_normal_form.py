from typing import List
from application.relation_helper_functions import *
from core.dependency import Dependency
from core.relation import Relation
from core.attribute_factory import AttributeFactory

def determine_normal_form(relation: Relation) -> str:
    if not isRelationIn1NF(relation):
        return "UNF"
    if not isRelationIn2NF(relation):
        return "1NF"
    if not isRelationIn3NF(relation):
        return "2NF"
    if not isRelationInBCNF(relation):
        return "3NF"
    if not isRelationIn4NF(relation):
        return "BCNF"
    if not isRelationIn5NF(relation):
        return "4NF"
    return "5NF"

def isRelationIn1NF(relation: Relation) -> bool:
    # Are all values atomic and are there any duplicate Attribute Names?
    attribute_names = []
    for attribute in relation.attributes:
        if not attribute.isAtomic:
            print(f"Relation is in UNF: {attribute.name} is not atomic.")
            return False
        if attribute.name in attribute_names:
            print(f"Relation is in UNF: {attribute.name} appears more than once as a column name.")
            return False
        attribute_names.append(attribute.name)
    
    # Are there any duplicate Tuples?
    data_rows = []
    for t in relation.tuples:
        row = ', '.join(t)
        if row in data_rows:
            print(f"Relation is in UNF: there are duplicate rows in the table. Duplicate Row: {row}")
            return False
        data_rows.append(row)

    # Are all columns of data the same data type?
    for index, attribute in enumerate(relation.attributes):
        for t in relation.tuples:
            data_type = AttributeFactory.get_data_type(t[index])
            if attribute.data_type != data_type:
                print(f"Relation is in UNF: data type is not consistent in Column '{attribute.name}'. Expected: {attribute.data_type}. Actual: {data_type}")
                return False

    # Check if there is a primary key 
    if not relation.primary_keys or len(relation.primary_keys) < 1:
        return False
    
    return True

def isRelationIn2NF(relation: Relation) -> bool:
    if len(relation.attributes) < 3:
        return True
    
    # Look for partial dependencies, X->Y where X is a subset of the key
    dependencies = relation.dependencies
    key_list = get_list_of_key_names(relation)
    
    for attribute in relation.attributes:
        
        # This for loop checks if there are any attributes which appear as children in our list of depenedencies
        parent_list = getParentAttributes(attribute.name, dependencies)
        if not parent_list or len(parent_list) < 1:
            continue
        
        # If it finds matching instances in dependencies, it ensures the determining attribute at least include the full key
        keys_not_in_parents = [key for key in key_list if key not in parent_list]
        if len(keys_not_in_parents) > 0:
            return False

    return True

def getParentAttributes(child_name: str, dependencies: List[Dependency]) -> List[str]:
    return [dep.parent for dep in dependencies if child_name in dep.children]

def isRelationIn3NF(relation: Relation) -> bool:
    if len(relation.attributes) < 3:
        return True
    
    # Look for Transitive Functional Dependencies where X -> Y -> Z where X is the key but Y is not
    dependencies = relation.dependencies
    key_list = get_list_of_key_names(relation)
    
    for attribute in relation.attributes:
        # Get our list of parents (X where X->Y and Y is our attribute)
        parent_list = getParentAttributes(attribute.name, dependencies)

        # Get instances of X where X is not in key
        parents_not_in_keys = [parent for parent in parent_list if parent not in key_list]

        # Recursively check if the parents are part of a transitive dependency chain
        for parent in parents_not_in_keys:
            if isNonKeyParentDeterminedByKey(parent, dependencies, key_list):
                print(f"Relation is in 2NF: '{attribute.name}' is determined by a Transitive Functional Dependency via '{parent}'.")
                return False
    
    return True

def isNonKeyParentDeterminedByKey(parent: str, dependencies: List[Dependency], key_list: List[str]) -> bool:
    # Try to go up the chain of dependencies one level
    grandparent_list = getParentAttributes(parent, dependencies)

    # If nothing determines the parent, return False, we'll catch it in BCNF
    if len(grandparent_list) > 0:

        # If the list of grandparents includes the keys, it's a Transitive Functional Dependency
        keys_not_in_grandparents = [key for key in key_list if key not in grandparent_list]
        if not keys_not_in_grandparents or len(keys_not_in_grandparents) == 0:
            return True
        
        # Get instances of X where X is not in key -- (shouldn't have to do this, but it's for safety in case this gets run without checking previous normal forms)
        grandparents_not_in_keys = [parent for parent in grandparent_list if parent not in key_list]

        # Recursively go up the chain of dependencies and see if the key is at the top
        for grandparent in grandparents_not_in_keys:
            if isNonKeyParentDeterminedByKey(grandparent, dependencies, key_list):
                return True

    return False

def isRelationInBCNF(relation: Relation) -> bool:
    if len(relation.attributes) < 3:
        return True
    # Look for Non-Trivial Functional Dependencies where X -> Y but X is not part of the keys
    dependencies = relation.dependencies
    key_list = get_list_of_key_names(relation)
    
    for attribute in relation.attributes:
        # Get our list of parents (X where X->Y and Y is our attribute)
        parent_list = getParentAttributes(attribute.name, dependencies)

        # If there are no parents (nothing determines the given attribute), continue
        if not parent_list or len(parent_list) < 1:
            continue
    
        # If the parent list doesn't exactly match the keys, it includes a Partial Functional Dependency (which we would have caught earlier)
        # or it includes attributes which are not part of the keys
        if not sorted(key_list) == sorted(parent_list):
            parent_not_in_keys = [parent for parent in parent_list if parent not in key_list]
            print(f"Relation is in 3NF: '{attribute}' is dependent on '{parent_not_in_keys}' which are not in the keys: '{key_list}'.")
            return False
        
    return True

def isRelationIn4NF(relation: Relation) -> bool:
    if len(relation.attributes) < 3:
        return True

    # Look for Multi-Valued Dependencies where X -> -> Y
    dependencies = relation.dependencies
    for attribute_index, attribute in enumerate(relation.attributes):
        # Get all children dependent on this attribute
        children_list = getChildAttributes(attribute.name, dependencies)

        # If there are no child attributes, we can't have any MVD's
        if not children_list or children_list < 1:
            continue

        # for each child, create a dictionary: key=attribute.value, value=List[all tuple values]
        for child in children_list:
            child_index = 0
            for i, attribute in enumerate(relation.attributes):
                if child == attribute.name():
                    child_index = i
                    break
            attribute_values_dict = {}
            for row in relation.tuples:
                if row[attribute_index] in attribute_values_dict:
                    attribute_values_dict[row[attribute_index]].append(row[child_index])
                else:
                    attribute_values_dict[row[attribute_index]] = [row[child_index]]
                    
            # Is the list longer than 1 for any key? Then there's a MVD
            for _, value in attribute_values_dict.items():
                unique_items = list(set(value))
                if len(unique_items) > 1:
                    print(f"Relation is in BCNF: There is a multivalue dependency '{attribute.name}->->{child}'.")
                    return False

    return True

def getChildAttributes(parent_name: str, dependencies: List[Dependency]) -> List[str]:
    return [dep.children for dep in dependencies if parent_name in dep.parent]

def isRelationIn5NF(relation: Relation) -> bool:
    dependencies = relation.dependencies
    
    # Two items are automatically in 5NF
    if len(relation.attributes) < 3:
        return True
    
    # If every attribute is also part of the keys
    key_list = get_list_of_key_names(relation)
    attribute_list = get_list_of_attribute_names(relation)
    if sorted(key_list) == sorted(attribute_list):
        return True

    # It's really hard to say just looking at one relation since Join Dependencies are so subjective
    return False