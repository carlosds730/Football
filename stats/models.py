# -*- coding: utf8 -*-
from django.db import models
from sorl.thumbnail import ImageField
from decimal import *
from stats.extra_functions import validate_fixture
from django.db.models import Sum
import datetime

from stats.extra_functions import calculate_elo_simple


def get_next_fixture():
    """
    Get the number of the next Fixture
    """

    next_fixture = Fixture.objects.aggregate(
        models.Max('number')
    )['number__max']

    if next_fixture:
        return next_fixture + 1
    else:
        return 1


def get_next_fixture_date():
    """
    Get the date of the next Fixture
    """

    a = Fixture.objects.first()
    if a:
        return a.date + datetime.timedelta(7)
    else:
        return datetime.date(2015, 6, 14)


# Create your models here.

class Player(models.Model):
    class Meta:
        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"
        ordering = ['-elo']

    name = models.CharField(verbose_name="Nombre", help_text="Nombre del jugador", max_length=200, unique=True)

    image = ImageField(verbose_name="Avatar", upload_to='Avatars', help_text="Foto del jugador", blank=True)

    # Numeric fields

    games_played = models.PositiveSmallIntegerField(verbose_name="Juegos jugados", default=0)

    wins = models.PositiveSmallIntegerField(verbose_name="Juegos ganados", default=0)

    draws = models.PositiveSmallIntegerField(verbose_name="Juegos empatados", default=0)

    losses = models.PositiveSmallIntegerField(verbose_name="Juegos perdidos", default=0)

    goals = models.PositiveSmallIntegerField(verbose_name="Goles anotados", default=0)

    assists = models.PositiveSmallIntegerField(verbose_name="Asistencias", default=0)

    elo = models.DecimalField(verbose_name="ELO", max_digits=7, decimal_places=5, default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # self.calculate_player_stats()
        self.elo = self.calculate_elo()
        super(Player, self).save(*args, **kwargs)

    def calculate_elo(self):
        return calculate_elo_simple(self.games_played, self.wins, self.losses, self.draws, self.goals, self.assists)

    def calculate_player_stats(self):
        data = Stats.objects.filter(player=self).aggregate(Sum('games_played'), Sum('wins'), Sum('losses'),
                                                           Sum('draws'), Sum('goals'), Sum('assists'))
        if data:
            self.games_played = data['games_played__sum']
            self.wins = data['wins__sum']
            self.losses = data['losses__sum']
            self.draws = data['draws__sum']
            self.goals = data['goals__sum']
            self.assists = data['assists__sum']
            self.save()
            self.calculate_elo()
            self.save()


class Fixture(models.Model):
    class Meta:
        verbose_name = "Jornada"
        verbose_name_plural = "Jornadas"
        ordering = ['-number']

    date = models.DateField(verbose_name="Fecha", help_text="Fecha de la jornada", unique=True,
                            default=get_next_fixture_date)

    image = ImageField(verbose_name="Foto", upload_to='Jornadas', help_text="Foto de la jornada", blank=True)

    number = models.PositiveSmallIntegerField(verbose_name="Jornada número", default=get_next_fixture)

    season = models.ForeignKey('Season', related_name='fixtures', verbose_name='Temporada', null=True)

    def __str__(self):
        return "Jornada " + str(self.number)


class Stats(models.Model):
    class Meta:
        verbose_name = "Actuación"
        verbose_name_plural = "Actuaciones"

    # Related fields
    player = models.ForeignKey('Player', verbose_name="Jugador", related_name="stats")

    fixture = models.ForeignKey('Fixture', verbose_name="Jornada", related_name="stats")

    # Numeric fields
    games_played = models.PositiveSmallIntegerField(verbose_name="Juegos jugados", default=0)

    wins = models.PositiveSmallIntegerField(verbose_name="Juegos ganados", default=0)

    draws = models.PositiveSmallIntegerField(verbose_name="Juegos empatados", default=0)

    losses = models.PositiveSmallIntegerField(verbose_name="Juegos perdidos", default=0)

    goals = models.PositiveSmallIntegerField(verbose_name="Goles anotados", default=0)

    assists = models.PositiveSmallIntegerField(verbose_name="Asistencias", default=0)

    elo = models.DecimalField(verbose_name="ELO", max_digits=7, decimal_places=5, default=0)

    def save(self, *args, **kwargs):
        validate_fixture(self.games_played, self.wins, self.losses, self.draws)
        self.elo = self.calculate_elo()
        super(Stats, self).save(*args, **kwargs)
        self.player.calculate_player_stats()
        # self.update_player()

    def calculate_elo(self):
        return calculate_elo_simple(self.games_played, self.wins, self.losses, self.draws, self.goals, self.assists)

    # WARNING: This shouldn't be used at least you can be sure the Stats object is being created and not updated
    def update_player(self):
        print(self.player.name + str(self.fixture))
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


class Season(models.Model):
    class Meta:
        verbose_name = 'Temporada'
        verbose_name_plural = 'Temporadas'
        ordering = ['-number']

    number = models.PositiveIntegerField(verbose_name='Numero')

    name = models.CharField(verbose_name='Nombre', max_length=200)

    def __str__(self):
        return str(self.number)
