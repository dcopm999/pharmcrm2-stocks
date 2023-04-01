from rest_framework import serializers

from stocks import models


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stock
        fields = ["id", "name", "slug", "created", "updated"]


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Batch
        fields = "__all__"


class BatchItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BatchItem
        fields = "__all__"


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Balance
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = "__all__"
