from django.shortcuts import render
from stats import models
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, PlayerEditForm, UserEditForm
from django.contrib.auth.decorators import login_required


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


def season(request, season_num):
    raise NotImplemented()


def general(request, order):
    players = models.Player.objects.order_by('-global_stats__' + order).all()
    return wrapper(request, 'general.html', {'players': players})


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
