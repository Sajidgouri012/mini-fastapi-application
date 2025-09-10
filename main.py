from fastapi import FastAPI
from routers import items
import models, database

app = FastAPI(title="CRUD Assignment")
models.Base.metadata.create_all(bind=database.engine)

app.include_router(items.router, prefix="/items", tags=["items"])
