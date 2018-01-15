from .settings import *

LOCAL_SETTINGS = True

if ON_OPENSHIFT:
    DEBUG = False
    DATABASES = {
        'default': {
            'NAME': os.getenv('POSTGRESQL_DATABASE'),
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': os.getenv('POSTGRESQL_USER'),
            'PASSWORD': os.getenv('POSTGRESQL_PASSWORD'),
            'HOST': os.getenv('POSTGRESQL_SERVICE_HOST'),
            'PORT': os.getenv('POSTGRESQL_SERVICE_PORT'),
        }
    }
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            },
        },
    }
else:
    DEBUG = True
    ALLOWED_HOSTS = []
    DATABASES = {
        'default': {
            'NAME': 'statscollect',
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'postgres',
            'PASSWORD': 'root'
        }
    }

