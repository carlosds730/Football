# -*- coding: utf8 -*-
__author__ = 'Carlos'

from django.core.exceptions import ValidationError
import json
import csv
import os
import sys


def validate_fixture(jj, w, l, d, ):
    if jj == 0:
        raise ValidationError('La cantidad de juegos jugados no puede ser 0 %d' % jj)
    if jj != (w + l + d):
        raise ValidationError('Hay inconsistencia en los datos: %d!=%d+%d+%d' % (jj, w, l, d))


def calculate_elo_simple(jj, w, l, d, g, a):
    if jj == 0:
        return 0
    else:
        num = 0.5 * g + 0.25 * a + 0.2 * w + (0.2 / 3) * d - 0.1 * l
        return round(num / jj, 5)


def convert_to_str(_list):
    return json.dumps({'result': _list})
