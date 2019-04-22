#!/bin/bash
python manage.py migrate                  # Aplique as migrações de banco de dados
python manage.py collectstatic --noinput -i jquery-ui*  # Colete os arquivos estáticos

# Inicie os processos do gunicorn
echo Starting Gunicorn.
exec gunicorn xram_memory.wsgi \
    --name xram_memory_webadmin \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    "$@"