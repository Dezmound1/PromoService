from rest_framework import status, viewsets
from rest_framework.request import Request
from django.http import JsonResponse

from orders.repository import OrderRepository


class OrderViewSet(viewsets.ViewSet):
    def create(self, request: Request):
        try:
            OrderRepository.create_order(request.POST)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
