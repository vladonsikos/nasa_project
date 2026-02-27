import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory
from filer.models.imagemodels import Image
from filer.models.foldermodels import Folder
from adminsortable2.admin import SortableAdminMixin
from landing.models import Slide
from landing.admin import SlideAdmin

User = get_user_model()

# Фикстура для создания тестового изображения
@pytest.fixture
def test_image():
    return SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

# Фикстура для создания слайда с изображением через Filer
@pytest.fixture
def slide_with_image(db, test_image):
    folder = Folder.objects.create(name="Test Folder")
    filer_image = Image.objects.create(owner=None, file=test_image, folder=folder, original_filename="test.jpg")
    slide = Slide.objects.create(title="Test Slide", order=1, image=filer_image)
    return slide

# Фикстура для создания слайда без изображения
@pytest.fixture
def slide_without_image(db):
    return Slide.objects.create(title="No Image Slide", order=2)

# Фикстура для админ-клиента
@pytest.fixture
def admin_client(db, client):
    user = User.objects.create_superuser(username="admin", password="admin", email="admin@test.com")
    client.force_login(user)
    return client

# ========== ТЕСТЫ МОДЕЛИ ==========
@pytest.mark.django_db
class TestSlideModel:
    def test_slide_creation(self, slide_without_image):
        assert slide_without_image.title == "No Image Slide"
        assert slide_without_image.order == 2
        assert slide_without_image.image is None
        assert str(slide_without_image) == "No Image Slide"

    def test_slide_with_filer_image(self, slide_with_image):
        assert slide_with_image.image is not None
        assert slide_with_image.image.original_filename == "test.jpg"

    def test_slide_ordering(self, slide_without_image, slide_with_image):
        # Проверка Meta.ordering = ['order']
        slides = Slide.objects.all()
        assert slides[0] == slide_with_image  # order=1
        assert slides[1] == slide_without_image  # order=2

# ========== ТЕСТЫ АДМИНКИ ==========
@pytest.mark.django_db
class TestSlideAdmin:
    def test_admin_list_display(self, admin_client, slide_with_image):
        url = reverse('admin:landing_slide_changelist')
        response = admin_client.get(url)
        assert response.status_code == 200
        content = response.content.decode()
        # Проверяем наличие заголовков (русские названия)
        assert 'Порядок' in content
        assert 'Превью' in content
        assert 'Название' in content

    def test_admin_add_page_has_filer_widget(self, admin_client):
        url = reverse('admin:landing_slide_add')
        response = admin_client.get(url)
        assert response.status_code == 200
        content = response.content.decode()
        # Проверяем, что поле image использует виджет Filer (по наличию class="filer_file")
        assert 'filer_file' in content or 'related-widget-wrapper' in content

    def test_admin_sortable_mixin_used(self):
        # Проверяем, что в админке используется SortableAdminMixin
        assert SortableAdminMixin in SlideAdmin.__bases__

# ========== ТЕСТЫ VIEWS ==========
@pytest.mark.django_db
class TestViews:
    def test_home_page_status(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200

    def test_home_page_template(self, client):
        response = client.get(reverse('home'))
        assert 'landing/index.html' in [t.name for t in response.templates]

    def test_home_page_context_contains_slides(self, client, slide_with_image):
        response = client.get(reverse('home'))
        assert 'slides' in response.context
        assert len(response.context['slides']) >= 1
        assert slide_with_image in response.context['slides']

    def test_home_page_renders_slides(self, client, slide_with_image):
        response = client.get(reverse('home'))
        content = response.content.decode()
        # Проверяем, что название слайда и изображение упоминаются в HTML
        assert slide_with_image.title in content
        assert slide_with_image.image.url in content

# ========== ТЕСТЫ ШАБЛОНА (подключение CSS/JS) ==========
@pytest.mark.django_db
class TestTemplateIncludes:
    def test_bootstrap_included(self, client):
        response = client.get(reverse('home'))
        content = response.content.decode()
        # Bootstrap 5
        assert 'bootstrap.min.css' in content
        assert 'bootstrap.bundle.min.js' in content

    def test_slick_included(self, client):
        response = client.get(reverse('home'))
        content = response.content.decode()
        # Slick Slider
        assert 'slick.css' in content
        assert 'slick.min.js' in content

    def test_custom_js_included(self, client):
        response = client.get(reverse('home'))
        content = response.content.decode()
        assert 'landing/js/main.js' in content

    def test_custom_css_included(self, client):
        response = client.get(reverse('home'))
        content = response.content.decode()
        assert 'landing/css/style.css' in content

# ========== ТЕСТЫ СОРТИРОВКИ ==========
@pytest.mark.django_db
class TestSorting:
    def test_slides_ordered_by_order_field(self):
        Slide.objects.create(title="A", order=3)
        Slide.objects.create(title="B", order=1)
        Slide.objects.create(title="C", order=2)
        slides = Slide.objects.all()
        assert [s.title for s in slides] == ["B", "C", "A"]

# ========== ТЕСТЫ FILER (опционально) ==========
@pytest.mark.django_db
class TestFilerIntegration:
    def test_filer_image_can_be_attached_to_slide(self, test_image):
        folder = Folder.objects.create(name="Test")
        filer_image = Image.objects.create(file=test_image, folder=folder)
        slide = Slide.objects.create(title="Filer Slide", order=5, image=filer_image)
        assert slide.image == filer_image
        assert slide.image.file.read() == b"file_content"
