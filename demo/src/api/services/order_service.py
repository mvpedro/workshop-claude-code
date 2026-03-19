from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from src.api.events import bus
from src.api.events.types import OrderCreated, OrderStatusChanged
from src.api.exceptions.business import InvalidStatusTransition, NotFound
from src.api.models.order import Order
from src.api.models.order_item import OrderItem
from src.api.models.product import Product
from src.api.schemas.order import OrderCreate
from src.api.services import inventory_service, pricing_service


async def create_order(session: AsyncSession, data: OrderCreate) -> Order:
    items_with_products: list[tuple[Product, int]] = []
    for item in data.items:
        product = await session.get(Product, item.product_id)
        if product is None:
            raise NotFound("Produto", item.product_id)
        items_with_products.append((product, item.quantity))

    # Reserve stock for all items
    for product, qty in items_with_products:
        await inventory_service.reserve_stock(session, product, qty)

    # Calculate total
    total = pricing_service.calculate_order_total(items_with_products)

    # Create order
    order = Order(customer_id=data.customer_id, total=total, notes=data.notes)
    session.add(order)
    await session.flush()

    # Create order items
    for product, qty in items_with_products:
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=qty,
            unit_price=product.price,
        )
        session.add(order_item)
    await session.flush()

    # Emit event
    bus.publish(OrderCreated(
        order_id=order.id,
        customer_id=data.customer_id,
        total=total,
        item_count=len(data.items),
    ))

    return order


async def transition_status(session: AsyncSession, order_id: str, new_status: str) -> Order:
    query = select(Order).where(Order.id == order_id).options(selectinload(Order.items))
    result = await session.execute(query)
    order = result.scalar_one_or_none()
    if order is None:
        raise NotFound("Pedido", order_id)
    if not order.can_transition_to(new_status):
        raise InvalidStatusTransition(order_id, order.status, new_status)

    old_status = order.status
    order.status = new_status
    await session.flush()

    # Release stock if cancelled
    if new_status == "cancelled":
        for item in order.items:
            product = await session.get(Product, item.product_id)
            if product:
                await inventory_service.release_stock(session, product, item.quantity)

    bus.publish(OrderStatusChanged(
        order_id=order.id, old_status=old_status, new_status=new_status
    ))

    return order
