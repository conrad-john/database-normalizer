from core.attribute import Attribute
from core.datetime_formatter import is_serialized_date
import dateparser
import uuid

class AttributeFactory:
    @classmethod
    def create_attribute(cls, name, value):
        attribute = Attribute(name=name)
        attribute.data_type = cls.get_data_type(value)
        attribute.isAtomic = not ('varchar' in attribute.data_type and ',' in value)
        return attribute

    @staticmethod
    def get_data_type(value):
        if value in ("0", "1"):
            return "bit(1)"
        if value in ("true", "false", "yes", "no", "on", "off", "t", "f"):
            return "boolean"
        try:
            int(value)
            return "int"
        except:
            try:
                float(value)
                return "float"
            except:
                if is_serialized_date(value):
                    return "datetime"
                try:
                    uuid.UUID(value)
                    return "UUID"
                except:
                    length = (int(len(value) / 50) + 1) * 50
                    return f"varchar({length})"