#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pharmcrm2-stocks
------------

Tests for `pharmcrm2-stocks` models module.
"""

from django.test import TestCase
from django.urls import reverse
from slugify import slugify

from stocks import models
from tests import factories


class ModelsCase(TestCase):
    def setUp(self):
        pass

    def test_something(self):
        pass

    def tearDown(self):
        pass


class BatchItemCase(TestCase):
    def setUp(self):
        self.item = factories.StockFactory()

    def test_save_slug(self):
        self.assertEqual(self.item.slug, slugify(self.item.name))

    def test_str(self):
        query = models.Stock.objects.last()
        self.assertEqual(query.__str__(), query.name)

    def test_get_absolute_url(self):
        query = models.Stock.objects.last()
        self.assertEqual(
            query.get_absolute_url(),
            reverse("stocks:stock-detail", args=[str(query.slug)]),
        )


"""
class BatchItemCase(TestCase):
    def setUp(self):
        query = factories.BatchItemFactory()
"""
