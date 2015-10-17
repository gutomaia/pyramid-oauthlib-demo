# -*- coding: utf-8 -*-
from flask import Flask
from flask import session, url_for, request, redirect, Response, flash
from flask_oauth import OAuth
from functools import wraps

import requests

app = Flask(__name__)

OAUTH_DOMAIN = 'http://localhost:8888'
OAUTH_BASEPATH = '/oauth'
OAUTH_PATH = OAUTH_DOMAIN + OAUTH_BASEPATH

oauth_client = OAuth()
gutonet = oauth_client.remote_app('gutonet',
    base_url='%s/' % OAUTH_DOMAIN,
    request_token_url=None,
    access_token_url='%s/access_token' % OAUTH_PATH,
    access_token_method='POST',
    authorize_url='%s/authorize' % OAUTH_PATH,
    consumer_key='8aad3a18abb1f2baa9e8',
    consumer_secret='e46cf7c82a4e4dff8ccb89af06aeeda2af6fc759',
    request_token_params={'response_type': 'token'},
    access_token_params={'grant_type': 'authorization_code'},
)


@gutonet.tokengetter
def get_gutonet_token(token=None):
    return gutonet.consumer_key, gutonet.consumer_secret


@app.route('/login')
def login():
    return gutonet.authorize(callback=url_for('oauth_authorized', _external=True))


@app.route('/private')
@gutonet.authorized_handler
def oauth_authorized(resp=None):
    if resp is None:
        flash(u'You denied the request to sign in.')
        return u'You denied the request to sign in.'

    session['gutonet_token'] = {'oauth2': resp}

    response = requests.get('%s/test'  % OAUTH_DOMAIN, headers={'Authorization': resp['refresh_token']})
    return response.content


if __name__ == "__main__":
    app.debug = True
    app.secret_key = 'this needs to be secret'
    app.run(host='0.0.0.0')
