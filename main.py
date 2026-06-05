from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routes.users import user_router
from routes.products import product_router
from routes.orders import order_router

app = FastAPI()
app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)


