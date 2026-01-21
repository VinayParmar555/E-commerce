from sqlalchemy.orm import Session
from app.schema.shipping import ShippingBase
from app.db.models.shipping import ShippingAddress

def create_shipping_address(db:Session, user_id:int, data:ShippingBase):
    address = ShippingAddress(**data.model_dump(), user_id=user_id)
    if not address:
        return False
    db.add(address)
    db.commit()
    db.refresh(address)
    return address

def fetch_address(db:Session, user_id:int):
    address = db.query(ShippingAddress).filter(ShippingAddress.user_id==user_id).all()
    if not address:
        return None
    return address