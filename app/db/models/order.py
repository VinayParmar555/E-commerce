from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, Enum, Column, Integer, ForeignKey, Float, func
from app.db.base import Base
from app.schema.order import OrderStatus

class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    shipping_address_id = Column(Integer, ForeignKey("shipping_addresses.id", ondelete="CASCADE"), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus, name="order_status_enum"), default=OrderStatus.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    items = relationship("OrderItems", back_populates="order")
    user_item = relationship("Users", back_populates="user_order")
    shippingaddress = relationship("ShippingAddress", back_populates="orders")
    shippingstatus = relationship("ShippingStatus", back_populates="orderid")
    payment = relationship("Payment", back_populates="order_payment")

class OrderItems(Base):

    __tablename__ = "orders_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    order_product = relationship("Product", back_populates="order_items")