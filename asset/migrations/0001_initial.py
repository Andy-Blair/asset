# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-01-22 14:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CategoryName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DiscardAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Discard_time', models.DateTimeField(auto_now_add=True)),
                ('DiscardReason', models.TextField()),
                ('Dispose_time', models.DateTimeField(null=True)),
                ('Dispose_Remark', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DiscardStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StatusName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Department', models.CharField(max_length=50, null=True)),
                ('UserName', models.CharField(max_length=50, null=True)),
                ('AssetBrand', models.CharField(max_length=50)),
                ('AssetType', models.CharField(max_length=50)),
                ('SerialNumber', models.CharField(max_length=100)),
                ('Buy_Time', models.DateField()),
                ('Buy_Channel', models.CharField(max_length=50)),
                ('Buy_Price', models.CharField(max_length=50)),
                ('Buyer', models.CharField(max_length=50)),
                ('Place', models.TextField(null=True)),
                ('Remark', models.TextField(null=True)),
                ('Discard', models.IntegerField(default=0)),
                ('AssetCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.AssetCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('action', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsageStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StatusName', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='information',
            name='UsageStatus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.UsageStatus'),
        ),
        migrations.AddField(
            model_name='discardasset',
            name='DiscardAssetID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.Information'),
        ),
        migrations.AddField(
            model_name='discardasset',
            name='Dispose_Status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.DiscardStatus'),
        ),
    ]
