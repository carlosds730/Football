# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-16 02:11
from __future__ import unicode_literals
from django.db import migrations, models
import stats.models


class Migration(migrations.Migration):
    dependencies = [
        ('stats', '0006_auto_20160423_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='number',
            field=models.PositiveSmallIntegerField(default=stats.models.get_next_fixture, verbose_name='Jornada'),
        ),
    ]
