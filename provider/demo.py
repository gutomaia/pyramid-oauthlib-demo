from __future__ import absolute_import

import os
from pyramid.config import Configurator
from wsgiref.simple_server import make_server

here = os.path.dirname(os.path.abspath(__file__))


def includeme(config):
    config.include('pyramid_mako')
    config.include('pyramid_oauthlib')
    config.include('provider.database')
    config.include('provider.acl')
    config.include('provider.admin')
    config.include('provider.oauth')

    config.add_route(
        'home',
        '/'
    )

    config.add_route(
        'login',
        '/login'
    )

    config.add_route(
        'logout',
        '/logout'
    )

    config.add_route(
        'restricted',
        '/restricted'
    )

    config.add_route(
        'authorize',
        '/oauth2/authorize'
    )

    config.add_route(
        'access_token',
        '/oauth2/access_token'
    )


    config.scan('provider.views')

def main():
    settings = {
        'auth.secret': 'seekrit',
        'mako.directories': '%s:templates' % __name__,
        'sqlalchemy.url': 'sqlite:///example.sqlite',
        'fixtures': True,
    }

    # settings['sqlalchemy.url'] = 'sqlite://'
    config = Configurator(
        settings=settings,
        )

    includeme(config)

    return config.make_wsgi_app()
