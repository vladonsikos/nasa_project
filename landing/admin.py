from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from .models import Slide


@admin.register(Slide)
class SlideAdmin(SortableAdminMixin, admin.ModelAdmin):
    """
    Администратор для управления слайдами галереи.
    
    Функции:
    - Drag & drop сортировка слайдов
    - Поиск по названию
    - Фильтрация по дате создания
    - Превью изображений в списке
    - Оптимизация запросов к БД
    """
    list_display = ('order', 'preview_image', 'title', 'created_at', 'image_size')
    list_display_links = ('preview_image', 'title')
    list_filter = ('created_at', 'order')
    search_fields = ('title',)
    readonly_fields = ('order', 'created_at', 'preview_image_large', 'image_info')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'order', 'created_at')
        }),
        ('Изображение', {
            'fields': ('image', 'preview_image_large', 'image_info')
        }),
    )
    
    list_select_related = ('image',)
    list_per_page = 25
    ordering = ('order',)

    def preview_image(self, obj):
        """Миниатюра изображения в списке."""
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px; border-radius:3px; object-fit:cover;" alt="{}"/>',
                obj.image.url,
                obj.title
            )
        return '—'
    preview_image.short_description = 'Превью'

    def preview_image_large(self, obj):
        """Большое превью в форме редактирования."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:400px; max-height:300px; border-radius:4px;" alt="{}"/>',
                obj.image.url,
                obj.title
            )
        return 'Изображение не загружено'
    preview_image_large.short_description = 'Предпросмотр'

    def image_size(self, obj):
        """Размер изображения в списке."""
        if obj.image and obj.image.size:
            size_mb = obj.image.size / (1024 * 1024)
            return f'{size_mb:.2f} MB'
        return '—'
    image_size.short_description = 'Размер'

    def image_info(self, obj):
        """Информация об изображении в форме редактирования."""
        if obj.image:
            info = f'Размер: {obj.image.size / (1024 * 1024):.2f} MB'
            if hasattr(obj.image, 'width') and hasattr(obj.image, 'height'):
                info += f'<br/>Разрешение: {obj.image.width}x{obj.image.height}px'
            return format_html(info)
        return 'Информация недоступна'
    image_info.short_description = 'Информация об изображении'

    def save_model(self, request, obj, form, change):
        """Валидация при сохранении."""
        obj.full_clean()
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('filer/css/admin_filer.css',)
        }
        js = (
            'admin/js/jquery.init.js',
            'filer/js/addons/popup_handling.js',
            'filer/js/addons/widget.js',
        )
