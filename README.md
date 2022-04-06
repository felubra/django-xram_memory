# Backend of the xRAM-Memory website

This project concentrates the content management system and the API for the xRAM-Memory website. The project used several Python libraries, especially: Django (base framework and CMS), Django REST Framework (API), newspaper3k and goose3 (news crawlers), django-filer (file management) and celery (queue management for processing). distributed).

Project dependencies are managed with the `pipenv` tool.

## Instalação

0) Install [Python 3.7.2+](https://www.python.org/downloads/) and [Pipenv](https://pypi.org/project/pipenv/)
1) Install the packages: `python3-pdfkit`, `poppler-utils` and `wkhtmltopdf`
3) Install project dependencies: `pipenv install --dev` and `npm install`
4) Set environment variables in `.env` from `.env.example`, in particular, set at least `DJANGO_SECRET_KEY` and `DJANGO_HASHID_FIELD_SALT` variables
5) Enter pipenv shell: `pipenv shell`
6) Install nltk bodies: `./scripts/download_corpora.py --user`
7) Collect the statics: `./manage.py collectstatic`
8) Run the migrations: `./manage.py migrate`
9) Create a superuser: `./manage.py createsuperuser`


## Local environment
### Application
0) Run the installation steps above
1) Enter a `pipenv` shell
3) Start a memcached container: `docker run --name my-memcache -d -p 127.0.0.1:11211:11211 memcached memcached -m 64`
3) Start the application locally: `./manage.py runserver_plus`
4) Go to `http://localhost:8000/admin/`
5) Run the `micro-lunr_index_builder` project:
```shell
docker run -d --name xram_memory__lunr_index_builder -v <path_to_the_index_file>:/usr/src/app/index.json:rw -e AUTH_TOKEN=avocado00 -p 3001:3000 xram_memory:lunr_index_builder
```


### Celery
0) Start a redis container listening on the default port locally:
```shell
docker run --name some-redis -d -p 127.0.0.1:6379:6379 redis
```
1) Start as many instances of celery as necessary. In a `pipenv` shell, run:
```shell
celery worker -A xram_memory -n 1
```
3) (Optional) Monitor workers with *Flower*. In a `pipenv` shell, run:
```shell
flower -A xram_memory
```


## Data Entities

The following models (entities) are present in this project:

The diagram below illustrates the relationship between the entities (click to open the image):

[![diagram](./docs/entidades.png)](./docs/entidades.png)

## Project structure

A Django project is made up of several applications, each with a specific responsibility, which can be expressed by the organization of folders. This is the structure of the `./xram_memory` folder, which contains the system source code:

```
.
├── albums - Album management application
├── artifact - Artifact management application
├── lib - Specialized libraries developed for the project
│ ├── file_previews - File preview generator
│ ├── news_fetcher - Main system program, more about it below
│ │ └── plugins - The various plugin implementations
│ │ ├── archives - News Archivers
│ │ ├── parsers - News Content Extractors
│ │ └── pdf_captures - PDF news capture generators
│ └── stopwords - A dictionary of stopwords in multiple languages
├── logger - Application responsible for logging system operations
├── lunr_index - Application responsible for generating client-side search indexes
├── page - Application for managing Static Pages
├── quill_widget - Application that provides a rich text editing widget with the Quill.js library
├── search_indexes - Application responsible for generating server-side search indexes (ElasticSearch)
├── static - Static files
├── taxonomy - Application responsible for classifying content (Taxonomy)
├── templates - Global changes to templates
├── users - Application responsible for managing users and groups
└── utils - Global Utilities
```

In the `./tests` folder we have the project tests. Code coverage is currently at 65%.
