from models import *

def includeme(config):
    config.include('pyramid_sacrud', route_prefix='admin')
    config.registry.settings['pyramid_sacrud.models'] = (
        ('Auth system', [User, Group]),
        ('Oauth Client', [Client, Grant, Token]),
    )
