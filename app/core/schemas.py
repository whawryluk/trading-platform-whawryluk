from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid
import enum


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"


class OrderCreate(BaseModel):
    symbol: str
    quantity: int


class OrderResponse(BaseModel):
    id: uuid.UUID
    symbol: str
    quantity: int
    price: float
    status: OrderStatus
    created_at: datetime

    class Config:
        from_attributes = True
