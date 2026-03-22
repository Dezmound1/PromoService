from rest_framework import status, viewsets
from rest_framework.request import Request
from django.http import JsonResponse

from promo_service.orders.serializer import CreateOrderSerializer


class OrderViewSet(viewsets.ViewSet):
    def create(self, request: Request):
        try:
            order_serializer = CreateOrderSerializer(data=request.POST)
            order_serializer.is_valid(raise_exception=True)
            # TODO order = OrderService.create_order(order_serializer.validated_data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
