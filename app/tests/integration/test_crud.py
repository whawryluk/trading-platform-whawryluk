import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import Order, OrderStatus
from app.core.crud import create_order, get_order_by_id, get_orders, cancel_order
from uuid import uuid4


@pytest.mark.asyncio
async def test_create_order(db_session: AsyncSession):
    """Tests succesful creation of single order"""
    order_input = {
        "symbol": "AAPL",
        "quantity": 10,
    }

    new_order = await create_order(db_session, order_input)

    assert new_order.symbol == "AAPL"
    assert new_order.quantity == 10
    assert new_order.status == OrderStatus.PENDING
    assert new_order.price == 100.0

    fetched_order = await get_order_by_id(db_session, str(new_order.id))

    assert fetched_order.symbol == "AAPL"
    assert fetched_order.quantity == 10
    assert fetched_order.price == 100.0
    assert fetched_order.created_at is not None
    assert datetime.utcnow() - fetched_order.created_at < timedelta(seconds=20)


@pytest.mark.asyncio
async def test_get_orders_crud(db_session):
    """Tests succesful retrieve of multiple created orders"""
    order_inputs = [
        {"symbol": "EURUSD", "quantity": 5},
        {"symbol": "MSFT", "quantity": 3},
        {"symbol": "GBPUSD", "quantity": 2},
    ]

    created_ids = []

    for inp in order_inputs:
        created_order = await create_order(db_session, inp)
        created_ids.append(created_order.id)

    all_orders = await get_orders(db_session)
    assert len(all_orders) == len(order_inputs)

    fetched_ids = [o.id for o in all_orders]
    for cid in created_ids:
        assert cid in fetched_ids


@pytest.mark.asyncio
async def test_get_order_by_id_crud(db_session):
    order_input = {"symbol": "PLNUSD", "quantity": 7}
    new_order = await create_order(db_session, order_input)

    fetched_order = await get_order_by_id(db_session, str(new_order.id))

    assert fetched_order is not None
    assert fetched_order.id == new_order.id
    assert fetched_order.symbol == "PLNUSD"
    assert fetched_order.quantity == 7
    assert fetched_order.status == OrderStatus.PENDING
    assert fetched_order.price == 1.75


@pytest.mark.asyncio
async def test_cancel_order_crud(db_session):
    order_input = {"symbol": "AAPL", "quantity": 10}
    new_order = await create_order(db_session, order_input)

    cancelled_order = await cancel_order(db_session, str(new_order.id))

    assert cancelled_order is not None
    assert cancelled_order.id == new_order.id
    assert cancelled_order.status == OrderStatus.CANCELLED
    assert cancelled_order.price == 100.0

    fetched_order = await get_order_by_id(db_session, str(new_order.id))
    assert fetched_order is not None
    assert fetched_order.status == OrderStatus.CANCELLED
    assert fetched_order.price == 100.0


@pytest.mark.asyncio
async def test_cancel_non_pending_order_crud(db_session):
    order_input = {"symbol": "PLNUSD", "quantity": 7}
    new_order = await create_order(db_session, order_input)

    new_order.status = OrderStatus.EXECUTED
    await db_session.commit()
    await db_session.refresh(new_order)

    cancelled_order = await cancel_order(db_session, str(new_order.id))
    assert cancelled_order is None

    fetched_order = await get_order_by_id(db_session, str(new_order.id))
    assert fetched_order is not None
    assert fetched_order.status == OrderStatus.EXECUTED


@pytest.mark.asyncio
async def test_cancel_order_not_found_crud(db_session):
    fake_id = str(uuid4())
    cancelled_order = await cancel_order(db_session, fake_id)

    assert cancelled_order is None