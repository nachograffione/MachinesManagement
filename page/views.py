from pickle import GET
from django.http import HttpResponse
from django.shortcuts import render
import requests


def index_view(request):
    return render(request, 'page/index.html', {'search': request.GET.get('search', '')})


def machine_view(request, id):
    return render(request, 'page/machine.html', {'id': id})
