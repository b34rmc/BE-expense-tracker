import uuid

def populate_object(obj, data_dict):
    fields = data_dict.keys()
    
    for field in fields:
        if hasattr(obj, field):
            setattr(obj, field, data_dict[field])
    return obj

def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False