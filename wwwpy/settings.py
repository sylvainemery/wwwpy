import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

with open(os.path.join(APP_STATIC, 'words/adjectives_exquisite_english.txt'), 'r') as file_adjectives:
	adjectives = file_adjectives.readlines()

with open(os.path.join(APP_STATIC, 'words/nouns_desserts_english.txt'), 'r') as file_nouns:
	nouns = file_nouns.readlines()
