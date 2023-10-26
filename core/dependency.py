from pydantic import BaseModel, Field
from typing import List, Optional

class Dependency(BaseModel):
    parent: Optional[str] = Field(default="X")
    children: Optional[List[str]] = Field(default_factory=list, example=["Y", "Z"])
