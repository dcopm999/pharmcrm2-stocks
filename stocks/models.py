# -*- coding: utf-8 -*-
import reversion
from django.db import models, transaction
from django.urls import reverse
from django.utils.translation import gettext as _
from mptt.models import MPTTModel, TreeForeignKey
from slugify import slugify


@reversion.register()
class Stock(MPTTModel):
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    slug = models.SlugField(
        max_length=250, blank=True, editable=False, verbose_name=_("slug")
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name=_("children"),
    )
    created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name=_("Created")
    )
    updated = models.DateTimeField(
        auto_now=True, editable=False, verbose_name=_("Updated")
    )

    class Meta:
        verbose_name = _("Stock")
        verbose_name_plural = _("Stocks")

    def get_absolute_url(self):
        return reverse("stocks:stock-detail", args=[str(self.slug)])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


@reversion.register()
class Batch(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, verbose_name=_("Stock"))
    number = models.CharField(max_length=250, verbose_name=_("Batch number"))
    slug = models.SlugField(
        max_length=250, blank=True, editable=False, verbose_name=_("slug")
    )
    created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name=_("Created")
    )
    updated = models.DateTimeField(
        auto_now=True, editable=False, verbose_name=_("Updated")
    )

    def get_absolute_url(self):
        return reverse("stocks:batch-detail", args=[str(self.slug)])

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        self.slug = slugify(self.number)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Batch")
        verbose_name_plural = _("Batches")


@reversion.register()
class BatchItem(models.Model):
    good = models.ForeignKey(
        "goods.Good", on_delete=models.CASCADE, verbose_name=_("Good")
    )
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, verbose_name=_("Batch"))
    serial = models.CharField(max_length=250, verbose_name=_("Serial number"))
    quantity_original = models.PositiveIntegerField(verbose_name=_("Quantity original"))
    price_original = models.DecimalField(
        max_digits=20, decimal_places=2, verbose_name=_("Original price")
    )
    quantity_item = models.PositiveIntegerField(
        default=0, verbose_name=_("Quantity item")
    )
    price_item = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_("Item price")
    )
    production_date = models.DateField(verbose_name=_("Production date"))
    expiration_date = models.DateField(verbose_name=_("Expiration date"))
    slug = models.SlugField(
        max_length=250, blank=True, editable=False, verbose_name=_("slug")
    )
    created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name=_("Created")
    )
    updated = models.DateTimeField(
        auto_now=True, editable=False, verbose_name=_("Updated")
    )

    def __str__(self):
        return f"{self.good}({self.serial})"

    def get_absolute_url(self):
        return reverse("stocks:batch-detail", args=[str(self.slug)])

    def order_create(self):
        order = Order(
            incoming=self.batch.stock,
            batch_item_id=self.id,
            quantity_original=self.quantity_original,
            quantity_item=self.quantity_item,
        )
        order.save()

    def order_update(self):
        order = Order.objects.get(incoming=self.batch.stock, batch_item_id=self.id)
        order.quantity_original = self.quantity_original
        order.quantity_item = self.quantity_item
        order.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())
        super().save(*args, **kwargs)
        if Order.objects.filter(
            incoming=self.batch.stock, batch_item_id=self.id
        ).exists():
            self.order_update()
        else:
            self.order_create()

    class Meta:
        verbose_name = _("Batch item")
        verbose_name_plural = _("Batch items")


@reversion.register()
class Balance(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name=_("Stock"))
    batch_item = models.ForeignKey(
        BatchItem,
        on_delete=models.PROTECT,
        verbose_name=_("Batch items"),
    )
    quantity_original = models.PositiveIntegerField(
        default=0, editable=False, verbose_name=_("Quantity original")
    )
    quantity_item = models.PositiveIntegerField(
        default=0, editable=False, verbose_name=_("Quantity item")
    )
    created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name=_("Created")
    )
    updated = models.DateTimeField(
        auto_now=True, editable=False, verbose_name=_("Updated")
    )

    def price_sum_original(self):
        return self.quantity_original * self.batch_item.price_original

    def price_sum_item(self):
        return self.quantity_item * self.batch_item.price_item

    def price_sum(self):
        return self.price_sum_original() + self.price_sum_item()

    def __str__(self):
        return f"{self.stock.name}({self.batch_item})"

    class Meta:
        unique_together = ("stock", "batch_item")
        verbose_name = _("Balance")
        verbose_name_plural = _("Balances")


@reversion.register()
class Order(models.Model):
    incoming = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name="incoming_stock",
        verbose_name=_("Incoming"),
    )
    outgoing = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="outgoing_stock",
        verbose_name=_("Outgoing"),
    )
    batch_item = models.ForeignKey(
        BatchItem,
        on_delete=models.CASCADE,
        related_name="batch_item",
        verbose_name=_("Batch item"),
    )
    quantity_original = models.PositiveIntegerField(
        default=0, verbose_name=_("Quantity original")
    )
    quantity_item = models.PositiveIntegerField(
        default=0, verbose_name=_("Quantity item")
    )
    balance = models.ForeignKey(
        Balance,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Balance"),
    )
    is_approved = models.BooleanField(
        default=False, editable=False, verbose_name=_("Is approved")
    )
    is_done = models.BooleanField(
        default=False, editable=False, verbose_name=_("Is done")
    )
    slug = models.SlugField(
        max_length=250, blank=True, editable=False, verbose_name=_("slug")
    )
    created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name=_("Created")
    )
    updated = models.DateTimeField(
        auto_now=True, editable=False, verbose_name=_("Updated")
    )

    def get_absolute_url(self):
        return reverse("stocks:order-detail", args=[str(self.slug)])

    def __str__(self):
        return f"{self.batch_item}({self.outgoing}->{self.incoming})"

    def balance_incoming(self):
        if not self.is_done:
            try:
                self.balance = Balance.objects.get(
                    stock_id=self.incoming_id, batch_item_id=self.batch_item_id
                )
                self.balance.stock = self.incoming
                self.balance.batch_item_id = self.batch_item_id
                self.balance.quantity_original += self.quantity_original
                self.balance.quantity_item += self.quantity_item
                self.balance.save()
            except Balance.DoesNotExist:
                self.balance = Balance(
                    stock_id=self.incoming_id,
                    batch_item_id=self.batch_item_id,
                    quantity_original=self.quantity_original,
                    quantity_item=self.quantity_item,
                )
                self.balance.save()

    def balance_outgoing(self):
        if self.outgoing is not None and not self.is_done:
            try:
                outgoung_balance = self.outgoing.balance_set.get(
                    batch_item_id=self.batch_item_id
                )
                outgoung_balance.quantity_original -= self.quantity_original
                outgoung_balance.quantity_item -= self.quantity_item
                outgoung_balance.save()
            except Balance.DoesNotExist:
                pass

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())
        if self.is_approved:
            self.balance_outgoing()
            self.balance_incoming()
            self.is_done = True
        super().save(*args, **kwargs)
