from pathlib import Path

import environ

env = environ.Env(DEBUG=(bool, False))

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env("SECRET_KEY", default="insecure-dev-key-cambiar-en-produccion")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.staticfiles",  # Necesario para servir CSS/JS de Swagger UI
    "rest_framework",  # Django REST Framework
    "drf_spectacular",  # Generador de Swagger/OpenAPI
    "estudiantes",  # Nuestra app de estudiantes
    "cursos",  # Nuestra app de cursos
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"

# Necesario para que drf-spectacular renderice la plantilla swagger_ui.html
# APP_DIRS=True hace que Django busque plantillas dentro de la carpeta
# 'templates/' de cada app instalada (incluyendo drf_spectacular).
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

# Leer la URL de conexión a PostgreSQL desde variable de entorno
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgresql://matricula_user:matricula_pass@localhost:5432/matricula_db",
    )
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# Ruta base para archivos estáticos (CSS/JS de Swagger UI, admin, etc.)
STATIC_URL = "/static/"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Matricula Service",
    "DESCRIPTION": "Gestión de estudiantes, cursos y matrículas",
    "VERSION": "1.0.0",
}
