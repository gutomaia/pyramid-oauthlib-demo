from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Table
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy_utils.types.password import PasswordType
Base = declarative_base()
DBSession = scoped_session(sessionmaker())

users = 'users'
groups = 'groups'
usergroups = 'usergroups'

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
