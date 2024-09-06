from fastapi.responses import JSONResponse


def standard_response(data: dict, code: int = 200):
    return JSONResponse(content={
        "code": 200, 
        "success": True, 
        "data": data
})


def error_response(code: int, message: str, error_data=None):
    if error_data is None:
        error_data = []
    content = {
        "code": code,
        "success": False,
        "errorData": error_data,
        "message": message
    }
    return JSONResponse(status_code=code, content=content)