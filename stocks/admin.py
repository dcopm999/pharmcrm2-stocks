# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import gettext as _
from mptt.admin import MPTTModelAdmin

from stocks import models


class BatchPharmItemInline(admin.TabularInline):
    model = models.BatchPharmItem
    autocomplete_fields = ["product"]


@admin.register(models.Stock)
class StockAdmin(MPTTModelAdmin):
    list_display = ["name", "updated", "created"]
    search_fields = ["name"]


@admin.register(models.Batch)
class BatchAdmin(admin.ModelAdmin):
    inlines = [
        BatchPharmItemInline,
    ]
    list_display = ["number", "stock", "created", "updated"]
    search_fields = ["number", "batch"]


@admin.register(models.BatchPharmItem)
class BatchPharmItemAdmin(admin.ModelAdmin):
    list_display = [
        "product",
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
    search_fields = ["product", "batch", "serial", "full_name"]
    autocomplete_fields = ["product", "batch"]


@admin.register(models.Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = [
        "pharm_item",
        "quantity_original",
        "quantity_item",
        "price_sum",
        "stock",
    ]
    list_filter = ["stock"]
    autocomplete_fields = ["stock", "pharm_item"]


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "pharm_item",
        "incoming",
        "outgoing",
        "quantity_original",
        "quantity_item",
        "is_approved",
        "is_done",
    ]
    list_filter = ["is_approved"]
    autocomplete_fields = ["incoming", "outgoing"]
    actions = ["make_approved"]

    def make_approved(self, request, queryset):
        for item in queryset:
            item.is_approved = True
            item.save()

    make_approved.short_description = _("Mark selected orders as approved")  # type: ignore
