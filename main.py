from fastapi import FastAPI
from app.router.products import router as product_router
from app.router.users import router as users_router

app = FastAPI(title="Radha Krishna")
app.include_router(product_router)
app.include_router(users_router)