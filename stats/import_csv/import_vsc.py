__author__ = 'Carlos'
# -*- coding: utf8 -*-
import csv
import os
import sys
from stats import models
from stats.models import Player, Fixture, Stats
from django.core.exceptions import AppRegistryNotReady
import datetime
import django

django.setup()

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


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

            Stats.objects.create(player=player, fixture=fixture, games_played=int(row[1]),
                                 wins=int(row[2]) if row[2] != '' else 0,
                                 draws=int(row[3]) if row[3] != '' else 0,
                                 losses=int(row[4]) if row[4] != '' else 0,
                                 goals=int(row[5]) if row[5] != '' else 0,
                                 assists=int(row[6]) if row[6] != '' else 0
                                 )

            # stats, _ = Stats.objects.get_or_create(player=player, fixture=fixture,
            #                                        defaults={'games_played': int(row[1]),
            #                                                  'wins': int(row[2]) if row[2] != '' else 0,
            #                                                  'draws': int(row[3]) if row[3] != '' else 0,
            #                                                  'losses': int(row[4]),
            #                                                  'goals': int(row[5]) if row[5] != '' else 0,
            #                                                  'assists': int(row[6]) if row[6] != '' else 0})


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


def test_error_one(path):
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

            stats, _ = Stats.objects.get_or_create(player=player, fixture=fixture,
                                                   defaults={'games_played': int(row[1]),
                                                             'wins': int(row[2]) if row[2] != '' else 0,
                                                             'draws': int(row[3]) if row[3] != '' else 0,
                                                             'losses': int(row[4]),
                                                             'goals': int(row[5]) if row[5] != '' else 0,
                                                             'assists': int(row[6]) if row[6] != '' else 0})


def import_all_fixtures(path):
    import re
    files = os.listdir(path)
    f = []
    for x in files:
        f.append(int(re.search("\d+", x).group()))

    f.sort()

    for file in f:
        test_error_one(os.path.join('football_stats', 'jornada' + str(file) + '.csv'))


# import_all_fixtures('football_stats')


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
