from stats import models


def execute(fixture, attr='wins'):
    tmp = []
    for player in models.Player.objects.all():
        pp = models.PlayerPerformance.objects.filter(player=player, fixture__number__lte=fixture.number)
        stat = models.get_total_stats(player_performance_query_set=pp)
        if stat:
            tmp.append(
                (player.name_excel, getattr(stat, attr) / stat.games_played, stat.games_played >= 3 * fixture.number))
    return tmp
