#!/usr/bin/env python3
# coding: utf-8

import copy

from datetime import datetime

from flask import Flask
from flask import request, make_response
from flask import render_template

from data import ARTICLES
from data import CATEGORIES

app = Flask(__name__)

translate = {"Monday":"Lundi","Tuesday":"Mardi","Wednesday":"Mercredi","Thursday":"Jeudi","Friday":"Vendredi","Saturday":"Samedi","Sunday":"Dimanche","January":"Janvier","February":"Février","March":"Mars","April":"Avril","May":"Mai","June":"Juin","July":"Juillet","August":"Août","September":"Septembre","October":"Octobre","November":"Novembre","December":"Décembre"}

def deal_with_post():
    # Get the form content
    form = request.form
    app.logger.debug(dict(form))
    # Do whatever you need with the data
    # Returns code 201 for "created" status
    return 'Hello, World! You posted {}'.format(dict(form.items())), 201


@app.route('/hello_world', methods=['GET', 'POST'])
def hello_world():
    # You may use this logger to print any variable in
    # the terminal running the web server
    app.logger.debug('Running the hello_world function')
    app.logger.debug('Client request: method:"{0.method}'.format(request))
    if request.method == 'POST':
        # Use curl to post some data
        # curl -d"param=value" -X POST http://127.0.0.1:8000/hello_world
        return deal_with_post()
    # Open http://127.0.0.1:8000/hello_world?key=value&foo=bar&name=yourself
    # and have a look at the logs in the terminal running the server
    app.logger.debug('request arguments: {}'.format(request.args))
    if request.args:
        if 'name' in request.args.keys():
            # Use the query string argument to format the response
            return 'Hello {name} !'.format(**request.args), 200
    return 'Hello, World!', 200


@app.route('/')
def index():
    app.logger.debug('serving root URL /')
    return render_template('index.html')


@app.route('/about')
def about(page_title="À propos"):
    app.logger.debug('about')
    today = datetime.today()
    # Create a context
    tpl_context = {}
    # Populate a context to feed the template
    # (cf. http://strftime.org/ for string formating with datetime)
    tpl_context.update({'day': translate['{:%A}'.format(today)]})
    tpl_context.update({'d_o_month': '{:%d}'.format(today)})
    tpl_context.update({'month': translate['{:%B}'.format(today)]})
    tpl_context.update({'time': '{:%X}'.format(today)})
    tpl_context.update({'date': today})
    # Now let's see how the context looks like
    app.logger.debug('About Context: {}'.format(tpl_context))
    app.logger.debug(page_title)
    return render_template('about.html', context=tpl_context,page_title=page_title)

@app.route('/texte')
@app.route('/texte/<articles>/')
def texte(article=None):
    app.logger.debug('texte')
    if article==None:
        return render_template('texte.html',article=CATEGORIES)
    

@app.route('/articles')
def articles():
    return render_template('articles.html', articlename=ARTICLES)



@app.route('/articles')
def add_articles():
    catégorie=request.form['catégorie-select']
    assert catégorie!=""
    titre=request.form['titre']
    auteur=request.form['auteur']
    texte=request.form['texte']
    date=request.form['date']
    ref=request.form['ref']
    with open(titre+".txt", "w") as fichier:
        fichier.write(texte)
    new_article={"id":len(ARTICLES),"auteur":auteur,"titre": titre, "référence": ref,
     "texte": titre+".txt", "date": date}
    CATEGORIES[catégorie].append(new_article["id"])
    return render_template('articles.html', articlename=ARTICLES)
   

@app.route('/test')
def test():
     resp = make_response('Thanks for all the fish', 501)
     resp.headers['X-My-Neat-Header'] = 'Foo/Bar'
     return resp
    #return 'Thanks for all the fish', 501


@app.route('/search/', methods=['GET'])
def search():
    app.logger.debug(request.args)
    if (request.method=="GET"):
        u = []
        a = []
        c = []

        for i in ARTICLES:
            n = i["titre"].lower()
            aut = i["auteur"].lower()

            pat = request.args["pattern"].lower()
            if n.find(pat) != -1 :
                u.append(i)

            if aut.find(pat) != -1 :
                a.append(i)
        
        for j in CATEGORIES:
            pat = request.args["pattern"].lower()
            if j.lower().find(pat) != -1 :
                for b in CATEGORIES[j] :
                    for i in ARTICLES :
                        if b == i["id"] :
                            c.append(i)


        t = copy.deepcopy(u)
        for i in a:
            if i not in t:
                t.append(i)
        for i in c:
            if i not in t:
                t.append(i)
 
    return render_template('search_article.html', titre=u, auteur = a, total = t, categorie = c, pattern = request.args["pattern"])


# Script starts here
if __name__ == '__main__':
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
