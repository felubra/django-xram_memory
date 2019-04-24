#!/bin/bash
set -e;
python manage.py collectstatic --noinput -i jquery-ui*  # Colete os arquivos estáticos
python manage.py migrate                  # Aplique as migrações de banco de dados

# Inicie os processos do gunicorn
echo Starting Gunicorn.
exec gunicorn xram_memory.wsgi \
    --name xram_memory_webadmin \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    "$@"