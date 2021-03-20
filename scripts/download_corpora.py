#!/usr/bin/python3
"""
Downloads the necessary NLTK models and corpora required to support
all of newspaper's features. Modify for your own needs.
"""
import sys
import nltk
import argparse

REQUIRED_CORPORA = [
    'brown',  # Required for FastNPExtractor
    'punkt',  # Required for WordTokenizer
    'maxent_treebank_pos_tagger',  # Required for NLTKTagger
    'movie_reviews',  # Required for NaiveBayesAnalyzer
    'wordnet',  # Required for lemmatization and Wordnet
    'stopwords'
]


def main(argv):
    parser = argparse.ArgumentParser(description='Downloads and installs nltk corpora.')
    parser.add_argument('--location', '-l',
        default="system",
        choices=["user", "system"],
        dest='location'
    )
    location = getattr(parser.parse_args(), 'location')

    for each in REQUIRED_CORPORA:
        print(('Downloading "{0}"'.format(each)))
        if location == 'system':
            nltk.download(each, download_dir='/usr/share/nltk_data')
        else:
            nltk.download(each)
    print("Finished.")


if __name__ == '__main__':
   main(sys.argv[1:])
