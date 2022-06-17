import json

from django.contrib.staticfiles import finders

# tenta retornar uma dicionário com palavras vazias por idioma
try:
    stopwords_json_file = finders.find("stopwords-iso/stopwords-iso.json")
    # Arquivo de: https://github.com/stopwords-iso/stopwords-iso
    with open(stopwords_json_file, encoding="utf-8") as f:
        stopwords = json.loads(f.read())
except TypeError:
    stopwords = {}
