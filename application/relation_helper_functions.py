from typing import List
from core.attribute import Attribute
from core.relation import Relation

def get_list_of_key_names(relation: Relation) -> List[str]:
        return [att.name for att in relation.primary_key]
    
def get_list_of_attribute_names(relation: Relation) -> List[str]:
        return [att.name for att in relation.attributes]