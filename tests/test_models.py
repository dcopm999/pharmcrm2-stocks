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


class OrderCase(TestCase):
    def setUp(self):
        self.item = factories.OrderFactory()

    def test_get_absolute_url(self):
        expected_url = reverse("stocks:order-detail", args=[str(self.item.slug)])
        self.assertEqual(self.item.get_absolute_url(), expected_url)

    def test_balance_incoming_existing_balance(self):
        # Создаём существующий баланс с начальными значениями
        balance = models.Balance.objects.create(
            stock_id=self.item.incoming_id,
            batch_item_id=self.item.batch_item_id,
            quantity_original=10,
            quantity_item=5,
        )
        self.item.balance = balance
        self.item.is_done = False
        self.item.quantity_original = 3
        self.item.quantity_item = 2
        self.item.save()

        self.item.balance_incoming()

        balance.refresh_from_db()
        self.assertEqual(balance.quantity_original, 13)  # 10 + 3
        self.assertEqual(balance.quantity_item, 7)  # 5 + 2
        self.assertEqual(self.item.balance, balance)

    def test_balance_incoming_create_balance(self):
        # Удаляем все балансы, чтобы быть уверенными, что их нет
        models.Balance.objects.filter(
            stock_id=self.item.incoming_id, batch_item_id=self.item.batch_item_id
        ).delete()

        self.item.balance = None
        self.item.is_done = False
        self.item.quantity_original = 4
        self.item.quantity_item = 6
        self.item.save()

        self.item.balance_incoming()

        balance = models.Balance.objects.get(
            stock_id=self.item.incoming_id, batch_item_id=self.item.batch_item_id
        )
        self.assertEqual(balance.quantity_original, 4)
        self.assertEqual(balance.quantity_item, 6)
        self.assertEqual(self.item.balance, balance)

    def test_balance_incoming_no_action_if_done(self):
        # Создаём баланс с начальными значениями
        balance = models.Balance.objects.create(
            stock_id=self.item.incoming_id,
            batch_item_id=self.item.batch_item_id,
            quantity_original=10,
            quantity_item=10,
        )
        self.item.balance = balance
        self.item.is_done = True  # Заказ уже выполнен
        self.item.quantity_original = 5
        self.item.quantity_item = 5
        self.item.save()

        self.item.balance_incoming()

        balance.refresh_from_db()
        # Баланс не должен измениться
        self.assertEqual(balance.quantity_original, 10)
        self.assertEqual(balance.quantity_item, 10)

    def test_balance_outgoing_no_balance_found(self):
        # Удаляем все балансы исходящего склада, чтобы вызвать исключение
        models.Balance.objects.filter(
            stock=self.item.outgoing, batch_item=self.item.batch_item
        ).delete()

        self.item.is_done = False
        self.item.quantity_original = 5
        self.item.quantity_item = 3
        self.item.save()

        # Метод должен отработать без ошибки, несмотря на отсутствие баланса
        try:
            self.item.balance_outgoing()
        except models.Balance.DoesNotExist:
            self.fail("balance_outgoing() raised Balance.DoesNotExist unexpectedly!")

    def test_save_generates_slug_and_updates_balances(self):
        # Подготовка: создаём исходящий баланс для проверки уменьшения
        outgoing_balance = models.Balance.objects.create(
            stock=self.item.outgoing,
            batch_item=self.item.batch_item,
            quantity_original=20,
            quantity_item=10,
        )

        # Устанавливаем параметры для утверждённого заказа
        self.item.is_approved = True
        self.item.is_done = False
        self.item.quantity_original = 5
        self.item.quantity_item = 3
        self.item.slug = ""  # Очистим slug, чтобы проверить генерацию
        self.item.save()

        # Проверяем, что slug сгенерирован
        expected_slug = slugify(str(self.item))
        self.assertEqual(self.item.slug, expected_slug)

        # Проверяем, что is_done установлен в True
        self.assertTrue(self.item.is_done)

        # Проверяем, что исходящий баланс уменьшился
        outgoing_balance.refresh_from_db()
        self.assertEqual(outgoing_balance.quantity_original, 15)  # 20 - 5
        self.assertEqual(outgoing_balance.quantity_item, 7)  # 10 - 3

        # Проверяем, что incoming баланс создался и увеличился
        incoming_balance = models.Balance.objects.get(
            stock=self.item.incoming, batch_item=self.item.batch_item
        )
        self.assertEqual(incoming_balance.quantity_original, 5)
        self.assertEqual(incoming_balance.quantity_item, 3)

        # Проверяем, что баланс заказа связан с incoming балансом
        self.assertEqual(self.item.balance, incoming_balance)

    def test_save_does_not_update_balances_if_not_approved(self):
        self.item.is_approved = False
        self.item.is_done = False
        self.item.quantity_original = 5
        self.item.quantity_item = 3
        self.item.slug = ""
        self.item.save()

        # is_done должен остаться False
        self.assertFalse(self.item.is_done)

        # Балансы не должны измениться (их может не быть, но проверим отсутствие ошибок)
        self.assertFalse(
            models.Balance.objects.filter(
                stock=self.item.incoming, batch_item=self.item.batch_item
            ).exists()
        )
