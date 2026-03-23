from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from orders.serializer import CreateOrderSerializer, OrderResponseSerializer
from orders.services import OrderService
from users.repository import UserRepository


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

        user = UserRepository.get_user(serializer.validated_data["user_id"])
        if not user:
            raise ValidationError("Пользователь не найден")

        result = OrderService.create_order(
            user=user,
            goods_data=serializer.validated_data["goods"],
            promo_code=serializer.validated_data.get("promo_code"),
        )

        response = OrderResponseSerializer(result)
        return Response(response.data, status=status.HTTP_201_CREATED)
