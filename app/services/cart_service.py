from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models.user import Users
from app.schema.cart import CartItem
from app.db.models.cart import Cart
from app.db.models.products import Product

def add_to_cart(db:Session, cart_item:CartItem, user_id:int):
    user = db.get(Users, user_id)
    if not user:
        return False
    product = db.query(Product).filter(Product.id==cart_item.product_id).with_for_update().first()
    if not product or product.quantity<cart_item.quantity:
        return None
    stmt = db.query(Cart).filter(Cart.user_id==user_id, Cart.product_id==cart_item.product_id).with_for_update().first()
    if stmt:
        stmt.quantity+=cart_item.quantity
        stmt.total_price=product.price*stmt.quantity
    else:
        stmt = Cart(**cart_item.model_dump(), user_id=user_id, price=product.price, total_price=product.price*cart_item.quantity)
        db.add(stmt)
        
    db.commit()
    db.refresh(stmt)
    return stmt

def see_cart(db:Session, user_id:int):
    items = db.query(Cart).filter(Cart.user_id==user_id).all()
    if not items:
        return None
    total_price = db.query(func.sum(Cart.total_price)).filter(Cart.user_id==user_id).scalar()
    return {"items" : items, "total_price" : total_price}

def remove_cart(db:Session, user_id:int, cart_id:int):
    cart = db.query(Cart).filter(Cart.id==cart_id).first()
    if not cart:
        return None
    db.delete(cart)
    db.commit()
    return True