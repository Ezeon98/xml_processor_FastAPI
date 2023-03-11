"""Integrate parts of FastAPI elements."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from app.api.routes import router as api_router
from app.dependency_injection.container import Container

container = Container()

app = FastAPI(
    title="Calyx Datareader xml Chile Processor",
    version="1.0.0",
    description="Cakyx Datareader xml Chile Processor",
)

app.container = container


class Settings(BaseModel):
    """AuthJWT settings"""

    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    """Get AuthJWT Config"""
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    """Handles AuthJWT Exception responses"""
    # pylint: disable=unused-argument
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/")
async def root():
    """Show base url."""
    return {"message": "Calyx Datareader xml Chile Processor. See docs in /docs url."}


# Includes all the routes
app.include_router(api_router)
