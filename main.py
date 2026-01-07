from fastapi import FastAPI
from app.router.products import router as product_router
from app.router.auth import router as auth_router
from app.router.user import router as user_router
from app.router.category import router as category_router

app = FastAPI(title="E-commerce Website")
app.include_router(product_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(category_router)