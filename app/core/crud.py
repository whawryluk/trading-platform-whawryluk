from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.models import Order, OrderStatus
from app.utils.pricing import calculate_price
import uuid


async def create_order(db: AsyncSession, order_input):
	order_price = calculate_price(order_input["symbol"], order_input["quantity"])

	new_order = Order(
		id=uuid.uuid4(),
		symbol=order_input["symbol"],
		quantity=order_input["quantity"],
		price=order_price,
		status=OrderStatus.PENDING
	)

	db.add(new_order)
	await db.commit()
	await db.refresh(new_order)
	return new_order


async def get_orders(db: AsyncSession):
	result = await db.execute(select(Order))
	return result.scalars().all()


async def get_order_by_id(db: AsyncSession, order_id: str):
	result = await db.execute(select(Order).where(Order.id == order_id))
	return result.scalar_one_or_none()


async def cancel_order(db: AsyncSession, order_id: str):
	order = await get_order_by_id(db, order_id)
	if order and order.status == OrderStatus.PENDING:
		order.status = OrderStatus.CANCELLED
		await db.commit()
		return order
	return None
