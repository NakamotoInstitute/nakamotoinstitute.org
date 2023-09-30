from functools import wraps
from typing import List, Type

from flask import jsonify
from pydantic import BaseModel, ValidationError


def response_model(model: Type[BaseModel] | List[Type[BaseModel]]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
                if isinstance(result, list):
                    model_list = [
                        model.__args__[0].model_validate(item) for item in result
                    ]
                    return jsonify([item.dict(by_alias=True) for item in model_list])

                model_instance = model.model_validate(result)
                return jsonify(model_instance.dict(by_alias=True))

            except ValidationError as e:
                return (
                    jsonify({"error": "Validation error", "details": e.errors()}),
                    400,
                )
            except Exception as e:
                raise e

        return decorated_function

    return decorator
