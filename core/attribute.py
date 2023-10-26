from pydantic import BaseModel, Field
from typing import List, Optional
import dateparser
import uuid

class Attribute(BaseModel):
    name: str = ""
    data_type: str = ""
    isAtomic: bool = False

    def __init__(self, name: str, value: str):
        super().__init__(name=name)
        self.data_type, self.isAtomic = self.get_data_type(value)

    def serialize(self):
        return f"{self.name} {self.data_type}"
    
    def get_data_type(self, value):
        # bit(size)
        if value in ("0", "1"):
            return "bit(1)", True
        # boolean
        if value in ("true", "false", "yes", "no", "on", "off", "t", "f"):
            return "boolean", True
        try:
            # binary(size)
            int(value, 2)
            return f"binary({len(value)+8})", True
        except:
            try:
                # int
                int(value) # Attempt to parse value as an integer
                return "int", True
            except:
                try:
                    #float
                    float(value)
                    return "float", True
                except:
                    try:
                        # datetime
                        dateparser.parse(value)
                        return "datetime", True
                    except:
                        try:
                            uuid.UUID(value)
                            return "UUID", True
                        except:
                            length = (int(len(value)/50) + 1) * 50
                            if ',' in value:
                                return f"varchar({length})", False
                            else:
                                return f"varchar({length})", True



