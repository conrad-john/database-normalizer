from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from core.attribute import Attribute
from core.dependency import Dependency
import json

class Relation(BaseModel):
    name: str = Field()
    attributes: List[Attribute] = Field(default_factory=list)
    tuples: List[List[str]] = Field(default_factory=list)
    primary_keys: Optional[List[Attribute]] = Field(default_factory=list)
    dependencies: List[Dependency] = Field(default_factory=list)

    def generate_create_table_query(self) -> str:
        # Generate a create table query with the given attribute names
        attributes_serialized = [attribute.serialize() for attribute in self.attributes]
        return f"CREATE TABLE {self.name} ({', '.join(attributes_serialized)})"
    
    def generate_create_table_query_with_foreign_keys(self, foreign_context: Dict[str, str]) -> str:
        raise NotImplementedError()
        # Generate a create table query with the given attribute names
        attributes_serialized = [attribute.serialize() for attribute in self.attributes]
        return f"CREATE TABLE {self.name} ({', '.join(attributes_serialized)})"
    
    def to_json(self):
        # Convert the class instance to a dictionary
        data = self.dict()
        # Serialize the dictionary to JSON
        return json.dumps(data, indent=2)