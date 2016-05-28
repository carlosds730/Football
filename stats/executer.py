from Algorithims import base
from stats import models
import stats.extra_functions as ef
from django.db.utils import IntegrityError

algorithims = {
    'base': base.execute
}


def execute(fixture):
    for x in algorithims.keys():
        achievement, _ = models.Achievements.objects.get_or_create(function_name=x)
        result = ef.convert_to_str(algorithims[x](fixture))
        try:
            models.Results.objects.create(result=result, fixture=fixture,
                                          achievement=achievement)
        except IntegrityError:
            models.Results.objects.get(fixture=fixture, achievement=achievement).delete()
            models.Results.objects.create(result=result, fixture=fixture,
                                          achievement=achievement)
