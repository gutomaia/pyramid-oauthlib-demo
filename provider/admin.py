from models import *

def includeme(config):
    config.include('pyramid_sacrud', route_prefix='admin')
    config.registry.settings['pyramid_sacrud.models'] = (
        # ('Catalouge', [Good]),
        ('Auth system', [User, Group])
    )
