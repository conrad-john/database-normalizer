from pydantic import BaseModel, Field
from typing import List, Optional
import json

class Dependency(BaseModel):
    parent: Optional[str] = Field(default="X")
    children: Optional[List[str]] = Field(default_factory=list, example=["Y", "Z"])

    def to_json(self):
        # Convert the class isntance to a dictionary
        data = self.dict()
        # Serialize the dictionary to JSON
        return json.dumps(data, indent=2)