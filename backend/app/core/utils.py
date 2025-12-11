from typing import Any, Dict

def format_response(data: Any, message: str = "Success", status_code: int = 200) -> Dict:
    return {
        "status_code": status_code,
        "message": message,
        "data": data
    }

def format_error(message: str, status_code: int = 400, data: Any = None) -> Dict:
    return {
        "status_code": status_code,
        "message": message,
        "data": data
    }

def get_pagination_params(skip: int = 0, limit: int = 10) -> tuple:
    if skip < 0:
        skip = 0
    if limit < 1 or limit > 100:
        limit = 10
    return skip, limit
