from pydantic import BaseModel, Field
from typing import List

class Dependency(BaseModel):
    parent: str = Field(default="X")
    children: List[str] = Field(default_factory=list, example=["Y", "Z"])
