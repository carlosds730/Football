from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json


# Create your views here.
def home(request):
    if request.method == 'GET':
        return render(request, 'home.html', {})
    elif request.is_ajax():
        return HttpResponse(json.dumps({'images': 'HELLO'}), content_type='application/json')
