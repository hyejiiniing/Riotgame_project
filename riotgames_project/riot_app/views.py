from django.shortcuts import render
from .utils import get_summoner_data

def summoner_view(request, summoner_name):
    data = get_summoner_data(summoner_name)
    return render(request, 'summoner.html', {'data': data})

def home_view(request):
    return render(request, 'home.html')
