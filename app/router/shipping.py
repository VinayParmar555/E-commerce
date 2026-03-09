from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.cache.rate_limit import ip_key, rate_limit, user_key
from app.db.models.user import Users
from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.schema.shipping import ShippingBase, ShippingAddress
from app.services.shipping_service import create_shipping_address, delete_address, fetch_address, get_address_by_id, update_address

router = APIRouter(prefix="/shipping_addresses", tags=["Shipping"])

@router.post("/add", response_model=ShippingAddress)
async def add_new_address(data:ShippingBase, user:Users=Depends(get_current_user), db:Session=Depends(get_db)):
    new_address = create_shipping_address(db, user.id, data)
    if not new_address:
        raise HTTPException(status_code=400, detail="Invalid format")
    return new_address

@router.get("/fetch", response_model=List[ShippingAddress])
async def see_address(user:Users=Depends(get_current_user), _:None=Depends(rate_limit(5,60,user_key)), db:Session=Depends(get_db)):
    address = fetch_address(db, user.id)
    if not address:
        raise HTTPException(status_code=404, detail="No shipping addresses found")
    return address

@router.get("/fetch_byid/{address_id}", response_model=ShippingAddress)
async def get_user_address_byid(address_id:int, _:None=Depends(rate_limit(5,60,ip_key)), db:Session=Depends(get_db)):
    address = get_address_by_id(db, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="address not found")
    return address

@router.put("/update/{address_id}")
async def update_existing_address(data:ShippingBase, address_id:int, user:Users=Depends(get_current_user), db:Session=Depends(get_db)):
    address = update_address(db, user.id, data, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"msg" : "Address updated successfully"}

@router.delete("/delete/{address_id}")
async def delete_existing_address(address_id:int, user:Users=Depends(get_current_user), db:Session=Depends(get_db)):
    address = delete_address(db, user.id, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"msg" : "Address deleted successfully"}