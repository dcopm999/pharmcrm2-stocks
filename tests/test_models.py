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


class StockCase(TestCase):
    def setUp(self):
        self.item = factories.StockFactory()

    def test_save_slug(self):
        self.assertEqual(self.item.slug, slugify(self.item.name))

    def test_str(self):
        self.assertEqual(str(self.item), self.item.name)

    def test_get_absolute_url(self):
        self.item.refresh_from_db()
        expected_url = reverse("stocks:stock-detail", args=[str(self.item.slug)])
        self.assertEqual(self.item.get_absolute_url(), expected_url)


class BatchCase(TestCase):
    def setUp(self):
        self.item = factories.BatchFactory()

    def test_save_slug(self):
        self.assertEqual(self.item.slug, slugify(self.item.number))

    def test_str(self):
        self.assertEqual(str(self.item), self.item.number)

    def test_get_absolute_url(self):
        expected_url = reverse("stocks:batch-detail", args=[str(self.item.slug)])
        self.assertEqual(self.item.get_absolute_url(), expected_url)


class BatchItemCase(TestCase):
    def setUp(self):
        self.item = factories.BatchItemFactory()

    def test_str(self):
        self.assertEqual(str(self.item), f"{self.item.good}({self.item.serial})")

    def test_save_slug(self):
        expected_slug = slugify(str(self.item))
        self.assertEqual(self.item.slug, expected_slug)

    def test_order_update(self):
        # Создаем связанный Order для теста order_update
        order = models.Order.objects.get(
            incoming=self.item.batch.stock, batch_item_id=self.item.id
        )
        updated_quantity_original = 100
        updated_quantity_item = 50

        # Изменяем поля BatchItem
        self.item.quantity_original = updated_quantity_original
        self.item.quantity_item = updated_quantity_item

        # Вызываем метод обновления заказа
        self.item.order_update()

        # Обновляем order из базы
        order.refresh_from_db()

        # Проверяем, что поля обновились
        self.assertEqual(order.quantity_original, 100)
        self.assertEqual(order.quantity_item, 50)

    def test_get_absolute_url(self):
        expected_url = reverse("stocks:batch-item-detail", args=[str(self.item.slug)])
        self.assertEqual(self.item.get_absolute_url(), expected_url)


class BalanceCase(TestCase):
    def setUp(self):
        self.item = factories.BalanceFactory()

    def test_price_sum_original(self):
        self.assertEqual(
            self.item.price_sum_original(),
            self.item.quantity_original * self.item.batch_item.price_original,
        )

    def test_price_sum_item(self):
        self.assertEqual(
            self.item.price_sum_item(),
            self.item.quantity_item * self.item.batch_item.price_item,
        )

    def test_price_sum(self):
        self.assertEqual(
            self.item.price_sum(),
            self.item.price_sum_original() + self.item.price_sum_item(),
        )

    def test_str(self):
        self.assertEqual(
            str(self.item), f"{self.item.stock.name}({self.item.batch_item})"
        )

    def test_get_absolute_url(self):
        expected_url = reverse("stocks:balance-detail", args=[str(self.item.slug)])
        self.assertEqual(self.item.get_absolute_url(), expected_url)
