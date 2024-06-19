from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastnode.controllers.fastnode import router as fastnode_router
from fastnode.config.settings import Settings

config = Settings()

app = FastAPI()

app.add_middleware(
    DBSessionMiddleware, db_url=config.DB_URL, engine_args=config.db_engine_args
)

app.include_router(fastnode_router, prefix="/api/fastnode")


@app.get("/health")
async def health_check():
    return {"status": "FastNode is Running"}
