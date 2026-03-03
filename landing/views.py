from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import condition
from .models import Slide

PLACEHOLDER_SLIDES = [
    {'title': 'Человек на фоне звёзд', 'image': None, 'order': 1},
    {'title': 'Звёздное небо', 'image': None, 'order': 2},
    {'title': 'Марсианский пейзаж', 'image': None, 'order': 3},
    {'title': 'Солнечное затмение', 'image': None, 'order': 4},
    {'title': 'Млечный путь', 'image': None, 'order': 5},
]


def get_slides_etag(request):
    """Генерирует ETag для кеширования на основе последнего слайда."""
    try:
        latest_slide = Slide.objects.latest('created_at')
        return f'{latest_slide.id}-{latest_slide.created_at.timestamp()}'
    except Slide.DoesNotExist:
        return 'no-slides'


def get_slides_last_modified(request):
    """Возвращает время последнего изменения слайдов."""
    try:
        latest_slide = Slide.objects.latest('created_at')
        return latest_slide.created_at
    except Slide.DoesNotExist:
        return None


@condition(etag_func=get_slides_etag, last_modified_func=get_slides_last_modified)
def index(request):
    """
    Отображает главную страницу с галереей слайдов.
    
    Получает все слайды из БД или показывает плейсхолдеры, если слайдов нет.
    Использует кеширование на основе ETag для оптимизации производительности.
    
    Args:
        request (HttpRequest): HTTP запрос
        
    Returns:
        HttpResponse: Отрендеренный HTML шаблон с слайдами
    """
    slides = Slide.objects.select_related('image').order_by('order')
    
    if not slides.exists():
        slides = PLACEHOLDER_SLIDES
    
    return render(request, 'landing/index.html', {'slides': slides})
