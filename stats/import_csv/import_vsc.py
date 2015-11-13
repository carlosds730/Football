__author__ = 'Carlos'
# -*- coding: utf8 -*-
import csv
import os
import sys
from stats.models import Player, Fixture, Stats
import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


def import_csv(path):
    csv_file = csv.reader(open(path, 'rb'))

    for row in csv_file:
        print(row)


def test(path, date):
    with open(path, newline='') as csvfile:
        line = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in line:
            pass

            # print(', '.join(row))


test('football_stats/jornada1.csv', date=datetime.date(2015, 6, 14))
