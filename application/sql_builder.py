from typing import List
from core.relation import Relation

def get_table_creation_queries(relations: List[Relation]) -> List[str]:
    sql_queries = []

    for relation in relations:
        attributes_sql = ", ".join(f"{attribute.name} {attribute.data_type}" for attribute in relation.attributes)
        primary_keys_sql = ", ".join(attribute.name for attribute in relation.primary_keys) if relation.primary_keys else ""

        create_table_sql = f"CREATE TABLE {relation.name} ({attributes_sql}"
        if primary_keys_sql:
            create_table_sql += f", PRIMARY KEY ({primary_keys_sql})"
        create_table_sql += ");"
        
        sql_queries.append(create_table_sql)

    return sql_queries
