# -*- coding: utf8 -*-
from django.db import models
from sorl.thumbnail import ImageField
from decimal import *
from stats.extra_functions import validate_fixture
from django.core.exceptions import ValidationError

from django.db.models import Sum
import datetime

from stats.extra_functions import calculate_elo_simple


# Create your models here.

class Player(models.Model):
    class Meta:
        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"
        ordering = ['name']

    name = models.CharField(verbose_name="Nombre", help_text="Nombre del jugador", max_length=200, unique=True)

    image = ImageField(verbose_name="Avatar", upload_to='Avatars', help_text="Foto del jugador", blank=True)

    # Numeric fields

    games_played = models.PositiveSmallIntegerField(verbose_name="Juegos jugados", default=0)

    wins = models.PositiveSmallIntegerField(verbose_name="Juegos ganados", default=0)

    draws = models.PositiveSmallIntegerField(verbose_name="Juegos empatados")

    losses = models.PositiveSmallIntegerField(verbose_name="Juegos perdidos")

    goals = models.PositiveSmallIntegerField(verbose_name="Goles anotados", default=0)

    assists = models.PositiveSmallIntegerField(verbose_name="Asistencias", default=0)

    elo = models.DecimalField(verbose_name="ELO", max_digits=7, decimal_places=5, default=0)

    def save(self, *args, **kwargs):
        self.elo = self.calculate_elo()
        super(Player, self).save(*args, **kwargs)

    def calculate_elo(self):
        return calculate_elo_simple(self.games_played, self.wins, self.losses, self.draws, self.goals, self.assists)

    def calculate_player_stats(self):
        data = Stats.objects.filter(player=self).aggregate(Sum('games_played'), Sum('wins'), Sum('losses'),
                                                           Sum('draws'), Sum('goals'), Sum('assists'))


class Fixture(models.Model):
    class Meta:
        verbose_name = "Jornada"
        verbose_name_plural = "Jornadas"
        ordering = ['-date']

    date = models.DateField(verbose_name="Fecha", help_text="Fecha de la jornada", unique=True,
                            default=lambda: Fixture.get_next_fixture_date())

    image = ImageField(verbose_name="Foto", upload_to='Jornadas', help_text="Foto de la jornada", blank=True)

    numero = models.PositiveSmallIntegerField(verbose_name="Jornada número", default=lambda: Fixture.get_next_fixture())

    def __str__(self):
        return "Jornada " + str(self.numero)

    @classmethod
    def get_next_fixture(cls):
        """
        Get the number of the next Fixture
        """

        next_fixture = cls.objects.aggregate(
            models.Max('numero')
        )['numero__max']

        if next_fixture:
            return next_fixture + 1
        else:
            return 1

    @classmethod
    def get_next_fixture_date(cls):
        """
        Get the date of the next Fixture
        """
        a = cls.objects.first()
        if a:
            return a.date + datetime.timedelta(7)
        else:
            return datetime.date(2015, 6, 14)


class Stats(models.Model):
    class Meta:
        verbose_name = "Actuación"
        verbose_name_plural = "Actuaciones"

    # Related fields
    player = models.ForeignKey('Player', verbose_name="Jugador", related_name="stats")

    fixture = models.ForeignKey('Fixture', verbose_name="Jornada", related_name="stats")

    # Numeric fields
    games_played = models.PositiveSmallIntegerField(verbose_name="Juegos jugados")

    wins = models.PositiveSmallIntegerField(verbose_name="Juegos ganados")

    draws = models.PositiveSmallIntegerField(verbose_name="Juegos empatados")

    losses = models.PositiveSmallIntegerField(verbose_name="Juegos perdidos")

    goals = models.PositiveSmallIntegerField(verbose_name="Goles anotados")

    assists = models.PositiveSmallIntegerField(verbose_name="Asistencias")

    elo = models.DecimalField(verbose_name="ELO", max_digits=7, decimal_places=5, default=0)

    def save(self, *args, **kwargs):
        validate_fixture(self.games_played, self.wins, self.losses, self.draws)
        self.elo = self.calculate_elo()
        super(Stats, self).save(*args, **kwargs)
        self.update_player()

    def calculate_elo(self):
        return calculate_elo_simple(self.games_played, self.wins, self.losses, self.draws, self.goals, self.assists)

    def update_player(self):
        player = self.player
        player.games_played += self.games_played
        player.wins += self.wins
        player.losses += self.losses
        player.draws += self.draws
        player.goals += self.goals
        player.assists += self.assists
        player.save()
        player.elo = player.calculate_elo()
        player.save()
