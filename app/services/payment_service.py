from sqlalchemy.orm import Session
from app.schema.payment import PaymentCreate, PaymentGateway, PaymentStatus
from app.db.models.payment import Payment
from app.utils.mock_id import generate_mock_id

def create_payment(db:Session, user_id:int, order_id:int, data:PaymentCreate):
    gateway = PaymentGateway(data.gateway)
    if gateway == PaymentGateway.mock:
        is_success = data.simulate_succ
        if not is_success:
            status = PaymentStatus.failed
            pg_order_id = None
            pg_payment_id = None
            pg_signature = None
        else:
            status = PaymentStatus.success
            ids = generate_mock_id()
            pg_order_id = ids["order_id"]
            pg_payment_id = ids["payment_id"]
            pg_signature = ids["signature_id"]
    elif gateway == PaymentGateway.razorpay:
        pass
    else:
        return False
    payment = Payment(
        order_id=order_id,
        user_id=user_id,
        amount=data.amount,
        status=status,
        payment_gateway=gateway,
        is_paid=(status == PaymentStatus.success),
        pg_order_id=pg_order_id,
        pg_payment_id=pg_payment_id,
        pg_signature=pg_signature
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

def fetch_payment_status(db:Session, user_id:int, order_id:int):
    payment = db.query(Payment).filter(Payment.user_id==user_id, Payment.order_id==order_id).first()
    if not payment:
        return None
    return payment