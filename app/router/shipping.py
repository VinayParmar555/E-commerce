from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models.user import Users
from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.schema.shipping import ShippingBase
from app.services.shipping_service import create_shipping_address

router = APIRouter(prefix="/shipping_addresses", tags=["Shipping"])

@router.post("/add_address")
async def add_new_address(data:ShippingBase, user:Users=Depends(get_current_user), db:Session=Depends(get_db)):
    new_address = create_shipping_address(db, user.id, data)
    if not new_address:
        raise HTTPException(status_code=400, detail="Invalid format")
    return new_address