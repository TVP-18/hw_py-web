import jsonschema
from flask import request, jsonify, make_response


def validate(source: str, req_schema: dict):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                jsonschema.validate(
                    instance=getattr(request, source), schema=req_schema,
                )
            except jsonschema.ValidationError as er:
                resp = make_response(jsonify({'success': False,
                                              'description': er.message}), 400)

                return resp

            result = func(*args, **kwargs)

            return result
        return wrapper
    return decorator