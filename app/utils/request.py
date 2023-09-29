from flask import request


def get_bool_param(key: str, default=False) -> bool:
    return request.args.get(key, default, type=lambda x: x.lower() == "true")
