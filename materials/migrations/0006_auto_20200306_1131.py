# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-03-06 02:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_auto_20200306_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beam',
            name='Receivingdate',
            field=models.CharField(default=datetime.datetime(2020, 3, 6, 11, 31, 54, 874557), max_length=16),
        ),
        migrations.AlterField(
            model_name='yarn',
            name='Receivingdate',
            field=models.CharField(default=datetime.datetime(2020, 3, 6, 11, 31, 54, 874557), max_length=16),
        ),
    ]
