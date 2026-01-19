from sqlalchemy.orm import Session
from app.schema.cart import CartOut
from app.db.models.cart import Cart
from app.db.models.products import Product

def add_to_cart(db:Session, cart_item:CartOut):
    product = db.get(Product, cart_item.product_id)
    if not product or product.quantity<=0:
        return None
    stmt = db.query(Cart).filter(Cart.user_id==cart_item.user_id, Cart.product_id==cart_item.product_id).first()
    if stmt:
        stmt.quantity+=cart_item.quantity
        stmt.total_price=product.price*stmt.quantity
    cart = Cart(**cart_item.model_dump(), price=product.price, total_price=product.price*cart_item.quantity)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart