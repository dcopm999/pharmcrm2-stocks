# -*- coding: utf-8 -*-
from django.urls import path

from stocks import views

app_name = "stocks"

urlpatterns = [
    # Stock
    path("", views.HomeView.as_view(), name="home"),
    path("stock/list/", views.StockListView.as_view(), name="stock-list"),
    path(
        "stock/detail/<slug:slug>/",
        views.StockDetailView.as_view(),
        name="stock-detail",
    ),
    path("stock/create/", views.StockCreateView.as_view(), name="stock-create"),
    path(
        "stock/update/<slug:slug>/",
        views.StockUpdateView.as_view(),
        name="stock-update",
    ),
    path(
        "stock/delete/<slug:slug>/",
        views.StockDeleteView.as_view(),
        name="stock-delete",
    ),
    # Batch
    path("batch/list/", views.BatchListView.as_view(), name="batch-list"),
    path(
        "batch/detail/<slug:slug>/",
        views.BatchDetailView.as_view(),
        name="batch-detail",
    ),
    path("batch/create/", views.BatchCreateView.as_view(), name="batch-create"),
    path(
        "batch/update/<slug:slug>", views.BatchUpdateView.as_view(), name="batch-update"
    ),
    path(
        "batch/delete/<slug:slug>", views.BatchDeleteView.as_view(), name="batch-delete"
    ),
    # BatchItem
    path("batch-item/list/", views.BatchItemListView.as_view(), name="batch-item-list"),
    path(
        "batch-item/detail/<slug:slug>/",
        views.BatchItemDetailView.as_view(),
        name="batch-item-detail",
    ),
    path(
        "batch-item/create/",
        views.BatchItemCreateView.as_view(),
        name="batch-item-create",
    ),
    path(
        "batch-item/update/<slug:slug>",
        views.BatchItemUpdateView.as_view(),
        name="batch-item-update",
    ),
    path(
        "batch-item/delete/<slug:slug>",
        views.BatchItemDeleteView.as_view(),
        name="batch-item-delete",
    ),
    # Balance
    path("balance/list/", views.BalanceListView.as_view(), name="balance-list"),
    path(
        "balance/detail/<slug:slug>/",
        views.BalanceDetailView.as_view(),
        name="balance-detail",
    ),
    # Order
    path("order/list/", views.OrderListView.as_view(), name="order-list"),
    path(
        "order/detail/<slug:slug>", views.OrderDetailView.as_view(), name="order-detail"
    ),
    path("order/create/", views.OrderCreateView.as_view(), name="order-create"),
    path(
        "order/update/<slug:slug>", views.OrderUpdateView.as_view(), name="order-update"
    ),
    path(
        "order/delete/<slug:slug>", views.OrderDeleteView.as_view(), name="order-delete"
    ),
]
