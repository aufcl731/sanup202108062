# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2020-12-01 07:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Style_fabric',
            fields=[
                ('fabric_code', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('fabric_name', models.CharField(max_length=500)),
                ('fabric_color', models.CharField(max_length=150)),
                ('fabric_size', models.CharField(max_length=200)),
                ('fabric_part', models.CharField(max_length=250)),
                ('fabric_Construction', models.CharField(max_length=600)),
                ('fabric_width', models.FloatField()),
                ('cuttable_width', models.FloatField()),
                ('sMeter_width', models.FloatField()),
                ('yard_weight', models.FloatField()),
                ('unit', models.CharField(max_length=200)),
                ('fabric_Csm', models.FloatField()),
                ('fabric_Mrp', models.FloatField()),
                ('dyeProcessTypeCode', models.CharField(max_length=100)),
                ('dyeProcessTypeName', models.CharField(max_length=100)),
                ('dyeCompanyName', models.CharField(max_length=100)),
                ('knitCompanyName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Style_order',
            fields=[
                ('style_key', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('factory_code', models.CharField(max_length=100)),
                ('style_ver', models.CharField(max_length=100)),
                ('design_ck', models.BooleanField(default=False)),
                ('fabric_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Style_fabric')),
            ],
        ),
        migrations.CreateModel(
            name='Style_yarn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('st_yarn_code', models.CharField(max_length=200)),
                ('st_yarn_name', models.CharField(max_length=200)),
                ('st_yarn_color', models.CharField(max_length=100)),
                ('st_yarn_rate', models.FloatField()),
                ('st_yarn_cnt', models.FloatField()),
                ('yn_Dye', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='style_fabric',
            name='yarn',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='order.Style_yarn'),
        ),
    ]
