import os
import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker

from app.core.db import Base
from app.core.models import Order, OrderStatus

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db"
)

test_engine: AsyncEngine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """
    Fixture to provide a fresh database session for each test.
    """
    # Ensure tables exist
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create a new session for the test
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()  # Rollback any changes made during the test

    # Drop all tables after the test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


@pytest.fixture
async def seed_orders(db_session):
    orders = [
        Order(
            id=uuid.uuid4(),
            symbol="AAPL",
            quantity=10,
            price=150.0,
            status=OrderStatus.PENDING,
        ),
        Order(
            id=uuid.uuid4(),
            symbol="MSFT",
            quantity=5,
            price=300.0,
            status=OrderStatus.PENDING,
        ),
    ]
    db_session.add_all(orders)
    await db_session.commit()
    return orders