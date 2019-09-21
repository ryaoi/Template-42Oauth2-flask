from app import app
from flask import request, redirect, session, url_for, render_template
from os import environ, urandom
from functools import wraps
import requests
import json
from FtApi import FtApi

@app.route('/')
@app.route('/index')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    print(session)
    print(app.secret_key)
    return render_template('index.html', title='index', user=session.get('user'))

@app.route('/login')
def login():
    random_state = urandom(32)
    redirect_uri = environ['REDIRECT_URI']
    client_id = environ['UID42']
    url = f'https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=public&state={random_state}'
    return redirect(url)

@app.route('/callback')
def callback():
    print(app.secret_key)
    if 'code' not in request.args:
        return 'Error'
    ft = FtApi(environ['UID42'], environ['SECRET42'], code=request.args['code'], redirect=environ['REDIRECT_URI'])
    headers = {'Authorization':"Bearer {}".format(ft.bearer)}
    me = requests.get('https://api.intra.42.fr/v2/me', headers=headers)
    me = json.loads(me.text)
    user = me['login']
    #session['bearer'] = ft.bearer
    session['user'] = user
    print(session['user'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    print(session)
    session.pop('user', None)
    return redirect(url_for('index'))

