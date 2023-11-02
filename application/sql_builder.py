from typing import List
from core.relation import Relation

def get_table_creation_queries(relations: List[Relation]) -> List[str]:
    queries = []
    for relation in relations:
        queries.append(relation.generate_create_table_query())
    return queries