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
