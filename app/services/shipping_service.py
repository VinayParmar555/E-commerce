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

def get_address_by_id(db:Session, address_id:int):
    address = db.query(ShippingAddress).filter(ShippingAddress.id==address_id).first()
    if not address:
        return None
    return address

def update_address(db:Session, user_id:int, data:ShippingBase, address_id:int):
    address = db.query(ShippingAddress).filter(ShippingAddress.id==address_id, user_id==user_id).first()
    if not address:
        return None
    address.address_line1 = data.address_line1
    address.address_line2 = data.address_line2
    address.city = data.city
    address.postal_code = data.postal_code
    address.state = data.state
    address.country = data.country
    db.add(address)
    db.commit()
    db.refresh(address)
    return address

def delete_address(db:Session, user_id:int, address_id:int):
    address = db.query(ShippingAddress).filter(ShippingAddress.id==address_id, user_id==user_id).first()
    if not address:
        return None
    db.delete(address)
    db.commit()
    return True