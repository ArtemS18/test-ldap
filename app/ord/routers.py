from fastapi import APIRouter, Depends

from app.auth.depends.autho import validate_role
from app.lib.web.models import Request
from app.ord.schemas.order import OrderCreate, OrderListResponse, OrderResponse
from app.lib.web import exeptions

router = APIRouter(
    prefix="/ord",
    tags=["Валидация роли"],
    dependencies=[Depends(validate_role("Admin", "Moderator"))],
)


@router.post(
    "/",
    response_model=OrderResponse,
    dependencies=[Depends(validate_role("Moderator"))],
)
async def order_create_handler(req: Request, order_shema: OrderCreate):
    ord_orm = await req.app.store.order_repo.create_order(order_shema)
    if ord_orm is None:
        raise exeptions.NOT_FOUND
    ord = OrderResponse.model_validate(ord_orm)
    return ord


@router.delete(
    "/{order_id}",
    response_model=OrderResponse,
    dependencies=[Depends(validate_role("Moderator"))],
)
async def order_delete_handler(req: Request, order_id: int):
    ord_orm = await req.app.store.order_repo.delete_order_by_id(order_id)
    if ord_orm is None:
        raise exeptions.NOT_FOUND
    ord = OrderResponse.model_validate(ord_orm)
    return ord


@router.get("/", response_model=OrderListResponse)
async def orders_get_handler(req: Request):
    ords_orm = await req.app.store.order_repo.get_orders()
    if ords_orm is None or ords_orm == []:
        raise exeptions.NOT_FOUND
    ords = OrderListResponse(
        orders=[OrderResponse.model_validate(ord) for ord in ords_orm]
    )
    return ords


@router.get("/{order_id}", response_model=OrderResponse)
async def order_get_handler(req: Request, order_id: int):
    ord_orm = await req.app.store.order_repo.get_order_by_id(order_id)
    if ord_orm is None:
        raise exeptions.NOT_FOUND
    ord = OrderResponse.model_validate(ord_orm)
    return ord
