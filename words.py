import os
import string
import nltk
from nltk.corpus import gutenberg
import pandas as pd

from urllib import request

'http://www.gutenberg.org/cache/epub/8019/pg8019.txt'


def clean_text(content):
    stopwords = nltk.corpus.stopwords.words('english')
    # content = [w for w in content if w.lower() not in stopwords]
    content = [w.lower() for w in content if w.isalpha()]
    return content


if not os.path.exists('shakespeare-complete-raw.txt'):
    url = 'https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt'
    response = request.urlopen(url)
    raw = response.read().decode('utf8')
    with open('shakespeare-complete-raw.txt', 'w') as o:
        o.write(raw)

text = open('shakespeare-complete-raw.txt').read()
sonnets = text[text.find('THE SONNETS'):text.find('THE END')]
words = clean_text(nltk.word_tokenize(sonnets))


# blake = gutenberg.words('blake-poems.txt')
# blake = nltk.Text(nltk.corpus.gutenberg.words('blake-poems.txt'))


# words = clean_text(blake.tokens)
# tagged = nltk.pos_tag(words)

# # nltk.help.upenn_tagset('RB')
