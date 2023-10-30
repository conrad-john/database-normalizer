from pydantic import BaseModel

class Attribute(BaseModel):
    name: str = ""
    data_type: str = ""
    isAtomic: bool = False
    
    def serialize(self):
        return f"{self.name} {self.data_type}"