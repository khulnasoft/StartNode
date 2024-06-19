from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from startnode.controllers.startnode import router as startnode_router
from startnode.config.settings import Settings

config = Settings()

app = FastAPI()

app.add_middleware(
    DBSessionMiddleware, db_url=config.DB_URL, engine_args=config.db_engine_args
)

app.include_router(startnode_router, prefix="/api/startnode")


@app.get("/health")
async def health_check():
    return {"status": "AutoNode is Running"}
