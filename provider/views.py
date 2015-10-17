from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPForbidden

from pyramid.security import remember, forget, authenticated_userid
from pyramid.view import forbidden_view_config

from models import DBSession, User

@view_config(route_name='home', renderer='home.mako')
def home_view(request):
    login = authenticated_userid(request)
    return {
        'user': login
    }

@view_config(route_name='restricted', renderer='restricted.mako', permission='admin')
def restricted(request):
    login = authenticated_userid(request)
    return {
        'user': login
    }

@view_config(route_name='login', renderer='login.mako')
def login_view(request):
    next = request.params.get('next') or request.route_url('home')
    login = ''
    did_fail = False

    if 'submit' in request.POST:
        login = request.POST.get('login', '')
        passwd = request.POST.get('passwd', '')

        if login:
            user = DBSession.query(User).filter_by(name=login).one()
            if user and user.name == login and user.password == passwd:
                headers = remember(request, login)
                return HTTPFound(location=next, headers=headers)

        did_fail = True

    return {
        'login': login,
        'next': next,
        'failed_attempt': did_fail,
    }


@view_config(route_name='logout')
def logout_view(request):
    headers = forget(request)
    loc = request.route_url('home')
    return HTTPFound(location=loc, headers=headers)


@forbidden_view_config()
def forbidden_view(request):
    if authenticated_userid(request):
        return HTTPForbidden()

    loc = request.route_url('login', _query=(('next', request.path),))
    return HTTPFound(location=loc)


@view_config(route_name='authorize')
def authorize(request):
    print 'request'
    print dir(request)

    return request.create_token_response(credentials=credentials)

@view_config(route_name='access_token')
def access_token(request):
    userid = request.authenticated_userid
    credentials = dict(userId=userid) if userid else {}
    # print dir(request)

    return request.create_token_response(credentials=credentials)
