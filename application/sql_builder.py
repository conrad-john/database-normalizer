from typing import List, Optional
from core.dependency import Dependency
from core.relation import Relation
from core.attribute_factory import AttributeFactory
from core.attribute import Attribute

def get_table_creation_queries(relations: List[Relation]) -> List[str]:
    queries = []
    for relation in relations:
        queries.append(relation.generate_create_table_query())
    return queries