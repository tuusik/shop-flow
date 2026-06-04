from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routes.users import user_router
from routes.products import product_router

app = FastAPI()
app.include_router(user_router)
app.include_router(product_router)



