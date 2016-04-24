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
        cursor = models.Fixture.objects.order_by('-number')[0].stats.all()
        last_day = [x for x in cursor]
        goals = [x for x in cursor.order_by('-goals') if x.goals]
        assist = [x for x in cursor.order_by('-assists') if x.assists]
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
    players = models.Player.objects.all().order_by('-' + order)
    return wrapper(request, 'general.html', {'players': players})
