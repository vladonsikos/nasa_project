from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from .models import Slide

@admin.register(Slide)
class SlideAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'preview_image', 'title')
    list_display_links = ('preview_image', 'title')

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px; border-radius:3px;" />', obj.image.url)
        return '—'
    preview_image.short_description = 'Превью'

    class Media:
        css = {
            'all': ('filer/css/admin_filer.css',)
        }
        js = (
            'admin/js/jquery.init.js',  # важно: инициализирует django.jQuery
            'filer/js/addons/popup_handling.js',
            'filer/js/addons/widget.js',
        )
