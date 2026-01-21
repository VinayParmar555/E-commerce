from app.db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class ShippingAddress(Base):

    __tablename__ = "shipping_addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    address_line1 = Column(String, nullable=False)
    address_line2 = Column(String,nullable=True)
    city = Column(String, nullable=False)
    postal_code = Column(Integer, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)

    user = relationship("Users", back_populates="shipping")