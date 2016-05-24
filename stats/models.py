# -*- coding: utf8 -*-
from django.db import models
from sorl.thumbnail import ImageField
from decimal import *
from stats.extra_functions import validate_fixture
from django.db.models import Sum
import datetime
import os
from stats.extra_functions import calculate_elo_simple
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Count


# TODO: get_last season.

# TODO: get_next_fixture should return the number of the next fixture of the active season.
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

    a = Fixture.objects.last()
    if a:
        return a.date + datetime.timedelta(7)
    else:
        return datetime.date(2015, 6, 14)


def get_total_stats(stats_query_set=None, player_performance_query_set=None):
    """
    Returns the overall stats (an Stats object which is a python object and is not stored in the database) of a
    collection of Stats or PlayerPerformance objects. Parameters stats_query_set and player_performance_query_set
    should not be used at the same time, if this happens only the stats_query_set will be used.
    :param stats_query_set: Stats QuerySet to extract the data from
    :type stats_query_set: QuerySet(Stats)
    :param player_performance_query_set: PlayerPerformance QuerySet to extract the data from
    :type player_performance_query_set: QuerySet(PlayerPerformance)
    :return: An Stats object (is a python object is not stored in the database)
    :rtype: Stats
    """
    data = None
    if stats_query_set:
        data = stats_query_set.aggregate(games_played=Sum('games_played'), wins=Sum('wins'),
                                         losses=Sum('losses'),
                                         draws=Sum('draws'), goals=Sum('goals'),
                                         assists=Sum('assists'))
    elif player_performance_query_set:
        data = player_performance_query_set.aggregate(games_played=Sum('stat__games_played'), wins=Sum('stat__wins'),
                                                      losses=Sum('stat__losses'),
                                                      draws=Sum('stat__draws'), goals=Sum('stat__goals'),
                                                      assists=Sum('stat__assists'))
    if data:
        stat = Stats(games_played=data['games_played'],
                     wins=data['wins'],
                     losses=data['losses'],
                     draws=data['draws'],
                     goals=data['goals'],
                     assists=data['assists'])
        stat.elo = stat.calculate_elo()
        return stat
    else:
        return None


# TODO: The result of this method should me cached.
def get_minimum_total_games():
    min_games = Season.objects.annotate(num_fix=Count('fixtures')).aggregate(total_fix=Sum('num_fix'))
    print(min_games)
    return min_games['total_fix']


class Player(models.Model):
    class Meta:
        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"
        ordering = ['name_excel']

    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)

    name_excel = models.CharField(verbose_name="Nombre en el Excel",
                                  help_text="Nombre del jugador tal como aparece en el Excel",
                                  max_length=200, unique=True)

    image = ImageField(verbose_name="Avatar", upload_to='Avatars', help_text="Foto del jugador", blank=True)

    def __str__(self):
        return self.name

    @property
    def is_active(self):
        return self.global_stats.games_played >= 3 * get_minimum_total_games()

    @property
    def name(self):
        if self.user:
            return self.user.username
        else:
            return self.name_excel

    def update_global_stats(self):
        """
        Update the global_stats attribute of the current player.
        It saves the player object by itself
        """
        try:
            stat = self.global_stats
            stat.delete()
        except Stats.DoesNotExist:
            pass
        global_stats = self.calculate_global_stats()
        if global_stats:
            global_stats.player = self
            global_stats.save()

    def calculate_global_stats(self):
        """
        Calculates the global stats of the current player.
        :return: Returns an Stats objects that contains the global stats of the current player
        :rtype: Stats
        """
        my_stats = PlayerPerformance.objects.filter(player=self)
        if my_stats.count() > 0:
            return get_total_stats(player_performance_query_set=my_stats)
        else:
            return None

    def save(self, *args, **kwargs):
        # If we are creating a Player with user but no name then the player's name will be the username
        if self.user and not self.name_excel:
            self.name_excel = self.user.username
        super(Player, self).save(*args, **kwargs)


class PlayerPerformanceCreator(models.Manager):
    def create_performance(self, player, fixture, stat=None, games_played=0, wins=0, draws=0, losses=0, goals=0,
                           assists=0):
        """
        This method creates a PlayerPerformance object given a player, a fixture and a Stats object.
        If the stat parameter isn't provided you can pass the necessary info to create one, if you don't, an Stats object
        with all data set to 0 will be created.
        """
        if not stat:
            stat = Stats.objects.create(games_played=games_played,
                                        wins=wins,
                                        draws=draws,
                                        losses=losses,
                                        goals=goals,
                                        assists=assists)
        performance = self.create(player=player, fixture=fixture)
        stat.stat = performance
        stat.save()
        return performance


class LastFixture(models.Manager):
    def get_queryset(self):
        last_fixture = Fixture.objects.latest('date')
        return super(LastFixture, self).get_queryset().filter(fixture=last_fixture)


class PlayerPerformance(models.Model):
    # This models represents the performance of a player in a fixture.
    class Meta:
        verbose_name = 'Desempeño'
        verbose_name_plural = 'Desempeños'
        # A player can't have more than one PlayerPerformance per fixture
        unique_together = ('player', 'fixture')

    player = models.ForeignKey('Player', related_name='performances', verbose_name='Jugaodr')

    fixture = models.ForeignKey('Fixture', related_name='performances', verbose_name='Jornada')

    # We override the default manager because we want to use the create_performance method to create
    # PlayerPerformance objects
    # To create PlayerPerformance objects DO NOT USE objects.create, USE instead objects.create_performance
    objects = PlayerPerformanceCreator()

    # Use this manager to obtain the PlayerPerformances of the last_fixture
    last_fixture_stats = LastFixture()

    def __str__(self):
        return "Jornada %s (%s)" % (self.fixture.number, str(self.fixture.date))

    def to_list(self, first_column=False):
        """
        See Stats.to_list for references.
        :param first_column: The first element of the list (optional)
        :type first_column: str or False
        :return: Stat info as a list
        :rtype: list
        """
        return self.stat.to_list(first_column=first_column)


class Fixture(models.Model):
    class Meta:
        verbose_name = "Jornada"
        verbose_name_plural = "Jornadas"
        ordering = ['number']
        unique_together = ('number', 'season')

    date = models.DateField(verbose_name="Fecha", help_text="Fecha de la jornada", unique=True,
                            default=get_next_fixture_date)

    image = ImageField(verbose_name="Foto", upload_to='Jornadas', help_text="Foto de la jornada", blank=True)

    number = models.PositiveSmallIntegerField(verbose_name="Jornada", default=get_next_fixture)

    season = models.ForeignKey('Season', related_name='fixtures', verbose_name='Temporada', null=True)

    def __str__(self):
        return "Jornada " + str(self.number)


class Stats(models.Model):
    class Meta:
        verbose_name = "Actuación"
        verbose_name_plural = "Actuaciones"
        ordering = ['-elo']

    games_played = models.PositiveSmallIntegerField(verbose_name="Juegos jugados", default=0)

    wins = models.PositiveSmallIntegerField(verbose_name="Juegos ganados", default=0)

    draws = models.PositiveSmallIntegerField(verbose_name="Juegos empatados", default=0)

    losses = models.PositiveSmallIntegerField(verbose_name="Juegos perdidos", default=0)

    goals = models.PositiveSmallIntegerField(verbose_name="Goles anotados", default=0)

    assists = models.PositiveSmallIntegerField(verbose_name="Asistencias", default=0)

    elo = models.DecimalField(verbose_name="ELO", max_digits=7, decimal_places=5, default=0)

    player = models.OneToOneField('Player', verbose_name='Estadísticas globales', related_name='global_stats',
                                  blank=True, null=True,
                                  help_text='Estadísticas totales del jugador. Incluye todas las temporadas')

    stat = models.OneToOneField('PlayerPerformance', related_name='stat', blank=True, null=True)

    @property
    def name(self):
        if self.player:
            return self.player.name
        elif self.stat:
            return self.stat.player.name
        return None

    def to_list(self, first_column=False):
        """
        Returns a list containing the numerical info of this Stat. The first element of the list can be settled using
        the parameter first_column, if this parameter is not present (by default it isn't) the first element will be
        the name of the player associated with this stat.
        :param first_column: The first element of the list (optional)
        :type first_column: str or False
        :return: Stat info as a list
        :rtype: list
        """
        if first_column:
            return [first_column, self.games_played, self.wins, self.draws, self.losses, self.goals, self.assists,
                    self.elo]
        else:
            return [self.name, self.games_played, self.wins, self.draws, self.losses, self.goals, self.assists,
                    self.elo]

    def save(self, *args, **kwargs):
        """
        Overrides the save method.
        It verifies that Stats object is valid, calculates its ELO and finally saves the object.
        """
        validate_fixture(self.games_played, self.wins, self.losses, self.draws)
        self.elo = self.calculate_elo()
        super(Stats, self).save(*args, **kwargs)

    def calculate_elo(self):
        """
        Calculates the ELO of the current Stats object
        :return: ELO
        :rtype: double
        """
        return calculate_elo_simple(self.games_played, self.wins, self.losses, self.draws, self.goals, self.assists)


class Season(models.Model):
    class Meta:
        verbose_name = 'Temporada'
        verbose_name_plural = 'Temporadas'
        ordering = ['-number']

    number = models.PositiveIntegerField(verbose_name='Numero')

    name = models.CharField(verbose_name='Nombre', max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.number)

    @property
    def min_num_games(self):
        return 3 * self._num_fixtures

    @property
    def init_date(self):
        """
        Returns the date of the first fixture related with this season
        :return: Date of the first fixture related with this season
        :rtype: date
        """
        return self.fixtures.first().date

    @property
    def end_date(self):
        """
        Returns the date of the last fixture related with this season
        :return: Date of the last fixture related with this season
        :rtype: date
        """
        return self.fixtures.last().date

    @property
    def _num_fixtures(self):
        """
        Returns the number of fixtures in the current season.
        For performance optimization this method should be used only if you just need the number of fixtures in this
        season. If you want to do some work with the fixtures related to this season is better to load those records
        into python objects and use len.
        :return: the number of fixtures in the given season
        :rtype: int
        """
        return self.fixtures.count()

    # TODO: The result of this method should be cached
    def global_info(self):
        """
        Calculates the info of the players for the current season. It returns a list of stat objects where stat.player
        is the player.
        :return: A list of Stat objects (not stored in database).
        :rtype: list
        """
        all_performances = PlayerPerformance.objects.filter(fixture__season__number=self.number)
        active_players = []
        inactive_players = []
        for player in Player.objects.all():
            # This stat objects are only stored in memory
            stat = get_total_stats(player_performance_query_set=all_performances.filter(player=player))
            if stat:
                stat.player = player
            else:
                continue
            if stat.games_played < 3 * self._num_fixtures:
                inactive_players.append(stat)
            else:
                active_players.append(stat)
        return active_players, inactive_players

    def get_absolute_url(self):
        return reverse('season', args=[self.number])


class MainPictures(models.Model):
    class Meta:
        verbose_name = 'Foto Portada'
        verbose_name_plural = 'Fotos Portada'

    picture = ImageField(verbose_name='Picture', upload_to='Main')

    def name(self):
        return self.picture.url.split('/')[-1]

    def url(self):
        return self.picture.url
