from django.db import models
from filer.fields.image import FilerImageField


class Slide(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = FilerImageField(
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Изображение',
        related_name='slides'
    )
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'

    def __str__(self):
        return self.title
