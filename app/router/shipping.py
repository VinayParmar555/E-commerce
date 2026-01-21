from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db.models.user import Users
from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.schema.shipping import ShippingBase, ShippingAddress
from app.services.shipping_service import create_shipping_address, fetch_address, get_address_by_id

router = APIRouter(prefix="/shipping_addresses", tags=["Shipping"])

@router.post("/add_address", response_model=ShippingAddress)
async def add_new_address(data:ShippingBase, user:Users=Depends(get_current_user), db:Session=Depends(get_db)):
    new_address = create_shipping_address(db, user.id, data)
    if not new_address:
        raise HTTPException(status_code=400, detail="Invalid format")
    return new_address

@router.get("/fetch", response_model=List[ShippingAddress])
async def see_address(user:Users=Depends(get_current_user), db:Session=Depends(get_db)):
    address = fetch_address(db, user.id)
    if not address:
        raise HTTPException(status_code=404, detail="add address!")
    return address