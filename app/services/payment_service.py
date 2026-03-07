import hashlib
import hmac
import razorpay
from sqlalchemy.orm import Session
from app.config.settings import settings
from app.db.models.order import Order
from app.db.models.shipping import ShippingStatus as ModelShipStatus
from app.exception.checkout import OrderError, PaymentError, RazorpayPaymentFailed
from app.schema.order import OrderStatus
from app.schema.payment import PaymentCreate, PaymentGateway, PaymentResponseRazorpay, PaymentStatus
from app.db.models.payment import Payment
from app.schema.shipping import ShippingStatus as SchemaShipStatus
from app.utils.mock_id import generate_mock_id

RAZORPAY_KEY_ID=settings.RAZORPAY_KEY_ID
RAZORPAY_KEY_SECRET=settings.RAZORPAY_KEY_SECRET
RAZORPAY_WEBHOOK_SECRET=settings.RAZORPAY_WEBHOOK_SECRET

_razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def create_payment(db:Session, user_id:int, order:Order, data:PaymentCreate) -> PaymentResponseRazorpay:
    pg_order_id = None
    pg_payment_id = None
    pg_signature = None
    rz_data = None
    gateway = PaymentGateway(data.gateway)
    if gateway == PaymentGateway.mock:
        is_success = data.simulate_succ
        if not is_success:
            payment_status = PaymentStatus.failed
            pg_order_id = None
            pg_payment_id = None
            pg_signature = None
            order.status = OrderStatus.cancelled
            shipstatus = ModelShipStatus(order_id=order.id, status=SchemaShipStatus.cancelled)
            db.add(shipstatus)
        else:
            payment_status = PaymentStatus.success
            ids = generate_mock_id()
            pg_order_id = ids["order_id"]
            pg_payment_id = ids["payment_id"]
            pg_signature = ids["signature_id"]
            order.status = OrderStatus.confirmed
            shipstatus = ModelShipStatus(order_id=order.id, status=SchemaShipStatus.pending)
            db.add(shipstatus)

    elif gateway == PaymentGateway.razorpay:
        try:
            order_data = {
                "amount" : int(float(data.amount) * 100),
                "currency" : "INR",
                "payment_capture" : 1
            }
            razorpay_order = _razorpay_client.order.create(order_data)
        except Exception as e:
            raise RazorpayPaymentFailed(f"Razorpay order creation failed: {e}")
        payment_status = PaymentStatus.pending
        pg_order_id = razorpay_order["id"]
        rz_data = {
            "pg_order_id" : pg_order_id,
            "razorpay_key_id" : RAZORPAY_KEY_ID,
            "amount" : order_data["amount"],
            "currency" : order_data["currency"],
        }
        order.status = OrderStatus.pending
    else:
        return False
    payment = Payment(
        order_id=order.id,
        user_id=user_id,
        amount=data.amount,
        status=payment_status,
        payment_gateway=gateway,
        is_paid=(payment_status == PaymentStatus.success),
        pg_order_id=pg_order_id,
        pg_payment_id=pg_payment_id,
        pg_signature=pg_signature
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return PaymentResponseRazorpay(payment=payment, rz_data=rz_data)

def verify_razorpay_signature(raw_body:bytes, signature:str) -> bool:
    expected_signature = hmac.new(RAZORPAY_WEBHOOK_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_signature, signature)

def process_razorpay_webhook(db:Session, payload:dict, signature:str):
    event = payload.get("event")
    payment_entity = payload["payload"]["payment"]["entity"]
    pg_order_id = payment_entity["order_id"]
    pg_payment_id = payment_entity["id"]

    payment = db.query(Payment).filter(Payment.pg_order_id == pg_order_id).with_for_update().first()
    if not payment:
        raise PaymentError("Payment not found")

    order = db.query(Order).filter(Order.id == payment.order_id).with_for_update().first()
    if not order:
        raise OrderError("Order not found")

    if event == "payment.captured":
        payment.status = PaymentStatus.success
        payment.is_paid = True
        payment.pg_payment_id = pg_payment_id
        payment.pg_signature = signature

        order.status = OrderStatus.confirmed

        ship_status = ModelShipStatus(order_id=order.id, status=SchemaShipStatus.processing)
        db.add(ship_status)

    elif event == "payment.failed":
        payment.status = PaymentStatus.failed
        payment.is_paid = False

        order.status = OrderStatus.cancelled

        ship_status = ModelShipStatus(order_id=order.id, status=SchemaShipStatus.cancelled)
        db.add(ship_status)

    else:
        return {"status": "ignored"}

    db.commit()
    return {"status": "success"}

def fetch_payment_status(db:Session, user_id:int, order_id:int):
    payment = db.query(Payment).filter(Payment.user_id==user_id, Payment.order_id==order_id).first()
    if not payment:
        return None
    return payment

def fetch_all_payments(db:Session, user_id:int):
    payment = db.query(Payment).filter(Payment.user_id==user_id).all()
    if not payment:
        return None
    return payment