from sqlalchemy.orm import Session, selectinload
from app.db.models.cart import Cart
from app.db.models.order import Order, OrderItem
from app.db.models.products import Product
from app.db.models.shipping import ShippingStatus, ShippingAddress
from app.schema.order import OrderStatus
from app.schema.shipping import ShippingStatus as SchemaShippingStatus
from app.schema.payment import PaymentCreate
from app.services.payment_service import create_payment
from app.exception.checkout import AddressIdError, CartItemError, PaymentFailedError, InsufficientStockError, PaymentAmountMismatch

def checkout(db:Session, user_id:int, payment_data:PaymentCreate):
    cart_items = db.query(Cart).filter(Cart.user_id==user_id).options(selectinload(Cart.product)).all()
    if not cart_items:
        raise CartItemError("No item in cart")
    for items in cart_items:
        product = db.query(Product).filter(Product.id==items.product_id).with_for_update().first()
        if product.quantity<items.quantity:
            raise InsufficientStockError("Insufficient Stock") 
    total_amount = sum(item.total_price for item in cart_items)
    
    address =  (db
               .query(ShippingAddress)
               .filter(
                   payment_data.shipping_address_id==ShippingAddress.id, 
                   ShippingAddress.user_id==user_id
                )
               .first()
    )
    if not address:
        raise AddressIdError("Invalid address id!")
    order = Order(user_id=user_id, shipping_address_id=payment_data.shipping_address_id, total_price=float(total_amount))
    db.add(order)
    db.flush()

    if payment_data.amount!=total_amount:
        raise PaymentAmountMismatch("Payment amount does not match cart total!")
    
    payment = create_payment(db, user_id, order.id, payment_data)
    if not payment or not payment.is_paid:
        db.rollback()
        raise PaymentFailedError("Payment failed/Invalid payment type")
    
    for its in cart_items:
        product = db.query(Product).filter(Product.id==its.product_id).with_for_update().first()
        product.quantity-=its.quantity
    order.status = OrderStatus.confirmed
    
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id, 
            product_id=item.product_id, 
            quantity=item.quantity, 
            price=item.price
        )
        db.add(order_item)

    db.query(Cart).filter(Cart.user_id==user_id).delete()

    shipping_status = ShippingStatus(order_id=order.id, status=SchemaShippingStatus.processing)
    db.add(shipping_status)
    stmt = (
        db.query(Order)
        .filter(Order.user_id==user_id)
        .options(
            selectinload(Order.items), 
            selectinload(Order.shippingaddress), 
            selectinload(Order.shippingstatus))
        .all()
    )
    return stmt

def fetch_placed_order(db:Session, user_id:int):
    order = (
        db.query(Order)
        .filter(Order.user_id==user_id)
        .options(selectinload(Order.items), selectinload(Order.items).selectinload(OrderItem.order_product))
        .all()
    )
    return order

def fetch_single_placed_order(db:Session, user_id:int, order_id:int):
    order = (
        db.query(Order)
        .filter(Order.id==order_id, Order.user_id==user_id)
        .options(selectinload(Order.items))
        .first()
    )
    if not order:
        return False
    return order

def cancel_placed_order(db:Session, user_id:int, order_id:int):
    order = fetch_single_placed_order(db, user_id, order_id)
    if not order:
        return None
    if not order.shippingstatus or order.shippingstatus.status not in (SchemaShippingStatus.pending, SchemaShippingStatus.processing):
        return False
    order.status = OrderStatus.cancelled
    order.shippingstatus.status = SchemaShippingStatus.cancelled
    db.commit()
    db.refresh(order)
    return order

def get_user_shipping_status(db:Session, user_id:int, order_id:int):
    ship_status = db.query(Order).filter(Order.user_id==user_id, Order.id==order_id).options(selectinload(Order.shippingstatus)).first()
    if not ship_status:
        return None
    return ship_status.shippingstatus

def update_shipping_status(db:Session, new_status:SchemaShippingStatus, order_id:int):
    order_shippingstatus = db.query(ShippingStatus).filter(ShippingStatus.order_id==order_id).first()
    if not order_shippingstatus or order_shippingstatus.status == SchemaShippingStatus.cancelled:
        return None
    order_shippingstatus.status = new_status
    db.commit()
    db.refresh(order_shippingstatus)
    return order_shippingstatus