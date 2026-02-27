from django.shortcuts import render
from .models import Slide

PLACEHOLDER_SLIDES = [
    {'title': 'Человек на фоне звёзд', 'image': None, 'order': 1},
    {'title': 'Звёздное небо', 'image': None, 'order': 2},
    {'title': 'Марсианский пейзаж', 'image': None, 'order': 3},
    {'title': 'Солнечное затмение', 'image': None, 'order': 4},
    {'title': 'Млечный путь', 'image': None, 'order': 5},
]


def index(request):
    slides = list(Slide.objects.all())
    if not slides:
        slides = PLACEHOLDER_SLIDES
    return render(request, 'landing/index.html', {'slides': slides})
