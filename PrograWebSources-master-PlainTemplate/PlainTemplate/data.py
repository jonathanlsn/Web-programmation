# coding: utf-8
"""App data

Get wiki page ID: https://en.wikipedia.org/w/api.php?action=query&format=json&titles=Page%20Title
Get a thumbnail : https://en.wikipedia.org/w/api.php?action=query&titles=Alan%20Turing&prop=pageimages&format=json&pithumbsize=100
"""

import json

from datetime import date, datetime

with open('data.json') as js:
    DATA = json.load(js)
    ARTICLES = DATA.get('ARTICLES')
    CATEGORIES = DATA.get('CATEGORIES')

def get_categories(a_id):
    for field, ids in CATEGORIES.items():
        if a_id in ids:
            yield field


#for article in ARTICLES:
#    article.update({'categories': [f for f in get_categories(article.get('id'))]})

# Script starts here
if __name__ == '__main__':
    pass

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
