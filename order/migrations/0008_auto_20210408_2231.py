# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2021-04-08 13:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20210408_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='buyer',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='company',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
