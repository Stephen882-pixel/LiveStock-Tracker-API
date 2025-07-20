#!/bin/bash

# Create main project directory
mkdir -p livestock_tracker || { echo "Failed to create livestock_tracker directory"; exit 1; }
cd livestock_tracker || { echo "Failed to change to livestock_tracker directory"; exit 1; }

# Create directory structure
mkdir -p livestock_tracker/settings || { echo "Failed to create settings directory"; exit 1; }
mkdir -p config docker/scripts docs/images media/{animal_photos,camera_snapshots,health_reports} || { echo "Failed to create config/docker/docs/media directories"; exit 1; }
mkdir -p static/{css,js,images,admin} staticfiles templates/{admin,emails,reports} || { echo "Failed to create static/templates directories"; exit 1; }
mkdir -p tests/{integration,unit,fixtures} scripts logs locale/{en,sw,fr} || { echo "Failed to create tests/scripts/logs/locale directories"; exit 1; }

# Create app directories with migrations explicitly
for app in authentication animals health cameras notifications chatbot analytics tracking core; do
    mkdir -p livestock_tracker/apps/$app/migrations || { echo "Failed to create migrations directory for $app"; exit 1; }
done

# Create files in main project directory
touch livestock_tracker/{__init__.py,urls.py,wsgi.py,asgi.py,celery.py}
touch livestock_tracker/settings/{__init__.py,base.py,development.py,production.py,testing.py}
touch manage.py requirements.txt requirements-dev.txt requirements-test.txt .env.example .gitignore .dockerignore pytest.ini setup.cfg tox.ini Makefile README.md LICENSE

# Create files in apps
touch livestock_tracker/apps/authentication/{__init__.py,models.py,serializers.py,views.py,urls.py,permissions.py,validators.py,signals.py,admin.py,apps.py,tests.py}
touch livestock_tracker/apps/authentication/migrations/__init__.py
touch livestock_tracker/apps/animals/{__init__.py,models.py,serializers.py,views.py,urls.py,filters.py,signals.py,utils.py,admin.py,apps.py,tests.py}
touch livestock_tracker/apps/animals/migrations/__init__.py
touch livestock_tracker/apps/health/{__init__.py,models.py,serializers.py,views.py,urls.py,filters.py,tasks.py,signals.py,admin.py,apps.py,tests.py}
touch livestock_tracker/apps/health/migrations/__init__.py
touch livestock_tracker/apps/cameras/{__init__.py,models.py,serializers.py,views.py,urls.py,services.py,utils.py,tasks.py,admin.py,apps.py,tests.py}
touch livestock_tracker/apps/cameras/migrations/__init__.py
touch livestock_tracker/apps/notifications/{__init__.py,models.py,serializers.py,views.py,urls.py,services.py,tasks.py,ussd_handlers.py,templates.py,admin.py,apps.py,tests.py}
touch livestock_tracker/apps/notifications/migrations/__init__.py
touch livestock_tracker/apps/chatbot/{__init__.py,models.py,serializers.py,views.py,urls.py,services.py,intent_handlers.py,entity_extractors.py,response_generators.py,admin.py,apps.py,tests.py}
touch livestock_tracker/apps/chatbot/migrations/__init__.py
touch livestock_tracker/apps/analytics/{__init__.py,models.py,serializers.py,views.py,urls.py,services.py,reports.py,metrics.py,tasks.py,admin.py,apps.py,tests.py}
touch livestock_tracker/apps/analytics/migrations/__init__.py
touch livestock_tracker/apps/tracking/{__init__.py,models.py,serializers.py,views.py,urls.py,consumers.py,routing.py,services.py,utils.py,admin.py,apps.py,tests.py}
touch livestock_tracker/apps/tracking/migrations/__init__.py
touch livestock_tracker/apps/core/{__init__.py,models.py,serializers.py,views.py,permissions.py,pagination.py,exceptions.py,middleware.py,utils.py,validators.py,tests.py}

# Create files in other directories
touch config/{nginx.conf,gunicorn.conf.py,supervisor.conf,redis.conf,celery.conf}
touch docker/{Dockerfile,docker-compose.yml,docker-compose.prod.yml,docker-compose.test.yml}
touch docker/scripts/{entrypoint.sh,wait-for-it.sh,init-db.sh}
touch docs/{API.md,DEPLOYMENT.md,DEVELOPMENT.md,ARCHITECTURE.md,CONTRIBUTING.md}
touch templates/base.html
touch tests/{__init__.py,conftest.py,test_settings.py}
touch tests/unit/{test_models.py,test_serializers.py,test_views.py,test_utils.py}
touch tests/integration/{test_api_endpoints.py,test_websockets.py,test_notifications.py}
touch tests/fixtures/{animals.json,users.json,health_events.json}
touch scripts/{setup.sh,deploy.sh,backup.sh,restore.sh,migrate.sh}
touch logs/{django.log,celery.log,nginx.log,error.log}

# Create .env.example
cat <<EOL > .env.example
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
# Database
DB_NAME=livestock_db
DB_USER=livestock_user
DB_PASSWORD=livestock_pass
DB_HOST=db
DB_PORT=5432
# Redis
REDIS_URL=redis://redis:6379/0
EOL

# Create requirements.txt
cat <<EOL > requirements.txt
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
EOL

# Create requirements-dev.txt
cat <<EOL > requirements-dev.txt
-r requirements.txt
black==23.9.1
flake8==6.1.0
isort==5.12.0
EOL

# Create requirements-test.txt
cat <<EOL > requirements-test.txt
-r requirements.txt
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0
factory-boy==3.3.0
EOL

# Create .gitignore
cat <<EOL > .gitignore
*.pyc
__pycache__/
*.pyo
*.pyd
.Python
env/
venv/
*.egg-info/
*.log
*.pot
*.py[cod]
*.sqlite3
media/
staticfiles/
.env
.env.local
.env.*.local
.idea/
.vscode/
*.swp
*.swo
docker-compose.override.yml
EOL

# Create .dockerignore
cat <<EOL > .dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
*.egg-info/
*.log
.env
.env.local
.env.*.local
.idea/
.vscode/
*.sqlite3
media/
staticfiles/
tests/
docs/
scripts/
logs/
*.md
LICENSE
EOL

# Create pytest.ini
cat <<EOL > pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = livestock_tracker.settings.test
python_files = tests.py test_*.py
addopts = --cov=apps --cov-report=html
EOL

# Create README.md
cat <<EOL > README.md
# LiveStock Tracker

A Django-based backend for livestock management, tracking, and monitoring.

## Getting Started

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/your-username/livestock-tracker.git
   cd livestock-tracker
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements-dev.txt
   \`\`\`

3. Setup environment:
   \`\`\`bash
   cp .env.example .env
   \`\`\`

4. Run migrations:
   \`\`\`bash
   python manage.py migrate
   \`\`\`

5. Start the development server:
   \`\`\`bash
   python manage.py runserver
   \`\`\`

See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed setup instructions.
EOL

# Make scripts executable
chmod +x scripts/*.sh
chmod +x docker/scripts/*.sh

echo "Project structure for LiveStock Tracker has been created successfully!"