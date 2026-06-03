from fastapi import FastAPI
from routes.routers import router
from database import Base, engine
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    Base.metadata.create_all(engine)
    app = FastAPI()

    app.include_router(router)

