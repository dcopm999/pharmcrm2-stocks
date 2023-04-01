# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import gettext as _
from import_export.admin import ImportExportModelAdmin
from mptt.admin import MPTTModelAdmin

from stocks import imports_exports, models


class BatchItemInline(admin.StackedInline):
    model = models.BatchItem
    autocomplete_fields = ["good"]
    extra = 1


@admin.register(models.Stock)
class StockAdmin(MPTTModelAdmin):
    list_display = ["name", "updated", "created"]
    search_fields = ["name"]


@admin.register(models.Batch)
class BatchAdmin(admin.ModelAdmin):
    inlines = [
        BatchItemInline,
    ]
    list_display = ["number", "stock", "created", "updated"]
    search_fields = ["number", "batch"]


@admin.register(models.BatchItem)
class BatchItemAdmin(admin.ModelAdmin):
    list_display = [
        "good",
        "batch",
        "serial",
        "quantity_original",
        "price_original",
        "quantity_item",
        "price_item",
        "production_date",
        "expirati\
on_date",
    ]
    search_fields = ["good", "batch", "serial", "full_name"]
    autocomplete_fields = ["good", "batch"]


@admin.register(models.Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = [
        "batch_item",
        "quantity_original",
        "quantity_item",
        "price_sum",
        "stock",
    ]
    list_filter = ["stock"]
    search_fields = ["batch_item"]
    autocomplete_fields = ["stock", "batch_item"]


@admin.register(models.Order)
class OrderAdmin(ImportExportModelAdmin):
    resource_class = imports_exports.OrderResource
    list_display = [
        "batch_item",
        "incoming",
        "outgoing",
        "quantity_original",
        "quantity_item",
        "is_approved",
        "is_done",
    ]
    list_filter = ["is_approved"]
    search_fields = ["goods"]
    autocomplete_fields = ["incoming", "outgoing"]
    actions = ["make_approved"]

    def make_approved(self, request, queryset):
        for item in queryset:
            item.is_approved = True
            item.save()

    make_approved.short_description = _("Mark selected orders as approved")  # type: ignore
