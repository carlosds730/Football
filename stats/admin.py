from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
import nested_admin
from stats import models


# Register your models here.

class StatInline(nested_admin.NestedStackedInline):
    model = models.Stats
    readonly_fields = ['games_played', 'wins', 'draws', 'losses', 'goals', 'assists', 'elo']
    exclude = ['stat', 'player']


class StatsInline(nested_admin.NestedStackedInline):
    model = models.PlayerPerformance
    inlines = [StatInline]
    readonly_fields = ['fixture', 'player']
    extra = 0


class GlobalStatsInline(admin.StackedInline):
    model = models.Stats
    readonly_fields = ['games_played', 'wins', 'draws', 'losses', 'goals', 'assists', 'elo']
    verbose_name = 'Estadística global'
    verbose_name_plural = 'Estadísticas globales'
    exclude = ['stat']
    # readonly_fields = ()


class PlayersAdmin(AdminImageMixin, nested_admin.NestedModelAdmin):
    model = models.Player
    inlines = [GlobalStatsInline, StatsInline]


class FixtureAdmin(AdminImageMixin, nested_admin.NestedModelAdmin):
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
