from sqlalchemy import Column, String, Integer, Float, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import enum
from .db import Base


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    symbol = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
