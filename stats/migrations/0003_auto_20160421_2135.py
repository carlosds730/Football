# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-22 01:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_auto_20160420_2157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Numero')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Temporada',
                'verbose_name_plural': 'Temporadas',
                'ordering': ['-number'],
            },
        ),
        migrations.AddField(
            model_name='fixture',
            name='season',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fixtures', to='stats.Season', verbose_name='Temporada'),
        ),
    ]
