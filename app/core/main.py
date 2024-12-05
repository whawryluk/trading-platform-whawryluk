from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.db import engine, Base, get_db
from app.core.crud import create_order, get_orders, get_order_by_id, cancel_order
from app.core.schemas import OrderCreate, OrderResponse

settings = Settings()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Trading platform API is running!"}


@app.on_event("startup")
async def startup():
    if settings.environment == "development":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            print("Tables created successfully!")
    else:
        print("Skipping dropping and recreating tables")


@app.post("/orders", response_model=OrderResponse)
async def create_new_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    new_order = await create_order(db, order.dict())
    return new_order


@app.get("/orders", response_model=list[OrderResponse])
async def fetch_orders(db: AsyncSession = Depends(get_db)):
    return await get_orders(db)


@app.get("/orders/{order_id}", response_model=OrderResponse)
async def fetch_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    order = await get_order_by_id(db, str(order_id))
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.delete("/orders/{order_id}", response_model=OrderResponse)
async def cancel_order_by_id(order_id: str, db: AsyncSession = Depends(get_db)):
    order = await cancel_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found or cannot be cancelled")
    return order
