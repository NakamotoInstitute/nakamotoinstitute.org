import json

from pydantic import BaseModel, ValidationError


def load_and_validate_json(json_file: str, item_schema: BaseModel):
    try:
        with open(json_file, "r") as file:
            data = json.load(file)
            if not isinstance(data, list):
                print(
                    f"Invalid data format. Expected a list but got {type(data).__name__}"
                )
                return None

            validated_data = [item_schema(**item) for item in data]
            return validated_data
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None
