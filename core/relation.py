from pydantic import BaseModel, Field
from typing import List, Optional
from core.attribute import Attribute

class Relation(BaseModel):
    name: str = Field()
    attributes: List[Attribute] = Field(default_factory=list)
    tuples: List[List[str]] = Field(default_factory=list)
    primary_key: Optional[List[Attribute]] = Field(default_factory=list)

    def generate_create_table_query(self):
        # Generate a create table query with the given attribute names
        attributes_serialized = [attribute.serialize() for attribute in self.attributes]
        return f"CREATE TABLE {self.name} ({', '.join(attributes_serialized)})"