DEBUG = True

# Celery configuration options
import djcelery
djcelery.setup_loader()
CELERY_RESULT_BACKEND = "database"
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_ALWAYS_EAGER = DEBUG

SECRET_KEY = 'Shhhhhhhhh!'

USE_TZ = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'snappybouncer.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Third-party apps
    'south',
    'djcelery',
    'tastypie',
    # Us
    'snappybouncer'
]

ROOT_URLCONF = 'snappybouncer.urls'
