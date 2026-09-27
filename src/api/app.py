from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.api.openai_compat import openai_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Smart LLM Router API",
        description="Semantic LLM routing system using Jev, deterministic policies, and multi-provider models.",
        version="0.1.0",
    )

    # Enable CORS for local dashboards or frontend clients
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    app.include_router(openai_router)

    # Mount compiled frontend dashboard if present
    from pathlib import Path
    from fastapi.staticfiles import StaticFiles

    dist_dir = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
    if dist_dir.exists():
        app.mount("/dashboard", StaticFiles(directory=str(dist_dir), html=True), name="dashboard")

    from fastapi.responses import RedirectResponse

    @app.get("/", include_in_schema=False)
    def root():
        if dist_dir.exists():
            return RedirectResponse(url="/dashboard/")
        return {"message": "Smart LLM Router API is running. Visit /docs for Swagger."}

    @app.get("/dashboard", include_in_schema=False)
    def dashboard_redirect():
        return RedirectResponse(url="/dashboard/")

    return app


app = create_app()
