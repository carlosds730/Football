from django.shortcuts import render
from stats import models
from django.http import HttpResponse, HttpResponseRedirect, Http404
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, PlayerEditForm, UserEditForm
from django.views.generic import View
from django.contrib.auth.decorators import login_required

ORDER_BY = [('games_played', 'Games', '-games_played'), ('wins', 'Wins', '-wins'), ('draws', 'Draws', '-draws'),
            ('losses', 'Losses', '-losses'), ('goals', 'Goals', '-goals'),
            ('assists', 'Assists', '-assists'), ('elo', 'ELO', '-elo')]


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


def season(request, season_num, order='elo'):
    season_info = models.Season.objects.get(number=season_num)

    active_players, inactive_players = season_info.global_info()
    new_order, reverse = order_trick(order)

    try:
        active_players.sort(key=lambda x: getattr(x, new_order), reverse=reverse)
        inactive_players.sort(key=lambda x: getattr(x, new_order), reverse=reverse)
    except AttributeError:
        raise Http404

    return wrapper(request, 'season.html',
                   {'active_players': active_players, 'inactive_players': inactive_players, 'season_num': season_info,
                    'min_num_games': season_info.min_num_games,
                    'order': order, 'order_by': ORDER_BY})


def order_trick(order):
    reverse = '-' not in order
    new_order = order
    if not reverse:
        new_order = order.split('-')[1]
    return new_order, reverse


def general(request, order='elo'):
    minimum_total_games = models.get_minimum_total_games()
    new_order, reverse = order_trick(order)
    if reverse:
        reverse = '-'
    else:
        reverse = ''
    active_players = models.Player.objects.filter(global_stats__games_played__gte=3 * minimum_total_games).order_by(
        reverse + 'global_stats__' + new_order)
    inactive_players = models.Player.objects.filter(global_stats__games_played__lt=3 * minimum_total_games).order_by(
        reverse + 'global_stats__' + new_order)

    return wrapper(request, 'general.html',
                   {'active_players': active_players, 'inactive_players': inactive_players, 'order': order,
                    'min_num_games': 3 * minimum_total_games,
                    'order_by': ORDER_BY})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password (instead of saving the raw password we call set_password which do this in a safe way)
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            try:
                player = models.Player.objects.get(name_excel=new_user.username)
                player.user = new_user
                player.save()
            except models.Player.DoesNotExist:
                models.Player.objects.create(user=new_user)
            return render(request,
                          'register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        player_form = PlayerEditForm(instance=request.user.player, data=request.POST, files=request.FILES)
        if user_form.is_valid() and player_form.is_valid():
            user_form.save()
            player_form.save()
            return HttpResponseRedirect('/')
    else:
        user_form = UserEditForm(instance=request.user)
        player_form = PlayerEditForm(
            instance=request.user.player)
    return render(request, 'edit.html', {'user_form': user_form, 'player_form': player_form})
