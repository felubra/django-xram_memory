FROM python:3

LABEL author=felipe.lubra@gmail.com

WORKDIR /app

RUN pip install pipenv

COPY Pipfile.lock .
COPY Pipfile .

RUN pipenv install --system --deploy

COPY . .

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "-w", "3", "xram_memory.wsgi" ]