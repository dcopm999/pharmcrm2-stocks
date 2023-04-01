from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.viewsets import ModelViewSet

from stocks import models
from stocks.api import serializers


class StockViewSet(ModelViewSet):
    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializer
    permission_class = [DjangoObjectPermissions]


class BatchViewSet(ModelViewSet):
    queryset = models.Batch.objects.all()
    serializer_class = serializers.BatchSerializer
    permission_class = [DjangoObjectPermissions]


class BatchItemViewSet(ModelViewSet):
    queryset = models.BatchItem.objects.all()
    serializer_class = serializers.BatchItemSerializer
    permission_class = [DjangoObjectPermissions]


class BalanceViewSet(ModelViewSet):
    queryset = models.Balance.objects.all()
    serializer_class = serializers.BalanceSerializer
    permission_class = [DjangoObjectPermissions]


class OrderViewSet(ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_class = [DjangoObjectPermissions]
