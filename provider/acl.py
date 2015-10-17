from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.security import Allow, Everyone, forget, remember
from pyramid_sacrud.security import permissions


class Root(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'admin', 'restricted'),
        (Allow, 'admin', 'admin')
        ]

    def __init__(self, request):
        for perm in permissions:
            self.__acl__.append(
                (Allow, 'admin', perm)
            )
        self.request = request


def groupfinder(username, request):
    # TODO
    if username == 'admin':
        return ['admin']
    return []


def includeme(config):
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret',
        callback=groupfinder,
    )

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_root_factory(Root)
