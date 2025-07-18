# 🏗️ LiveStock Tracker - Project Structure

## 📁 Complete Project Directory Structure

```
livestock_tracker/
├── 📁 livestock_tracker/                    # Main project directory
│   ├── 📄 __init__.py
│   ├── 📄 settings/                         # Settings module
│   │   ├── 📄 __init__.py
│   │   ├── 📄 base.py                       # Base settings
│   │   ├── 📄 development.py               # Development settings
│   │   ├── 📄 production.py                # Production settings
│   │   └── 📄 testing.py                   # Testing settings
│   ├── 📄 urls.py                          # Main URL configuration
│   ├── 📄 wsgi.py                          # WSGI configuration
│   ├── 📄 asgi.py                          # ASGI configuration (for WebSockets)
│   └── 📄 celery.py                        # Celery configuration
│
├── 📁 apps/                                # Django applications
│   ├── 📁 authentication/                  # User authentication & authorization
│   │   ├── 📄 __init__.py
│   │   ├── 📄 models.py                    # User model, roles, permissions
│   │   ├── 📄 serializers.py               # User serializers
│   │   ├── 📄 views.py                     # Auth views (login, register, profile)
│   │   ├── 📄 urls.py                      # Auth URLs
│   │   ├── 📄 permissions.py               # Custom permissions
│   │   ├── 📄 validators.py                # Input validators
│   │   ├── 📄 tests.py                     # Authentication tests
│   │   └── 📁 migrations/                  # Database migrations
│   │
│   ├── 📁 animals/                         # Animal management
│   │   ├── 📄 __init__.py
│   │   ├── 📄 models.py                    # Animal, Location, AnimalHistory
│   │   ├── 📄 serializers.py               # Animal serializers
│   │   ├── 📄 views.py                     # CRUD views for animals
│   │   ├── 📄 urls.py                      # Animal URLs
│   │   ├── 📄 filters.py                   # Animal filtering logic
│   │   ├── 📄 signals.py                   # Django signals for animal events
│   │   ├── 📄 utils.py                     # Utility functions
│   │   ├── 📄 tests.py                     # Animal tests
│   │   └── 📁 migrations/                  # Database migrations
│   │
│   ├── 📁 health/                          # Health monitoring & records
│   │   ├── 📄 __init__.py
│   │   ├── 📄 models.py                    # HealthEvent, Vaccination, Treatment
│   │   ├── 📄 serializers.py               # Health serializers
│   │   ├── 📄 views.py                     # Health record views
│   │   ├── 📄 urls.py                      # Health URLs
│   │   ├── 📄 filters.py                   # Health filtering
│   │   ├── 📄 tasks.py                     # Celery tasks for health reminders
│   │   ├── 📄 tests.py                     # Health tests
│   │   └── 📁 migrations/                  # Database migrations
│   │
│   ├── 📁 cameras/                         # Camera feed management
│   │   ├── 📄 __init__.py
│   │   ├── 📄 models.py                    # CameraFeed, CameraSnapshot
│   │   ├── 📄 serializers.py               # Camera serializers
│   │   ├── 📄 views.py                     # Camera views
│   │   ├── 📄 urls.py                      # Camera URLs
│   │   ├── 📄 services.py                  # Camera streaming services
│   │   ├── 📄 utils.py                     # Camera utilities
│   │   ├── 📄 tests.py                     # Camera tests
│   │   └── 📁 migrations/                  # Database migrations
│   │
│   ├── 📁 notifications/                   # SMS, Voice, USSD integration
│   │   ├── 📄 __init__.py
│   │   ├── 📄 models.py                    # Notification, SMSLog, VoiceCall
│   │   ├── 📄 serializers.py               # Notification serializers
│   │   ├── 📄 views.py                     # Notification views
│   │   ├── 📄 urls.py                      # Notification URLs
│   │   ├── 📄 services.py                  # External API integrations
│   │   ├── 📄 tasks.py                     # Celery tasks for notifications
│   │   ├── 📄 ussd_handlers.py             # USSD session handlers
│   │   ├── 📄 tests.py                     # Notification tests
│   │   └── 📁 migrations/                  # Database migrations
│   │
│   ├── 📁 chatbot/                         # Chatbot integration
│   │   ├── 📄 __init__.py
│   │   ├── 📄 models.py                    # ChatSession, ChatMessage
│   │   ├── 📄 serializers.py               # Chat serializers
│   │   ├── 📄 views.py                     # Chat views
│   │   ├── 📄 urls.py                      # Chat URLs
│   │   ├── 📄 services.py                  # NLP processing services
│   │   ├── 📄 intent_handlers.py           # Intent processing
│   │   ├── 📄 entity_extractors.py         # Entity extraction
│   │   ├── 📄 tests.py                     # Chatbot tests
│   │   └── 📁 migrations/                  # Database migrations
│   │
│   ├── 📁 analytics/                       # Analytics & reporting
│   │   ├── 📄 __init__.py
│   │   ├── 📄 models.py                    # Analytics models
│   │   ├── 📄 serializers.py               # Analytics serializers
│   │   ├── 📄 views.py                     # Analytics views
│   │   ├── 📄 urls.py                      # Analytics URLs
│   │   ├── 📄 services.py                  # Analytics processing
│   │   ├── 📄 reports.py                   # Report generation
│   │   ├── 📄 tests.py                     # Analytics tests
│   │   └── 📁 migrations/                  # Database migrations
│   │
│   ├── 📁 tracking/                        # Real-time tracking
│   │   ├── 📄 __init__.py
│   │   ├── 📄 models.py                    # LocationData, TrackingDevice
│   │   ├── 📄 serializers.py               # Tracking serializers
│   │   ├── 📄 views.py                     # Tracking views
│   │   ├── 📄 urls.py                      # Tracking URLs
│   │   ├── 📄 consumers.py                 # WebSocket consumers
│   │   ├── 📄 routing.py                   # WebSocket routing
│   │   ├── 📄 services.py                  # Tracking services
│   │   ├── 📄 tests.py                     # Tracking tests
│   │   └── 📁 migrations/                  # Database migrations
│   │
│   └── 📁 core/                            # Core utilities & shared code
│       ├── 📄 __init__.py
│       ├── 📄 models.py                    # Base models
│       ├── 📄 serializers.py               # Base serializers
│       ├── 📄 views.py                     # Base views
│       ├── 📄 permissions.py               # Shared permissions
│       ├── 📄 pagination.py                # Custom pagination
│       ├── 📄 exceptions.py                # Custom exceptions
│       ├── 📄 middleware.py                # Custom middleware
│       ├── 📄 utils.py                     # Shared utilities
│       ├── 📄 validators.py                # Shared validators
│       └── 📄 tests.py                     # Core tests
│
├── 📁 config/                              # Configuration files
│   ├── 📄 nginx.conf                       # Nginx configuration
│   ├── 📄 gunicorn.conf.py                 # Gunicorn configuration
│   ├── 📄 supervisor.conf                  # Supervisor configuration
│   ├── 📄 redis.conf                       # Redis configuration
│   └── 📄 celery.conf                      # Celery configuration
│
├── 📁 docker/                              # Docker configuration
│   ├── 📄 Dockerfile                       # Main Dockerfile
│   ├── 📄 docker-compose.yml               # Docker Compose for development
│   ├── 📄 docker-compose.prod.yml          # Docker Compose for production
│   ├── 📄 docker-compose.test.yml          # Docker Compose for testing
│   └── 📁 scripts/                         # Docker scripts
│       ├── 📄 entrypoint.sh                # Container entrypoint
│       ├── 📄 wait-for-it.sh               # Wait for services script
│       └── 📄 init-db.sh                   # Database initialization
│
├── 📁 docs/                                # Documentation
│   ├── 📄 API.md                           # API documentation
│   ├── 📄 DEPLOYMENT.md                    # Deployment guide
│   ├── 📄 DEVELOPMENT.md                   # Development setup
│   ├── 📄 ARCHITECTURE.md                  # System architecture
│   ├── 📄 CONTRIBUTING.md                  # Contributing guidelines
│   └── 📁 images/                          # Documentation images
│
├── 📁 media/                               # Media files (uploaded content)
│   ├── 📁 animal_photos/                   # Animal photos
│   ├── 📁 camera_snapshots/                # Camera snapshots
│   └── 📁 health_reports/                  # Health report files
│
├── 📁 static/                              # Static files
│   ├── 📁 css/                             # CSS files
│   ├── 📁 js/                              # JavaScript files
│   ├── 📁 images/                          # Static images
│   └── 📁 admin/                           # Admin static files
│
├── 📁 staticfiles/                         # Collected static files (production)
│
├── 📁 templates/                           # HTML templates
│   ├── 📄 base.html                        # Base template
│   ├── 📁 admin/                           # Admin templates
│   ├── 📁 emails/                          # Email templates
│   └── 📁 reports/                         # Report templates
│
├── 📁 tests/                               # Test files
│   ├── 📄 __init__.py
│   ├── 📄 conftest.py                      # Pytest configuration
│   ├── 📄 test_settings.py                 # Test settings
│   ├── 📁 integration/                     # Integration tests
│   ├── 📁 unit/                            # Unit tests
│   └── 📁 fixtures/                        # Test fixtures
│
├── 📁 scripts/                             # Management scripts
│   ├── 📄 setup.sh                         # Initial setup script
│   ├── 📄 deploy.sh                        # Deployment script
│   ├── 📄 backup.sh                        # Database backup script
│   ├── 📄 restore.sh                       # Database restore script
│   └── 📄 migrate.sh                       # Migration script
│
├── 📁 logs/                                # Log files
│   ├── 📄 django.log                       # Django logs
│   ├── 📄 celery.log                       # Celery logs
│   ├── 📄 nginx.log                        # Nginx logs
│   └── 📄 error.log                        # Error logs
│
├── 📁 locale/                              # Internationalization
│   ├── 📁 en/                              # English translations
│   ├── 📁 sw/                              # Swahili translations
│   └── 📁 fr/                              # French translations
│
├── 📄 manage.py                            # Django management script
├── 📄 requirements.txt                     # Production dependencies
├── 📄 requirements-dev.txt                 # Development dependencies
├── 📄 requirements-test.txt                # Testing dependencies
├── 📄 .env.example                         # Environment variables example
├── 📄 .gitignore                           # Git ignore file
├── 📄 .dockerignore                        # Docker ignore file
├── 📄 pytest.ini                           # Pytest configuration
├── 📄 setup.cfg                            # Setup configuration
├── 📄 tox.ini                              # Tox configuration
├── 📄 Makefile                             # Make commands
├── 📄 README.md                            # Main README
└── 📄 LICENSE                              # License file
```

---

## 📱 App-Level Structure Breakdown

### 🔐 Authentication App (`apps/authentication/`)

```
authentication/
├── 📄 models.py                    # User, Role, Permission models
├── 📄 serializers.py               # UserSerializer, LoginSerializer
├── 📄 views.py                     # LoginView, RegisterView, ProfileView
├── 📄 urls.py                      # /api/auth/* endpoints
├── 📄 permissions.py               # IsFarmer, IsVeterinarian, IsAdmin
├── 📄 validators.py                # Phone number, email validators
├── 📄 signals.py                   # User creation signals
├── 📄 admin.py                     # Django admin configuration
├── 📄 apps.py                      # App configuration
└── 📄 tests.py                     # Authentication tests
```

### 🐄 Animals App (`apps/animals/`)

```
animals/
├── 📄 models.py                    # Animal, AnimalHistory, Location
├── 📄 serializers.py               # AnimalSerializer, LocationSerializer
├── 📄 views.py                     # AnimalViewSet, LocationViewSet
├── 📄 urls.py                      # /api/animals/* endpoints
├── 📄 filters.py                   # AnimalFilter, LocationFilter
├── 📄 signals.py                   # Animal creation/update signals
├── 📄 utils.py                     # Animal utilities
├── 📄 admin.py                     # Admin configuration
├── 📄 apps.py                      # App configuration
└── 📄 tests.py                     # Animal tests
```

### 🩺 Health App (`apps/health/`)

```
health/
├── 📄 models.py                    # HealthEvent, Vaccination, Treatment
├── 📄 serializers.py               # HealthEventSerializer, VaccinationSerializer
├── 📄 views.py                     # HealthEventViewSet, VaccinationViewSet
├── 📄 urls.py                      # /api/health/* endpoints
├── 📄 filters.py                   # HealthEventFilter
├── 📄 tasks.py                     # Celery tasks for health reminders
├── 📄 signals.py                   # Health event signals
├── 📄 admin.py                     # Admin configuration
├── 📄 apps.py                      # App configuration
└── 📄 tests.py                     # Health tests
```

### 📸 Cameras App (`apps/cameras/`)

```
cameras/
├── 📄 models.py                    # CameraFeed, CameraSnapshot
├── 📄 serializers.py               # CameraFeedSerializer, SnapshotSerializer
├── 📄 views.py                     # CameraFeedViewSet, SnapshotView
├── 📄 urls.py                      # /api/cameras/* endpoints
├── 📄 services.py                  # Camera streaming services
├── 📄 utils.py                     # Camera utilities (OpenCV)
├── 📄 tasks.py                     # Celery tasks for camera processing
├── 📄 admin.py                     # Admin configuration
├── 📄 apps.py                      # App configuration
└── 📄 tests.py                     # Camera tests
```

### 📱 Notifications App (`apps/notifications/`)

```
notifications/
├── 📄 models.py                    # Notification, SMSLog, VoiceCall, USSDSession
├── 📄 serializers.py               # NotificationSerializer, SMSSerializer
├── 📄 views.py                     # NotificationViewSet, SMSView, USSDView
├── 📄 urls.py                      # /api/notifications/* endpoints
├── 📄 services.py                  # AfricasTalking, Twilio integrations
├── 📄 tasks.py                     # Celery tasks for notifications
├── 📄 ussd_handlers.py             # USSD session handlers
├── 📄 templates.py                 # Message templates
├── 📄 admin.py                     # Admin configuration
├── 📄 apps.py                      # App configuration
└── 📄 tests.py                     # Notification tests
```

### 🤖 Chatbot App (`apps/chatbot/`)

```
chatbot/
├── 📄 models.py                    # ChatSession, ChatMessage, Intent
├── 📄 serializers.py               # ChatMessageSerializer, IntentSerializer
├── 📄 views.py                     # ChatViewSet, QueryView
├── 📄 urls.py                      # /api/chatbot/* endpoints
├── 📄 services.py                  # NLP processing services
├── 📄 intent_handlers.py           # Intent processing logic
├── 📄 entity_extractors.py         # Entity extraction (animals, dates, etc.)
├── 📄 response_generators.py       # Response generation
├── 📄 admin.py                     # Admin configuration
├── 📄 apps.py                      # App configuration
└── 📄 tests.py                     # Chatbot tests
```

### 📊 Analytics App (`apps/analytics/`)

```
analytics/
├── 📄 models.py                    # Report, Metric, Dashboard
├── 📄 serializers.py               # ReportSerializer, MetricSerializer
├── 📄 views.py                     # AnalyticsViewSet, ReportView
├── 📄 urls.py                      # /api/analytics/* endpoints
├── 📄 services.py                  # Analytics processing
├── 📄 reports.py                   # Report generation logic
├── 📄 metrics.py                   # Metric calculations
├── 📄 tasks.py                     # Celery tasks for analytics
├── 📄 admin.py                     # Admin configuration
├── 📄 apps.py                      # App configuration
└── 📄 tests.py                     # Analytics tests
```

### 🗺️ Tracking App (`apps/tracking/`)

```
tracking/
├── 📄 models.py                    # LocationData, TrackingDevice, Geofence
├── 📄 serializers.py               # LocationSerializer, DeviceSerializer
├── 📄 views.py                     # TrackingViewSet, LocationView
├── 📄 urls.py                      # /api/tracking/* endpoints
├── 📄 consumers.py                 # WebSocket consumers
├── 📄 routing.py                   # WebSocket routing
├── 📄 services.py                  # GPS tracking services
├── 📄 utils.py                     # Location utilities
├── 📄 admin.py                     # Admin configuration
├── 📄 apps.py                      # App configuration
└── 📄 tests.py                     # Tracking tests
```

---

## 🔧 Configuration Files

### Django Settings (`livestock_tracker/settings/`)

```python
# base.py - Base settings
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Celery configuration
CELERY_BROKER_URL = env('REDIS_URL')
CELERY_RESULT_BACKEND = env('REDIS_URL')

# Channels configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [env('REDIS_URL')],
        },
    },
}
```

### Requirements (`requirements.txt`)

```
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.1
django-environ==0.11.2
django-filter==23.3
psycopg2-binary==2.9.8
celery==5.3.4
redis==5.0.1
channels==4.0.0
channels-redis==4.1.0
opencv-python==4.8.1.78
Pillow==10.1.0
gunicorn==21.2.0
whitenoise==6.6.0
drf-yasg==1.21.7
pytest==7.4.3
pytest-django==4.7.0
coverage==7.3.2
```

---

## 🚀 Getting Started

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/your-username/livestock-tracker.git
cd livestock-tracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Copy environment file
cp .env.example .env
```

### 2. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data
python manage.py loaddata fixtures/initial_data.json
```

### 3. Run Development Server

```bash
# Start Redis (for Celery and Channels)
redis-server

# Start Celery worker
celery -A livestock_tracker worker -l info

# Start Django development server
python manage.py runserver
```

---

## 🧪 Testing Structure

### Test Organization

```
tests/
├── unit/                           # Unit tests
│   ├── test_models.py              # Model tests
│   ├── test_serializers.py         # Serializer tests
│   ├── test_views.py               # View tests
│   └── test_utils.py               # Utility tests
├── integration/                    # Integration tests
│   ├── test_api_endpoints.py       # API endpoint tests
│   ├── test_websockets.py          # WebSocket tests
│   └── test_notifications.py      # Notification tests
└── fixtures/                      # Test data
    ├── animals.json               # Animal test data
    ├── users.json                 # User test data
    └── health_events.json         # Health event test data
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py

# Run tests with verbose output
pytest -v
```

---

## 📦 Deployment Structure

### Docker Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/livestock_db
      - REDIS_URL=redis://redis:6379/0

  db:
    image: postgres:14
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=livestock_db
      - POSTGRES_USER=livestock_user
      - POSTGRES_PASSWORD=livestock_pass

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery:
    build: .
    command: celery -A livestock_tracker worker -l info
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

This comprehensive project structure provides a solid foundation for your LiveStock Tracker backend, with clear separation of concerns, scalable architecture, and proper organization for development, testing, and deployment.