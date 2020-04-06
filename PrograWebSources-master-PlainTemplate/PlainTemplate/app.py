#!/usr/bin/env python3
# coding: utf-8

import copy

from datetime import datetime
from flask import Flask, render_template, url_for
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


@app.route('/about', methods=['GET', 'POST'])
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
@app.route('/texte/<article>/')
def texte(article=None):
    app.logger.debug(request.args)
    if article==None:
        return render_template('texte.html',article=CATEGORIES)
    elif article in CATEGORIES:
        liste=CATEGORIES[article]
        articles = []
        for num in liste:
            for dico in ARTICLES:
                if dico["id"] == num:
                    articles.append(dico)
        return render_template('<articles>.html',articles=articles,vname=article,vcat=CATEGORIES)
    else:
        for dico in ARTICLES:
            if dico["titre"] == article:
                titre=dico["titre"]
                auteur=dico["auteur"]
                date= dico["date"]
                with open(dico["texte"], "r") as fichier:
                    texte=fichier.read()
                    return render_template('<articles>.html',titre=titre, auteur=auteur, date=date, texte=texte.split("\n"))
    

@app.route('/articles')
def articles():
    return render_template('articles.html', articlename=ARTICLES)


@app.route('/articles', methods=['POST'])
def add_articles():
    catégorie=request.form['catégorie-select']
    assert catégorie!=""
    titre=request.form['titre']
    auteur=request.form['auteur']
    texte=request.form['texte']
    date=request.form['date']
    ref=request.form['ref']
    with open("./articles_file/"+titre+".txt", "a") as fichier:
        fichier.write(texte)
    new_article={"id":len(ARTICLES),"auteur":auteur,"titre": titre, "référence": ref,
     "texte": titre+".txt", "date": date}  
    ARTICLES.append(new_article)
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
        wordsearch=request.args.get("pattern",'')
        id_list,result=[],[]
        for article in ARTICLES:
            if wordsearch.lower() in article["titre"].lower() :  # comparaison par titre
                id_list.append(article["id"])
            elif wordsearch.lower() in article["auteur"].lower() :  # comparaison par auteur
                id_list.append(article["id"])

        for categorie, ID in CATEGORIES.items():   # comparaison par catégorie
            if wordsearch.lower() in categorie.lower():  
                for identifiant in ID:
                    id_list.append(identifiant)

        id_list=list(set(id_list)) #suppression des doublons
        for ID in id_list:
            for article in ARTICLES:
                if article["id"]==ID:
                    result.append(article)  # ajout de tous les articles concernés par la recherche
                    break
        if result==[]:
            return render_template('texte.html',articlename=ARTICLES, error="true")
        else:
            return render_template('texte.html',articlename=result)     



# Script starts here
if __name__ == '__main__':
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
