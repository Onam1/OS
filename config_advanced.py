"""
Configurations supplémentaires avancées pour l'application
Inclut: Redis, Celery, Sentry, AWS, Stripe, etc.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# REDIS CONFIGURATION
# ============================================================================

REDIS_CONFIG = {
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': int(os.getenv('REDIS_PORT', 6379)),
    'db': int(os.getenv('REDIS_DB', 0)),
    'password': os.getenv('REDIS_PASSWORD', None),
    'socket_connect_timeout': 5,
    'socket_keepalive': True,
    'socket_keepalive_options': {
        1: 1,  # TCP_KEEPIDLE
        2: 3,  # TCP_KEEPINTVL
        3: 5,  # TCP_KEEPCNT
    },
    'connection_pool_kwargs': {
        'max_connections': 50,
        'retry_on_timeout': True,
    }
}

REDIS_URL = f"redis://:{REDIS_CONFIG['password']}@{REDIS_CONFIG['host']}:{REDIS_CONFIG['port']}/{REDIS_CONFIG['db']}" if REDIS_CONFIG['password'] else f"redis://{REDIS_CONFIG['host']}:{REDIS_CONFIG['port']}/{REDIS_CONFIG['db']}"

# ============================================================================
# CELERY CONFIGURATION (Tâches asynchrones)
# ============================================================================

CELERY_CONFIG = {
    'broker_url': REDIS_URL,
    'result_backend': REDIS_URL,
    'task_serializer': 'json',
    'accept_content': ['json'],
    'result_serializer': 'json',
    'timezone': 'UTC',
    'enable_utc': True,
    'task_track_started': True,
    'task_time_limit': 30 * 60,  # 30 minutes
    'task_soft_time_limit': 25 * 60,  # 25 minutes
    'worker_prefetch_multiplier': 1,
    'worker_max_tasks_per_child': 1000,
    'beat_schedule': {
        'cleanup-old-files': {
            'task': 'tasks.cleanup_old_files',
            'schedule': 3600.0,  # Chaque heure
        },
        'send-daily-report': {
            'task': 'tasks.send_daily_report',
            'schedule': 86400.0,  # Quotidien
            'options': {'queue': 'email'}
        },
    }
}

# ============================================================================
# SENTRY CONFIGURATION (Error tracking)
# ============================================================================

SENTRY_CONFIG = {
    'dsn': os.getenv('SENTRY_DSN', ''),
    'environment': os.getenv('ENVIRONMENT', 'development'),
    'traces_sample_rate': 0.1,
    'profiles_sample_rate': 0.1,
    'attach_stacktrace': True,
    'send_default_pii': False,
    'max_breadcrumbs': 50,
}

# ============================================================================
# AWS S3 CONFIGURATION (Cloud storage)
# ============================================================================

AWS_CONFIG = {
    'access_key_id': os.getenv('AWS_ACCESS_KEY_ID', ''),
    'secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY', ''),
    'region_name': os.getenv('AWS_REGION', 'us-east-1'),
    's3_bucket': os.getenv('AWS_S3_BUCKET', ''),
    's3_custom_domain': os.getenv('AWS_S3_CUSTOM_DOMAIN', None),
    's3_use_ssl': True,
    's3_signature_version': 's3v4',
    's3_addressing_style': 'virtual',
}

# ============================================================================
# STRIPE CONFIGURATION (Paiements)
# ============================================================================

STRIPE_CONFIG = {
    'api_key': os.getenv('STRIPE_API_KEY', ''),
    'public_key': os.getenv('STRIPE_PUBLIC_KEY', ''),
    'webhook_secret': os.getenv('STRIPE_WEBHOOK_SECRET', ''),
    'api_version': '2023-10-16',
}

# ============================================================================
# TWILIO CONFIGURATION (SMS/Appels)
# ============================================================================

TWILIO_CONFIG = {
    'account_sid': os.getenv('TWILIO_ACCOUNT_SID', ''),
    'auth_token': os.getenv('TWILIO_AUTH_TOKEN', ''),
    'phone_number': os.getenv('TWILIO_PHONE_NUMBER', ''),
    'api_base_url': 'https://api.twilio.com',
}

# ============================================================================
# SENDGRID CONFIGURATION (Email service)
# ============================================================================

SENDGRID_CONFIG = {
    'api_key': os.getenv('SENDGRID_API_KEY', ''),
    'from_email': os.getenv('SENDGRID_FROM_EMAIL', 'noreply@example.com'),
    'from_name': os.getenv('SENDGRID_FROM_NAME', 'Mon App'),
}

# ============================================================================
# JWT ADVANCED CONFIGURATION
# ============================================================================

JWT_ADVANCED_CONFIG = {
    'secret_key': os.getenv('JWT_SECRET_KEY', 'super-secret-key'),
    'algorithm': 'HS256',
    'access_token_expire_minutes': 30,
    'refresh_token_expire_days': 7,
    'reset_token_expire_hours': 24,
    'verify_email_token_expire_hours': 48,
    'issuer': 'mon-app',
    'audience': 'mon-app-users',
}

# ============================================================================
# OAUTH2 CONFIGURATION (Google, GitHub, Microsoft)
# ============================================================================

OAUTH2_CONFIG = {
    'google': {
        'client_id': os.getenv('GOOGLE_OAUTH2_CLIENT_ID', ''),
        'client_secret': os.getenv('GOOGLE_OAUTH2_CLIENT_SECRET', ''),
        'redirect_uri': os.getenv('GOOGLE_OAUTH2_REDIRECT_URI', 'http://localhost:8000/auth/google/callback'),
    },
    'github': {
        'client_id': os.getenv('GITHUB_OAUTH2_CLIENT_ID', ''),
        'client_secret': os.getenv('GITHUB_OAUTH2_CLIENT_SECRET', ''),
        'redirect_uri': os.getenv('GITHUB_OAUTH2_REDIRECT_URI', 'http://localhost:8000/auth/github/callback'),
    },
    'microsoft': {
        'client_id': os.getenv('MICROSOFT_OAUTH2_CLIENT_ID', ''),
        'client_secret': os.getenv('MICROSOFT_OAUTH2_CLIENT_SECRET', ''),
        'redirect_uri': os.getenv('MICROSOFT_OAUTH2_REDIRECT_URI', 'http://localhost:8000/auth/microsoft/callback'),
    },
}

# ============================================================================
# MONITORING & OBSERVABILITY
# ============================================================================

MONITORING_CONFIG = {
    # Prometheus
    'prometheus_enabled': os.getenv('PROMETHEUS_ENABLED', 'false').lower() == 'true',
    'prometheus_port': int(os.getenv('PROMETHEUS_PORT', 8001)),
    
    # Datadog
    'datadog_enabled': os.getenv('DATADOG_ENABLED', 'false').lower() == 'true',
    'datadog_api_key': os.getenv('DATADOG_API_KEY', ''),
    'datadog_app_key': os.getenv('DATADOG_APP_KEY', ''),
    
    # New Relic
    'newrelic_enabled': os.getenv('NEWRELIC_ENABLED', 'false').lower() == 'true',
    'newrelic_license_key': os.getenv('NEWRELIC_LICENSE_KEY', ''),
}

# ============================================================================
# RATE LIMITING CONFIGURATION
# ============================================================================

RATE_LIMIT_CONFIG = {
    'enabled': True,
    'storage_url': REDIS_URL,
    'storage_options': {},
    'default_limits': [
        '200 per day',
        '50 per hour'
    ],
    'key_func': 'get_remote_address',
    'strategies': {
        'moving_window': True,
        'fixed_window': False,
    },
}

# ============================================================================
# SECURITY CONFIGURATION
# ============================================================================

SECURITY_CONFIG = {
    # CORS
    'cors_origins': os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','),
    'cors_credentials': True,
    'cors_methods': ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
    'cors_headers': ['*'],
    
    # HTTPS/SSL
    'force_https': os.getenv('FORCE_HTTPS', 'false').lower() == 'true',
    'ssl_redirect': True,
    'hsts_max_age': 31536000,  # 1 year
    
    # CSRF
    'csrf_enabled': True,
    'csrf_token_name': 'X-CSRF-Token',
    
    # Security Headers
    'x_frame_options': 'SAMEORIGIN',
    'x_content_type_options': 'nosniff',
    'x_xss_protection': '1; mode=block',
    'content_security_policy': "default-src 'self'",
}

# ============================================================================
# DATABASE ADVANCED CONFIGURATION
# ============================================================================

DATABASE_ADVANCED_CONFIG = {
    'sqlalchemy': {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'echo_pool': False,
        'echo': os.getenv('ENVIRONMENT', 'development') == 'development',
    },
    'mongodb': {
        'connection_string': os.getenv('MONGODB_URI', 'mongodb://localhost:27017'),
        'database': os.getenv('MONGODB_DB', 'myapp'),
        'max_pool_size': 50,
        'min_pool_size': 10,
    },
}

# ============================================================================
# ELASTICSEARCH CONFIGURATION
# ============================================================================

ELASTICSEARCH_CONFIG = {
    'hosts': os.getenv('ELASTICSEARCH_HOSTS', 'localhost:9200').split(','),
    'scheme': os.getenv('ELASTICSEARCH_SCHEME', 'http'),
    'username': os.getenv('ELASTICSEARCH_USERNAME', ''),
    'password': os.getenv('ELASTICSEARCH_PASSWORD', ''),
    'timeout': 20,
    'max_retries': 3,
    'index_prefix': os.getenv('ELASTICSEARCH_INDEX_PREFIX', 'myapp'),
}

# ============================================================================
# FILE STORAGE ADVANCED
# ============================================================================

FILE_STORAGE_CONFIG = {
    'type': os.getenv('FILE_STORAGE_TYPE', 'local'),  # 'local', 's3', 'gcs', 'azure'
    'local': {
        'upload_folder': os.getenv('UPLOAD_FOLDER', 'uploads'),
        'max_file_size': 100 * 1024 * 1024,  # 100 MB
    },
    's3': {
        'bucket': os.getenv('AWS_S3_BUCKET', ''),
        'region': os.getenv('AWS_REGION', 'us-east-1'),
    },
    'gcs': {
        'bucket': os.getenv('GCS_BUCKET', ''),
        'project_id': os.getenv('GCS_PROJECT_ID', ''),
    },
    'azure': {
        'container': os.getenv('AZURE_CONTAINER', ''),
        'account_name': os.getenv('AZURE_ACCOUNT_NAME', ''),
    },
}

# ============================================================================
# FEATURE FLAGS
# ============================================================================

FEATURE_FLAGS = {
    'new_dashboard': os.getenv('FEATURE_NEW_DASHBOARD', 'false').lower() == 'true',
    'beta_api': os.getenv('FEATURE_BETA_API', 'false').lower() == 'true',
    'advanced_analytics': os.getenv('FEATURE_ADVANCED_ANALYTICS', 'false').lower() == 'true',
    'dark_mode': os.getenv('FEATURE_DARK_MODE', 'true').lower() == 'true',
    'two_factor_auth': os.getenv('FEATURE_2FA', 'true').lower() == 'true',
}

# ============================================================================
# NOTIFICATION CONFIGURATION
# ============================================================================

NOTIFICATION_CONFIG = {
    'email': {
        'enabled': True,
        'provider': os.getenv('EMAIL_PROVIDER', 'sendgrid'),  # 'sendgrid', 'mailgun', 'smtp'
    },
    'sms': {
        'enabled': os.getenv('SMS_ENABLED', 'false').lower() == 'true',
        'provider': os.getenv('SMS_PROVIDER', 'twilio'),
    },
    'push': {
        'enabled': os.getenv('PUSH_ENABLED', 'false').lower() == 'true',
        'providers': {
            'ios': os.getenv('APPLE_PUSH_CERT', ''),
            'android': os.getenv('FCM_API_KEY', ''),
        }
    },
    'webhook': {
        'enabled': True,
        'retry_attempts': 3,
        'retry_delay': 60,  # secondes
    },
}

# ============================================================================
# CACHE ADVANCED CONFIGURATION
# ============================================================================

CACHE_ADVANCED_CONFIG = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': True,
        },
        'KEY_PREFIX': 'myapp',
        'TIMEOUT': 300,
    }
}

# ============================================================================
# API DOCUMENTATION CONFIGURATION
# ============================================================================

API_DOCS_CONFIG = {
    'swagger_enabled': True,
    'redoc_enabled': True,
    'openapi_version': '3.0.0',
    'openapi_url': '/api/openapi.json',
    'swagger_url': '/api/docs',
    'redoc_url': '/api/redoc',
}

# ============================================================================
# TESTING CONFIGURATION
# ============================================================================

TESTING_CONFIG = {
    'test_database': 'sqlite:///:memory:',
    'test_redis': 'fakeredis://localhost',
    'fixtures_path': 'tests/fixtures',
    'coverage_min_percentage': 80,
    'use_fixtures': True,
    'parallel_execution': True,
    'workers': 4,
}

# ============================================================================
# LOGGING ADVANCED CONFIGURATION
# ============================================================================

LOGGING_ADVANCED_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
            'formatter': 'json',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'sentry_sdk.integrations.logging.EventHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'sentry'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'myapp': {
            'handlers': ['console', 'file', 'sentry'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# ============================================================================
# PERFORMANCE OPTIMIZATION
# ============================================================================

PERFORMANCE_CONFIG = {
    'query_optimization': {
        'select_related': True,
        'prefetch_related': True,
        'use_only': True,
    },
    'caching': {
        'page_cache': True,
        'query_cache': True,
        'cache_timeout': 300,
    },
    'compression': {
        'gzip': True,
        'brotli': True,
        'min_size_bytes': 1024,
    },
}

# ============================================================================
# API RATE LIMITING TIERS
# ============================================================================

API_TIERS = {
    'free': {
        'requests_per_minute': 10,
        'requests_per_day': 1000,
        'concurrent_requests': 5,
    },
    'premium': {
        'requests_per_minute': 100,
        'requests_per_day': 100000,
        'concurrent_requests': 50,
    },
    'enterprise': {
        'requests_per_minute': None,  # Unlimited
        'requests_per_day': None,
        'concurrent_requests': None,
    },
}

# ============================================================================
# SUMMARY
# ============================================================================

ADVANCED_CONFIGS = {
    'redis': REDIS_CONFIG,
    'celery': CELERY_CONFIG,
    'sentry': SENTRY_CONFIG,
    'aws': AWS_CONFIG,
    'stripe': STRIPE_CONFIG,
    'twilio': TWILIO_CONFIG,
    'sendgrid': SENDGRID_CONFIG,
    'jwt': JWT_ADVANCED_CONFIG,
    'oauth2': OAUTH2_CONFIG,
    'monitoring': MONITORING_CONFIG,
    'rate_limit': RATE_LIMIT_CONFIG,
    'security': SECURITY_CONFIG,
    'elasticsearch': ELASTICSEARCH_CONFIG,
    'file_storage': FILE_STORAGE_CONFIG,
    'feature_flags': FEATURE_FLAGS,
    'notifications': NOTIFICATION_CONFIG,
    'api_docs': API_DOCS_CONFIG,
    'testing': TESTING_CONFIG,
}

if __name__ == '__main__':
    print("Advanced Configuration Loaded Successfully ✅")
    print(f"Available configurations: {list(ADVANCED_CONFIGS.keys())}")
