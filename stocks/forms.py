from django.forms import ModelForm

from stocks import models


class StockForm(ModelForm):
    class Meta:
        model = models.Stock
        fields = ["name", "parent"]


class BatchForm(ModelForm):
    class Meta:
        model = models.Batch
        fields = ["stock", "number"]


class BatchItamForm(ModelForm):
    class Meta:
        model = models.BatchItem
        fields = [
            "good",
            "batch",
            "serial",
            "quantity_original",
            "price_original",
            "quantity_item",
            "price_item",
        ]
