from fastapi import FastAPI
from app.router.products import router as product_router
# from fastapi import OAuth2PasswordBearer, OAuth2PasswordRequestForm



app = FastAPI(title="Radha Krishna")
app.include_router(product_router)

