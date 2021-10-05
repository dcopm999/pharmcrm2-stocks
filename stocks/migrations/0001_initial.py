# Generated by Django 3.2.8 on 2021-10-05 09:03

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_original', models.PositiveIntegerField(default=0, editable=False, verbose_name='Quantity original')),
                ('quantity_item', models.PositiveIntegerField(default=0, editable=False, verbose_name='Quantity item')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Balance',
                'verbose_name_plural': 'Balances',
            },
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=250, verbose_name='Batch number')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=250, verbose_name='slug')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Product batch',
                'verbose_name_plural': 'Product batchs',
            },
        ),
        migrations.CreateModel(
            name='BatchPharmItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=250, verbose_name='Serial number')),
                ('quantity_original', models.PositiveIntegerField(verbose_name='Quantity original')),
                ('price_original', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Original price')),
                ('quantity_item', models.PositiveIntegerField(default=0, verbose_name='Quantity item')),
                ('price_item', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Item price')),
                ('production_date', models.DateField(verbose_name='Production date')),
                ('expiration_date', models.DateField(verbose_name='Expiration date')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=250, verbose_name='slug')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.batch', verbose_name='Batch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.pharmproduct', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Pharmaceutical batch item',
                'verbose_name_plural': 'Pharmaceutical batch items',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=250, verbose_name='slug')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='stocks.stock')),
            ],
            options={
                'verbose_name': 'Stock',
                'verbose_name_plural': 'Stocks',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_original', models.PositiveIntegerField(default=0, verbose_name='Quantity original')),
                ('quantity_item', models.PositiveIntegerField(default=0, verbose_name='Quantity item')),
                ('is_approved', models.BooleanField(default=False, editable=False, verbose_name='Is approved')),
                ('is_done', models.BooleanField(default=False, editable=False, verbose_name='Is done')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=250, verbose_name='slug')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('balance', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='stocks.balance', verbose_name='Balance')),
                ('incoming', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_stock', to='stocks.stock', verbose_name='Incoming')),
                ('outgoing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_stock', to='stocks.stock', verbose_name='Outgoing')),
                ('pharm_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pharm_item', to='stocks.batchpharmitem', verbose_name='Pharm item')),
            ],
        ),
        migrations.AddField(
            model_name='batch',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.stock', verbose_name='Stock'),
        ),
        migrations.AddField(
            model_name='balance',
            name='pharm_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.batchpharmitem', verbose_name='Pharmaceutical batch items'),
        ),
        migrations.AddField(
            model_name='balance',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.stock', verbose_name='Stock'),
        ),
        migrations.AlterUniqueTogether(
            name='balance',
            unique_together={('stock', 'pharm_item')},
        ),
    ]
