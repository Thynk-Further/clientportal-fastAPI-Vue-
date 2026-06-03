from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

from app.config import settings
from app.core.openapi import openapi_tags
from app.core.exceptions import CPException, cp_exception_handler, http_exception_handler
from app.routers import auth, users, clients, projects, deliverables, files, approvals, websockets, messages, invoices, webhooks, time_entries

def create_app() -> FastAPI:
    docs_url = "/docs" if settings.ENVIRONMENT != "production" else None
    redoc_url = "/redoc" if settings.ENVIRONMENT != "production" else None
    openapi_url = "/openapi.json" if settings.ENVIRONMENT != "production" else None

    app = FastAPI(
        title="ClientPortal API",
        description="Internal API for ClientPortal freelancer and client endpoints.",
        version="2.0.0",
        openapi_tags=openapi_tags,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
    )

    if settings.ENVIRONMENT == "production":
        origins = [settings.FRONTEND_URL]
    else:
        origins = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            settings.FRONTEND_URL,
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(CPException, cp_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)

    app.include_router(auth.router, prefix="/api/v1/auth")
    app.include_router(users.router, prefix="/api/v1/users")
    app.include_router(clients.router, prefix="/api/v1/clients")
    app.include_router(projects.router, prefix="/api/v1/projects")
    app.include_router(deliverables.router, prefix="/api/v1")
    app.include_router(files.router, prefix="/api/v1/files")
    app.include_router(approvals.router, prefix="/api/v1")
    app.include_router(messages.router, prefix="/api/v1")
    app.include_router(invoices.router, prefix="/api/v1")
    app.include_router(webhooks.router, prefix="/api/v1")
    app.include_router(time_entries.router, prefix="/api/v1")
    app.include_router(websockets.router)

    return app

app = create_app()
