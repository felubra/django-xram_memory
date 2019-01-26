import os
from pathlib import Path
import json

# Arquivo de: https://github.com/stopwords-iso/stopwords-iso
with open(str(Path(os.path.dirname(__file__), 'stopwords.json')), encoding='utf-8') as f:
    stopwords = json.loads(f.read())
