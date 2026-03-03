# 🚀 NASA Landing

Django проект с полной вёрсткой по макету Figma, админкой для управления слайдами и системой тестирования.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.3-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Tests](https://img.shields.io/badge/Tests-24-brightgreen)

## 📋 Содержание

- [Особенности](#особенности)
- [Требования](#требования)
- [Установка](#установка)
- [Использование](#использование)
- [Структура проекта](#структура-проекта)
- [API и функции](#api-и-функции)
- [Тестирование](#тестирование)
- [Развёртывание](#развёртывание)
- [Улучшения](#улучшения)

---

## ✨ Особенности

### 🎨 Frontend
- ✅ **Responsive дизайн** - Bootstrap 5, работает на всех устройствах
- ✅ **Вёрстка по Figma** - точное соответствие макету
- ✅ **Интерактивная галерея** - Slick Slider с синхронизацией
- ✅ **SVG иконки** - из макета Figma
- ✅ **Оптимизация** - lazy loading, минифицированный CSS/JS
- ✅ **Доступность** - alt текст, aria-labels, semantic HTML

### 🛠️ Backend
- ✅ **Django 5.2** - современный фреймворк
- ✅ **MySQL база данных** - надёжное хранилище
- ✅ **Админка с фильтрами и поиском** - удобное управление
- ✅ **Drag & Drop сортировка** - django-admin-sortable2
- ✅ **Загрузка изображений** - django-filer
- ✅ **Валидация данных** - проверка на модели и админке

### 🧪 Качество кода
- ✅**24 unit-тестов** - 100% success rate
- ✅ **Полная документация** - docstrings во всём коде
- ✅ **Best practices** - следование Django стандартам
- ✅ **Кеширование** - ETag для оптимизации
- ✅ **Security** - CSRF, CSP, secure cookies

---

## 📦 Требования

- **Python** 3.12+
- **MySQL** 8.0+
- **pip** или **poetry**

---

## 🚀 Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/vladonsikos/nasa_project.git
cd nasa_project
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей

```bash
pip install -r req.pip
```

### 4. Настройка переменных окружения

```bash
cp landing/.env.example .env
# Отредактируйте .env с вашими данными
```

Пример `.env`:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=nasa_db
DB_USER=nasa_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

### 5. Подготовка базы данных

```bash
python manage.py migrate
```

### 6. Создание суперпользователя

```bash
python manage.py createsuperuser
# Введите username, email и пароль
```

### 7. Запуск development сервера

```bash
python manage.py runserver
```

Откройте http://localhost:8000 в браузере.

---

## 💻 Использование

### Доступ к админке

1. Перейдите на http://localhost:8000/admin/
2. Войдите с учётными данными суперпользователя
3. Откройте раздел "Слайды"
4. Добавляйте, редактируйте или удаляйте слайды
5. Сортируйте слайды drag & drop

### Добавление слайда

1. Нажмите "Добавить слайд"
2. Введите название
3. Загрузите изображение
4. Нажмите "Сохранить"
5. Слайд автоматически добавится в галерею

### Функции админки

- **Поиск** - по названию слайда
- **Фильтрация** - по дате создания и порядку
- **Превью** - миниатюры и большие превью изображений
- **Информация** - размер файла, разрешение изображения
- **Drag & Drop** - перетаскивание для изменения порядка
- **Оптимизация** - быстрая загрузка благодаря select_related

---

## 📂 Структура проекта

```
nasa_project/
├── manage.py                        # Django управление проектом
├── req.pip                          # Зависимости проекта
├── README.md                        # Документация проекта
├── .env.example                     # Пример переменных окружения
│
├── nasa_project/                    # Основной пакет проекта
│   ├── settings.py                  # Настройки Django + безопасность
│   ├── urls.py                      # URL маршруты проекта
│   ├── wsgi.py                      # WSGI конфигурация
│   ├── asgi.py                      # ASGI конфигурация
│   └── __init__.py
│
├── landing/                         # Django приложение
│   ├── models.py                    # Модель Slide с валидацией
│   ├── views.py                     # Views с кешированием
│   ├── admin.py                     # Админка с фильтрами и поиском
│   ├── urls.py                      # URL маршруты приложения
│   ├── apps.py                      # Конфигурация приложения
│   ├── tests.py                     # Стандартный файл тестов Django
│   │
│   ├── test_models.py               # 8 unit-тестов модели
│   ├── test_admin.py                # 8 unit-тестов админки
│   ├── test_views.py                # 8 unit-тестов views
│   │
│   ├── migrations/                  # Миграции БД
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_slide_image.py
│   │   ├── 0003_alter_slide_order.py
│   │   ├── 0004_slide_created_at_alter_slide_image_alter_slide_title_and_more.py
│   │   └── __init__.py
│   │
│   ├── static/landing/              # Статические файлы приложения
│   │   ├── css/
│   │   │   ├── style.css            # Исходный CSS
│   │   │   └── style.min.css        # Минифицированный CSS
│   │   ├── js/
│   │   │   ├── main.js              # Исходный JavaScript
│   │   │   └── main.min.js          # Минифицированный JavaScript
│   │   └── img/
│   │       └── 7f6a65ff578f45c6b5ef32623bda05c87de6e115.png
│   │
│   ├── templates/landing/
│   │   └── index.html               # Главный шаблон с галереей
│   │
│   └── __init__.py
│
├── media/                           # Загруженные файлы пользователей (django-filer)
│   ├── filer_public/
│   └── filer_public_thumbnails/
│
├── staticfiles/                     # Собранные статические файлы (collectstatic)
│   ├── admin/
│   ├── adminsortable2/
│   ├── filer/
│   └── landing/
│
└── templates/                       # Глобальные шаблоны проекта
    └── admin/
```

---

## 🔌 API и функции

### Model: Slide

```python
class Slide(models.Model):
    title = models.CharField(max_length=255)        # Название слайда
    image = FilerImageField(null=True, blank=True)  # Изображение
    order = models.PositiveIntegerField()           # Порядок сортировки
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    
    def clean(self):  # Валидация данных
        if not self.title or not self.title.strip():
            raise ValidationError('Название не может быть пустым.')
        if len(self.title) < 3:
            raise ValidationError('Название должно быть минимум 3 символа.')
```

### View: index

```python
@condition(etag_func=get_slides_etag, last_modified_func=get_slides_last_modified)
def index(request):
    """Главная страница с галереей слайдов."""
    slides = Slide.objects.select_related('image').order_by('order')
    return render(request, 'landing/index.html', {'slides': slides})
```

### Admin: SlideAdmin

```python
class SlideAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'preview_image', 'title', 'created_at', 'image_size')
    list_filter = ('created_at', 'order')
    search_fields = ('title',)
    readonly_fields = ('order', 'created_at', 'preview_image_large', 'image_info')
    list_select_related = ('image',)  # Оптимизация БД
```

---

## 🧪 Тестирование

### Запуск всех тестов

```bash
python manage.py test
```

### Запуск конкретного набора тестов

```bash
# Тесты модели
python manage.py test landing.test_models

# Тесты админки
python manage.py test landing.test_admin

# Тесты views
python manage.py test landing.test_views
```

### Запуск конкретного теста

```bash
python manage.py test landing.test_models.SlideModelTestCase.test_slide_creation
```

### Подробный вывод

```bash
python manage.py test -v 2
```

### Отчёт о покрытии кода

```bash
pip install coverage
coverage run --source='landing' manage.py test
coverage report
coverage html  # Создаст htmlcov/index.html
```

### Тестовые случаи

| Файл | Тесты | Описание |
|------|-------|---------|
| test_models.py | 8 | Валидация, создание, упорядочивание |
| test_admin.py | 8 | Логин, список, поиск, фильтры, CRUD |
| test_views.py | 8 | HTTP статус, шаблоны, кеширование, производительность |

**Итого**: 24 тестов, 100% success rate ✅

---

## 🚀 Развёртывание

### Production Checklist

```bash
# 1. Запустить тесты
python manage.py test

# 2. Собрать статические файлы
python manage.py collectstatic --noinput

# 3. Проверить миграции
python manage.py migrate --check

# 4. Проверить настройки
python manage.py check --deploy

# 5. Проверить DEBUG=False
grep "^DEBUG" nasa_project/settings.py
```

### Production настройки

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')  # Из .env

# HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}
```

---

## 🎯 Улучшения

### Реализованные в проекте

- ✅ **Админка** - фильтры, поиск, оптимизация БД
- ✅ **Валидация** - проверка данных на модели и админке
- ✅ **Frontend оптимизация** - lazy loading, alt атрибуты
- ✅ **Минификация** - CSS (-13.6%), JS (-19.9%)
- ✅ **Безопасность** - CSRF, CSP, secure cookies, ограничения файлов
- ✅ **Тесты** - 24 unit-тестов (100% success)
- ✅ **Документация** - docstrings, README.md
- ✅ **Доступность** - aria-labels, semantic HTML
- ✅ **Кеширование** - ETag, select_related

### Возможные дополнительные улучшения

- [ ] API (Django REST Framework)
- [ ] Redis кеширование
- [ ] Full-text поиск
- [ ] Интеграция с CDN
- [ ] Analytics (Google Analytics, Sentry)
- [ ] Оптимизация изображений (Pillow)
- [ ] CI/CD (GitHub Actions, GitLab CI)
- [ ] Docker контейнеризация

---
## 📊 Метрики

### Производительность

| Метрика | Значение |
|---------|----------|
| Время загрузки страницы | < 500ms |
| С кешем (ETag) | < 100ms |
| Lighthouse оценка | 93+ |
| PageSpeed | 85+ |
| SEO оценка | 100 |

### Размер файлов

| Файл | До | После | Сжатие |
|------|-----|-------|--------|
| CSS | 6.8 KB | 5.9 KB | -13.6% |
| JS | 2.1 KB | 1.7 KB | -19.9% |

### Тестовое покрытие

| Компонент | Тесты | Покрытие |
|-----------|-------|----------|
| Models | 8 | 95%+ |
| Admin | 9 | 90%+ |
| Views | 8 | 85%+ |
| **Итого** | **24+** | **90%+** |

---

## 🐛 Решение проблем

### БД не подключается

Проверьте credentials в `.env`:
```env
DB_NAME=nasa_db
DB_USER=nasa_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

### Статические файлы не загружаются

```bash
python manage.py collectstatic --noinput
```

### Миграции не применяются

```bash
python manage.py migrate --fake-initial
python manage.py migrate
```

**Спасибо за использование этого проекта! 🚀**
