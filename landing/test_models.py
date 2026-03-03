from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Slide


class SlideModelTestCase(TestCase):
    """Тесты для модели Slide."""

    def setUp(self):
        """Подготовка тестовых данных."""
        self.slide = Slide.objects.create(
            title='Тестовый слайд',
            order=1
        )

    def test_slide_creation(self):
        """Тест создания слайда."""
        self.assertEqual(self.slide.title, 'Тестовый слайд')
        self.assertEqual(self.slide.order, 1)

    def test_slide_str_representation(self):
        """Тест строкового представления слайда."""
        self.assertEqual(str(self.slide), 'Тестовый слайд')

    def test_slide_empty_title_validation(self):
        """Тест валидации пустого названия."""
        slide = Slide(title='', order=2)
        with self.assertRaises(ValidationError):
            slide.full_clean()

    def test_slide_short_title_validation(self):
        """Тест валидации короткого названия (менее 3 символов)."""
        slide = Slide(title='АБ', order=3)
        with self.assertRaises(ValidationError):
            slide.full_clean()

    def test_slide_whitespace_title_validation(self):
        """Тест валидации названия из одних пробелов."""
        slide = Slide(title='   ', order=4)
        with self.assertRaises(ValidationError):
            slide.full_clean()

    def test_slide_ordering(self):
        """Тест упорядочивания слайдов."""
        slide2 = Slide.objects.create(title='Слайд 2', order=2)
        slide3 = Slide.objects.create(title='Слайд 3', order=3)
        
        slides = list(Slide.objects.all())
        self.assertEqual(slides[0].order, 1)
        self.assertEqual(slides[1].order, 2)
        self.assertEqual(slides[2].order, 3)

    def test_slide_created_at_field(self):
        """Тест автоматического заполнения поля created_at."""
        self.assertIsNotNone(self.slide.created_at)

    def test_multiple_slides(self):
        """Тест создания нескольких слайдов."""
        for i in range(5):
            Slide.objects.create(
                title=f'Слайд {i+1}',
                order=i+1
            )
        
        self.assertEqual(Slide.objects.count(), 6)
