# -*- coding: utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StocksConfig(AppConfig):
    name = "stocks"
    verbose_name = _("stocks")
