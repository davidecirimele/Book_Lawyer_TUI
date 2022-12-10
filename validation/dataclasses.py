from dataclass_type_validator import dataclass_type_validator, TypeValidationError

def validate_dataclass(data):
    try:
        dataclass_type_validator(data)

    except TypeValidationError as e:
        raise TypeError(e)

