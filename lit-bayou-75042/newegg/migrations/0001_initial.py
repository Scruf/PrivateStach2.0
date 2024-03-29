# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-20 23:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import newegg.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]



    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('user', models.OneToOneField(db_column='auth_user_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', models.CharField(default=False, max_length=12)),
                ('client_id', models.IntegerField(db_column='id', default=0)),
                ('seller_id', models.CharField(db_column='newegg_seller_id', default=False, max_length=200)),
                ('authorization', models.CharField(db_column='newegg_authorization', default=False, max_length=200)),
                ('referral_code', models.CharField(db_column='referral_code', default=None, max_length=200)),
                ('newegg_secretkey', models.CharField(db_column='newegg_secretkey', default=None, max_length=200)),
                ('commitment_time_hours', models.IntegerField(db_column='commitment_time_hours', default=None)),
            ],
            options={
                'db_table': 'app_client',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('document', models.FileField(upload_to=newegg.models.file_handler)),
                ('upload_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newegg.Client')),
            ],
            options={
                'db_table': 'app_document',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_number', models.CharField(max_length=100)),
                ('newegg_item_number', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=500)),
                ('country', models.CharField(max_length=10)),
                ('currency', models.CharField(max_length=10)),
                ('msrp', models.DecimalField(decimal_places=2, max_digits=100)),
                ('quantity', models.IntegerField()),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=100)),
                ('is_active', models.BooleanField(default=False)),
                ('in_stock', models.BooleanField(default=True)),
                ('fullfilment_option', models.CharField(max_length=100)),
                ('shipment', models.CharField(max_length=100)),
                ('price_min', models.DecimalField(decimal_places=2, default=0.0, max_digits=18)),
                ('price_max', models.DecimalField(decimal_places=2, default=0.0, max_digits=18)),
                ('dateadded', models.DateTimeField(auto_now_add=True, db_column='dateadded')),
                ('dateupdated', models.DateTimeField(auto_now_add=True, db_column='dateupdated')),
                ('dateexpired', models.DateTimeField(db_column='dateexpired', default='5003-01-01 00:00')),
            ],
            options={
                'db_table': 'app_product',
            },
        ),
    ]
