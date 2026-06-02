from fastapi import FastAPI
from routes.routers import router
from database import Base, engine

Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(router)

