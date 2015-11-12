# -*- coding: utf8 -*-
from django.db import models
from sorl.thumbnail import ImageField
from django.core.exceptions import ValidationError


# Create your models here.

class Player(models.Model):
    class Meta:
        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"
        ordering = ['name']

    name = models.CharField(verbose_name="Nombre", help_text="Nombre del jugador", max_length=200, unique=True)

    image = ImageField(verbose_name="Avatar", upload_to='Avatars', help_text="Foto del jugador")


class Fixture(models.Model):
    class Meta:
        verbose_name = "Jornada"
        verbose_name_plural = "Jornadas"
        ordering = ['date']

    date = models.DateField(verbose_name="Fecha", help_text="Fecha de la jornada", unique=True)


class Stats(models.Model):
    class Meta:
        verbose_name = "Actuación"

    # Related fields
    player = models.ForeignKey('Player', verbose_name="Jugador", related_name="stats")

    fixture = models.ForeignKey('Fixture', verbose_name="Jornada", related_name="stats")

    # Numeric fields
    games_played = models.PositiveSmallIntegerField(verbose_name="Juegos jugados")

    wins = models.PositiveSmallIntegerField(verbose_name="Juegos ganados")

    losts = models.PositiveSmallIntegerField(verbose_name="Juegos empatados")

    draws = models.PositiveSmallIntegerField(verbose_name="Juegos perdidos")

    goals = models.PositiveSmallIntegerField(verbose_name="Goles anotados")

    assists = models.PositiveSmallIntegerField(verbose_name="Asistencias")

    elo = models.DecimalField(verbose_name="ELO", max_digits=5, decimal_places=7)
