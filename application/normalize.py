from typing import List, Optional
from core.dependency import Dependency
from core.relation import Relation
from core.attribute_factory import AttributeFactory
from core.attribute import Attribute
from application.determine_normal_form import *

async def normalize(relation: Relation, target_nf: str, current_nf: str) -> List[Relation]:
    # Convert/Get NF Integers for easier comparison
    target = get_nf_integer(target_nf)
    current = get_nf_integer(determine_normal_form(relation)) if current_nf == "N/A" else get_nf_integer(current_nf)
    
    if target <= current:
        print(f"The Relationship is already normalized to {current_nf} which is equal to or higher than {target_nf}.")
        return [relation]
    
    subrelations = [relation]
    
    # Normalize from UNF to 1NF
    if target >= 1 and current < 1:
        normalized_subrelations = []
        for relation in subrelations:
            if isRelationIn1NF(relation):
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
        normalized_subrelations = normalize_to_5NF(subrelations)
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

async def normalize_to_2NF(input_relation: Relation) -> List[Relation]:
    # Look for partial dependencies in each relation and split the relation accordingly

    # Ensure relation is normalized to lower normal forms first
    lower_normalized_relations = normalize(input_relation, "1NF", "N/A")
        
    # Initialize Empty Normalized Relations
    normalized_relations = []

    for relation in lower_normalized_relations:

        # While the relation is not normalized to the desired normal form
        while not isRelationIn2NF(relation):

            # Split relation on a condition matching the normalization form
            parents = [dep.parent for dep in relation.dependencies]
            key_list = [att.name for att in relation.primary_key]
            non_key_parents = [parent for parent in parents if parent not in key_list]

            # We want non-key parents that have children with other parents that are in the key list
            non_key_partial_parent = None
            for parent in non_key_parents:
                children = [dep.children for dep in relation.dependencies if dep.parent == parent]
                for child in children:
                    other_parents_of_child = [dep.parent for dep in getParentAttributes(child) if dep.parent != parent]
                    other_parents_who_are_keys = [key for key in key_list if key in other_parents_of_child]
                    if other_parents_who_are_keys > 0:
                        non_key_partial_parent = parent
                        break
                if non_key_partial_parent:
                    break

            # Add breaking condition in case while condition is faulty
            if not non_key_partial_parent:
                print(f"Warning: In normalize_to_2NF, something is wrong with the cnf checker. No non-key parents were found. Breaking loop.")
                normalized_relations.append(relation)
                break

            split_key = [att for att in relation.attributes if att.name == non_key_partial_parent]
            partial_dependencies = [dep for dep in relation.dependencies if dep.parent == non_key_partial_parent]
            stepchildren_names = [dep.children for dep in partial_dependencies]
            stepchildren_attributes = [att for att in relation.attributes if att.name in stepchildren_names]

            (staying_tuples, going_tuples) = split_tuples(relation, split_key[0].name, stepchildren_names)

            split_relation = Relation(
                name=f"{non_key_partial_parent}s",
                attributes=stepchildren_attributes,
                tuples=going_tuples,
                primary_key=[split_key],
                dependencies=[partial_dependencies]
            )

            # Normalize the split relation to the desired normal form
            normalized_split_relations = normalize(split_relation, "2NF", "N/A")

            # Add the split relation to normalized_relations
            normalized_relations.append(normalized_split_relations)
            
            # Remove necessary attributes and tuple data from the original relation, keeping the key of the new relation as a foreign key
            relation.attributes=[att for att in relation.attributes if att.name not in stepchildren_names]
            relation.dependencies=[dep for dep in relation.dependencies if dep not in partial_dependencies]
            relation.tuples=staying_tuples
    
        normalized_relations.append(relation)

    return normalized_relations

async def normalize_to_3NF(input_relation: Relation) -> List[Relation]:
    # Look for partial dependencies in each relation and split the relation accordingly

    # Ensure relation is normalized to lower normal forms first
    lower_normalized_relations = normalize(input_relation, "2NF", "N/A")
        
    # Initialize Empty Normalized Relations
    normalized_relations = []

    for relation in lower_normalized_relations:

        # While the relation is not normalized to the desired normal form
        while not isRelationIn3NF(relation):

            # Split relation on a condition matching the normalization form
            parents = [dep.parent for dep in relation.dependencies]
            key_list = [att.name for att in relation.primary_key]
            non_key_parents = [parent for parent in parents if parent not in key_list]

            # We want non-key parents that have a key parent, grandparent, great-grandparent, etc.
            non_key_partial_parent_with_key_ancestor = None
            for parent in non_key_parents:
                if isNonKeyParentDeterminedByKey(parent, relation.dependencies, key_list):
                    non_key_partial_parent_with_key_ancestor = parent
                    break

            # Add breaking condition in case while condition is faulty
            if not non_key_partial_parent_with_key_ancestor:
                print(f"Warning: In normalize_to_3NF, something is wrong with the cnf checker. No non-key partial parents were found with key ancestor. Breaking loop.")
                normalized_relations.append(relation)
                break

            split_key = [att for att in relation.attributes if att.name == non_key_partial_parent_with_key_ancestor]
            partial_dependencies = [dep for dep in relation.dependencies if dep.parent == non_key_partial_parent_with_key_ancestor]
            stepchildren_names = [dep.children for dep in partial_dependencies]
            stepchildren_attributes = [att for att in relation.attributes if att.name in stepchildren_names]

            (staying_tuples, going_tuples) = split_tuples(relation, split_key[0].name, stepchildren_names)

            split_relation = Relation(
                name=f"{non_key_partial_parent_with_key_ancestor}s",
                attributes=stepchildren_attributes,
                tuples=going_tuples,
                primary_key=[split_key],
                dependencies=[partial_dependencies]
            )

            # Normalize the split relation to the desired normal form
            normalized_split_relations = normalize(split_relation, "3NF", "N/A")

            # Add the split relation to normalized_relations
            normalized_relations.append(normalized_split_relations)
            
            # Remove necessary attributes and tuple data from the original relation, keeping the key of the new relation as a foreign key
            relation.attributes=[att for att in relation.attributes if att.name not in stepchildren_names]
            relation.dependencies=[dep for dep in relation.dependencies if dep not in partial_dependencies]
            relation.tuples=staying_tuples
    
        normalized_relations.append(relation)
    
    return normalized_relations

async def normalize_to_BCNF(input_relation: Relation) -> List[Relation]:
    # Ensure relation is normalized to lower normal forms first
    lower_normalized_relations = normalize(input_relation, "3NF", "N/A")
        
    # Initialize Empty Normalized Relations
    normalized_relations = []

    for relation in lower_normalized_relations:
        
        # While the relation is not normalized to the desired normal form
        while not isRelationInBCNF(relation):

            # Split relation on a condition matching the normalization form
            parents = [dep.parent for dep in relation.dependencies]
            key_list = [att.name for att in relation.primary_key]
            non_key_parents = [parent for parent in parents if parent not in key_list]

            # Add breaking condition in case while condition is faulty
            if len(non_key_parents) < 1:
                print(f"Warning: In normalize_to_BCNF, something is wrong with the cnf checker. No non-key parents were found. Breaking loop.")
                normalized_relations.append(relation)
                break

            split_key_name = non_key_parents[0]
            split_key = [att for att in relation.attributes if att.name == split_key_name]
            partial_dependencies = [dep for dep in relation.dependencies if dep.parent == split_key_name]
            stepchildren_names = [dep.children for dep in partial_dependencies]
            stepchildren_attributes = [att for att in relation.attributes if att.name in stepchildren_names]

            (staying_tuples, going_tuples) = split_tuples(relation, split_key_name, stepchildren_names)

            split_relation = Relation(
                name=f"{split_key_name}s",
                attributes=stepchildren_attributes,
                tuples=going_tuples,
                primary_key=[split_key],
                dependencies=[partial_dependencies]
            )

            # Normalize the split relation to the desired normal form
            normalized_split_relations = normalize(split_relation, "BCNF", "N/A")

            # Add the split relation to normalized_relations
            normalized_relations.append(normalized_split_relations)
            
            # Remove necessary attributes and tuple data from the original relation, keeping the key of the new relation as a foreign key
            relation.attributes=[att for att in relation.attributes if att.name not in stepchildren_names]
            relation.dependencies=[dep for dep in relation.dependencies if dep not in partial_dependencies]
            relation.tuples=staying_tuples
    
        normalized_relations.append(relation)
    
    return normalized_relations

async def normalize_to_4NF(input_relation: Relation) -> List[Relation]:
    # Ensure relation is normalized to lower normal forms first
    lower_normalized_relations = normalize(input_relation, "BCNF", "N/A")
        
    # Initialize Empty Normalized Relations
    normalized_relations = []

    for relation in lower_normalized_relations:
        # While the relation is not normalized to the desired normal form
        while not isRelationIn4NF(relation):
            # Split relation on a condition matching the normalization form
            (split_key, mvd) = getAttributeWithMVD(relation)

            # Add breaking condition in case while condition is faulty
            if not split_key:
                print(f"Warning: In normalize_to_4NF, something is wrong with the cnf checker. No non-key parents were found. Breaking loop.")
                normalized_relations.append(relation)
                break
            
            partial_dependencies = [dep for dep in relation.dependencies if dep.parent == split_key.name]
            stepchildren_attributes = [att for att in relation.attributes if att.name == mvd.name]
            stepchildren_names = [mvd.name]

            (staying_tuples, going_tuples) = split_tuples(relation, split_key.name, stepchildren_names)

            split_relation = Relation(
                name=f"{split_key.name}s",
                attributes=stepchildren_attributes,
                tuples=going_tuples,
                primary_key=[split_key],
                dependencies=[partial_dependencies]
            )

            # Normalize the split relation to the desired normal form
            normalized_split_relations = normalize(split_relation, "4NF", "N/A")
            
            # Add the split relation to normalized_relations
            normalized_relations.append(normalized_split_relations)
            
            # Remove necessary attributes and tuple data from the original relation, keeping the key of the new relation as a foreign key
            relation.attributes=[att for att in relation.attributes if att.name not in stepchildren_names]
            relation.dependencies=[dep for dep in relation.dependencies if dep not in partial_dependencies]
            relation.tuples=staying_tuples

        normalized_relations.append(relation)

    return normalized_relations

def getAttributeWithMVD(relation: Relation) -> (Optional[Attribute], Optional[Attribute]):
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
                    mvd = [att for att in relation.attributes if att.name == child]
                    return (attribute, mvd)

    return True

async def normalize_to_5NF(relations: List[Relation]) -> List[Relation]:
    # Ensure relation is normalized to lower normal forms first
    lower_normalized_relations = []
    for relation in relations:
        lower_normalized_relations.append(normalize(relation, "4NF", "N/A"))
        
    # Initialize Empty Normalized Relations
    normalized_relations = []

    for relation in lower_normalized_relations:
        # While the relation is not normalized to the desired normal form
        while not isRelationIn5NF(relation):
            # Split relation on a condition matching the normalization form
            # Looking for foreign keys which are not part of the relation's dependencies
            all_keys = [r.primary_key for r in lower_normalized_relations]
            key_list = [att.name for att in relation.primary_key]
            foreign_key_list = [key.name for key in all_keys if key not in key_list]
            join_dependency = [att.name for att in relation.attributes if att.name in foreign_key_list]

            # Add breaking condition in case while condition is faulty
            if not join_dependency:
                print(f"Warning: In normalize_to_5CNF, I'm not sure what other context I can programmatically review to determine where to split. Breaking loop.")
                normalized_relations.append(relation)
                break
            
            split_key_name = join_dependency[0]
            split_key = [att for att in relation.attributes if att.name == split_key_name]
            split_dependency = []
            stepchildren_attributes = [relation.primary_key[0]]
            stepchildren_names = [att.name for att in stepchildren_attributes]

            normalized_split_relations = Relation(
                name=f"{split_key_name}{stepchildren_attributes[0].name}s",
                attributes=stepchildren_attributes,
                tuples=[],
                primary_key=[split_key],
                dependencies=[split_dependency]
            )

            # Automatically in 5NF based on this criteria - normalize the split relation to the desired normal form
            # normalized_split_relations = normalize(split_relation, "5CNF", "N/A")

            # Add the split relation to normalized_relations
            normalized_relations.append(normalized_split_relations)
            
            # Remove necessary attributes and tuple data from the original relation, keeping the key of the new relation as a foreign key
            relation.attributes=[att for att in relation.attributes if att.name not in split_key_name]

        normalized_relations.append(relation)

    return normalized_relations

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

def split_tuples(original_relation: Relation, split_relation_key: str, split_relation_attributes: List[str]) -> (List[List[str]], List[List[str]]):
    # Move top to bottom, left to right appending cells accordingly
    original_tuples = []
    splitting_tuples = []
    for row in original_relation.tuples:
        ori_tuple = []
        spl_tuple = []
        for index, attribute in enumerate(original_relation.attributes):
            # Only Split - Split Relation Key and Attributes
            if attribute in split_relation_attributes or attribute == split_relation_key:
                spl_tuple.append(row[index])
            # Only Original - Split Relation Key and Non Split Relation Attributes
            if attribute not in split_relation_attributes:
                ori_tuple.append(row[index])
        original_tuples.append(ori_tuple)
        splitting_tuples.append(spl_tuple)

    return (original_tuples, splitting_tuples)