from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI  # noqa: E402

from routes.orders import order_router  # noqa: E402
from routes.products import product_router  # noqa: E402
from routes.users import user_router  # noqa: E402

app = FastAPI()
app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)


@app.get("/")
def root():
    return {"status": "ok"}
