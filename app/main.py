from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import init_db, AsyncSessionLocal
from app.core.seed import seed_system
from app.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1 Database structure
    await init_db()

    # 2 System seeding (IAM, root admin, policies)
    async with AsyncSessionLocal() as db:
        await seed_system(db)

    print("INFINTREE started")
    yield
    print("INFINTREE shutdown")


def create_app() -> FastAPI:
    app = FastAPI(
        title="INFINTREE API",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        redirect_slashes=False
    )

    # Central API registry
    app.include_router(api_router, prefix="/api")

    return app


app = create_app()
app.router.lifespan_context = lifespan

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)