from import_export import resources

from stocks import models


class OrderResource(resources.ModelResource):
    class Meta:
        model = models.Order
        fields = [
            "id",
            "incoming__name",
            "outgoing__name",
            "batch_item__good__full_name",
            "quantity_original",
            "quantity_item",
            "balance",
        ]
        export_order = [
            "id",
            "incoming__name",
            "outgoing__name",
            "batch_item__good__full_name",
            "quantity_original",
            "quantity_item",
            "balance",
        ]
