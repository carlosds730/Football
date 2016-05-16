__author__ = 'Carlos'
# -*- coding: utf8 -*-

import csv
import os
import sys
from Football.settings import STATS_PATH
from stats import models
from stats.models import Player, Fixture, Stats, PlayerPerformance
import datetime
from django.core.management.base import BaseCommand, CommandError


def import_csv(path):
    csv_file = csv.reader(open(path, 'rb'))

    for row in csv_file:
        print(row)


def test(path):
    with open(path, newline='') as csvfile:
        line = csv.reader(csvfile, delimiter=',', quotechar='|')
        line.__next__()
        fixture = Fixture.objects.create()
        fixture.save()

        for row in line:
            print(row)
            if row[1] == '' or row[1] == '0':
                continue
            player, _ = Player.objects.get_or_create(name=row[0])

            PlayerPerformance.objects.create_performance(player=player, fixture=fixture, games_played=int(row[1]),
                                                         wins=int(row[2]) if row[2] != '' else 0,
                                                         draws=int(row[3]) if row[3] != '' else 0,
                                                         losses=int(row[4]) if row[4] != '' else 0,
                                                         goals=int(row[5]) if row[5] != '' else 0,
                                                         assists=int(row[6]) if row[6] != '' else 0
                                                         )


def test_error(path):
    with open(path, newline='') as csvfile:
        line = csv.reader(csvfile, delimiter=',', quotechar='|')
        line.__next__()
        fixture = Fixture.objects.create()
        fixture.save()

        for row in line:
            print(row)
            if row[1] == '':
                continue
            player, _ = Player.objects.get_or_create(name=row[0])
            player.save()

            try:
                stats = Stats.objects.get(player=player, fixture=fixture)
            except Exception:
                stats = Stats.objects.create(player=player, fixture=fixture)

            stats.games_played = int(row[1])
            stats.wins = int(row[2]) if row[2] != '' else 0
            stats.draws = int(row[3]) if row[3] != '' else 0
            stats.losses = int(row[4]) if row[4] != '' else 0
            stats.goals = int(row[5]) if row[5] != '' else 0
            stats.assists = int(row[6]) if row[6] != '' else 0
            stats.save()


def test_error_one(path, jornada, season):
    with open(path, newline='') as csvfile:
        line = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(line)
        fixture = Fixture.objects.create()
        fixture.season = season
        fixture.save()

        for row in line:
            print(row)
            if row[1] == '':
                continue
            player, _ = Player.objects.get_or_create(name=row[0])
            player.save()

            PlayerPerformance.objects.create_performance(player=player, fixture=fixture, games_played=int(row[1]),
                                                         wins=int(row[2]) if row[2] != '' else 0,
                                                         draws=int(row[3]) if row[3] != '' else 0,
                                                         losses=int(row[4]) if row[4] != '' else 0,
                                                         goals=int(row[5]) if row[5] != '' else 0,
                                                         assists=int(row[6]) if row[6] != '' else 0
                                                         )


def import_all_fixtures(path, season=models.Season.objects.last()):
    import re
    files = os.listdir(path)
    f = []
    for x in files:
        f.append(int(re.search("\d+", x).group()))

    f.sort()
    fixtures = [x.number for x in Fixture.objects.all()]
    for file in f:
        if file not in fixtures:
            test_error_one(os.path.join(path, 'jornada' + str(file) + '.csv'), file, season)


def fix_dates(pk):
    """
    Increases in a week the date of the Fixture whose pk is pk. It also increases in a week the date of every Fixture whose date is greater or equal than Fixture.objects.get(pk=pk).date+ datetime.timedelta(7)
    :param pk: Is the pk of Fixture object whose date wants to be changed
    :return: It doesn't return anything

    """
    fix = models.Fixture.objects.get(pk=pk)
    to_fix = models.Fixture.objects.filter(date__gte=fix.date + datetime.timedelta(7))
    for fixt in to_fix:
        fixt.date = fixt.date + datetime.timedelta(7)
        fixt.save()
    fix.date = fix.date + datetime.timedelta(7)
    fix.save()


# TODO: This command should allow us to specify the the season (the number) corresponding to the fixtures we are importing.
class Command(BaseCommand):
    help = "Import all stats"

    def handle(self, *args, **options):
        try:
            import_all_fixtures(STATS_PATH)
        except Exception as e:
            raise CommandError('Something went wrong "%s"' % e)
        self.stdout.write(self.style.SUCCESS('Stats imported successfully'))
