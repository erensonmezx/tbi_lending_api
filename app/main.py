import logging
from uuid import UUID
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from .logging import setup_logging, get_or_create_correlation_id, CORRELATION_HEADER
from .models import CreateApplicationRequest, new_application
from .storage import InMemoryApplicationStore
from .errors import ErrorResponse, NotFoundError

def create_app() -> FastAPI:
    setup_logging()
    logger = logging.getLogger("tbi_lending")

    app = FastAPI(title="tbi lending api", version="0.1.0")
    store = InMemoryApplicationStore()

    @app.middleware("http")
    async def correlation_middleware(request: Request, call_next):
        cid = get_or_create_correlation_id(request)
        request.state.correlation_id = cid
        response: Response = await call_next(request)
        response.headers[CORRELATION_HEADER] = cid
        return response

    def log_adapter(request: Request) -> logging.LoggerAdapter:
        cid = getattr(request.state, "correlation_id", None)
        return logging.LoggerAdapter(logger, {"correlation_id": cid or "-"})

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        err = ErrorResponse(
            error_code="NOT_FOUND",
            message=exc.message,
            details=exc.details,
            correlation_id=getattr(request.state, "correlation_id", None),
        )
        return JSONResponse(status_code=404, content=err.model_dump())

    @app.get("/health")
    async def health(request: Request):
        log_adapter(request).info("health_check")
        return {"status": "ok"}

    @app.post("/applications", status_code=201)
    async def create_application(req: CreateApplicationRequest, request: Request):
        app_obj = new_application(req)
        store.create(app_obj)
        log_adapter(request).info("application_created id=%s", str(app_obj.id))
        return app_obj

    @app.get("/applications/{app_id}")
    async def get_application(app_id: UUID, request: Request):
        app_obj = store.get(app_id)
        log_adapter(request).info("application_fetched id=%s", str(app_obj.id))
        return app_obj

    return app

app = create_app()
