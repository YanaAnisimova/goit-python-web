from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Column,
    Integer, String, Unicode, Date,
    Table,
)
from sqlalchemy.orm import relationship

from db import Base, metadata


class Contact(Base):
    __tablename__ = 'contacts'
    contact_id = Column('contact_id', Integer, primary_key=True)
    name = Column('name', Unicode(50), nullable=False)
    birthday = Column('birthday', Date, nullable=False)
    note = Column('note', Unicode(250), nullable=True)

    # one to many
    phones = relationship('Phone', back_populates='contact', passive_deletes=True)

    # one to many
    emails = relationship('Email', back_populates='contact', passive_deletes=True)


class Phone(Base):
    __tablename__ = 'phones'
    phone_id = Column('phone_id', Integer, primary_key=True)
    phone = Column('phone', String(50), nullable=False)

    # relationship
    contact_id = Column(Integer, ForeignKey('contacts.contact_id', ondelete='CASCADE'), nullable=False)
    contact = relationship('Contact', back_populates='phones')


class Email(Base):
    __tablename__ = 'emails'
    email_id = Column('email_id', Integer, primary_key=True)
    email = Column('email', String(50), nullable=False)

    # relationship
    contact_id = Column(Integer, ForeignKey('contacts.contact_id', ondelete='CASCADE'), nullable=False)
    contact = relationship('Contact', back_populates='emails')

