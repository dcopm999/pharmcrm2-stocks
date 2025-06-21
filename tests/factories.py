import factory
from factory.django import DjangoModelFactory
from goods import factories as good_factories

from stocks import models

factory.Faker._DEFAULT_LOCALE = "ru_RU"


class StockFactory(DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = models.Stock


class BatchFactory(DjangoModelFactory):
    stock = factory.SubFactory(StockFactory)
    number = factory.Faker("ssn")

    class Meta:
        model = models.Batch


class BatchItemFactory(DjangoModelFactory):
    good = factory.SubFactory(good_factories.GoodFactory)
    batch = factory.SubFactory(BatchFactory)
    serial = factory.Faker("ssn")
    quantity_original = factory.Faker("random_digit_not_null")
    price_original = factory.Faker("random_digit_not_null")
    production_date = factory.Faker("date")
    expiration_date = factory.Faker("date")

    class Meta:
        model = models.BatchItem


class BalanceFactory(DjangoModelFactory):
    stock = factory.SubFactory(StockFactory)
    batch_item = factory.SubFactory(BatchItemFactory)
    quantity_original = factory.Faker("random_digit_not_null")
    quantity_item = factory.Faker("random_digit_not_null")

    class Meta:
        model = models.Balance


class OrderFactory(DjangoModelFactory):
    incoming = factory.SubFactory(StockFactory)
    outgoing = factory.SubFactory(StockFactory)
    batch_item = factory.SubFactory(BatchItemFactory)
    quantity_original = factory.Faker("random_digit_not_null")
    quantity_item = factory.Faker("random_digit_not_null")

    class Meta:
        model = models.Order
