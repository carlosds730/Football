# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-16 04:11
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('stats', '0007_auto_20160515_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerPerformance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fixture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performances',
                                              to='stats.Fixture', verbose_name='Jornada')),
            ],
            options={
                'verbose_name': 'Desempeño',
                'verbose_name_plural': 'Desempeños',
            },
        ),
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['name'], 'verbose_name': 'Jugador', 'verbose_name_plural': 'Jugadores'},
        ),
        migrations.RemoveField(
            model_name='player',
            name='assists',
        ),
        migrations.RemoveField(
            model_name='player',
            name='draws',
        ),
        migrations.RemoveField(
            model_name='player',
            name='elo',
        ),
        migrations.RemoveField(
            model_name='player',
            name='games_played',
        ),
        migrations.RemoveField(
            model_name='player',
            name='goals',
        ),
        migrations.RemoveField(
            model_name='player',
            name='losses',
        ),
        migrations.RemoveField(
            model_name='player',
            name='wins',
        ),
        migrations.RemoveField(
            model_name='stats',
            name='fixture',
        ),
        migrations.RemoveField(
            model_name='stats',
            name='player',
        ),
        migrations.AddField(
            model_name='player',
            name='global_stats',
            field=models.OneToOneField(default=None,
                                       help_text='Estadísticas totales del jugador. Incluye todas las temporadas',
                                       on_delete=django.db.models.deletion.CASCADE, to='stats.Stats',
                                       verbose_name='Estadísticas globales'),
        ),
        migrations.AddField(
            model_name='playerperformance',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performances',
                                    to='stats.Player', verbose_name='Jugaodr'),
        ),
        migrations.AddField(
            model_name='playerperformance',
            name='stat',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stats.Stats',
                                       verbose_name='Estadística'),
        ),
        migrations.AlterUniqueTogether(
            name='playerperformance',
            unique_together=set([('player', 'fixture')]),
        ),
    ]
