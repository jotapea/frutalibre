from django.http import HttpResponse
from django.shortcuts import render

from frutalibre.models import FruitSnap


def index(request):
    fruits = FruitSnap.objects.all()
    context = {
        'fruits': fruits,
    }
    return render(request, 'frutaui/index.html', context)    


def more(request):
    return HttpResponse("Coming soon...")
