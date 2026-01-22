from app.db.base import Base
from app.schema.payment import PaymentStatus, PaymentGateway
from sqlalchemy import Boolean, Column, DateTime, Integer, ForeignKey, Enum, String, func
from sqlalchemy.orm import relationship

class Payment(Base):

    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(Enum(PaymentStatus, name="payment_status_enum"), default=PaymentStatus.pending)
    payment_gateway = Column(Enum(PaymentGateway, name="payment_gateway_enum"), default=PaymentGateway.mock)
    is_paid = Column(Boolean, default=False)
    pg_order_id = Column(String, nullable=True)
    pg_payment_id = Column(String, nullable=True)
    pg_signature = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)

    order_payment = relationship("Order", back_populates="payment")
    user_payment = relationship("Users", back_populates="paymentuser")