# from models import Base
from models import *

def add_fixtures():
    for user_name in ('admin', 'moderator', 'user1', 'user2'):
        DBSession.add(User(name=user_name, password='123456'))

    admin_group = Group(name='admin')
    DBSession.add(admin_group)


    client = Client(
        name='gutonet',
        client_id='8aad3a18abb1f2baa9e8',
        client_secret='e46cf7c82a4e4dff8ccb89af06aeeda2af6fc759',
        is_confidential=True,
        _redirect_uris='localhost:8888',
        _default_scopes='email'
        )

    DBSession.add(client)




    # for group in ('admin', 'moderator'):
    #     DBSession.add(Group(name=group))


    # for group_name in ('Electronics', 'Fashion', 'Home & Garden', 'Motors'):
    #     group = Group(name=group_name)
    #     DBSession.add(group)
    #     if group_name == 'Electronics':
    #         DBSession.add(Good(name='iPhone', group=group))
    #         DBSession.add(Good(name='Fridge', group=group))
    #         DBSession.add(Good(name='YotaPhone', group=group))
    #     elif group_name == 'Fashion':
    #         DBSession.add(Good(name='Jeans', group=group))
    #     elif group_name == 'Home & Garden':
    #         DBSession.add(Good(name='Rake', group=group))
    #     elif group_name == 'Motors':
    #         DBSession.add(Good(name='Chevrolet Cavalier', group=group))
    #         DBSession.add(Good(name='LADA Granta', group=group))

    DBSession.commit()


def includeme(config):
    from sqlalchemy import engine_from_config
    settings = config.registry.settings
    engine = engine_from_config(settings, 'sqlalchemy.')
    Base.metadata.bind = engine
    Base.metadata.drop_all()
    Base.metadata.create_all()
    add_fixtures()
