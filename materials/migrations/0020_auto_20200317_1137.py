# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-03-17 02:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0019_auto_20200317_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beam',
            name='Receivingdate',
            field=models.CharField(default='2020-03-17 11:37', max_length=30),
        ),
        migrations.AlterField(
            model_name='yarn',
            name='Receivingdate',
            field=models.CharField(default='2020-03-17 11:37', max_length=30),
        ),
    ]
