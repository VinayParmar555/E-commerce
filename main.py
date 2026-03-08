from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.router.products import router as product_router
from app.router.auth import router as auth_router
from app.router.user import router as user_router
from app.router.category import router as category_router
from app.router.cart import router as cart_router
from app.router.shipping import router as shipping_router
from app.router.order import router as order_router
from app.router.payment import router as payment_router
from app.db.session import session as SessionLocal
from app.services.auth_service import cleanup_expired_tokens

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: clean up expired refresh tokens
    db = SessionLocal()
    try:
        cleanup_expired_tokens(db)
    finally:
        db.close()
    yield

app = FastAPI(title="E-commerce Website", lifespan=lifespan)
@app.get("/")
def root():
    return {
        "message" : "E-commerce Backend is live",
        "docs" : "/docs"
    }

app.include_router(product_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(cart_router)
app.include_router(shipping_router)
app.include_router(order_router)
app.include_router(payment_router)