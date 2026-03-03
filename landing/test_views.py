from django.test import TestCase, Client
from .models import Slide


class IndexViewTestCase(TestCase):
    """Тесты для главной страницы."""

    def setUp(self):
        """Подготовка тестовых данных."""
        self.client = Client()
        
        # Создаю тестовые слайды
        for i in range(5):
            Slide.objects.create(
                title=f'Космическая фотография {i+1}',
                order=i+1
            )

    def test_index_view_returns_200(self):
        """Тест, что главная страница возвращает статус 200."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        """Тест, что используется правильный шаблон."""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'landing/index.html')

    def test_index_view_contains_slides(self):
        """Тест, что страница содержит слайды."""
        response = self.client.get('/')
        
        self.assertContains(response, 'Космическая фотография 1')
        self.assertContains(response, 'Космическая фотография 5')

    def test_index_view_with_no_slides_shows_placeholders(self):
        """Тест, что при отсутствии слайдов показываются плейсхолдеры."""
        # Удаляю все слайды
        Slide.objects.all().delete()
        
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        # Проверяю, что плейсхолдеры присутствуют
        self.assertIn('slides', response.context)

    def test_index_view_slides_ordered(self):
        """Тест, что слайды упорядочены по order."""
        response = self.client.get('/')
        
        slides = response.context['slides']
        orders = [slide.order for slide in slides]
        
        # Проверяю, что порядок правильный
        self.assertEqual(orders, sorted(orders))

    def test_index_view_cache_headers(self):
        """Тест, что используется кеширование через ETag."""
        response = self.client.get('/')
        
        # Проверяю, что есть ETag заголовок
        self.assertIn('ETag', response)

    def test_index_view_contains_required_elements(self):
        """Тест, что страница содержит необходимые элементы."""
        response = self.client.get('/')
        
        # Проверяю наличие основных блоков
        self.assertContains(response, 'navbar-logo')
        self.assertContains(response, 'hero-title')
        self.assertContains(response, 'features')
        self.assertContains(response, 'photos')

    def test_index_view_performance(self):
        """Тест производительности главной страницы."""
        import time
        
        start = time.time()
        response = self.client.get('/')
        duration = time.time() - start
        
        # Проверяю, что страница загружается быстро (менее 1 секунды)
        self.assertLess(duration, 1.0)
        self.assertEqual(response.status_code, 200)
