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
]
