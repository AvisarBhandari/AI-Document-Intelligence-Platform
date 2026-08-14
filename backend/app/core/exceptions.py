from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError

async def pydantic_core_validation_exception_handler(request: Request, exc: ValidationError):
    error = []
    for err in exc.errors(include_url=False, include_context=False):
        loc = list(err.get("loc", []))
        if "email" in loc:
            loc = ["body", ""]

        error.append({
            "type": err.get("type"),
            "loc": loc,
            "input": err.get("input")
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "status": "fail",
            "message": "Invalid Email address ",
            "errors": error
        },
    )

# The hook runner function that links handels back to the application instance
def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ValidationError, pydantic_core_validation_exception_handler)