import structlog
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from orders.serializer import CreateOrderSerializer, OrderResponseSerializer
from orders.services import OrderService
from users.repository import UserRepository

logger = structlog.get_logger(__name__)


class OrderViewSet(viewsets.ViewSet):
    """ViewSet for handling order-related operations."""

    @swagger_auto_schema(
        operation_summary="Создать заказ",
        operation_description=(
            "Создаёт заказ для пользователя. При указании промокода применяется скидка к подходящим товарам."
        ),
        request_body=CreateOrderSerializer,
        responses={
            201: OrderResponseSerializer,
            400: "Ошибка валидации (невалидные данные, промокод, товары)",
        },
    )
    def create(self, request: Request):
        """Handle the creation of a new order."""
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user_id = data["user_id"]
        log = logger.bind(user_id=user_id)

        user = UserRepository.get_user(user_id)
        if not user:
            log.warning("order.user_not_found")
            raise ValidationError("Пользователь не найден")

        result = OrderService.create_order(
            user=user,
            goods_data=data["goods"],
            promo_code=data.get("promo_code"),
        )

        log.info(
            "order.created",
            order_id=result["order_id"],
            total=str(result["total"]),
        )

        response = OrderResponseSerializer(result)
        return Response(response.data, status=status.HTTP_201_CREATED)
