"""
Configuration Python - Fichier centralisé pour toutes les configurations
"""

import os
import logging
import logging.config
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# ============================================================================
# CONFIGURATIONS GÉNÉRALES
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_NAME = "mon-app"
VERSION = "1.0.0"

# ============================================================================
# ENVIRONNEMENT
# ============================================================================

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
DEBUG = ENVIRONMENT == 'development'
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# ============================================================================
# BASE DE DONNÉES
# ============================================================================

DATABASE_CONFIG = {
    'development': {
        'engine': 'sqlite:///dev.db',
        'echo': True,
    },
    'production': {
        'engine': os.getenv('DATABASE_URL', 'postgresql://localhost/prod'),
        'echo': False,
    },
    'testing': {
        'engine': 'sqlite:///:memory:',
        'echo': False,
    }
}

DATABASE_URL = DATABASE_CONFIG[ENVIRONMENT]['engine']

# ============================================================================
# API ET CLÉS
# ============================================================================

API_KEY = os.getenv('API_KEY', '')
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')
API_TIMEOUT = int(os.getenv('API_TIMEOUT', 30))

# ============================================================================
# LOGGING
# ============================================================================

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': str(BASE_DIR / 'logs' / 'app.log'),
            'formatter': 'detailed',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': str(BASE_DIR / 'logs' / 'errors.log'),
            'formatter': 'detailed',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

# Créer le répertoire des logs s'il n'existe pas
logs_dir = BASE_DIR / 'logs'
logs_dir.mkdir(exist_ok=True)

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# ============================================================================
# FLASK CONFIGURATION
# ============================================================================

class FlaskConfig:
    """Configuration Flask de base"""
    SECRET_KEY = SECRET_KEY
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = DEBUG


class FlaskDevelopmentConfig(FlaskConfig):
    """Configuration développement Flask"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class FlaskProductionConfig(FlaskConfig):
    """Configuration production Flask"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class FlaskTestingConfig(FlaskConfig):
    """Configuration tests Flask"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


FLASK_CONFIG = {
    'development': FlaskDevelopmentConfig,
    'production': FlaskProductionConfig,
    'testing': FlaskTestingConfig,
    'default': FlaskDevelopmentConfig
}

# ============================================================================
# DJANGO CONFIGURATION
# ============================================================================

DJANGO_CONFIG = {
    'SECRET_KEY': SECRET_KEY,
    'DEBUG': DEBUG,
    'ALLOWED_HOSTS': os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(','),
    'INSTALLED_APPS': [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'postgres'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    },
    'MIDDLEWARE': [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
}

# ============================================================================
# FASTAPI CONFIGURATION
# ============================================================================

FASTAPI_CONFIG = {
    'title': PROJECT_NAME,
    'version': VERSION,
    'description': 'API FastAPI',
    'debug': DEBUG,
}

# ============================================================================
# SESSION ET CACHE
# ============================================================================

SESSION_CONFIG = {
    'session_type': 'filesystem',
    'permanent': False,
    'cookie_secure': not DEBUG,
    'cookie_httponly': True,
    'cookie_samesite': 'Lax',
}

CACHE_CONFIG = {
    'type': 'simple' if DEBUG else 'redis',
    'default_timeout': 300,
}

# ============================================================================
# CORS (Cross-Origin Resource Sharing)
# ============================================================================

CORS_CONFIG = {
    'origins': os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:8000').split(','),
    'allow_credentials': True,
    'allow_methods': ['*'],
    'allow_headers': ['*'],
}

# ============================================================================
# JWT / AUTHENTICATION
# ============================================================================

JWT_CONFIG = {
    'algorithm': 'HS256',
    'expiration_delta_minutes': 60,
    'refresh_expiration_delta_days': 7,
}

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

EMAIL_CONFIG = {
    'smtp_server': os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('EMAIL_SMTP_PORT', 587)),
    'sender_email': os.getenv('EMAIL_SENDER', 'noreply@example.com'),
    'sender_password': os.getenv('EMAIL_PASSWORD', ''),
    'use_tls': True,
}

# ============================================================================
# PAGINATION
# ============================================================================

PAGINATION_CONFIG = {
    'default_page_size': 20,
    'max_page_size': 100,
}

# ============================================================================
# UPLOAD DES FICHIERS
# ============================================================================

UPLOAD_CONFIG = {
    'max_file_size': 10 * 1024 * 1024,  # 10 MB
    'allowed_extensions': {'pdf', 'txt', 'csv', 'jpg', 'jpeg', 'png', 'gif'},
    'upload_folder': str(BASE_DIR / 'uploads'),
}

# Créer le dossier uploads s'il n'existe pas
upload_folder = Path(UPLOAD_CONFIG['upload_folder'])
upload_folder.mkdir(exist_ok=True)

# ============================================================================
# FONCTION UTILITAIRE
# ============================================================================

def get_config(framework='flask'):
    """
    Retourne la configuration pour un framework donné
    
    Args:
        framework (str): 'flask', 'django', 'fastapi'
    
    Returns:
        dict: Configuration du framework
    """
    if framework == 'flask':
        return FLASK_CONFIG[ENVIRONMENT]
    elif framework == 'django':
        return DJANGO_CONFIG
    elif framework == 'fastapi':
        return FASTAPI_CONFIG
    else:
        raise ValueError(f"Framework '{framework}' non supporté")


# ============================================================================
# AFFICHER LA CONFIGURATION AU DÉMARRAGE
# ============================================================================

if __name__ == '__main__':
    print(f"Environment: {ENVIRONMENT}")
    print(f"Debug: {DEBUG}")
    print(f"Database: {DATABASE_URL}")
    print(f"Logging Config: {LOGGING_CONFIG['handlers'].keys()}")
