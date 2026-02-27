from .settings import *

# Используем SQLite в памяти для тестов
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Можно также отключить создание реальных папок для медиа (по желанию)
import tempfile
MEDIA_ROOT = tempfile.mkdtemp()
