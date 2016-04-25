# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-25 20:04
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields
import stats.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=stats.models.get_next_fixture_date, help_text='Fecha de la jornada',
                                          unique=True, verbose_name='Fecha')),
                ('image',
                 sorl.thumbnail.fields.ImageField(blank=True, help_text='Foto de la jornada', upload_to='Jornadas',
                                                  verbose_name='Foto')),
                ('number',
                 models.PositiveSmallIntegerField(default=stats.models.get_next_fixture, verbose_name='Jornada')),
            ],
            options={
                'verbose_name_plural': 'Jornadas',
                'verbose_name': 'Jornada',
                'ordering': ['-number'],
            },
        ),
        migrations.CreateModel(
            name='MainPictures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', sorl.thumbnail.fields.ImageField(upload_to='Main', verbose_name='Picture')),
            ],
            options={
                'verbose_name_plural': 'Fotos Portada',
                'verbose_name': 'Foto Portada',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name',
                 models.CharField(help_text='Nombre del jugador', max_length=200, unique=True, verbose_name='Nombre')),
                ('image',
                 sorl.thumbnail.fields.ImageField(blank=True, help_text='Foto del jugador', upload_to='Avatars',
                                                  verbose_name='Avatar')),
                ('games_played', models.PositiveSmallIntegerField(default=0, verbose_name='Juegos jugados')),
                ('wins', models.PositiveSmallIntegerField(default=0, verbose_name='Juegos ganados')),
                ('draws', models.PositiveSmallIntegerField(default=0, verbose_name='Juegos empatados')),
                ('losses', models.PositiveSmallIntegerField(default=0, verbose_name='Juegos perdidos')),
                ('goals', models.PositiveSmallIntegerField(default=0, verbose_name='Goles anotados')),
                ('assists', models.PositiveSmallIntegerField(default=0, verbose_name='Asistencias')),
                ('elo', models.DecimalField(decimal_places=5, default=0, max_digits=7, verbose_name='ELO')),
            ],
            options={
                'verbose_name_plural': 'Jugadores',
                'verbose_name': 'Jugador',
                'ordering': ['-elo'],
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Numero')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
            ],
            options={
                'verbose_name_plural': 'Temporadas',
                'verbose_name': 'Temporada',
                'ordering': ['-number'],
            },
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games_played', models.PositiveSmallIntegerField(default=0, verbose_name='Juegos jugados')),
                ('wins', models.PositiveSmallIntegerField(default=0, verbose_name='Juegos ganados')),
                ('draws', models.PositiveSmallIntegerField(default=0, verbose_name='Juegos empatados')),
                ('losses', models.PositiveSmallIntegerField(default=0, verbose_name='Juegos perdidos')),
                ('goals', models.PositiveSmallIntegerField(default=0, verbose_name='Goles anotados')),
                ('assists', models.PositiveSmallIntegerField(default=0, verbose_name='Asistencias')),
                ('elo', models.DecimalField(decimal_places=5, default=0, max_digits=7, verbose_name='ELO')),
                ('fixture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats',
                                              to='stats.Fixture', verbose_name='Jornada')),
                ('player',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='stats.Player',
                                   verbose_name='Jugador')),
            ],
            options={
                'verbose_name_plural': 'Actuaciones',
                'verbose_name': 'Actuación',
                'ordering': ['-elo'],
            },
        ),
        migrations.AddField(
            model_name='fixture',
            name='season',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fixtures',
                                    to='stats.Season', verbose_name='Temporada'),
        ),
    ]
