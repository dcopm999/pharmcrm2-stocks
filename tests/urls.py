# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Goods API",
        default_version="v1",
        description="PharmCRM2: Goods management",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="dcopm999@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("stocks.urls", namespace="stocks")),
    path("api/", include("stocks.api.urls", namespace="stocks-api")),
    url(
        "^swagger(?P<format>\.json|\.yaml)$",  # noqa
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-selfwagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
