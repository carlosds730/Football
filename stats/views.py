from django.shortcuts import render
from stats import models
from django.http import HttpResponse, HttpResponseRedirect
import json


def wrapper(request, page, context):
    context.update({
        'seasons': models.Season.objects.all()
    })
    return render(request, page, context)


# Create your views here.
def home(request):
    if request.method == 'GET':
        main_pictures = models.MainPictures.objects.all()
        cursor = models.PlayerPerformance.last_fixture_stats.order_by('-stat__elo')
        last_day = [x for x in cursor]
        goals = [x for x in cursor.order_by('-stat__goals') if x.stat.goals]
        assist = [x for x in cursor.order_by('-stat__assists') if x.stat.assists]
        context = {
            'main_pictures': main_pictures,
            'goals': goals,
            'assist': assist,
            'last_matchday': last_day
        }
        return wrapper(request, 'home.html', context)


def season(request, season):
    raise NotImplemented()


def general(request, order):
    players = models.Player.objects.order_by('-global_stats__' + order).all()
    return wrapper(request, 'general.html', {'players': players})
