from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Table
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy_utils.types.password import PasswordType
Base = declarative_base()
DBSession = scoped_session(sessionmaker())

users = 'users'
groups = 'groups'
usergroups = 'usergroups'
clients = 'clients'

usergroups_table = Table(usergroups, Base.metadata,
    Column('user_id', Integer, ForeignKey('%s.id' % users)),
    Column('group_id', Integer, ForeignKey('%s.id' % groups ))
)


class User(Base):
    __tablename__ = users
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    password = Column(PasswordType(schemes=['pbkdf2_sha512']))
    groups = relationship("Group", secondary=usergroups_table)

    sacrud_detail_col = [
        ('profile', [name]),
        ('groups', [groups])
    ]

    def __repr__(self):
        return self.name



class Group(Base):
    __tablename__ = groups
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)

    sacrud_detail_col = [
        ('', [name]),
    ]

    def __repr__(self):
        return self.name


class Client(Base):
    __tablename__ = clients
    name = Column(String(40))
    description = Column(String(400))

    user_id = Column(ForeignKey('%s.id' % users))
    user = relationship('User')


    client_id = Column(String(40), primary_key=True)
    client_secret = Column(String(55), unique=True, index=True,
        nullable=False)

    is_confidential = Column(Boolean)

    _redirect_uris = Column(Text)
    _default_scopes = Column(Text)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


class Grant(Base):
    __tablename__ = 'grants'

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer, ForeignKey('%s.id' % users, ondelete='CASCADE')
    )
    user = relationship('User')

    client_id = Column(
        String(40), ForeignKey('%s.client_id' % clients),
        nullable=False,
    )
    client = relationship('Client')

    code = Column(String(255), index=True, nullable=False)

    redirect_uri = Column(String(255))
    expires = Column(DateTime)

    _scopes = Column(Text)

    def delete(self):
        session.delete(self)
        session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    client_id = Column(
        String(40), ForeignKey('%s.client_id' % clients),
        nullable=False,
    )
    client = relationship('Client')

    user_id = Column(
        Integer, ForeignKey('%s.id' % users)
    )
    user = relationship('User')

    # currently only bearer is supported
    token_type = Column(String(40))

    access_token = Column(String(255), unique=True)
    refresh_token = Column(String(255), unique=True)
    expires = Column(DateTime)
    _scopes = Column(Text)

    def delete(self):
        session.delete(self)
        session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
