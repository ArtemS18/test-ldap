from app.ord.schemas.order import OrderCreate
from app.store.postgres.accessor import PgAccessor
from sqlalchemy import delete, insert, select
from ..models import OrderORM


class OrderRepository(PgAccessor):
    async def create_order(self, create_data: OrderCreate) -> OrderORM:
        query = (
            insert(OrderORM)
            .values(name=create_data.name, price=create_data.price)
            .returning(OrderORM)
        )
        result = await self._execute(query)
        return result.scalar_one_or_none()

    async def get_orders(self) -> list[OrderORM]:
        query = select(OrderORM)
        result = await self._execute(query, commit=False)
        return result.scalar_one_or_none()

    async def get_order_by_id(self, order_id: int) -> OrderORM:
        query = select(OrderORM).where(OrderORM.id == order_id)
        result = await self._execute(query, commit=False)
        return result.scalar_one_or_none()

    async def delete_order_by_id(self, order_id: int) -> OrderORM:
        query = delete(OrderORM).where(OrderORM.id == order_id).returning(OrderORM)
        result = await self._execute(query)
        return result.scalar_one_or_none()
