from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from stats import models


# Register your models here.

class StatsInline(admin.StackedInline):
    model = models.Stats
    extra = 0
    readonly_fields = ['elo']


class PlayersAdmin(AdminImageMixin, admin.ModelAdmin):
    model = models.Player
    inlines = [StatsInline]
    list_display = ['name', 'elo', 'goals', 'assists', 'wins', 'draws', 'losses']
    readonly_fields = ['games_played', 'wins', 'losses', 'draws', 'goals', 'assists', 'elo']


class FixtureAdmin(AdminImageMixin, admin.ModelAdmin):
    model = models.Fixture
    inlines = [StatsInline]
    list_display = ['number', 'date', 'season']
    list_filter = ['season__number', 'date', 'number']


class SeasonAdmin(admin.ModelAdmin):
    list_display = ['number', 'name']


class MainAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ['id', 'name', 'url']


admin.site.register(models.Fixture, FixtureAdmin)
admin.site.register(models.Player, PlayersAdmin)
admin.site.register(models.Season, SeasonAdmin)
admin.site.register(models.MainPictures, MainAdmin)
