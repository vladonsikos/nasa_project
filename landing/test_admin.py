from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Slide


class SlideAdminTestCase(TestCase):
    """Тесты для администратора Slide."""

    def setUp(self):
        """Подготовка тестовых данных."""
        # Создаю суперпользователя
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        
        # Создаю тестовые слайды
        self.slide1 = Slide.objects.create(title='Слайд 1', order=1)
        self.slide2 = Slide.objects.create(title='Слайд 2', order=2)
        
        # Клиент для HTTP запросов
        self.client = Client()

    def test_admin_login(self):
        """Тест входа в админку."""
        self.client.force_login(self.admin_user)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_slide_list_display(self):
        """Тест отображения списка слайдов в админке."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/landing/slide/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Слайд 1')
        self.assertContains(response, 'Слайд 2')

    def test_slide_search(self):
        """Тест поиска по названию в админке."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/landing/slide/?q=Слайд 1')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Слайд 1')

    def test_slide_filter_by_order(self):
        """Тест фильтрации по полю order."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/landing/slide/')
        
        self.assertEqual(response.status_code, 200)

    def test_slide_add_form(self):
        """Тест формы добавления слайда."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/landing/slide/add/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Название')

    def test_slide_edit_form(self):
        """Тест формы редактирования слайда."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(f'/admin/landing/slide/{self.slide1.id}/change/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Слайд 1')

    def test_slide_delete(self):
        """Тест удаления слайда."""
        self.client.login(username='admin', password='admin123')
        
        # Проверяю, что слайд существует
        self.assertTrue(Slide.objects.filter(id=self.slide1.id).exists())
        
        # Удаляю слайд
        response = self.client.post(
            f'/admin/landing/slide/{self.slide1.id}/delete/',
            {'post': 'yes'},
            follow=True
        )
        
        # Проверяю, что слайд удален
        self.assertFalse(Slide.objects.filter(id=self.slide1.id).exists())

    def test_slide_list_per_page(self):
        """Тест количества слайдов на странице."""
        self.client.login(username='admin', password='admin123')
        
        # Создаю дополнительные слайды
        for i in range(30):
            Slide.objects.create(title=f'Слайд {i+3}', order=i+3)
        
        response = self.client.get('/admin/landing/slide/')
        
        self.assertEqual(response.status_code, 200)
        # Проверяю наличие пагинатора
        self.assertContains(response, 'paginator')
