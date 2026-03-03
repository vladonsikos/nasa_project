from django.db import models
from django.core.exceptions import ValidationError
from filer.fields.image import FilerImageField


class Slide(models.Model):
    """
    Модель для хранения слайдов галереи.
    
    Атрибуты:
        title (str): Название слайда
        image (FilerImageField): Изображение слайда
        order (int): Порядок отображения слайда (автоматический)
    """
    title = models.CharField(
        max_length=255,
        verbose_name='Название',
        blank=False,
        help_text='Введите название слайда'
    )
    image = FilerImageField(
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Изображение',
        related_name='slides',
        help_text='Загрузите изображение для слайда'
    )
    order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True,
        verbose_name='Порядок'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title
    
    def clean(self):
        """Валидация модели."""
        if not self.title or not self.title.strip():
            raise ValidationError('Название не может быть пустым.')
        if len(self.title) < 3:
            raise ValidationError('Название должно быть минимум 3 символа.')
