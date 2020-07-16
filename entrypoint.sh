#!/bin/bash
set -e;
python manage.py collectstatic --noinput --noinput -i jquery-ui* # Colecione arquivos estáticos
python manage.py migrate # Aplique as migrações de banco de dados

environment="${ENVIRONMENT:-production}"
echo $environment
if [ "$environment" == "Development"  ]; then
    # Inicie o servidor de desenvolvimento do Django
    echo Starting Django Development Server.
    exec ./manage.py runserver_plus 0.0.0.0:8000
else
    # Inicie os processos do gunicorn
    echo Starting Gunicorn.
    exec gunicorn xram_memory.wsgi \
        --name xram_memory_webadmin \
        --bind 0.0.0.0:8000 \
        --timeout 90 \
        --workers 3 \
        --log-level=info \
        "$@"
fi
