from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

class CPException(Exception):
    def __init__(self, detail: str, code: str, status_code: int = 400, field: str = None):
        self.detail = detail
        self.code = code
        self.status_code = status_code
        self.field = field

async def cp_exception_handler(request: Request, exc: CPException):
    content = {
        "detail": exc.detail,
        "code": exc.code
    }
    if exc.field:
        content["field"] = exc.field
    return JSONResponse(
        status_code=exc.status_code,
        content=content
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
        
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "code": "HTTP_EXCEPTION"
        }
    )
